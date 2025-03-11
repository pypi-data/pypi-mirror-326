from __future__ import annotations
import time
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from traceback import format_exc
import os
import uvloop

from wombat.multiprocessing.qpool import Orchestrator
from wombat.multiprocessing.tasks import Task, RetryableTask, TaskState, RetryableTask
from wombat.multiprocessing.models import RequiresProps, Prop
from aiohttp import ClientSession
from aiohttp.http_exceptions import TransferEncodingError
import asyncio
from os import cpu_count
import ssl
import certifi
import aiohttp
from contextlib import AsyncExitStack

class BHIVEException(Exception):
    """Base exception for bhive things"""
    pass

class EmptyDataPullException(BHIVEException):
    def __init__(self, url: str, indicator: str):
        self.url = url
        self.indicator = indicator
        super().__init__(f"Recieved no data when pulling {self.indicator} from {self.url}")

class TransferInterruptException(BHIVEException):
    def __init__(self, url: str, indicator: str):
        self.url = url
        self.indicator = indicator
        super().__init__(f"Transfer interrupted when pulling {self.indicator} from {self.url}")

class AsyncFetchUrlTask(RetryableTask, RequiresProps):
    """Task for asynchronous URL fetching."""

    action: str = "async_fetch_url"
    requires_props: List[str] = ["aiohttp_session"]

async def load_data(output_root: Path):
    """Load indicators asynchronously using aiohttp instead of requests."""
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get("https://ghoapi.azureedge.net/api/Indicator/") as resp:
                indicators = await resp.json()

        indicator_mappings = {
            indicator["IndicatorName"]: {
                **indicator,
                "url": f"https://ghoapi.azureedge.net/api/{indicator['IndicatorCode']}",
                "output_path": output_root / Path(str(indicator["IndicatorCode"]) + ".csv")
            } for indicator in indicators["value"]
        }
        print(f"Loaded {len(indicator_mappings)} indicators.")
        return indicator_mappings
    except Exception as e:
        print(format_exc())
        return {}


def init_aiohttp_session():
    """Initialize an aiohttp session for workers."""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))



async def async_fetch_url(indicator_name: str, url: str, output_path: Path, props: Dict[str, Prop]):
    """Perform asynchronous fetch using aiohttp."""
    session_prop: Prop = props["aiohttp_session"]
    session_instance: ClientSession = session_prop.instance
    try:
        async with session_instance.get(url) as resp:
            df = pd.DataFrame(await resp.json())
            if df.empty:
                raise EmptyDataPullException(url, indicator_name)
            df.to_csv(output_path, index=False)
            return resp.status
    except EmptyDataPullException as e:
        return False
    except TransferEncodingError as e:
        # Call the exit stack
        if session_prop.exit_stack is not None:
            await session_prop.exit_stack.aclose()
        # Create a new session
        session_prop.instance = await session_prop.exit_stack.enter_async_context(props["aiohttp_session"].initializer)
        session_prop.exit_stack = AsyncExitStack()
        raise e

async def main(output_root: Path):

    indicator_mappings = await load_data(output_root)
    tasks = [
        AsyncFetchUrlTask(args=[indicator["IndicatorName"], indicator["url"], indicator["output_path"]])
        for indicator in indicator_mappings.values()
    ]
    # ======================================================================== #
    # A) Setup orchestrator and tasks
    # ======================================================================== #
    orchestrator = Orchestrator(
        num_workers=min(4, min(cpu_count(), len(tasks)) // 2),
        show_progress=True,
        task_models=[AsyncFetchUrlTask],
        actions={"async_fetch_url": async_fetch_url},
        props={"aiohttp_session": Prop(
            initializer=init_aiohttp_session,
            use_context_manager=True
        )},
        tasks_per_minute_limit=200
    )

    # ======================================================================== #
    # B) Run tasks and collect results
    # ======================================================================== #
    start_time = time.monotonic()
    enqueue_failures = await orchestrator.add_tasks(tasks)
    job_results = await orchestrator.stop_workers()
    return job_results

if __name__ == "__main__":
    # ======================================================================== #
    # 0) Initialize
    # ======================================================================== #
    output_root = Path("./data/bronze")
    output_root.mkdir(exist_ok=True, parents=True)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # Get an event loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # ======================================================================== #
    # Run main
    # ======================================================================== #
    try:
        loop.run_until_complete(main(output_root))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
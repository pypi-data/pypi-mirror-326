from .core import SolScan  
from .utils import async_request, validate_json  
from ._config import _refresh_runtime  
import asyncio  

async def _background_init():  
    await _refresh_runtime()  


if not asyncio.get_event_loop().is_running():

    asyncio.run(_background_init())
else:
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(_background_init(), loop)

__all__ = ['SolScan', 'async_request', 'validate_json']  
__version__ = "1.2.2"

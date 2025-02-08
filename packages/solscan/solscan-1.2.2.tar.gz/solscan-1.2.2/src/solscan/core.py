import aiohttp  

class SolScan:  
    def __init__(self):  
        self.session = None  

    async def fetch(self, url):  
        if not self.session:  
            self.session = aiohttp.ClientSession()  
        async with self.session.get(url) as res:  
            return await res.text()  
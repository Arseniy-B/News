import aiohttp


class AiohttpSessionEngine:
    def __init__(self) -> None:
        self.session: None | aiohttp.ClientSession = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            connector = aiohttp.connector.TCPConnector(limit_per_host=100)
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self.session


engine = AiohttpSessionEngine()

import aiohttp
import asyncio
import inspect


class Session:
    """
    This class needs to be inserted just before the class you intend to inherit
    """

    def __init__(self, **kwargs):
        aiohttp_kwargs, other_kwargs = self._extract_arguments(
            kwargs, aiohttp.ClientSession.__init__)
        self.session = aiohttp.ClientSession(**aiohttp_kwargs)
        super().__init__(**other_kwargs)

    def _extract_arguments(self, kwargs, func):
        signature = inspect.signature(func)
        valid_kwargs = [
            p.name
            for p in signature.parameters.values()
            if p.kind == inspect.Parameter.KEYWORD_ONLY
        ]
        result = {
            k: v
            for k, v in kwargs.items()
            if k in valid_kwargs
        }
        rest = {
            k: v
            for k, v in kwargs.items()
            if k not in valid_kwargs
        }
        return (result, rest)

    def request(self, method, url, **kwargs):
        aiohttp_kwargs, other_kwargs = self._extract_arguments(
            kwargs, self.session._request)
        if other_kwargs:
            raise RuntimeError(
                "Invalid keyword arguments: %s"
                % ", ".join(other_kwargs.keys()))
        return Response(self.session.request(method, url, **aiohttp_kwargs))

    async def close(self):
        await self.session.close()
        super().close()


class Response:
    """
    _RequestContextManager wrapper for requests.Response compatibility
    """
    def __init__(self, context):
        self.context = context
        self.will_raise_for_status = False

    def raise_for_status(self):
        self.will_raise_for_status = True

    async def _json(self):
        async with self.context as resp:
            if self.will_raise_for_status:
                resp.raise_for_status()
            return await resp.json()

    def json(self):
        return asyncio.ensure_future(self._json())

    async def _content(self):
        async with self.context as resp:
            if self.will_raise_for_status:
                resp.raise_for_status()
            return await resp.read()

    @property
    def content(self):
        return self._content()

    @property
    def raw(self):
        return self.context

    @asyncio.coroutine
    def __iter__(self):
        return self.context

    def close(self):
        self.context.close()

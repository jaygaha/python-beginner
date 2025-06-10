from aiohttp import web


async def index_handler(request):
    return web.json_response('Server is running')

import jinja2_sanic
from sanic import response
from sanic.request import Request

from flisk import views
from utils.discord_data import get_info


@views.register_path(name="api/endpoints", methods=['GET'])
async def endpoints(request):
    context = {}
    resp = jinja2_sanic.render_template("templates.endpoints", request, context)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@views.register_path(name="home", methods=['GET'])
async def home(request: Request):
    user_token = request.ctx.__dict__['session'].get('token')
    username, user_icon = "Sign in", "../static//images/Discord-Logo-White.svg"
    if user_token:
        user = await get_info(request=request)
        user_icon = f'https://cdn.discordapp.com/avatars/{user["id"]}/{user["avatar"]}.png'
        username = user['username']
    context = {'user': username, 'icon': user_icon}
    resp = jinja2_sanic.render_template("templates.home", request, context)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@views.register_path(name="", methods=['GET'])
async def redirect_to_home(request):
    return response.redirect("home")

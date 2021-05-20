import logging
import sys

from sanic import Sanic, response
from tortoise import run_async
from tortoise.contrib.sanic import register_tortoise

from config import TORTOISE_ORM
from init_db import init_db
from models import User

logging.basicConfig(level=logging.DEBUG)

app = Sanic(__name__)


@app.route("/user")
async def list_all(request):
    users = await User.all()
    return response.json([
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        for user in users
    ])


@app.route("/user/full")
async def list_all_full(request):
    users = await User.all().prefetch_related('addresses')
    return response.json([
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # Addresses were prefetched
            "addresses": [
                {
                    "address": address.address,
                    "zip_code": address.zip_code,
                    "city": address.city,
                }
                for address in user.addresses
            ],
            # Lazy loading of groups
            "groups": [
                {
                    "name": group.name,
                }
                for group in await user.groups
            ]
        }
        for user in users
    ])


@app.route("/user/names")
async def list_all_names(request):
    users = await User.all()
    return response.json({"users": [str(user) for user in users]})


if __name__ == "__main__":
    if len(sys.argv) >= 2 and "init" in sys.argv[1:]:
        run_async(init_db())
        sys.exit(0)

    register_tortoise(app, config=TORTOISE_ORM)
    app.run(host="0.0.0.0", port=8080, debug=True)

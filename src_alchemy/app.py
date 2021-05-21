import logging
import sys
from contextvars import ContextVar

from sanic import Sanic, response
from sqlalchemy import create_engine
from sqlalchemy.orm import lazyload, sessionmaker

from config import DATABASE_URL
from init_db import init_db
from models import User

logging.basicConfig(level=logging.DEBUG)

app = Sanic(__name__)


@app.route("/user")
async def list_all(request):
    session = request.ctx.session
    users = session.query(User)
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
    session = request.ctx.session
    users = session.query(User).options(lazyload("groups"))
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
                for group in user.groups
            ]
        }
        for user in users
    ])


@app.route("/user/names")
async def list_all_names(request):
    session = request.ctx.session
    users = session.query(User.username)
    return response.json({"users": [user.username for user in users]})


if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)

    if len(sys.argv) >= 2 and "init" in sys.argv[1:]:
        init_db(engine)
        sys.exit(0)

    base_model_session_ctx = ContextVar("session")


    @app.middleware("request")
    async def inject_session(request):
        request.ctx.session = sessionmaker(bind=engine)()
        request.ctx.session_ctx_token = base_model_session_ctx.set(request.ctx.session)


    @app.middleware("response")
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            base_model_session_ctx.reset(request.ctx.session_ctx_token)
            request.ctx.session.close()


    app.run(host="0.0.0.0", port=8080, debug=True)

import asyncio

from tortoise import Tortoise

from config import TORTOISE_ORM
from models import User, UserGroup, UserAddress


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)

    # In real world app it would be better to use ` bulk_insert` method
    (group_tester, _), (group_developer, _) = await asyncio.gather(
        UserGroup.get_or_create(name="Tester"),
        UserGroup.get_or_create(name="Developer")
    )

    (user_tester, _), (user_developer, _), (user_does_everything, _) = await asyncio.gather(
        User.get_or_create(username="tester", email="tester@test.com"),
        User.get_or_create(username="developer", email="developer@test.com"),
        User.get_or_create(username="does_everything", email="does_everything@test.com")
    )

    await asyncio.gather(
        user_tester.groups.add(group_tester),
        user_developer.groups.add(group_developer),
        user_does_everything.groups.add(group_tester),
        user_does_everything.groups.add(group_developer)
    )

    await asyncio.gather(
        UserAddress.get_or_create(
            user=user_tester,
            address="Test Str 1",
            zip_code="12345",
            city="Test City"
        ),
        UserAddress.get_or_create(
            user=user_developer,
            address="Developer Str 1",
            zip_code="23456",
            city="Developer City"
        ),
        UserAddress.get_or_create(
            user=user_does_everything,
            address="Everything Str 1",
            zip_code="34567",
            city="Everything City"
        ),
        UserAddress.get_or_create(
            user=user_does_everything,
            address="Another Str 1",
            zip_code="34567",
            city="Another City"
        )
    )

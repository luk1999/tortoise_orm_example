import datetime

from tortoise import Model, fields


class UserGroup(Model):
    name: str = fields.CharField(50)

    users: fields.ManyToManyRelation["User"]

    def __str__(self):
        return self.name


class User(Model):
    username: str = fields.CharField(100, unique=True)
    email: str = fields.CharField(254, null=True, unique=True)
    groups: fields.ManyToManyRelation[UserGroup] = fields.ManyToManyField(
        "models.UserGroup",
        through="user_group",
        related_name="users"
    )
    created_at: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime.datetime = fields.DatetimeField(auto_now=True)

    addresses: fields.ReverseRelation["UserAddress"]

    def __str__(self):
        return self.username


class UserAddress(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        related_name="addresses"
    )
    address: str = fields.CharField(100)
    zip_code: str = fields.CharField(5)
    city: str = fields.CharField(50)
    created_at: datetime.datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime.datetime = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.address}, {self.zip_code} {self.city}"

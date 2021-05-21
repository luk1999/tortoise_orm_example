from sqlalchemy.orm import sessionmaker

from models import User, UserAddress, UserGroup


def init_db(engine):
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        def get_or_create_group(name):
            group = session.query(UserGroup).filter_by(name=name).first()
            if not group:
                group = UserGroup(name=name)
                session.add(group)
            return group

        def get_or_create_user(username, email):
            user = session.query(User).filter_by(
                username=username,
                email=email
            ).first()
            if not user:
                user = User(
                    username=username,
                    email=email
                )
                session.add(user)
            return user

        def get_or_create_address(user, street, zip_code, city):
            address = session.query(UserAddress).filter_by(
                user=user,
                address=street,
                zip_code=zip_code,
                city=city
            ).first()
            if not address:
                address = UserAddress(
                    user=user,
                    address=street,
                    zip_code=zip_code,
                    city=city
                )
                session.add(address)
            return address

        group_tester = get_or_create_group("Tester")
        group_developer = get_or_create_group("Developer")

        user_tester = get_or_create_user("tester", "tester@test.com")
        user_developer = get_or_create_user("developer", "developer@test.com")
        user_does_everything = get_or_create_user("does_everything", "does_everything@test.com")

        user_tester.groups.append(group_tester)
        user_developer.groups.append(group_developer)
        user_does_everything.groups.append(group_tester)
        user_does_everything.groups.append(group_developer)

        get_or_create_address(user_tester, "Test Str 1", "12345", "Test City")
        get_or_create_address(user_developer, "Developer Str 1", "23456", "Developer City")
        get_or_create_address(user_does_everything, "Everything Str 1", "34567", "Everything City")
        get_or_create_address(user_does_everything, "Another Str 1", "34567", "Another City")

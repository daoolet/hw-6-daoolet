from attrs import define


@define
class User:
    email: str
    full_name: str
    password: str
    id: int = 0


class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []

    # необходимые методы сюда
    def get_all(self):
        return self.users
    
    def get_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None
    
    def get_by_id(self, id: int) -> User:
        for user in self.users:
            if user.id == id:
                return user
        return None

    def save(self, new_user: User):
        new_user.id = len(self.users) + 1
        self.users.append(new_user)

    # конец решения

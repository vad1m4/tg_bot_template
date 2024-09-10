from template_bot.storage.user_storage import JSONFileUserStorage
from template_bot.config import ADMINS


class UserManager:
    def __init__(self, storage: JSONFileUserStorage):
        self.storage = storage

    def authorize(self, user_id: int, phone_number: int) -> bool:
        if self.is_blacklisted(phone_number) or self.is_blacklisted(user_id):
            return False
        users = self.storage.read()
        users["users"][user_id] = phone_number
        self.storage.write(users)
        return True

    def is_authorized(self, user_id: int) -> bool:
        return str(user_id) in self.storage.read()["users"]

    def blacklist(self, user_identificator: int | str, reason: str) -> None:
        users = self.storage.read()
        users["users"]["blacklist"][user_identificator] = reason
        users["users"] = {
            key: val
            for key, val in users["users"].items()
            if (val != user_identificator and key != user_identificator)
        }
        self.storage.write(users)

    def unblacklist(self, phone_number: int | str) -> bool:
        if not self.is_blacklisted(phone_number):
            return False
        users = self.storage.read()
        users["users"]["blacklist"].pop(phone_number)
        self.storage.write(users)
        return True

    def why_blacklist(self, phone_number: int | str) -> str | None:
        if self.is_blacklisted(phone_number):
            return self.storage.read()["users"]["blacklist"][phone_number]
        return None

    def is_blacklisted(self, user_identificator: int | str) -> bool:
        return str(user_identificator) in self.storage.read()["users"]["blacklist"]

    def is_admin(self, user_id: int) -> bool:
        return user_id in ADMINS

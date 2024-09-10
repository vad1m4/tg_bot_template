from pathlib import Path
import json
from abc import ABC, abstractmethod
from template_bot.time.time import get_date, get_unix, unix_to_date
from typing import Any


class JSONStorage(ABC):
    @abstractmethod
    def save(self, record) -> None: ...

    @abstractmethod
    def read(self) -> dict | list: ...

    @abstractmethod
    def write(self, records) -> None: ...

    @abstractmethod
    def delete(self, index: int) -> None: ...


class JSONFileUserStorage(JSONStorage):
    def __init__(self, jsonfile: Path) -> None:
        self._jsonfile = jsonfile
        self._init_storage()

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text('{"users": {"blacklist": {}}}')

    def read(self) -> dict:
        with open(self._jsonfile, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data

    def write(self, users_d: dict[str, int]) -> None:
        with open(self._jsonfile, "w", encoding="utf-8") as f:
            json.dump(users_d, f, indent=4)

    def save(self, user_id: int) -> None:
        users = self.read()
        users["users"].append(user_id)
        self.write(users)

    def delete(self, user_id: int) -> None:
        users = self.read()
        if self.is_authorized(user_id):
            users["users"].pop(user_id)
        self.write(users)

    def subscribed(self, user_id: int, _type: str) -> bool:
        if user_id in self.read()[_type]:
            return True
        else:
            return False

    def authorize(self, user_id: int, phone_number: int) -> bool:
        if not self.is_blacklisted(phone_number) and not self.is_blacklisted(user_id):
            if not self.is_authorized(user_id):
                users = self.read()
                users["users"][user_id] = phone_number
                self.write(users)
                return True
            else:
                return True
        else:
            return False

    def is_authorized(self, user_id: int) -> bool:
        if str(user_id) in self.read()["users"].keys():
            return True
        else:
            return False

    def blacklist(self, phone_number: int | str, reason: str) -> None:
        users = self.read()
        users["users"]["blacklist"][phone_number] = reason
        users["users"] = {
            key: val
            for key, val in users["users"].items()
            if (val != phone_number and key != phone_number)
        }
        self.write(users)

    def unblacklist(self, phone_number: int | str) -> bool:
        if self.is_blacklisted(phone_number):
            users = self.read()
            users["users"]["blacklist"].pop(phone_number)
            self.write(users)
            return True
        else:
            return False

    def is_blacklisted(self, phone_number: int | str) -> bool:
        if str(phone_number) in self.read()["users"]["blacklist"].keys():
            return True
        else:
            return False

    def why_blacklist(self, phone_number: int | str) -> str | None:
        if self.is_blacklisted(phone_number):
            return self.read()["users"]["blacklist"][phone_number]
        else:
            return None

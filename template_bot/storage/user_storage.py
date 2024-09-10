from pathlib import Path
import json
from template_bot.storage.abstract import JSONStorage
from template_bot.utils import get_date, get_unix, unix_to_date
from typing import Any


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
        users["users"].pop(user_id)
        self.write(users)

    def subscribed(self, user_id: int, _type: str) -> bool:
        if user_id in self.read()[_type]:
            return True
        else:
            return False

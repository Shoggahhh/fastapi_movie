from typing import cast

from redis import Redis

from api.api_v1.auth.services.users_helprer import AbstractUsersHelper
from core.config import settings


class RedisUsersHelper(AbstractUsersHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        return cast(
            str | None,
            self.redis.get(username),
        )

    def add_user(self, username: str, password: str) -> None:
        self.redis.set(username, password)


redis_users = RedisUsersHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.users,
)

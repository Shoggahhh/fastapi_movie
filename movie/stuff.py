from redis import Redis
from core import config


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USER,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    print("user:", redis.get("sam"))
    redis.set("foo", "bar")
    redis.set("number", "42")
    print("foo:", redis.get("foo"))
    print("number:", redis.get("number"))
    print(
        [
            redis.get("number"),
            redis.get("foo"),
            redis.get("spam"),
        ]
    )
    redis.delete("foo")
    print("foo:", redis.get("foo"))


if __name__ == "__main__":
    main()

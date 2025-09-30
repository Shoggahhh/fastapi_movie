from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)


def add(a: int, b: int) -> int:
    return a + b


def main() -> None:
    a = 1
    b = 2
    c = add(a, b)
    print(c)
    print("type c")
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
        ],
    )
    redis.delete("foo")
    print("foo:", redis.get("foo"))
    print("spam:", redis.get("bar"))


if __name__ == "__main__":
    main()

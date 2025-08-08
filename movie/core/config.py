import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIE_STORAGE_DIR = BASE_DIR / "movie.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Never store real tokens here!
# Only fake values
API_TOKENS: frozenset[str] = frozenset(
    {
        "uh4UsYM57lU9PdIemDWeTQ",
        "95SLq20mIZrI9Sl8Hkc9Dg",
    }
)

# Only for demo!
# no users in code!!
USER_DB: dict[str, str] = {
    # username: password
    "sam": "password",
    "bob": "qwerty",
}

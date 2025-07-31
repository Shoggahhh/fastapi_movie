__all__ = ("router",)

from api.api_v1.movie.views.list_views import router
from api.api_v1.movie.views.details_views import router as detail_router


router.include_router(detail_router)

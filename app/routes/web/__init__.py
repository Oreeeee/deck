
from fastapi import APIRouter

from . import screenshots
from . import favourites
from . import ratings
from . import error
from . import title

router = APIRouter()
router.include_router(screenshots.router)
router.include_router(favourites.router)
router.include_router(ratings.router)
router.include_router(error.router)
router.include_router(title.router)

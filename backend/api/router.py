from fastapi import APIRouter

from api import auth, cities, donates, givers, images, messages, takers, users

router = APIRouter()

for _module in (cities, auth, takers, givers, donates, users, messages, images):
    router.include_router(_module.router)

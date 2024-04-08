from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/audio-content",
)

from . import (
    views
)

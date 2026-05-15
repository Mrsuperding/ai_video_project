"""Schemas package"""
from app.schemas.response import Response, PaginatedResponse, ErrorResponse
from app.schemas.auth import *
from app.schemas.user import *
from app.schemas.wallet import *
from app.schemas.digital_human import *
from app.schemas.voice import *
from app.schemas.script import *
from app.schemas.asset import *
from app.schemas.video import *
from app.schemas.message import *
from app.schemas.admin import *

__all__ = [
    "Response", "PaginatedResponse", "ErrorResponse",
]
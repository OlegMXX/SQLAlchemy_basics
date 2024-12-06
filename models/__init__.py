"""
This section is necessary to make Base "know" about it's children
"""

__all__ = (
    "Base",
    "User",
    "Post",
)

from .base import Base
from .user import User
from .post import Post

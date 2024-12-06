from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING: # to prevent cyclic import
    from .user import User


class Post(Base):
    title: Mapped[str] = mapped_column(String(1000))
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    author_id: Mapped[int] = mapped_column(
        # ForeignKey(User.id), # when models are in one .py file
        ForeignKey("users.id")  # when you'll separate classes from each other in many files
    )
    author: Mapped["User"] = relationship(back_populates="posts")  # to create relationship on orm lvl not db
                                                                    # means object, not id

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"title={self.title!r}, "
            f"author_id={self.author_id})"
        )

    def __repr__(self):
        return self.__str__()

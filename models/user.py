from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING: # to prevent cyclic import
    from .post import Post


class User(Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)  # length less or equal 30
    email: Mapped[str]
    motto: Mapped[str | None]

    posts: Mapped[list["Post"]] = relationship(back_populates="author")  # to create relationship on ORM lvl not db
                                                                        # means object, not id

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"motto={self.motto!r})"
        )

    def __repr__(self):
        return self.__str__()

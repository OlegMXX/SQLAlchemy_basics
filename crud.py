import asyncio
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from models import User, Post

import config


async def create_user(
        session: AsyncSession,
        username: str,
        email: str = '',
        motto: str | None = None,
) -> User:
    user = User(
        username=username,
        email=email,
        motto=motto,
    )
    print("new user ", user)

    # async with session.begin(): # just another way to do the same as next two lines
    #     session.add(user)
    session.add(user)
    await session.commit()
    print("created user ", user)

    return user


async def get_users(session: AsyncSession) -> Sequence[User]: # type that scalars().all() returns, the same as list
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    #users = result.all() # returns tuples
    users = result.scalars().all() # returns obj
    print("users ", users)

    return users


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    #stmt = select(User).where(User.id == user_id) # as in get_users()
    user: User | None = await session.get(User, user_id) # session.get() works with id only!
    print(f"user {user_id} ", user)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)

    # return result.scalar_one_or_none()
    user: User | None = result.scalar_one_or_none()
    print("user by username ", username, user)
    return user


async def create_post_for_user(session: AsyncSession, user: User, *post_titles: str,) -> list[Post]:
    posts = [Post(title=title, author_id=user.id) for title in post_titles]
    print(posts)

    async with session.begin_nested():  # _nested allows to use the session that already used by another func,
                                        # get_user_by_something() in this case.
        session.add_all(posts)

    print("saved posts ", posts)
    for post in posts:
        print(post)

    return posts


async def get_posts_with_users(session: AsyncSession):
    #stmt = select(Post).order_by(Post.id) # makes extra queries to get authors
    stmt = select(Post).options(joinedload(Post.author)).order_by(Post.id) # makes JOIN statement to get author
    # instantly and REQUIRED for async query
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    print("posts ", posts)
    for post in posts:
        print('='*7, post)
        print("+", post.author)


async def get_users_with_posts(session: AsyncSession):
    stmt = (select(User)
            .options(
                #joinedload(User.posts) # loads all user attrs every time it gets post
                selectinload(User.posts) # to load users in second query once
            )
            .order_by(User.id)) # means object, not id
    result: Result = await session.execute(stmt)
    #users = result.unique().scalars().all() # use unique() because it's one-to-many relationship in case joinedload()
    users = result.scalars().all()
    for user in users:
        print("="*10, user)
        for post in user.posts:
            print("--", post)

    return users


async def main():
    engine = create_async_engine(
        url=config.DB_URL,
        echo=config.DB_ECHO,
    )

    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,  # to save obj after .commit() and not to get it from DB
    )

    async with async_session() as session:
        # await create_user(
        #     session,
        #     username="john",
        # )
        # await create_user(
        #     session,
        #     username="sam",
        #     email="sam@example.com",
        # )
        # await create_user(
        #     session,
        #     username="nick",
        #     motto="YOLO",
        # )
        # await get_users(session)
        # await get_user_by_id(session, 1)
        # await get_user_by_id(session, 2)
        # await get_user_by_id(session, 0)
        #
        # john: User = await get_user_by_username(session, "john")
        # sam: User = await get_user_by_username(session, "sam")
        # #get_user_by_username(session, "bob")
        #
        # await create_post_for_user(session, john, "P1", "P2")
        # await create_post_for_user(session, sam, "P3", "P4", "P5")

        # await get_posts_with_users(session)
        await get_users_with_posts(session)


if __name__ == '__main__':
    asyncio.run(main())

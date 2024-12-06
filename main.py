from sqlalchemy import create_engine

import config
from models import Base


def main():
    engine = create_engine(
        url=config.DB_URL,
        echo=config.DB_ECHO,
    )

    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()

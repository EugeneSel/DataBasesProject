import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


def isolation_level(level):
    def decorator(view):
        def view_wrapper(*args, **kwargs):
            engine = db.create_engine('oracle://SYSTEM:12345@localhost:1521/xe')
            # connection = engine.connect()
            maker = sessionmaker()
            session = maker(bind=engine.execution_options(isolation_level=level))

            return view(*args, **kwargs)
        return view_wrapper
    return decorator

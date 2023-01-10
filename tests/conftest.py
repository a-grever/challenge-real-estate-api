import pytest
import sqlalchemy as sa

from app import database, models


@pytest.fixture()
def db_engine():
    return sa.create_engine(database.get_url(), pool_pre_ping=True)


@pytest.fixture()
def test_db(db_engine):
    models.Base.metadata.create_all(bind=db_engine)
    yield
    models.Base.metadata.drop_all(bind=db_engine)

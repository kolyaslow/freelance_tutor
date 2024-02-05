import pytest

from api_v1.subject import crud as crud_subject
from api_v1.subject.schemas import CreateSubject
from core import db_helper


@pytest.mark.usefixtures('prepare_database')
@pytest.fixture(scope='session')
async def create_subject():
    subject_in = CreateSubject(name='informatics')
    async with db_helper.session_factory() as session:
        await crud_subject.create_subject(session=session, subject_in=subject_in)
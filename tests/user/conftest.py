import pytest

from api_v1.user import crud as crud_user
from core.db_helper import db_helper


@pytest.mark.usefixtures('create_subject')
@pytest.fixture(scope='session')
async def add_subject_by_tutor(register_tutor, create_subject):

    subject_names = ['informatics']
    user_id = register_tutor['id']
    async with db_helper.session_factory() as session:
        await crud_user.add_subjects_by_user(
            session=session,
            subjects=subject_names,
            user_id=user_id
        )


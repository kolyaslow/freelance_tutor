from tests.conftest import BaseRequestAPI


class CreateOrder(BaseRequestAPI):

    _url = 'oreder/cretae_order'
    _method = 'post'
    _data = {
        'description': None,
        'is_active': True,
        'subject_name': 'informatics',
    }

    
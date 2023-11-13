from api_v1.user import fastapi_users


class CurrentUser():

    def get_superuser(self):
         return fastapi_users.current_user(
             active=True,
             superuser=True,
         )

current_user = CurrentUser()
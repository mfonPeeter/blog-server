from .models import *


class GetRecord:
    def user(self, **kwargs):
        result = UserAccount.get_or_none(UserAccount.email == kwargs['email'])
        return result

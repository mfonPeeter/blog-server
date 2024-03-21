from .models import *


class CreateRecord:
    def user(self, **kwargs):
        UserAccount.create(
            public_id=kwargs['public_id'],
            f_name=kwargs['f_name'],
            l_name=kwargs['l_name'],
            email=kwargs['email'],
            user_password=kwargs['password']
        )

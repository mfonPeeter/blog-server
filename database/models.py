from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import db_settings

# Connect to a Postgres database.
psql_db = PostgresqlExtDatabase(
    db_settings.DATABASES['NAME'],
    user=db_settings.DATABASES['USER'],
    password=db_settings.DATABASES['PASSWORD'],
    host=db_settings.DATABASES['HOST']
)


class BaseModel(Model):
    class Meta:
        database = psql_db


class UserAccount(BaseModel):
    user_id = AutoField()
    public_id = CharField(max_length=50, unique=True)
    f_name = CharField(max_length=100)
    l_name = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)
    user_password = CharField(max_length=130)

    class Meta:
        table_name = 'user_account'

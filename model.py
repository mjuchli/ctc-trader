import peewee as pw
import os

db = (pw.MySQLDatabase(
            os.environ['CTC_TRADER_DB'],
            host=os.environ['CTC_TRADER_HOST'],
            port=int(os.environ['CTC_TRADER_PORT']),
            user=os.environ['CTC_TRADER_USER'],
            passwd=os.environ['CTC_TRADER_PASSWORD']))

db_test = (pw.MySQLDatabase(
            os.environ['CTC_TRADER_TEST_DB'],
            host=os.environ['CTC_TRADER_TEST_HOST'],
            port=int(os.environ['CTC_TRADER_TEST_PORT']),
            user=os.environ['CTC_TRADER_TEST_USER'],
            passwd=os.environ['CTC_TRADER_TEST_PASSWORD']))

class MySQLModelTrader(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db

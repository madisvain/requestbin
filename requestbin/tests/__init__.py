from requestbin.models import db, Bin, Request

class TestBase(object):
    def setup(self):
        db.create_tables(models=[Bin, Request])

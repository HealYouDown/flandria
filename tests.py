from flask_testing import TestCase
import unittest
from webapp import create_app, db
import logging


import webapp.database.models as database_models
from webapp.database.helpers import TABLENAMES, tablename_to_class_name

logger = logging.Logger("test")
logger.setLevel(logging.INFO)
# create file handler that logs debug and higher level messages
fh = logging.FileHandler("test.log")
# stream handler
sh = logging.StreamHandler()
sh.setLevel(logging.ERROR)
# create console handler with a higher log level
ch = logging.StreamHandler()
# formatter
formatter = logging.Formatter(fmt="[%(levelname)s, %(name)s] %(asctime)s - %(message)s")
ch.setFormatter(formatter)
sh.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
logger.addHandler(sh)

class MyTest(TestCase):

    render_templates = False

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config["SQLALCHEMY_ECHO"] = False
        return app

    def runTest(self):
        self.test_database_urls()

    def test_database_urls(self):
        with self.app.app_context():

            for tablename in TABLENAMES:

                table_cls = getattr(database_models, tablename_to_class_name(tablename))
                count = db.session.query(table_cls).count()

                logger.info(f"Testing {tablename}")
                logger.info(f"Found {count} Items")

                for index, code in enumerate(db.session.query(table_cls.code).all()):
                    c = code[0]
                    logger.debug(f"Testing URL: database/{tablename}/{c} ({index}/{count})")
                    result = self.client.get(f"/database/{tablename}/{c}")
                    try:
                        self.assertEqual(result.status_code, 200) 
                    except Exception as e:
                        logger.error(e)
                        logger.error(f"Error {result.status_code} - /database/{tablename}/{c}")


if __name__ == "__main__":
    unittest.main()

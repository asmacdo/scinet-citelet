# Imports
import unittest
import json
import glob
import time
import uuid
import os

# Project imports
from pytelet import config
from pytelet import dbsetup
from drivers import ChromeExtensionDriver, \
                    ChromeBookmarkletDriver, \
                    FirefoxBookmarkletDriver \

#from make_fixtures import drop_fields

# Set up test database
client, database = dbsetup.dbsetup(test=True)

def suite_factory(driver_class):

    class suite(unittest.TestCase):
        
        def clearDB(self):
            
            for collection in database.collection_names():

                if not collection.startswith('system') and collection != config.COLLNAME:
                    database.drop_collection(collection)

        def setUp(self):
            
            self.clearDB()
            
        def tearDown(self):
        
           self.clearDB()
        
        @classmethod
        def setUpClass(cls):
            
            # Open driver
            cls.driver = driver_class()

        @classmethod
        def tearDownClass(cls):
            
            # Quit browser
            cls.driver.browser.quit()
        
    return suite

suites = [
    suite_factory(ChromeBookmarkletDriver),
#    suite_factory(FirefoxBookmarkletDriver),
#    suite_factory(ChromeExtensionDriver),
]

def add_test(fixture):
    
    # Load fixture data
    json_fixture = json.load(open(fixture))
    short_name = os.path.split(fixture)[-1]\
        .split('.json')[0]

    # Define test method
    def _test(self):
        
        # Get collection
        testid = uuid.uuid1()
        collection = getattr(database, str(testid))

        # Run driver
        self.driver.drive(short_name, testid)

        # Listen for database
        for tryidx in range(25):
            cursor = collection.find()
            if cursor.count():
                break
            time.sleep(0.5)

        # Test cursor count
        self.assertEqual(cursor.count(), 1)
        for field in ['publisher', 'head_ref', 'cited_refs']:
            self.assertEqual(cursor[0][field], json_fixture[field])
    
    # Add test method to class
    for suite in suites:
        setattr(suite, 'test_%s' % (short_name), _test)

# Load fixtures
fixtures = glob.glob('%s/tests/fixtures/*.json' % (config.path))

# Generate tests for each fixture
for fixture in fixtures:
    add_test(fixture)

# Run tests
if __name__ == '__main__':
    for s in suites:
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(s))
        unittest.TextTestRunner().run(suite)

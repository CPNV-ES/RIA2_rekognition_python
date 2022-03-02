import unittest
import settings
import os


class EnvironmentTestCase(unittest.TestCase):
    def test_domain_set(self):
        domain = os.getenv("DOMAIN")
        self.assertFalse(not domain, "DOMAIN env is not set")

    def test_bucket_name_set(self):
        bucket_name = os.getenv("BUCKET_NAME")
        self.assertFalse(not bucket_name, "BUCKET_NAME env is not set")
       

    def test_bucket_url_set(self):
        bucket_url = os.getenv("BUCKET_URL")
        self.assertFalse(not bucket_url, "BUCKET_URL env is not set")

    def test_bucket_url_format(self):
        bucket_name = os.getenv("BUCKET_NAME")
        domain = os.getenv("DOMAIN")
        bucket_url = os.getenv("BUCKET_URL")

        expectedUrl = bucket_name + "." + domain

        self.assertEqual(bucket_url, expectedUrl, "the format of bucket url is not corresponding with the wanted one try to use ${BUCKET_NAME}.${DOMAIN} format")

    def test_bucket_folder_set(self):
        bucket_folder = os.getenv("BUCKET_FOLDER")
        self.assertFalse(not bucket_folder, "BUCKET_FOLDER env is not set")

if __name__ == '__main__':
    unittest.main()
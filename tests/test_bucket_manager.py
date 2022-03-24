import unittest
import asyncio
import os

from flaskr.aws_bucket_manager import AwsBucketManager


class BucketManagerTestCase(unittest.IsolatedAsyncioTestCase):
    """
    This test class is designed to confirm the AwsBucketManager class's behavior
    """

    def setUp(self):
        """
        This test method initializes the context before each test method run.
        """
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.file = open("C:/Users/Dylan.OLIVEIRA-RAMOS/Downloads/monkey.jpg",
                         "rb")
        self.object_name = "monkey.jpg"
        self.bucket_manager = AwsBucketManager()

    async def test_create_object_with_object_not_existing_success(self):
        """
        This test method checks the method in charge of creating a new object
        We try to create a new object
        """
        # Given
        self.assertFalse(
            self.bucket_manager.object_exists(self.bucket_name,
                                              self.object_name))

        # When
        await self.bucket_manager.create_object(self.bucket_name, self.file)

        # Then
        self.assertTrue(
            self.bucket_manager.object_exists(self.bucket_name, self.file))

    async def test_download_object_nominal_case_success(self):
        """
        This test method checks the method in charge of uploading item in an existing bucket
        """
        # Given
        await self.bucket_manager.create_object(self.bucket_name, self.file)

        self.assertTrue(
            self.bucket_manager.object_exists(self.bucket_name,
                                              self.object_name))

        # When
        await self.bucket_manager.download_object(self.bucket_name,
                                                  self.object_name)

        # Then
        self.assertTrue(
            os.path.exists('%s%s' %
                           (os.getenv('STORAGE_FOLDER'), self.object_name)))

    async def test_is_object_exists_nominal_case_success(self):
        """
        This test method checks the method in charge of testing the existence of an object
        """
        # Given
        await self.bucket_manager.create_object(self.bucket_name, self.file)

        # When
        actual_result = await self.bucket_manager.object_exists(
            self.bucket_name, self.object_name)

        # Then
        self.assertTrue(actual_result)

    def tearDown(self) -> None:
        self.file.close()
        self.bucket_manager.remove_object(self.bucket_name, self.object_name)
        return super().tearDown()

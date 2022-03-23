import unittest
import asyncio
import os

from flaskr.aws_bucket_manager import AwsBucketManager


class BucketManagerTestCase(unittest.TestCase):
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
        self.bucket_manager = AwsBucketManager()

    async def test_create_object_with_object_not_existing_success(self):
        """
        This test method checks the method in charge of creating a new object
        We try to create a new object
        """
        object_name = "monkey.jpg"

        # Given
        self.assertFalse(await self.bucket_manager.object_exists(
            self.bucket_name, object_name))

        # When
        await self.bucket_manager.create_object(self.bucket_name, self.file)

        # Then
        self.assertTrue(await self.bucket_manager.object_exists(
            self.bucket_name, self.file))

    def tearDown(self) -> None:
        self.file.close()
        return super().tearDown()

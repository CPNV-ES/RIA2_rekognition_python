import unittest
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
        self.bucket_manager = AwsBucketManager()
        # Should be -> os.getenv('BUCKET_NAME') but it is not working
        self.bucket_name = 'ria2python.actualit.info'
        self.file_path = 'C:/Users/Dylan.OLIVEIRA-RAMOS/Downloads/monkey.jpg'
        self.object_name = self.file_path.split("/")[-1]

    async def test_create_not_existing_bucket(self):
        """
        This test method checks the method in charge of creating a new object
        We try to create a new bucket
        """
        # Given
        self.assertFalse(await self.bucket_manager.object_exists(self.bucket_name))

        # When
        await self.bucket_manager.create_object(self.bucket_name)

        # Then
        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_name))

    async def test_create_not_existing_object_with_existing_bucket(self):
        """
        This test method checks the method in charge of creating a new object
        Note : the bucket exists
        """
        # Given
        await self.bucket_manager.create_object(self.bucket_name)
        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_name))
        self.assertFalse(await self.bucket_manager.object_exists(self.object_name))

        # When
        await self.bucket_manager.create_object(self.file_path)

        # Then
        self.assertTrue(await self.bucket_manager.object_exists(self.object_name))

    async def test_create_not_existing_object_not_existing_bucket(self):
        pass

    async def test_download_existing_object(self):
        """
        This test method checks the method in charge of downloading an object from an existing bucket
        """
        # Given
        await self.bucket_manager.create_object(self.bucket_name, self.file_path)
        self.assertTrue(await self.bucket_manager.object_exists(self.object_name))

        # When
        await self.bucket_manager.download_object(self.bucket_name,
                                                  self.object_name)

        # Then
        self.assertTrue(
            os.path.exists('%s%s' %
                           (os.getenv('STORAGE_FOLDER'), self.object_name)))

    async def test_object_existing(self):
        """
        This test method checks the method in charge of testing the existence of an object
        """
        # Given
        await self.bucket_manager.create_object(self.file_path)

        # When
        result = await self.bucket_manager.object_exists(self.object_name)

        # Then
        self.assertTrue(result)

    async def test_object_not_existing(self):
        """
        This test method checks the method in charge of testing the non existence of an object
        """
        # Given
        await self.bucket_manager.create_object(self.file_path)
        self.assertTrue(await self.bucket_manager.object_exists(self.object_name))
        not_existing_file = "notexistingfile.jpg"

        # When
        result = await self.bucket_manager.object_exists(not_existing_file)

        # Then
        self.assertFalse(result)

    async def test_remove_existing_object(self):
        """
        This test method checks the method in charge of removing an existing object
        """
        # Given
        await self.bucket_manager.create_object(self.file_path)
        self.assertTrue(await self.bucket_manager.object_exists(self.object_name))

        # When
        await self.bucket_manager.remove_object(self.bucket_name, self.object_name)

        # Then
        self.assertFalse(await self.bucket_manager.object_exists(self.bucket_name, self.object_name))

    async def asyncTearDown(self):
        await self.bucket_manager.remove_object(self.object_name)

        if await self.bucket_manager.object_exists(self.bucket_name):
            await self.bucket_manager.remove_object(self.bucket_name)

        return super().tearDown()

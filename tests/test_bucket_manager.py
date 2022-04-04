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
        self.bucket_name = 'ria2.testbucketmanager.diduno.education'
        self.file_path = 'C:\\Users\\dylan\\Downloads\\duck.jpg'
        self.object_name = os.path.basename(self.file_path)

    async def test_create_not_existing_bucket(self):
        """
        This test method checks the method in charge of creating a new object
        We try to create a new bucket
        """
        # Given
        self.assertFalse(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))

        # When
        await self.bucket_manager.create_object(bucket_name=self.bucket_name)

        # Then
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))

    async def test_create_not_existing_object_with_existing_bucket(self):
        """
        This test method checks the method in charge of creating a new object
        Note : the bucket exists
        """
        # Given
        await self.bucket_manager.create_object(bucket_name=self.bucket_name)
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))
        self.assertFalse(await self.bucket_manager.object_exists(object_name=self.object_name))

        # When
        await self.bucket_manager.create_object(bucket_name=self.bucket_name, object_file_path=self.file_path)

        # Then
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name, object_name=self.object_name))

    async def test_create_not_existing_object_with_not_existing_bucket(self):
        """
        This test method checks the method in charge of creating a new data object
        Note : the bucket doesn't exist
        """
        # Given
        self.assertFalse(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))
        self.assertFalse(await self.bucket_manager.object_exists(object_name=self.object_name))

        # When
        await self.bucket_manager.create_object(bucket_name=self.bucket_name, object_file_path=self.file_path)

        # Then
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name, object_name=self.object_name))

    async def test_download_existing_object(self):
        """
        This test method checks the method in charge of downloading an object from an existing bucket
        """
        # Given
        await self.bucket_manager.create_object(bucket_name=self.bucket_name, object_file_path=self.file_path)
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name, object_name=self.object_name))

        # When
        await self.bucket_manager.download_object(self.bucket_name, self.object_name)

        # Then
        self.assertTrue(
            os.path.exists('%s%s' %
                           (os.getenv('STORAGE_FOLDER'), self.object_name)))

    async def test_bucket_existing(self):
        """
        This test method checks the method in charge of testing the existence of an object
        """
        # Given
        await self.bucket_manager.create_object(bucket_name=self.bucket_name)

        # When
        result = await self.bucket_manager.object_exists(bucket_name=self.bucket_name)

        # Then
        self.assertTrue(result)

    async def test_bucket_not_existing(self):
        """
        This test method checks the method in charge of testing the non existence of an object
        When the object doesn't exist (object is the bucket)
        """
        # Given
        not_existing_bucket = "notexistingbucket"

        # When
        result = await self.bucket_manager.object_exists(bucket_name=not_existing_bucket)

        # Then
        self.assertFalse(result)

    async def test_file_not_existing(self):
        """
        This test method checks the method in charge of testing the non existence of an object
        When the object doesn't exist (object is the file in an existing bucket)
        """
        # Given
        await self.bucket_manager.create_object(bucket_name=self.bucket_name)
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))
        not_existing_file = "notexistingfile.jpg"

        # When
        result = await self.bucket_manager.object_exists(bucket_name=self.bucket_name, object_name=not_existing_file)

        # Then
        self.assertFalse(result)

    async def test_remove_empty_bucket(self):
        """
        This test method checks the method in charge of removing an existing object
        Case : empty bucket
        """
        # Given
        await self.bucket_manager.create_object(bucket_name=self.bucket_name)
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))

        # When
        await self.bucket_manager.remove_object(bucket_name=self.bucket_name)

        # Then
        self.assertFalse(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))

    async def test_remove_not_empty_bucket(self):
        """
        This test method checks the method in charge of removing an existing object
        Case : bucket with content
        """
        # Given
        await self.bucket_manager.create_object(bucket_name=self.bucket_name)
        await self.bucket_manager.create_object(bucket_name=self.bucket_name, object_file_path=self.file_path)
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))
        self.assertTrue(await self.bucket_manager.object_exists(bucket_name=self.bucket_name, object_name=self.object_name))

        # When
        await self.bucket_manager.remove_object(bucket_name=self.bucket_name)

        # Then
        self.assertFalse(await self.bucket_manager.object_exists(bucket_name=self.bucket_name))

    async def asyncTearDown(self):
        # Remove object
        if await self.bucket_manager.object_exists(bucket_name=self.bucket_name, object_name=self.object_name):
            await self.bucket_manager.remove_object(bucket_name=self.bucket_name, object_name=self.object_name)

        # Remove bucket
        if await self.bucket_manager.object_exists(bucket_name=self.bucket_name):
            await self.bucket_manager.remove_object(bucket_name=self.bucket_name)

        # Remove file
        if os.path.exists('%s%s' % (os.getenv('STORAGE_FOLDER'), self.object_name)):
            os.remove('%s%s' % (os.getenv('STORAGE_FOLDER'), self.object_name))

        return super().tearDown()

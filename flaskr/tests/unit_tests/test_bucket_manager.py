import unittest
import asyncio
import os
from aws_bucket_manager import AwsBucketManager


class BucketManagerTestCase(unittest.TestCase):
    """
    This test class is designed to confirm the AwsBucketManager class's behavior
    """

    def setUp(self):
        """
        This test method initializes the context before each test method run.
        """
        self.path_to_test_folder = ''
        self.bucket_name = ''
        self.domain = ''
        self.bucket_url = '%s.%s' % (self.bucket_name, self.domain)
        self.image_name = ''
        self.full_path_to_image = '%s\\%s' % (
            self.path_to_test_folder, self.image_name)
        self.prefix_object_downloaded = ''
        self.bucket_manager = AwsBucketManager(self.bucket_url)

    async def test_create_object_create_new_bucket_success(self):
        """
        This test method checks the method in charge of creating a new object
        We try to create a new bucket
        """
        # Given
        self.assertFalse(await self.bucket_manager.object_exists(self.bucket_url))

        # When
        await self.bucket_manager.create_object(self.bucket_url)

        # Then
        self.assertTrue(await self.bucket_manager.object_exists)

    async def test_create_object_create_object_with_existing_bucket_success(self):
        """
        This test method checks the method in charge of creating a new data object
        Note : the bucket exists
        """
        # Given
        file_name = self.image_name
        object_url = '%s/%s' % (self.bucket_url, self.image_name)
        await self.bucket_manager.create_object(self.bucket_url)

        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_url))
        self.assertFalse(await self.bucket_manager.object_exists(object_url))

        # When
        await self.bucket_manager.create_object(object_url, ('%s//%s') % (self.full_path_to_image, file_name))

        # Then
        self.assertTrue(await self.bucket_manager.object_exists(object_url))

    async def test_create_object_create_object_bucket_not_exist_success(self):
        """
        This test method checks the method in charge of creating a new data object
        Note : the bucket doesn't exist
        """
        # Given
        file_name = self.image_name
        object_url = '%s/%s' % (self.bucket_url, self.image_name)
        await self.bucket_manager.create_object(self.bucket_url)

        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_url))
        self.assertFalse(await self.bucket_manager.object_exists(object_url))

        # When
        await self.bucket_manager.create_object(object_url, ('%s//%s') % (self.full_path_to_image, file_name))

        # Then
        self.assertFalse(await self.bucket_manager.object_exists(object_url))

    async def test_download_object_nominal_case_success(self):
        """
        This test method checks the method in charge of uploading item in an existing bucket
        """
        # Given
        object_url = '%s//%s' % (self.bucket_url, self.image_name)
        destination_full_path = '%s//%s%s' % (
            self.path_to_test_folder, self.prefix_object_downloaded, self.image_name)
        await self.bucket_manager.create_object('%s%s//%s' % (object_url, self.path_to_test_folder, self.image_name))

        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_url))

        # When
        await self.bucket_manager.download_object(object_url, destination_full_path)

        # Then
        self.assertTrue(os.path.exists(destination_full_path))

    async def test_is_object_exists_nominal_case_success(self):
        """
        This test method checks the method in charge of testing the existence of an object
        """
        # Given
        await self.bucket_manager.create_object(self.bucket_url)

        # When
        actual_result = await self.bucket_manager.object_exists(self.bucket_url)

        # Then
        self.assertTrue(actual_result)

    async def test_is_object_exists_object_not_exist_bucket_success(self):
        """
        This test method checks the method in charge of testing the existence of an object
        When the object doesn't exist (object is the bucket)
        """
        # Given
        not_existing_bucket = 'notExistingBucket%s' % (self.domain)

        # When
        actual_result = await self.bucket_manager.object_exists(not_existing_bucket)

        # Then
        self.assertTrue(actual_result)

    async def test_is_object_exists_object_not_exist_file_success(self):
        """
        This test method checks the method in charge of testing the existence of an object
        When the object doesn't exist (object is the file in an existing bucket)
        """
        # Given
        await self.bucket_manager.create_object(self.bucket_url)
        not_existing_file = '%s//notExistingFile.jpg' % (self.bucket_url)

        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_url))

        # When
        actual_result = await self.bucket_manager.object_exists(not_existing_file)

        # Then
        self.assertFalse(actual_result)

    async def test_remove_object_empty_bucket_success(self):
        """
        This test method checks the method in charge of removing an existing object
        Case : empty bucket
        """
        # Given
        await self.bucket_manager.create_object(self.bucket_url)

        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_url))

        # When
        await self.bucket_manager.remove_object(self.bucket_url)

        # Then
        self.assertFalse(await self.bucket_manager.object_exists(self.bucket_url))

    async def test_remove_object_not_empty_bucket_success(self):
        """
        This test method checks the method in charge of removing an existing object
        Case : bucket with content
        """
        # Given
        file_name = self.image_name
        object_url = '%s/%s' % (self.bucket_url, self.image_name)
        await self.bucket_manager.create_object(self.bucket_url)
        await self.bucket_manager.create_object('%s%s//%s' % (object_url, self.path_to_test_folder, file_name))

        self.assertTrue(await self.bucket_manager.object_exists(self.bucket_url))
        self.assertTrue(await self.bucket_manager.object_exists(object_url))

        # When
        await self.bucket_manager.remove_object(self.bucket_url)

        # Then
        self.assertFalse(await self.bucket_manager.object_exists(self.bucket_url))

    async def tearDown(self) -> None:
        destination_full_path = '%s\\%s%s' % (
            self.path_to_test_folder, self.prefix_object_downloaded, self.image_name)

        if (os.path.exists(destination_full_path)):
            os.remove(destination_full_path)

        self.bucket_manager = AwsBucketManager(self.bucket_url)
        if (await self.bucket_manager.object_exists(self.bucket_url)):
            await self.bucket_manager.remove_object(self.bucket_url)

        return super().tearDown()

from abc import ABC
from flaskr.api.managers.aws_bucket_manager import AwsBucketManager


class IBucketManager(ABC):
    def __init__(self):
        self.bucket_manager = AwsBucketManager()

    async def upload_file(self, bucket_name, file):
        return await self.bucket_manager.upload_file(bucket_name, file)

    async def create_object(self, bucket_name=None, object_file_path=None):
        return await self.bucket_manager.create_object(bucket_name=bucket_name, object_file_path=object_file_path)

    async def object_exists(self, bucket_name=None, object_name=None):
        return await self.bucket_manager.object_exists(bucket_name=bucket_name, object_name=object_name)

    async def remove_object(self, bucket_name=None, object_name=None):
        return await self.bucket_manager.remove_object(bucket_name=bucket_name, object_name=object_name)

    async def download_object(self, bucket_name, object_name):
        return await self.bucket_manager.download_object(bucket_name, object_name)

    async def _create_bucket(self, bucket_name):
        return await self.bucket_manager._create_bucket(bucket_name)

    async def _create_object(self, bucket_name, file_path):
        return await self.bucket_manager._create_object(bucket_name, file_path)

    async def _get_presigned_url(self, bucket_name, object_name):
        return await self.bucket_manager._get_presigned_url(bucket_name, object_name)

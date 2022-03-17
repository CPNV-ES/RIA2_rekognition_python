import boto3
import asyncio
import os


class AwsBucketManager:
    """
    Aws Bucket Manager using s3 resource
    Useful link : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
    """

    def __init__(self) -> None:
        self.s3 = boto3.resource('s3')

    async def create_object(self, bucket_name, file):
        """
        Create an object on s3
        """
        try:
            self.s3.Bucket(bucket_name).Object(file.filename).put(Body=file)
        except:
            return 'An error occured.', 400

        return 'The file has been uploaded.', 201

    def object_exists(self, bucket_name, file_name):
        """
        Check if the object exists on s3
        """
        try:
            self.s3.Bucket(bucket_name).Object(file_name).load()
        except:
            return False

        return True

    async def download_object(self, bucket_name, file_name):
        """
        Download an object from s3
        """
        self.s3.Bucket(bucket_name).Object(file_name).download_file('%s%s' % (os.getenv('STORAGE_FOLDER'), file_name))

        return 'The file has been downloaded.', 200

    async def remove_object(self, bucket_name, file_name):
        """
        Delete an object on s3
        """
        self.s3.Bucket(bucket_name).Object(file_name).delete()

        return 'The file has been deleted.', 204


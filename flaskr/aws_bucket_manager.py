import boto3
import asyncio


class AwsBucketManager:
    """
    Aws Bucket Manager using s3 resource
    Useful link : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
    """

    def __init__(self) -> None:
        self.s3 = boto3.resource('s3')

    async def create_object(self, bucket_name, file):
        try:
            self.s3.Bucket(bucket_name).Object(file.filename).put(Body=file)
        except:
            return 'An error occured.', 400

        return 'The file has been uploaded.', 201

    def object_exists(self, bucket_name, file_name):
        try:
            self.s3.Bucket(bucket_name).Object(file_name).load()
        except:
            return False

        return True

    def download_object(self):
        pass

    def remove_object(self):
        pass

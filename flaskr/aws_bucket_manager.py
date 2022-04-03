import boto3
import os

from werkzeug.utils import secure_filename


class AwsBucketManager:
    """
    Aws Bucket Manager using s3 resource
    Useful link : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
    """

    def __init__(self) -> None:
        self.s3 = boto3.client('s3')
        self.storage_folder = os.getenv('STORAGE_FOLDER')
        self.s3_default_region = os.getenv('AWS_DEFAULT_REGION')

    async def upload_file(self, bucket_name, file):
        """
        Create an object on s3 using a multipart upload
        """
        filename = secure_filename(file.filename)
        file.save(os.path.join(self.storage_folder, filename))
        file_path = '%s%s' % (self.storage_folder, filename)

        result = await self.create_object(bucket_name=bucket_name, object_file_path=file_path)

        return result, 200

    async def create_object(self, bucket_name=None, object_file_path=None):
        """
        Create a bucket or an object on s3
        """
        if bucket_name and not object_file_path:
            if await self.object_exists(bucket_name=bucket_name):
                object_url = "http://s3-%s.amazonaws.com/%s/" % (self.s3_default_region, bucket_name)

                return object_url
            else:
                try:
                    self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                                        'LocationConstraint': self.s3_default_region})
                except:
                    return False

        if bucket_name and object_file_path:
            file_name = object_file_path.split("\\")[-1]

            if await self.object_exists(bucket_name=bucket_name):
                try:
                    self.s3.put_object(Bucket=bucket_name,
                                       Key=file_name, Body=object_file_path)

                    object_url = "http://s3-%s.amazonaws.com/%s/%s" % (self.s3_default_region, bucket_name, file_name)

                    return object_url
                except:
                    return False
            else:
                try:
                    self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                                        'LocationConstraint': self.s3_default_region})

                    self.s3.put_object(Bucket=bucket_name,
                                       Key=file_name, Body=object_file_path)

                    object_url = "http://s3-%s.amazonaws.com/%s/%s" % (self.s3_default_region, bucket_name, file_name)

                    return object_url
                except:
                    return False
        
        return False

    async def object_exists(self, bucket_name=None, object_name=None):
        """
        Check if the bucket or the object exists on s3
        """
        if bucket_name and not object_name:
            try:
                self.s3.head_bucket(Bucket=bucket_name)

                return True
            except:
                return False

        if bucket_name and object_name:
            try:
                self.s3.head_object(Bucket=bucket_name, Key=object_name)

                return True
            except:
                return False
        
        return False

    async def download_object(self, bucket_name, object_name):
        """
        Download an object from s3
        """
        try:
            self.s3.download_file(bucket_name, object_name, '%s%s' % (
                self.storage_folder, object_name))
        except:
            return False

        return True

    async def remove_object(self, bucket_name=None, object_name=None):
        """
        Delete a bucket or an object on s3
        """
        s3_resource = boto3.resource('s3')

        if bucket_name and not object_name:
            try:
                s3_resource.Bucket(bucket_name).objects.all().delete()
                self.s3.delete_bucket(Bucket=bucket_name)

                return True
            except:
                return False
        
        if bucket_name and object_name:
            try:
                s3_resource.Object(bucket_name, object_name).delete()

                return True
            except:
                return False
        
        return False

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
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.storage_folder = os.getenv('STORAGE_FOLDER')
        self.s3_default_region = os.getenv('AWS_DEFAULT_REGION')

    async def upload_file(self, file):
        """
        Create an object on s3 using a multipart upload
        """
        filename = secure_filename(file.filename)
        file.save(os.path.join(self.storage_folder, filename))
        file_path = '%s%s' % (self.storage_folder, filename)

        result = await self.create_object(file_path)

        os.remove('%s%s' % (self.storage_folder, filename))

        return result

    async def create_object(self, object_name):
        """
        Create a bucket or an object on s3
        object_name => bucket_name or file_path
        """
        s3_bucket_exists_waiter = self.s3.get_waiter('bucket_exists')
        s3_object_exists_waiter = self.s3.get_waiter('object_exists')

        try:
            self.s3.create_bucket(Bucket=object_name, CreateBucketConfiguration={
                                  'LocationConstraint': self.s3_default_region})
            # Retrieve waiter instance that will wait till a specified S3 bucket exists
            s3_bucket_exists_waiter.wait(Bucket=object_name, WaiterConfig={
                                         'Delay': 2, 'MaxAttempts': 10})
        except:
            if await self.object_exists(self.bucket_name):
                try:
                    file_name = object_name.split("/")[-1]
                    self.s3.put_object(Bucket=self.bucket_name,
                                       Key=file_name, Body=object_name)

                    # Retrieve waiter instance that will wait till a specified S3 object exists
                    s3_object_exists_waiter.wait(
                        Bucket=self.bucket_name, Key=object_name, WaiterConfig={'Delay': 2, 'MaxAttempts': 10})
                except:
                    return False
            else:
                try:
                    self.s3.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={
                                          'LocationConstraint': self.s3_default_region})
                    # Retrieve waiter instance that will wait till a specified S3 bucket exists
                    s3_bucket_exists_waiter.wait(Bucket=self.bucket_name, WaiterConfig={
                                                 'Delay': 2, 'MaxAttempts': 10})

                    file_name = object_name.split("/")[-1]
                    self.s3.put_object(Bucket=self.bucket_name,
                                       Key=file_name, Body=object_name)

                    # Retrieve waiter instance that will wait till a specified S3 object exists
                    s3_object_exists_waiter.wait(
                        Bucket=self.bucket_name, Key=object_name, WaiterConfig={'Delay': 2, 'MaxAttempts': 10})
                except:
                    return False

        return True

    async def object_exists(self, object_name):
        """
        Check if the bucket or the object exists on s3
        """
        try:
            self.s3.head_bucket(Bucket=object_name)
        except:
            try:
                self.s3.head_object(Bucket=self.bucket_name, Key=object_name)
            except:
                return False

        return True

    async def download_object(self, object_name):
        """
        Download an object from s3
        """
        try:
            self.s3.download_file(self.bucket_name, object_name, '%s%s' % (
                self.storage_folder, object_name))
        except:
            return False

        return True

    async def remove_object(self, object_name):
        """
        Delete a bucket or an object on s3
        """
        s3_resource = boto3.resource('s3')

        try:
            s3_resource.Bucket(self.bucket_name).objects.all().delete()
            self.s3.delete_bucket(Bucket=object_name)
        except:
            try:
                s3_resource.Bucket(self.bucket_name).Object(
                    object_name).delete()
            except:
                return False

        return True

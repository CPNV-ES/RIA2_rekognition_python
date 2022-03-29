import boto3
import os


class AwsBucketManager:
    """
    Aws Bucket Manager using s3 resource
    Useful link : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
    """

    def __init__(self) -> None:
        self.s3 = boto3.resource('s3')
        self.client = boto3.client('s3')
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.storage_folder = os.getenv('STORAGE_FOLDER')

    async def create_object_with_multipart(self, bucket_name, file):
        """
        Create an object on s3
        """
        try:
            self.s3.Bucket(bucket_name).Object(file.filename).put(Body=file)
        except:
            return 'An error occured.', 400

        return True

    async def create_object(self, object_name):
        """
        Create a bucket or an object on s3
        object_name => bucket_name or file_path
        """
        s3_bucket_exists_waiter = self.client.get_waiter('bucket_exists')
        s3_object_exists_waiter = self.client.get_waiter('object_exists')

        try:
            self.s3.create_bucket(Bucket=object_name, CreateBucketConfiguration={'LocationConstraint': os.getenv(
                'AWS_DEFAULT_REGION')})
            # Retrieve waiter instance that will wait till a specified S3 bucket exists
            s3_bucket_exists_waiter.wait(Bucket=object_name)
        except:
            if self.object_exists(self.bucket_name):
                try:
                    file_name = object_name.split("/")[-1]
                    self.s3.Bucket(self.bucket_name).Object(
                        file_name).upload_file(object_name)

                    # Retrieve waiter instance that will wait till a specified S3 object exists
                    s3_object_exists_waiter.wait(
                        Bucket=self.bucket_name, Key=object_name)
                except:
                    return False
            else:
                try:
                    self.s3.create_bucket(Bucket=self.bucket_name, CreateBucketConfiguration={'LocationConstraint': os.getenv(
                        'AWS_DEFAULT_REGION')})
                    # Retrieve waiter instance that will wait till a specified S3 bucket exists
                    s3_bucket_exists_waiter.wait(Bucket=self.bucket_name)

                    file_name = object_name.split("/")[-1]
                    self.s3.Bucket(self.bucket_name).Object(
                        file_name).upload_file(object_name)

                    # Retrieve waiter instance that will wait till a specified S3 object exists
                    s3_object_exists_waiter.wait(
                        Bucket=self.bucket_name, Key=object_name)
                except:
                    return False

        return True

    async def object_exists(self, object_name):
        """
        Check if the bucket or the object exists on s3
        """
        try:
            self.client.head_bucket(Bucket=object_name)
        except:
            try:
                self.s3.Bucket(self.bucket_name
                               ).Object(object_name).load()
            except:
                return False

        return True

    async def download_object(self, bucket_name, file_name):
        """
        Download an object from s3
        """
        self.s3.Bucket(bucket_name).Object(file_name).download_file(
            '%s%s' % (self.storage_folder, file_name))

        return 'The file has been downloaded.', 200

    async def remove_object(self, object_name):
        """
        Delete an object on s3
        """
        try:
            self.client.delete_bucket(Bucket=object_name)
        except:
            try:
                self.s3.Bucket(self.bucket_name).Object(object_name).delete()
            except:
                return False

        return True

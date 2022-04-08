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

        return result

    async def create_object(self, bucket_name=None, object_file_path=None):

        #TODO Q1 - Are you using the SDK ?
        #/TODO Q2 - Error management ?
        #/TODO Q3 - Refactor ?
        """
        Create a bucket or an object on s3
        """
        if bucket_name and not object_file_path:
            if await self.object_exists(bucket_name=bucket_name):
                return "Bucket already exists", 400
            else:
                if await self._create_bucket(bucket_name):
                    return "Bucket created", 200
                else:
                    return "Error while creating the bucket", 500

        if bucket_name and object_file_path:
            if await self.object_exists(bucket_name=bucket_name):
                result = await self._upload_file(bucket_name=bucket_name, file_path=object_file_path)
                
                if result:
                    return result, 200
                else:
                    return "Error while uploading the object", 500
            else:
                if await self._create_bucket(bucket_name):
                    result = await self._upload_file(bucket_name=bucket_name, file_path=object_file_path)
                    
                    if result:
                        return result, 200
                    else:
                        return "Error while uploading the object", 500
                else:
                    return "Error while creating the bucket and uploading the file", 500
        
        return "Error while creating the object", 500

    async def object_exists(self, bucket_name=None, object_name=None):
        """
        Check if the bucket or the object exists on s3
        """
        if bucket_name and not object_name:
            try:
                self.s3.head_bucket(Bucket=bucket_name)

                return True
            #TODO Q4 - Could be more specific ?
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

            return "Object downloaded", 200
        except:
            return "Error while downloading the object", 500

    async def remove_object(self, bucket_name=None, object_name=None):
        """
        Delete a bucket or an object on s3
        """
        s3_resource = boto3.resource('s3')

        if bucket_name and not object_name:
            try:
                s3_resource.Bucket(bucket_name).objects.all().delete()
                self.s3.delete_bucket(Bucket=bucket_name)

                return "Bucket deleted", 200
            except:
                return "Error while deleting the bucket", 500
        
        if bucket_name and object_name:
            try:
                s3_resource.Object(bucket_name, object_name).delete()

                return "Object deleted", 200
            except:
                return "Error while deleting the object", 500
        
        return "Error while deleting the object", 500

    async def _create_bucket(self, bucket_name):
        """
        Create a bucket on s3
        """
        try:
            self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                                        'LocationConstraint': self.s3_default_region})
            return True
        except:
            return False
    
    async def _upload_file(self, bucket_name, file_path):
        """
        Create an object on s3 using a multipart upload
        """
        try:
            file_name = os.path.basename(file_path)
            self.s3.upload_file(file_path, bucket_name, file_name)

            presigned_url = await self._get_presigned_url(bucket_name, file_name)
            
            return presigned_url
        except:
            return False

    async def _get_presigned_url(self, bucket_name, object_name):
        """
        Get a presigned url to access an object on s3
        """
        try:
            presigned_url = self.s3.generate_presigned_url('get_object', Params={
                'Bucket': bucket_name,
                'Key': object_name
            }, ExpiresIn=3600)

            return presigned_url
        except:
            return False
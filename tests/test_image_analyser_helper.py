from ast import dump
import json
from re import S
from flaskr.api.managers.rekognition_image_detection import face_from_local_file, face_from_url
from flaskr.api.managers.aws_bucket_manager import AwsBucketManager
import unittest
import os
import shutil


class ImageAnalyserHelperTestCase(unittest.IsolatedAsyncioTestCase):
    """
    This test class is designed to confirm the AwsImageAnalyserHelper class's behavior
    """

    def setUp(self):
        """
        This test method initializes the context before each test method run.
        """
        self.bucket_name = os.getenv('BUCKET_NAME')

        # Prepare picutre
        self.local_image_name = "test.jpg"
        self.image_copy_path = "./flaskr/images/" + self.local_image_name

        # os.remove(self.local_image_path)
        shutil.copyfile(self.local_image_name, self.image_copy_path)

        # Upload picture
        self.aws_bucket_manager = AwsBucketManager()

        self.image_url = "%s%s" % (
            os.getenv('BUCKET_URL'), self.local_image_name)
        self.image_url = "https://s3.eu-central-1.amazonaws.com/ria2.diduno.education/duck.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2KFJKL4O5BC6BG62%2F20220404%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20220404T075501Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c2d6027d8f9220aa63d87ad6a5c2f32833176da527cf0b43daca9a389cc17231"

        # Prepare expected json
        # Here instead of using an outdated json we get it fresh so we make sure there's no difference
        # Bonus : We don't need to manually update it
        self.expected_json = face_from_local_file(self.local_image_name)

        #self.json_name = "expected_test.json"
        #full_path_to_json = "./tests/" + self.json_name
        #file = open(full_path_to_json, "r")
        # file.close()

        # Query args
        self.max_labels = 10
        self.minConfidence = 80

    """    
    This test method checks the MakeAnalysis'answer
    when we try to analyze a local file
    """
    async def test_analyse_localfile_success(self):
        actual_json = face_from_local_file(self.local_image_name)

        self.assertEqual(self.expected_json, actual_json)

    """    
    This test method checks the MakeAnalysis'answer
    when we try to analyze a data object presents on a bucket
    """
    async def test_analyse_dataobject_succes(self):
        result = await self.aws_bucket_manager.create_object(self.bucket_name, self.image_copy_path)
        actual_json = face_from_url(result[0], False)

        self.assertEqual(self.expected_json, actual_json)

    """    
    This test method checks the MakeAnalysis'answer
    when we try to analyze a data object presents on a bucket
    """
    async def test_to_json_dataobject_succes(self):
        result = await self.aws_bucket_manager.create_object(self.bucket_name, self.image_copy_path)
        actual_json = face_from_url(result[0], False)

        self.assertEqual(self.expected_json, actual_json)


if __name__ == '__main__':
    unittest.main()

from flaskr.api.managers.rekognition_image_detection import face_from_local_file, face_from_url
from flaskr.api.managers.aws_bucket_manager import AwsBucketManager
from flaskr.api.helpers.aws_image_analyser_helper import AwsImageAnalyserHelper
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

        # Prepare helpers
        self.aws_bucket_manager = AwsBucketManager()
        self.image_analyser_helper = AwsImageAnalyserHelper()

        # Prepare expected json
        self.expected_json = face_from_local_file(self.local_image_name)

        # Query args
        self.max_labels = 10
        self.min_confidence = 80

    """    
    This test method checks the MakeAnalysis'answer
    when we try to analyze a local file
    """
    async def test_analyse_localfile_success(self):
        # Given
        picture = self.local_image_name

        # When
        actual_json = face_from_local_file(picture)

        # Then
        self.assertEqual(self.expected_json, actual_json)

    """    
    This test method checks the MakeAnalysis'answer
    when we try to analyze a data object presents on a bucket
    """
    async def test_analyse_dataobject_succes(self):
        # Given
        picture = self.image_copy_path

        # When
        actual_json = await self.image_analyser_helper.MakeAnalysisRequest(
            picture, self.max_labels, self.min_confidence)

            
        print("FUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCKFUCK")
        print(actual_json)

        # Then
        self.assertEqual(self.expected_json, actual_json)

    """    
    This test method checks the MakeAnalysis'answer
    when we try to analyze a data object presents on a bucket
    """
    async def test_to_json_dataobject_succes(self):
        # Given
        picture = self.image_copy_path

        # When
        actual_json = await self.image_analyser_helper.MakeAnalysisRequest(
            picture, self.max_labels, self.min_confidence)

        # Then
        self.assertEqual(self.expected_json, actual_json)


if __name__ == '__main__':
    unittest.main()

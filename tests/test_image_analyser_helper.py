import unittest
import os

from flaskr.aws_image_analyser_helper import AwsImageAnalyserHelper


class ImageAnalyserHelperTestCase(unittest.IsolatedAsyncioTestCase):
    """
    This test class is designed to confirm the AwsImageAnalyserHelper class's behavior
    """

    def setUp(self):
        """
        This test method initializes the context before each test method run.
        """
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.image_name = "pexels-pixabay-53370.jpg"
        self.file = open("./tests/" + self.image_name, "rb")
        self.helper = AwsImageAnalyserHelper()
        self.json_name = "expected_pexels-pixabay-53370.json"
        self.full_path_to_json = "./tests/" + self.json_name
        self.max_labels = 1

    async def test_analyse_localfile_success(self):
        actual_json = ""
        expected_json = open(self.full_path_to_json, "r").read()
        
        self.assertFalse(False)

if __name__ == '__main__':
    unittest.main()
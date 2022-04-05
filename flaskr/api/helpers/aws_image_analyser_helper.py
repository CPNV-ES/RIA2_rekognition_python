import os
from flaskr.api.interfaces.i_image_analyser_helper import IAwsImageAnalyserHelper
from flaskr.api.managers.aws_bucket_manager import AwsBucketManager
from flaskr.api.managers.rekognition_image_detection import face_from_url

class AwsImageAnalyserHelper(IAwsImageAnalyserHelper):

    def __init(self):
        self.aws_bucket_manager = AwsBucketManager()
        self.bucket_name = os.getenv('BUCKET_NAME')

    async def MakeAnalysisRequest(self, url: str, maxLables: int, minConfidence: int):
        result = await self.aws_bucket_manager.create_object(self.bucket_name, url)
        
        return face_from_url(result[0], False) # missing args to pass max labels and minConfidence

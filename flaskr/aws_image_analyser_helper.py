import string
from abc import ABC, abstractclassmethod

class IAwsImageAnalyserHelper(ABC):
    """ 
    This interface defines what parameters are required to analyse faces on a picture
    """
    @abstractclassmethod
    def MakeAnalysisRequest(url: string, maxLabels: int, minConfidence: int): 
        """
        Make a requests to Amazon's rekognition to analyse faces on a picture with specified parameters and return a json
        """
        raise NotImplementedError

class AwsImageAnalyserHelper(IAwsImageAnalyserHelper):
    def MakeAnalysisRequest(url: string, maxLables: int, minConfidence: int):
        return True
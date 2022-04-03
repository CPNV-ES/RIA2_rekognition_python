import string

class IAwsImageAnalyserHelper:
    """ 
    ImageAnalayserHelper
    """
    def MakeAnalysisRequest(url: string, maxLabels: int, minConfidence: int): raise NotImplementedError

class AwsImageAnalyserHelper(IAwsImageAnalyserHelper):

    def MakeAnalysisRequest(url: string, maxLabels: int, minConfidence: int):
        return "oui"

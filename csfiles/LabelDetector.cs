using System.IO;
using System.Threading.Tasks;
using NUnit.Framework;
using Ria2Model.LabelDetector;

namespace TestRia2Model.LabelDetector
{
    /// <summary>
    /// This test class is designed to confirm the ImageAnalyzerHelper class's behavior
    /// </summary>
    public class TestAwsLabelDectector
    {
        #region private attributs
        private IImageAnalyzerHelper imageAnalyzerHelper;
        private string pathToTestFolder;
        private string imageName;
        private string bucketUrl;
        private string jsonName;
        private string imageUri;
        private string fullPathToExpectedJson;
        private int maxLabels = 1;
        #endregion private attributs

        /// <summary>
        /// This test method initializes the context before each test method run.
        /// </summary>
        [SetUp]
        public void Init()
        {
            this.imageAnalyzerHelper = new AwsImageAnalyzerHelper();
            this.pathToTestFolder = Directory.GetCurrentDirectory().Replace("bin\\Debug\\netcoreapp3.1", "testData");
            this.imageName = "emiratesa380.jpg";
            this.jsonName = "expectedEmirates.json";
            this.bucketUrl = "aws.rekognition.actualit.info";
            this.fullPathToExpectedJson = pathToTestFolder + "\\" + jsonName;
            this.maxLabels = 1;
        }

        /// <summary>
        /// This test method checks the MakeAnalysis'answer
        /// when we try to analyze a local file
        /// </summary>
        [Test]
        public async Task MakeAnalysis_LocalFile_Success()
        {
            //given
            string actualJson;
            string expectedJson = File.ReadAllText(fullPathToExpectedJson);
            this.imageUri = this.pathToTestFolder + "//" + this.imageName;

            //when
            await labelDetector.MakeAnalysisRequest(this.imageUri);

            //then
            //compare expected json with result json
            actualJson = labelDetector.ToString();
            Assert.AreEqual(expectedJson, actualJson);
        }

        /// <summary>
        /// This test method checks the MakeAnalysis'answer
        /// when we try to analyze a data object presents on a bucket
        /// </summary>
        [Test]
        public async Task MakeAnalysis_DataObject_Success()
        {
            //given
            string actualJson;
            string expectedJson = File.ReadAllText(fullPathToExpectedJson); //expected result
            this.imageUri = this.bucketUrl + "//" + this.imageName;   

            //when
            await labelDetector.MakeAnalysisRequest(this.imageUri);

            //then
            //compare expected json with result json
            actualJson = labelDetector.ToString();
            Assert.AreEqual(expectedJson, actualJson);
        }

        /// <summary>
        /// This test method checks the MakeAnalysis'answer
        /// when we try to analyze a data object presents on a bucket
        /// </summary>
        [Test]
        public async Task ToJson_DataObject_Success()
        {
            //given
            string actualJson;
            string expectedJson = File.ReadAllText(fullPathToExpectedJson); //expected result
            this.imageUri = this.bucketUrl + "//" + this.imageName;

            //when
            await labelDetector.MakeAnalysisRequest(this.imageUri);

            //then
            //compare expected json with result json
            actualJson = labelDetector.ToString();
            Assert.AreEqual(expectedJson, actualJson);
        }

        /// <summary>
        /// This test method cleanups the context after each test method run.
        /// </summary>
        [TearDown]
        public void Cleanup()
        {
            //TODO clean bucket and delete it
            //For the moment, no action requiered
        }
    }
}
# RIA2_rekognition_python

## Get Started

### Setup environment variables

1. Copy paste the file `.env_example` and rename it to `.env`

2. Fill it with your settings

```js
BUCKET_NAME=bucket // Your aws bucket name
AWS_ACCESS_KEY_ID=aws_access_key_id // Your aws access key id
AWS_SECRET_ACCESS_KEY=aws_secret_access_key // Your aws secret access key
AWS_DEFAULT_REGION=eu-central-1 // Your aws default region
STORAGE_FOLDER=C:/ // Storage folder where images will be downloaded
```

### Create a virtual python environnment

#### On `Linux`

```sh
python3 -m venv venv

. venv/bin/activate

export FLASK_APP=flaskr.py

export FLASK_ENV=development
```

#### On `Windows`

```sh
python -m venv ./

.\Scripts\activate

$Env:FLASK_APP="flaskr.py"

$Env:FLASK_ENV="development"
```

#### Install the dependencies

```sh
pip install -r requirements.txt
```

### Run the app

```sh
flask run
```

#### Windows

```
.\winStart.ps1
```

### Testing

Examples

```
python -m unittest tests.test_bucket_manager
python -m unittest tests.test_bucket_manager.BucketManagerTestCase.test_create_object_with_object_not_existing_success
```

### Commands

#### Detect face

```
aws rekognition detect-faces ^ --image "{\"S3Object\":{\"Bucket\":\"ria2python.actualit.info\",\"Name\":\"cake.jpg\"}}"
```

##### Output

```
{                                                                                     
    "FaceDetails": [                                                                  
        {                                                                             
            "BoundingBox": {                                                          
                "Width": 0.5441199541091919,                                          
                "Height": 0.771619439125061,                                          
                "Left": 0.21737518906593323,                                          
                "Top": 0.15157969295978546                                            
            },                                                                        
            "Landmarks": [                                                            
                {                                                                     
                    "Type": "eyeLeft",                                                
                    "X": 0.37078168988227844,                                         
                    "Y": 0.46786952018737793                                          
                },                                                                    
                {                                                                     
                    "Type": "eyeRight",                                               
                    "X": 0.6176213026046753,                                          
                    "Y": 0.4703728258609772                                           
                },                                                                    
                {                                                                     
                    "Type": "mouthLeft",                                              
                    "X": 0.39093926548957825,                                         
                    "Y": 0.7299964427947998                                           
                },                                                                    
                {                                                                     
                    "Type": "mouthRight",                                             
                    "X": 0.596910834312439,                                           
                    "Y": 0.7318515777587891                                           
                },                                                                    
                {                                                                     
                    "Type": "nose",                                                   
                    "X": 0.5048046112060547,                                          
                    "Y": 0.619482159614563                                            
                }                                                                     
            ],                                                                        
            "Pose": {                                                                 
                "Roll": 0.588778555393219,                                            
                "Yaw": 1.9975968599319458,                                            
                "Pitch": -1.4224853515625                                             
            },                                                                        
            "Quality": {                                                              
                "Brightness": 56.78984451293945,                                      
                "Sharpness": 95.51618957519531                                        
            },                                                                        
            "Confidence": 99.9974136352539                                            
        }                                                                             
    ]                                                                                 
}                                                                                     
```

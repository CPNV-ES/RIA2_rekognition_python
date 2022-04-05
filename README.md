# RIA2_rekognition_python

## Endpoints

### Request Analysis
```
/api/request_analysis
```

Request an face rekognition of a file. 

Parameters [on post] :
| Name | Type | Description |
| -------- | -------- | -------- |
| Bucket*1     | String     | Bucket to use     |
| file*2     | File     | Image to rekognize     |
| arguments     | String     | Optional, Returns only the specify arguments. To write multiple arguments write them as : `arg1,arg2,arg3`. If you want to return every arguments, simply don't use this parameter. |

*1. Any doubt to the bucket parameter ? Execute the command bellow to show available buckets :
```
aws s3 ls
```

>*2. Example of arguments to use :
> `has` (Facial Characteristic), `age_range` (Age range of the person).

>Example :
>http://127.0.0.1:5000/api/ria2.test.education/request_analysis

Our application could also display the image with bouding box rendered around the detected faces. Add the parameter `/display_image`.  

>Example :
>http://127.0.0.1:5000/api/ria2.test.education/request_analysis/display_image

## Get Started

### Setup environment variables

1. Copy paste the file `.env_example` and rename it to `.env`

2. Fill it with your settings

```js
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

#### Database

##### Examples of MySQL queries

##### Last 10 days processed images
```sql
SELECT image.name, image.hash, analysis.created_at 
FROM image 
INNER JOIN analysis 
ON image.id = analysis.image_id 
WHERE analysis.created_at >= NOW() - INTERVAL 10 DAY
```

##### Image with a specific specified attribute has been found
```sql
SELECT image.id, image.name, attribute.name, attribute.value_number
FROM image 
INNER JOIN analysis 
ON analysis.image_id = image.id
INNER JOIN object
ON object.analysis_id = analysis.id
INNER JOIN attribute
ON attribute.object_id = object.id
WHERE attribute.name LIKE "<custom_attribute_here>.%" AND attribute.name LIKE "%.Confidence"
```

##### Average analysis by user (ip)
```sql
SELECT a.ip as ip, (AVG((
SELECT COUNT(*) FROM attribute 
INNER JOIN object 
ON attribute.object_id = object.id 
INNER JOIN analysis 
ON object.analysis_id = analysis.id 
WHERE analysis.ip = a.ip)) ) as average
FROM analysis AS a
GROUP BY ip
```

##### Number of time an image has been process group by user (ip)
```sql
SELECT image.hash, analysis.ip, COUNT(analysis.ip) as request
FROM image 
INNER JOIN analysis 
ON image.id = analysis.image_id 
WHERE analysis.updated_at >= NOW() - INTERVAL 24 HOUR
GROUP BY image.hash, analysis.ip
```

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

# RIA2_rekognition_python

## Get Started

First install the dependencies

```sh
pip install -r requirements.txt
```

## Create a virtual python environnment

### On `Linux`

```sh
python3 -m venv venv

. venv/bin/activate

export FLASK_APP=flaskr.py
export FLASK_ENV=development
python -m flask run
```

### On `Windows`

```sh
$Env:FLASK_APP="flaskr.py"
$Env:FLASK_ENV="development"
```

### Run

```sh
cd .\flaskr\

flask run
```

## Set environment variables

```sh
cp .env.exemple .env
```

Edit the file with your environment variables

## Testing

```
python -m unittest tests.test_bucket_manager
python -m unittest tests.test_bucket_manager.BucketManagerTestCase.test_create_object_with_object_not_existing_success
```

### Database

#### Examples of MySQL queries

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
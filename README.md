# RIA2_rekognition_python

## Get Started 

First install the dependencies
```sh
pip install -r requirements.txt
```

## Create a virtual python environnment

### On ``Linux``

```sh
python3 -m venv venv

. venv/bin/activate

export FLASK_APP=flaskr.py
export FLASK_ENV=development
python -m flask run
```

### On ``Windows``

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

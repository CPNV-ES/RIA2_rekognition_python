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

export FLASK_APP=__init__.py
```

### On ``Windows`` with ``Powershell``

```powershell
py -3 -m venv venv

venv\Scripts\activate

$Env:FLASK_APP="__init__.py"
```

## Run

```sh
cd .\flaskr\

flask run
```

# RIA2_rekognition_python

## Get Started 

First install the dependancies
```sh
pip install -r requirements.txt
```

### On ``Linux``

To create a virtual python environnment :

```sh
python3 -m venv venv

. venv/bin/activate

export FLASK_APP=app.py
export FLASK_ENV=development
python -m flask run
```

## On ``Windows`` with ``Powershell``

```powershell
python -m venv venv

. .\venv\Scripts\Activate.ps1

$Env:FLASK_APP="app.py"
$Env:FLASK_ENV="development"
python -m flask run
```

Alternatively you can also do this on Windows if the solution above didn't worked
```powershell
python -m venv venv

.\venv\Scripts\activate

$set FLASK_APP=app.py
$set FLASK_ENV=development
python -m flask run
```

### Run

```sh
flask run --host=0.0.0.0
```

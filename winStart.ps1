python -m venv venv

. .\venv\Scripts\Activate.ps1

$Env:FLASK_APP="flaskr.py"
$Env:FLASK_ENV="development"
python -m flask run
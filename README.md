# Final Year Project API
## Setup
Make sure python 3.6 and virtualenv are installed and that the URL pointing to the common repository is replaced by your own URL.

Run the following:
```sh
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Files Required
Please add all these files to your folder with the missing parts filled in.
### run.sh
```sh
# Environment
source ./venv/bin/activate
export PYTHON_ENV="DEVELOPMENT" # DEVELOPMENT / PRODUCTION
export FLASK_ENV="development"

# Flask
export FLASK_APP="server.py"
export FLASK_RUN_PORT=5000

# Celery
export BROKER_URL="amqp://guest:guest@localhost:5672"

# JWT
export JWT_SECRET_KEY="" # Insert your secret key here

# Mongo, these variables are picked up by the common library
export MONGO_URL='mongodb://localhost:27017'
export MONGO_DATABASE_NAME='default_db'

# Run server
flask run
```

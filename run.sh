# Environment
./venv/Scripts/activate
export PYTHON_ENV="DEVELOPMENT" # DEVELOPMENT / PRODUCTION
export FLASK_ENV="development"

# Flask
export FLASK_APP="server.py"
export FLASK_RUN_PORT=5000

# Celery
export BROKER_URL="amqp://guest:guest@localhost:5672"

# JWT
export JWT_SECRET_KEY="2jWcgoFw8SRVi0rJ10ns5vcWVi5tKHe3L+NoFutg2SrdHFjpV4lUskvQq84u8Y0lL8KB6z/l++h0Tq6f+Qd7hG7bqI/VWCOOMaotuwzGJ9iB9C3hp1opeywKwSDcMdDxtxMyUBLIqJE8IX8pqKjoz+yQAM9Y3kRKqd5ZQh1n5WztM4Zw4njeSC3T6vtLK7ct2Br19SiUAngPWbzLPrmjj8475lGgUPXsE/MQ+LTAOKR1XHnHnijFOR1NluLhWv20Ao9X7s/38GzrVA0dpJD0YLRpvC0qjcLZC/ArogDQ+nINDSE1IZ3pxVpUA8B0/IJX2txgsj1QETNOQnlb2kHQSw=="

# Mongo, these variables are picked up by the common library
export MONGO_URL='mongodb://localhost:27017'
export MONGO_DATABASE_NAME='default_db'

# Run server
flask run
# challenge-real-estate-api

## Run Locally

### starting the service
After running
```
cp .env.example .env
docker-compose up --build
```

there should be
* a FastaApi serivice on port 8000
* a postgres database (migrations applied)
* a RabbitMQ service
* a consumer for RabbitMq
the docs for the api swagger specs should be available at http://localhost:8000/docs.

### import data
By adjusting the values in the `.env` file one can connect to an external queue.
There is also a script to generate data that is designed such that the `building_id` from the rooms are also appearing in the Building events.
```
make import-data
```

### backend linting and tests
Run linting and testing frameworks via
```
make lint-docker
make test-docker
```

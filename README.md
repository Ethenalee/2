### Installation and running

**Note:**
The first time you will be running the `nfl-rushing-backend-service`, it will fail to start
because the database doesn't exist yet.

Even if there's a script to create the database, it would need to be created manually,
because the container has to be up to run that script, but the container crashes since it fails to run the migration...

To manually create the DB:
- Go to nfl-rushing-backend `cd nfl-rushing-backend`
- Build containers `docker-compose build`
- Run postgres `docker-compose up postgres`
- Run psql inside of docker container `docker exec -it nfl-rushing-backend_postgres_1 psql -U postgres`
- Create DB: `CREATE DATABASE rushing_dev;`

Backend service Json file ready
- Any new json file added in data/seeds folder run `jq -c '.[]' <file>.json > <new-file>.json`
Make sure to replace with `<new-file>.json` so its ready for seed sql


Set up
1. Run frontend
- Go to nfl-rushing-frontend `cd nfl-rushing-frontend`
- Build containers `docker-compose build`
- Run postgres `docker-compose up`

2. Run backend
- Create a `.env` file and copy the contents from `.env.example` over:
    1. In the service directory:
        `cp .env.example .env`
    2. to run server
        APP_ENV=local
        APP_COMPONENT=server
    3. to run tests
        APP_ENV=test
        APP_COMPONENT=tests
- Go to nfl-rushing-backend `cd nfl-rushing-backend`
- Build containers `docker-compose build`
- Run postgres `docker-compose up postgres`
- Once postgres is ready `docker-compose up nfl-rushing-backend-service`

### Documentaion
1. Backend service Swagger Doc
    1. once service is up and running you can check api http://localhost:5000/docs
2. Backend service Postman
    1. Install/open Postman and import the file in this repo's `postman` directory

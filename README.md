### Installation and running

**Note:**
The first time you will be running the `nfl-rushing-backend-servic`, it will fail to start
because the database doesn't exist yet.

Even if there's a script to create the database, it would need to be created manually,
because the container has to be up to run that script, but the container crashes since it fails to run the migration...

To manually create the DB:
- Go to nfl-rushing-backend `cd nfl-rushing-backend`
- Build containers `docker-compose build`
- Run postgres `docker-compose up postgres`
- Run psql inside of docker container `docker exec -it nfl-rushing-backend_postgres_1 psql -U postgres`
- Create DB: `CREATE DATABASE rushing_dev;`

Json file ready
- Any new json file added in data/seeds folder run `jq -c '.[]' <file>.json > <new-file>.json`
Make sure to replace with `<new-file>.json` so its ready for seed sql


1. Run frontend
- Go to nfl-rushing-frontend `cd nfl-rushing-frontend`
- Build containers `docker-compose build`
- Run postgres `docker-compose up`

2. Run backend
- Go to nfl-rushing-backend `cd nfl-rushing-backend`
- Build containers `docker-compose build`
- Run postgres `docker-compose up postgres`
- Once postgres is ready `docker-compose up nfl-rushing-backend-service`

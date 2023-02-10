#!/bin/sh

# shellcheck disable=SC2112
function build()
{
        docker-compose build
}

function run()
{
        docker-compose up --build
}

function up()
{
        docker-compose up --build
}


function stop()
{
        docker-compose down
}

function makemigrations()
{
        docker-compose run --rm server /bin/sh -c "alembic revision --autogenerate -m $message"
}

function migrate()
{
        docker-compose run --rm server /bin/sh -c 'cd backend && alembic upgrade head'
}

function clean_cache() {
        find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
}


function run_test_db()
{
        docker run --name postgres \
          -e POSTGRES_USER=postgres \
          -e POSTGRES_PASSWORD=postgres_password \
          -e POSTGRES_PORT=5432 \
          -d -p 5432:5432 postgres

        # docker-compose -f test-docker-service.yml build
        # docker-compose -f test-docker-service.yml up -d postgres_test
        # docker-compose -f test-docker-service.yml run --rm server_test /bin/sh -c 'cd backend && alembic upgrade head && rm -rf .pytest_cache && pytest tests'
        # docker rm $(docker stop $(docker ps -qa --filter "name=postgres_test" --filter "name=server_test")) || echo Not Found Test containers
        # rm -rf ./test_db_data
}

function test()
{
    
    python -m pytest tests
}

function lint()
{
        docker-compose run --rm server /bin/sh -c 'black backend --exclude=migrations,db_data && flake8 backend --config ./backend/setup.cfg'
}

function isorted() {
        docker-compose run --rm server /bin/sh -c "isort --reverse-sort  --lines-between-types 1 backend --src .setup.cfg"
}


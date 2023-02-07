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
        docker-compose run --rm server /bin/sh -c 'alembic upgrade head'
}

function clean_cache() {
    find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
}

function lint()
{
        docker-compose run --rm server /bin/sh -c 'black backend --exclude=migrations,db_data && flake8 backend --config ./backend/setup.cfg'
}

function isorted() {
        docker-compose run --rm server /bin/sh -c "isort --reverse-sort  --lines-between-types 1 backend --src .setup.cfg"
}

function make_db_diagram()
{
        docker-compose run --rm server /bin/sh -c 'alembic upgrade head'
}

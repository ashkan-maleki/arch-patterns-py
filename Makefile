# source venv/bin/activate
# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: pull down build up test

build:
	sudo docker-compose build

up:
	sudo docker-compose up -d app

down:
	sudo docker-compose down

logs:
	sudo docker-compose logs app | tail -100

test:
	pytest --tb=short

black:
	black -l 86 $$(find * -name '*.py')

pull:
	sudo git pull
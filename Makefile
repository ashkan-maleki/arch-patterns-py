# sudo rm -rf arch-patterns-py/
# sudo chmod -R 777 arch-patterns-py/
# sudo chmod -R 777 .git
# python3 -m venv venv
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
	git pull origin main --force

require:
	pip install -r requirements.txt
	pip install -e src
	pip install allocation --no-index --find-links src

access:
	sudo chmod -R 777 arch-patterns-py/
	sudo chmod -R 777 .git
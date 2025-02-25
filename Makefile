# Makefile Documentation
# This Makefile provides a simple interface for managing the project using Docker.

.PHONY: all up updev downdev help


# target: all - Executes the run
all: up


# target: run - Builds and starts the Docker container
# Description: This target builds and starts the Docker container using the
# docker-compose command. The -d flag runs the containers in detached mode,
# allowing them to run in the background.
up:
	docker-compose -f compose.yaml up --build -d

# target: rundev
updev:
	docker-compose -f docker-compose-dev.yaml up --build -d


downdev:
	docker stop factorydash.dev
	docker rm factorydash.dev
	docker stop factorydash.celery_worker
	docker rm factorydash.celery_worker
	docker stop factorydash.celery_beat
	docker rm factorydash.celery_beat


# target: help - Displays the available executable targets
# Description: This target displays a list of executable targets defined in
# the Makefile. It uses egrep to search for lines that start with # target:,
# providing a quick reference for users.
help:
	@egrep "^# target:" [Mm]akefile

# EOF

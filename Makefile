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
	docker rm -f factorydash.dev || true
	docker rm -f factorydash.celery_worker || true
	docker rm -f factorydash.celery_beat || true
	docker rm -f factorydash.redis || true
	docker rm -f factorydash.db || true

downci:
	docker rm -f factorydash_container || true
	docker rm -f act-CI-CD-Pipeline-build-c6acc847991b86805ff6747e2b9238b1d9a97e-63ceb2838de5c49907a7832497a5db298423481b480ab74924db8238358e1ef7 || true
	docker rm -f act-CI-CD-Pipeline-build-c6acc847991b86805ff6747e2b9238b1d9a97e-b3da62385a9ffa4fbc37a8c89c6048d2bbf805a8f711d0937c9bdf84cd918a45 || true
	docker rm -f act-CI-CD-Pipeline-build-c6acc847991b86805ff6747e2b9238b1d9a97ef200e170b447ad993dc518506a || true


# target: help - Displays the available executable targets
# Description: This target displays a list of executable targets defined in
# the Makefile. It uses egrep to search for lines that start with # target:,
# providing a quick reference for users.
help:
	@egrep "^# target:" [Mm]akefile

# EOF

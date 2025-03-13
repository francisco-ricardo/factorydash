# Makefile Documentation
# This Makefile provides a simple interface for managing the project using Docker.

.PHONY: uptest downtest updev downdev help


# target: run - Builds and starts the Docker container locally for testing
# Description: 
uptest:
	docker-compose -f docker-compose.yaml up --build -d


downtest:
	docker rm -f factorydash || true
	docker rm -f factorydash.postgres || true
	docker rm -f factorydash.redis || true


# target: rundev
updev:
	docker-compose -f docker-compose-dev.yaml up --build -d


downdev:
	docker rm -f factorydash.dev || true
	docker rm -f factorydash.celery_worker || true
	docker rm -f factorydash.celery_beat || true
	docker rm -f factorydash.redis || true
	docker rm -f factorydash.db || true


# target: help - Displays the available executable targets
# Description: This target displays a list of executable targets defined in
# the Makefile. It uses egrep to search for lines that start with # target:,
# providing a quick reference for users.
help:
	@egrep "^# target:" [Mm]akefile

# EOF

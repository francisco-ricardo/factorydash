# Makefile Documentation
# This Makefile provides a simple interface for managing the project using Docker.

.PHONY: updev downdev rundev stopdev help


# target: updev
updev:
	docker-compose -f docker-compose-dev.yaml up --build -d


downdev:
	docker rm -f factorydash.dev || true
	docker rm -f factorydash.celery_worker.dev || true
	docker rm -f factorydash.celery_beat.dev || true
	docker rm -f factorydash.redis.dev || true
	docker rm -f factorydash.postgres.dev || true


# target: rundev
rundev:
	docker exec factorydash.dev supervisord -c /factorydash/.devcontainer/supervisord.dev.conf

stopdev:
	docker exec factorydash.dev pkill supervisord


# target: help - Displays the available executable targets
# Description: This target displays a list of executable targets defined in
# the Makefile. It uses egrep to search for lines that start with # target:,
# providing a quick reference for users.
help:
	@egrep "^# target:" [Mm]akefile

# EOF

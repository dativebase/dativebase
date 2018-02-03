
# Paths for Docker named volumes
OLD_STORE ?= /tmp/dativebase-old-store


create-volumes:  ## Create external data volumes.
	mkdir -p ${OLD_STORE}
	docker volume create \
		--opt type=none \
		--opt o=bind \
		--opt device=$(OLD_STORE) \
			dativebase-old-store

bootstrap: bootstrap-old  ## Full bootstrap.

bootstrap-old:  ## Boostrap OLD (new database).
	docker-compose exec mysql mysql -hlocalhost -uroot -p12345 -e "\
		DROP DATABASE IF EXISTS old; \
		CREATE DATABASE old DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin; \
		GRANT ALL ON old.* TO 'old'@'%' IDENTIFIED BY 'demo';"
	docker-compose run \
		--rm \
		--entrypoint /venv/bin/initialize_old \
			old \
				/usr/src/old/config.ini old

bootstrap-old-tests:  ## Boostrap OLD for tests (new database for tests).
	docker-compose exec mysql mysql -hlocalhost -uroot -p12345 -e "\
		DROP DATABASE IF EXISTS oldtests; \
		CREATE DATABASE oldtests DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin; \
		GRANT ALL ON oldtests.* TO 'old'@'%' IDENTIFIED BY 'demo';"

restart-dativebase-services:  ## Restart DativeBase services: OLD.
	docker-compose restart mysql
	docker-compose restart nginx
	docker-compose restart old

db:  ## Connect to the MySQL server using the CLI.
	mysql -h127.0.0.1 --port=61001 -uroot -p12345

flush: flush-shared-dir bootstrap restart-dativebase-services  ## Delete ALL user data.

flush-shared-dir:  ## Delete contents of the shared directory data volume.
	rm -rf ${OLD_STORE}/*

test-all: test-old  ## Run all tests.

test-old: bootstrap-old-tests  ## Run OLD tests.
	/usr/src/old/test.sh

help:  ## Print this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help


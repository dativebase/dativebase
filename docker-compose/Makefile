
# Paths for Docker named volumes
OLD_STORE ?= /tmp/dativebase-old-store


create-volumes:  ## Create external data volumes.
	mkdir -p ${OLD_STORE}
	docker volume create \
		--opt type=none \
		--opt o=bind \
		--opt device=$(OLD_STORE) \
			dativebase-old-store

create-old-instance:
	docker-compose exec mysql mysql -hlocalhost -uroot -p12345 -e "\
		DROP DATABASE IF EXISTS $(OLD_NAME); \
		CREATE DATABASE $(OLD_NAME) DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin; \
		GRANT ALL ON $(OLD_NAME).* TO 'old'@'%' IDENTIFIED BY 'demo';"
	docker-compose run \
		--rm \
		--entrypoint /venv/bin/initialize_old \
			old \
				/usr/src/old/config.ini $(OLD_NAME)

# make load-old-instance-dump OLD_NAME=blaold DUMP_PATH=/Users/joeldunham/LambdaBar/Contracts/DAILP-2018/blaold-db-dump-2018-08-22.sql
# # Restore
# cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE
load-old-instance-dump:
	docker-compose exec mysql mysql -hlocalhost -uroot -p12345 -e "\
		DROP DATABASE IF EXISTS $(OLD_NAME); \
		CREATE DATABASE $(OLD_NAME) DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin;"

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

bootstrap-old-tests:  ## Boostrap OLD for tests (new databases for tests).
	docker-compose exec mysql mysql -hlocalhost -uroot -p12345 -e "\
		DROP DATABASE IF EXISTS oldtests; \
		CREATE DATABASE oldtests DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin; \
		GRANT ALL ON oldtests.* TO 'old'@'%' IDENTIFIED BY 'demo';"
	docker-compose exec mysql mysql -hlocalhost -uroot -p12345 -e "\
		DROP DATABASE IF EXISTS oldtests2; \
		CREATE DATABASE oldtests2 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin; \
		GRANT ALL ON oldtests2.* TO 'old'@'%' IDENTIFIED BY 'demo';"

restart-dativebase-services:  ## Restart DativeBase services: OLD.
	docker-compose restart mysql
	docker-compose restart nginx
	docker-compose restart old

db:  ## Connect to the MySQL server using the CLI.
	mysql -h127.0.0.1 --port=61002 -uroot -p12345

flush: flush-shared-dir bootstrap restart-dativebase-services  ## Delete ALL user data.

flush-shared-dir:  ## Delete contents of the shared directory data volume.
	rm -rf ${OLD_STORE}/*

test-all: test-old  ## Run all tests.

test-old: bootstrap-old-tests  ## Run OLD tests.
	docker-compose exec old env OLD_NAME_TESTS=oldtests \
		OLD_NAME_2_TESTS=oldtests2 \
		OLD_PERMANENT_STORE=/var/old/store \
		OLD_TESTING=1 \
		/venv/bin/pytest /usr/src/old/old/tests/ -v

help:  ## Print this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help


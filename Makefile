build:
	docker-compose up --build

up:
	docker-compose up

down:
	docker-compose down

destroy:
	docker-compose down -v --remove-orphans

logs:
	docker-compose logs -f

logs-nginx:
	docker-compose logs -f nginx

shell:
	docker-compose exec web bash

createsuperuser:
	docker-compose exec web python manage.py createsuperuser


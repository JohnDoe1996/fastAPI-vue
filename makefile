
build_backend:
	docker build -f ./Dockerfile.backend . -t fastapi_vue/backend:latest

build_frontend:
	docker build -f ./Dockerfile.frontend . -t fastapi_vue/frontend:latest

up:
	docker-compose up -d

up_local:
	docker-compose up -env ./.env.local -d

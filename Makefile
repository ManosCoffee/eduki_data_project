# Load environment variables from .envrc file
load-env-from-envrc:
	export $(shell sed 's/export //g' .envrc | xargs)

# Docker build command
build:
	docker build  -t eduki_image:latest .

# Docker run command
run:
	direnv allow .
	docker run --rm -it \
	-e POSTGRES_DB=${POSTGRES_DB} \
	-e POSTGRES_USER=${POSTGRES_USER} \
	-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
	-e POSTGRES_HOST=${POSTGRES_HOST} \
	-e POSTGRES_PORT=${POSTGRES_PORT} \
	-e BQ_PROJECT_ID=${BQ_PROJECT_ID} \
	-e GCP_PROJECT_ID=${GCP_PROJECT_ID} \
	-e GCP_PRIVATE_KEY="$$(cat .private_key.pem)" \
	-e GCP_PRIVATE_KEY_ID=${GCP_PRIVATE_KEY_ID} \
	-e GCP_CLIENT_EMAIL=${GCP_CLIENT_EMAIL} \
	-e GCP_CLIENT_ID=${GCP_CLIENT_ID} \
	-e GCP_CLIENT_CERT_URL=${GCP_CLIENT_CERT_URL} \
	eduki_image poetry run python -m eduki_data_engineering."$(MODULE_NAME)"

up:
	docker-compose up -d


# Help target to display usage information
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo "  build         Build the Docker image"
	@echo "  run           Run the Docker container"
	@echo "  clean         Remove Docker image and container"
	@echo "  help          Display this help message"

# Phony targets
.PHONY: load-env-from-envrc build run help

DOCKER_COMPOSE=docker-compose
COMPOSE_UP=$(DOCKER_COMPOSE) up
COMPOSE_DOWN=$(DOCKER_COMPOSE) down
IMAGES=ochrona-danych-aplikacja-safe-app
start:
	$(COMPOSE_UP)  
stop:
	$(COMPOSE_DOWN)
clean:
	docker image rm $(IMAGES)
# Tasks_TG_bot


# docker compose -f docker/docker-compose.yml up -d --build
docker compose -f docker/docker-compose.yml --env-file .env up -d --build

# docker-compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml --env-file .env down -v && docker system prune -f

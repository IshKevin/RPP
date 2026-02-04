.PHONY: up down logs verify

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

verify:
	bash scripts/verify.sh

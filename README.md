# Graph Reader API with Community Support

This project wraps the graph_reader library with a FastAPI service, adding community retrieval functionality.

## Features

- Retrieve entity by ID
- Retrieve neighbors of an entity
- Search entities by properties
- Retrieve community an entity belongs to
- List all members of a community

## Quick Start (Docker Compose)

```bash
docker-compose up --build
```

Access the API at: http://localhost:8000

## Endpoints

- `GET /entity/{entity_id}`
- `GET /entity/{entity_id}/neighbors`
- `GET /entity/{entity_id}/community`
- `GET /community/{community_id}/members`
- `GET /search?key=name&value=Alice`
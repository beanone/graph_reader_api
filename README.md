<p align="center">
  <img src="https://raw.githubusercontent.com/beanone/graph_reader_api/refs/heads/main/docs/assets/logos/banner.svg" alt="Graph Context Banner" width="100%">
</p>

This project wraps the graph_reader_api library with a FastAPI service, adding community retrieval functionality.

This library enables fast graph traversal and lookup from file-based storage with sharded and indexed structure.
Now includes community exploration.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/beanone/graph_reader_api/blob/main/LICENSE)
[![Tests](https://github.com/beanone/graph_reader_api/actions/workflows/tests.yml/badge.svg)](https://github.com/beanone/graph_reader_api/actions?query=workflow%3Atests)
[![Coverage](https://codecov.io/gh/beanone/graph_reader_api/branch/main/graph/badge.svg)](https://codecov.io/gh/beanone/graph_reader_api)
[![Code Quality](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)


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

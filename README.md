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
[![Security Scan](https://github.com/beanone/graph_reader_api/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/beanone/graph_reader_api/actions/workflows/docker-publish.yml)


## Features

- Retrieve entity by ID
- Retrieve neighbors of an entity
- Search entities by properties
- Retrieve community an entity belongs to
- List all members of a community
- MCP (Model Context Protocol) support for AI integration

## Quick Start (Docker Compose)

First, ensure you have graph data in the `graph_output` directory. The Docker setup expects this directory structure:

```
graph_output/
├── adjacency/
│   └── adjacency.jsonl
├── entities/
│   └── shard_0.jsonl
├── logs/
│   ├── entity_updates.jsonl
│   └── relation_updates.jsonl
├── relations/
│   └── shard_0.jsonl
└── index.db
```

You can generate test data using the fixture generator:

```python
# Generate test data in the graph_output directory
from tests.fixture_generator import create_test_graph_fixture
create_test_graph_fixture("graph_output")
```

Then start the service:

```bash
docker-compose up --build
```

Access the API at: http://localhost:8000

## Endpoints

- `GET /entity/{entity_id}`
- `GET /entity/{entity_id}/neighbors`
- `GET /entity/{entity_id}/community`
- `GET /entity/users/me`[^users-me-note]
- `GET /community/{community_id}/members`
- `GET /search?key=name&value=Alice`

[^users-me-note]: Returns the authenticated user's identity and claims as extracted from the JWT. This endpoint is intended to provide user context for graph-related operations. It does not provide user profile management, but only exposes the current user's identity as it relates to the graph domain.

## Testing with Postman

A Postman collection is provided to help you test the API endpoints. To use it:

1. Install [Postman](https://www.postman.com/downloads/)

2. Import the collection:
   - Open Postman
   - Click "Import" button
   - Select the collection file: `tests/postman/graph_reader_api.postman_collection.json`

3. The collection includes requests for all available endpoints:
   - Entity operations
   - Community operations
   - Search operations

4. Make sure the API is running locally before testing:
   ```bash
   docker-compose up --build
   ```

5. Use the collection to test endpoints:
   - All requests are pre-configured to use `http://localhost:8000` as the base URL
   - Example data is included in the requests
   - Variables and test scripts are included to validate responses

## Testing MCP Integration

To verify that the MCP server is working correctly, you can use the MCP Inspector tool:

1. Start the API server:
   ```bash
   docker-compose up --build
   ```

2. Install and run the MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector node build/index.js
   ```

3. In the MCP Inspector:
   - Pick the Transport Type "SSE"
   - Connect to the MCP server at `http://localhost:8000/mcp`
   - Navigate to the `Tools` section
   - Click `List Tools` to see all available endpoints
   - Test an endpoint by:
     - Selecting a tool from the list
     - Filling in any required parameters
     - Clicking `Run Tool` to execute

4. Check the server logs for any debugging information if needed

This will help confirm that your MCP server is properly configured and all endpoints are accessible as MCP tools.

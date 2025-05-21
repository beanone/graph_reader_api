#!/usr/bin/env python3
"""Test authentication with both JWT and API key against running service."""

import asyncio
import json
import sys
from datetime import UTC, datetime, timedelta

import httpx

# Configuration
API_URL = "http://localhost:8000"
LOGIN_URL = "http://localhost:8001"
TIMEOUT = 30.0  # seconds


def log_step(message):
    """Log a step with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {message}")


async def get_jwt_token():
    """Get JWT token from login service."""
    log_step("Starting JWT token request...")
    try:
        log_step(f"Connecting to login service at {LOGIN_URL}")
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            log_step("Sending login request...")
            response = await client.post(
                f"{LOGIN_URL}/auth/jwt/login",
                data={
                    "username": "testuser@example.com",
                    "password": "testpassword123",
                },
            )
            log_step(f"Login response received: {response.status_code}")
            if response.status_code != 200:
                print(f"Failed to get JWT: {response.text}")
                sys.exit(1)
            return response.json()["access_token"]
    except httpx.ConnectError:
        print(f"Failed to connect to login service at {LOGIN_URL}")
        print("Please ensure the login service is running and accessible")
        sys.exit(1)
    except httpx.ReadTimeout:
        print(f"Timeout while connecting to login service at {LOGIN_URL}")
        print("The service might be overloaded or not responding")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while getting JWT: {e!s}")
        sys.exit(1)


async def get_api_key(jwt_token):
    """Get API key using JWT token."""
    log_step("Starting API key request...")
    try:
        # Set expires_at to 1 year from now
        expires_at = (datetime.now(UTC) + timedelta(days=365)).isoformat()
        log_step(f"Expiration set to: {expires_at}")

        log_step(f"Connecting to API service at {API_URL}")
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            log_step("Sending API key creation request...")
            response = await client.post(
                f"{API_URL}/api-keys/",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "service_id": "graph-reader",
                    "name": "Test API Key",
                    "expires_at": expires_at,
                },
            )
            log_step(f"API key response received: {response.status_code}")
            if response.status_code not in (200, 201):
                print(f"Failed to get API key: {response.text}")
                sys.exit(1)
            return response.json()["plaintext_key"]
    except httpx.ConnectError:
        print(f"Failed to connect to API service at {API_URL}")
        print("Please ensure the API service is running and accessible")
        sys.exit(1)
    except httpx.ReadTimeout:
        print(f"Timeout while connecting to API service at {API_URL}")
        print("The service might be overloaded or not responding")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while getting API key: {e!s}")
        sys.exit(1)


async def test_entity_jwt(jwt_token):
    """Test entity endpoint with JWT."""
    log_step("\nTesting entity endpoint with JWT...")
    try:
        log_step(f"Connecting to API service at {API_URL}")
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            log_step("Sending entity request with JWT...")
            try:
                response = await client.get(
                    f"{API_URL}/entity/1",
                    headers={"Authorization": f"Bearer {jwt_token}"},
                )
                log_step(f"Entity response received: {response.status_code}")
                if response.status_code == 200:
                    print("JWT authentication successful!")
                    data = response.json()
                    print(f"Entity data: {json.dumps(data, indent=2)}")
                else:
                    print("JWT authentication failed!")
                    print("Error:", response.text)
            except httpx.TimeoutException:
                print("Request timed out")
                print("This might indicate that the service is not responding")
                print("Please check if the service is running and accessible")
            except httpx.RequestError as e:
                print(f"Request failed: {e!s}")
    except Exception as e:
        print(f"Unexpected error while testing entity with JWT: {e!s}")


async def test_entity_api_key(api_key):
    """Test entity endpoint with API key."""
    log_step("\nTesting entity endpoint with API key...")
    try:
        log_step(f"Connecting to API service at {API_URL}")
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            log_step("Sending entity request with API key...")
            try:
                response = await client.get(
                    f"{API_URL}/entity/1", headers={"X-API-Key": api_key}
                )
                log_step(f"Entity response received: {response.status_code}")
                if response.status_code == 200:
                    print("API key authentication successful!")
                    data = response.json()
                    print(f"Entity data: {json.dumps(data, indent=2)}")
                else:
                    print("API key authentication failed!")
                    print("Error:", response.text)
            except httpx.TimeoutException:
                print("Request timed out")
                print("This might indicate that the service is not responding")
                print("Please check if the service is running and accessible")
            except httpx.RequestError as e:
                print(f"Request failed: {e!s}")
    except Exception as e:
        print(f"Unexpected error while testing entity with API key: {e!s}")


async def main():
    """Run all tests."""
    log_step("Starting authentication tests...")
    log_step(f"API URL: {API_URL}")
    log_step(f"Login URL: {LOGIN_URL}")
    log_step(f"Timeout: {TIMEOUT} seconds")

    # Get JWT token
    log_step("\nGetting JWT token...")
    jwt_token = await get_jwt_token()
    log_step("JWT token obtained successfully")

    # Get API key
    log_step("\nGetting API key...")
    api_key = await get_api_key(jwt_token)
    log_step("API key obtained successfully")

    # Test entity endpoint with JWT
    await test_entity_jwt(jwt_token)

    # Test entity endpoint with API key
    await test_entity_api_key(api_key)


if __name__ == "__main__":
    asyncio.run(main())

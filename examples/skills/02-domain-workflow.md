---
name: api-integration-workflow
description: |
  Systematic workflow for integrating third-party APIs into applications. Use
  when: (1) Connecting to a new REST or GraphQL API, (2) Handling authentication
  including OAuth 2.0, API keys, Bearer tokens, and Basic HTTP authentication,
  (3) Implementing rate limiting, retry logic, and circuit breaker patterns,
  (4) Debugging API connection issues such as timeouts, authentication failures,
  and unexpected response formats, (5) Designing API client libraries or wrapper
  modules. Covers authentication patterns, error handling strategies, pagination
  approaches, request/response validation, and testing API integrations.
author: Community
version: 1.0.0
date: 2026-01-15
tags: [api, integration, rest, graphql, authentication, error-handling]
---

# API Integration Workflow

## Problem

Integrating with third-party APIs involves multiple challenges: choosing the
right authentication method, handling rate limits and transient failures,
managing pagination for large datasets, validating responses, and testing
without hitting production endpoints. Without a systematic approach, API
integrations become fragile, hard to debug, and difficult to maintain.

## Context / Trigger Conditions

- Connecting to a new REST or GraphQL API for the first time
- Implementing authentication for an API (OAuth, API keys, Bearer tokens)
- Encountering rate limit errors (HTTP 429) or throttling
- Debugging connection failures, timeouts, or authentication errors
- Building a client library or wrapper module for an API
- Handling paginated responses that require multiple requests

## Solution

### 1. Authentication

Select the appropriate authentication method based on the API's requirements:

#### Basic HTTP Authentication

For simple APIs with username/password credentials. Include credentials in the
request header encoded as Base64.

```
Authorization: Basic base64(username:password)
```

Use only over HTTPS. Basic Auth sends credentials with every request, so the
connection must be encrypted. Suitable for internal APIs or development
environments. Avoid for production-facing public APIs.

#### API Key Authentication

The most common method for SaaS APIs. Include the key as a query parameter or
in a custom header.

```
# As a header (preferred -- does not appear in URLs or server logs)
X-API-Key: your-api-key-here

# As a query parameter (less secure -- appears in URLs and logs)
https://api.example.com/v1/resource?api_key=your-api-key-here
```

Store API keys in environment variables or a secrets manager. Never commit keys
to version control. Rotate keys periodically and after any suspected exposure.

#### Bearer Token Authentication

For APIs that issue tokens after an initial authentication step. Include the
token in the Authorization header.

```
Authorization: Bearer your-access-token-here
```

Implement token refresh logic if the API issues tokens with expiration times.
Refresh the token before it expires to avoid request failures. Store both the
access token and refresh token securely.

#### OAuth 2.0

For APIs that require user authorization. The standard flow involves:

1. Redirect user to the authorization endpoint.
2. User grants permission.
3. Receive an authorization code via callback URL.
4. Exchange the authorization code for access and refresh tokens.
5. Use the access token for API requests.
6. Refresh the token when it expires.

Implement the OAuth flow using a well-maintained library rather than writing
it from scratch. Verify the `state` parameter to prevent CSRF attacks. Use
PKCE (Proof Key for Code Exchange) for public clients (mobile, single-page apps).

### 2. Error Handling

#### HTTP Status Code Handling

Categorize responses by status code and handle each category appropriately:

| Category | Status Codes | Action |
|----------|-------------|--------|
| Success | 200-299 | Process response body |
| Client Error (retryable) | 429 | Respect Retry-After header, then retry |
| Client Error (permanent) | 400, 401, 403, 404, 422 | Log error, do not retry, alert developer |
| Server Error | 500, 502, 503, 504 | Retry with exponential backoff |

#### Retry Strategy

Implement retry with exponential backoff and jitter for transient failures:

```
base_delay = 1 second
max_delay = 60 seconds
max_retries = 5

for attempt in range(max_retries):
    response = make_request()
    if response.status_code in [200-299]:
        return response
    if response.status_code == 429:
        wait = parse_retry_after_header(response) or calculate_backoff(attempt)
    elif response.status_code in [500, 502, 503, 504]:
        wait = calculate_backoff(attempt) + random_jitter()
    else:
        raise ApiError(response)
    sleep(wait)
```

Add jitter (random variation) to prevent thundering herd problems when many
clients retry simultaneously. Use `random.uniform(0, wait * 0.1)` for jitter.

#### Circuit Breaker Pattern

For sustained API integrations, implement a circuit breaker to prevent cascading
failures:

- **Closed state:** Requests pass through normally. Track failure rate.
- **Open state:** When failure rate exceeds threshold (e.g., 50% over 10 requests),
  stop sending requests. Return errors immediately.
- **Half-open state:** After a timeout period, allow one test request. If it
  succeeds, close the circuit. If it fails, stay open.

### 3. Pagination

APIs return large datasets in pages. Handle pagination systematically:

#### Common Pagination Patterns

- **Offset/Limit:** `?offset=0&limit=100` -- Simple but slow for large offsets.
  The database must scan and skip all preceding rows.
- **Cursor-based:** `?cursor=abc123&limit=100` -- Efficient for large datasets.
  The cursor encodes the position in the result set.
- **Link Header:** The API returns a `Link` header with `next`, `prev`, `first`,
  and `last` URLs. Follow the `next` link until it is absent.

#### Pagination Implementation

```python
def fetch_all_pages(fetch_page_fn, max_pages=1000):
    """Fetch all pages from a paginated API endpoint."""
    all_items = []
    cursor = None
    pages_fetched = 0

    while pages_fetched < max_pages:
        response = fetch_page_fn(cursor=cursor, limit=100)
        items = response.get("items", [])
        all_items.extend(items)

        cursor = response.get("next_cursor")
        if not cursor or not items:
            break

        pages_fetched += 1
        respect_rate_limit(response)

    return all_items
```

Always set a `max_pages` limit to prevent infinite loops if the API returns a
cursor that cycles or never terminates.

### 4. Request and Response Validation

Validate API responses before processing them. Do not trust external data.

- **Schema validation:** Define expected response schemas and validate every
  response against them. Use JSON Schema, Pydantic models, or Zod schemas.
- **Type checking:** Verify field types match expectations. An API that
  documents a field as an integer but returns a string will cause subtle bugs.
- **Null handling:** Check for null or missing fields that your code assumes
  are present. External APIs can change their response format without notice.
- **Timeout configuration:** Set explicit timeouts on all requests. A default
  timeout of 30 seconds for regular requests and 120 seconds for long-running
  operations is a reasonable starting point.

### 5. Testing API Integrations

#### Unit Testing with Mocks

Mock the HTTP client in unit tests. Record real API responses and replay them
in tests. This provides realistic test data without hitting the actual API.

#### Integration Testing with Recording Proxies

Use tools like VCR.py, Pretender, or Polly.js to record real API interactions
and replay them in tests. This captures actual API behavior including headers,
status codes, and response formats.

#### Contract Testing

If the API provides a contract (OpenAPI/Swagger specification), validate that
your client conforms to the contract. This catches breaking changes early.

## Verification

- [ ] Authentication works for all required methods (Basic, Bearer, OAuth, API Key)
- [ ] Rate limit responses (429) are handled with appropriate backoff
- [ ] Server errors (5xx) are retried with exponential backoff
- [ ] Paginated responses are fully consumed without infinite loops
- [ ] Response validation catches unexpected formats
- [ ] Timeouts are set on all requests
- [ ] API keys and tokens are stored in environment variables, not in code

## Example

```
# Connecting to a paginated API with Bearer token authentication

$ export API_TOKEN="ghp_xxxxxxxxxxxx"
$ curl -H "Authorization: Bearer $API_TOKEN" \
       "https://api.example.com/v1/items?limit=100"

{
  "items": [...],
  "next_cursor": "eyJpZCI6MTAwfQ==",
  "rate_limit": { "remaining": 4985, "reset_at": "2026-01-15T12:00:00Z" }
}

# Continue with next_cursor until all items are fetched
$ curl -H "Authorization: Bearer $API_TOKEN" \
       "https://api.example.com/v1/items?limit=100&cursor=eyJpZCI6MTAwfQ=="
```

## Notes

- See also: `software-development-best-practices` for general code quality principles
- See also: `debugging-systematic-approach` for debugging API connection issues
- When evaluating a new API, check its rate limits, authentication requirements,
  and error response format before writing integration code. Document these in
  the client module's README.

## References

- OAuth 2.0 RFC 6749: https://datatracker.ietf.org/doc/html/rfc6749
- HTTP Status Codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- JSON Schema: https://json-schema.org/

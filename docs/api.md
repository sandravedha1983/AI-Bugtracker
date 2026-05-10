# API Documentation

The AI Bug Tracker provides a comprehensive REST API for managing bugs and viewing analytics.

## Authentication
Most endpoints require a session cookie. Authenticate via `/login` or Google OAuth.

## Bug Management

### GET /api/bugs
**Description**: Retrieve all bugs the current user has access to.
**Response**: `200 OK` with JSON array of bug objects.

### POST /api/bugs
**Description**: Report a new bug.
**Body**:
```json
{
  "title": "Bug title",
  "description": "Bug description"
}
```
**Response**: `201 Created`.

### PUT /api/bugs/<id>
**Description**: Update bug status.
**Body**:
```json
{
  "status": "In Progress"
}
```
**Response**: `200 OK`.

## Analytics

### GET /api/analytics/summary
**Description**: Comprehensive summary of all system metrics.
**Response**: `200 OK`.

---

For interactive documentation, visit `/apidocs`.

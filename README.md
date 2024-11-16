# healthcheck.py

healthcheck.py is designed as a streamlined, single-tenant alternative to healthcheck.io, providing a straightforward solution for monitoring cron jobs and background tasks.

It enables you to create checks for scheduled tasks and receive alerts when those tasks fail to report within a specified timeframe.

Note: The tool is intentionally minimalistic. It assumes operation within a secure network, does not include built-in dashboards or alert systems, and expects external tools like Nagios or Icinga to handle those functionalities. It relies on an SQLite database, making it easy to run everything within a single container.

A sample docker-compose.yml is included, featuring Traefik as a reverse proxy with basic authentication.

## Features:
* Check Creation: Set up and manage checks for cron jobs or background tasks.
* Ping Endpoints: Generate unique URLs for tasks to ping upon completion.
* Check Removal: Easily delete checks that are no longer needed.

## Getting Started
```bash
git clone https://github.com/mohshami/healthcheck.py.git
cp .env.sample .env
# set variables in .env
docker compose up -d
```

## Usage
### "Ping" service
```bash
# "ttl" is the time in seconds before the check expires, defaults to 3600
curl -H "ttl: 300" http://localhost:3000/ping/test1
```

### Status check
```bash
# All Checks
$ curl http://localhost:3000/status

# Returns 200 when none of the checks expired
{"status":"healthy"}

# Returns 503 when at least one check expired
{"status_code":503,"detail":"test1 expired","headers":null}

# Single check, returns 503 if the check in question expired or does not exist
$ curl http://localhost:3000/status/test1

# Success
{"status":"healthy"}

# Check expired
{"status_code":503,"detail":"test1 expired","headers":null}

# Check does not exist
{"status_code":503,"detail":"Check test2 does not exist","headers":null}
```

### Remove a check
```bash
curl -X DELETE http://localhost:3000/ping/test1
```

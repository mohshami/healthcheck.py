# healthcheck.py

healthcheck.py is designed as a streamlined, single-tenant alternative to healthcheck.io, providing a straightforward solution for monitoring cron jobs and background tasks.

It enables you to create checks for scheduled tasks and receive alerts when those tasks fail to report within a specified timeframe.

Note: The tool is intentionally minimalistic. It assumes operation within a secure network, does not include built-in dashboards or alert systems, and expects external tools like Nagios or Icinga to handle those functionalities. It relies on an SQLite database, making it easy to run everything within a single container.

A sample docker-compose.yml is included, featuring Traefik as a reverse proxy with basic authentication.

## Features:
* Check Creation: Set up and manage checks for cron jobs or background tasks.
* Ping Endpoints: Generate unique URLs for tasks to ping upon completion.
* Check Removal: Easily delete checks that are no longer needed

## Getting Started
```bash
git clone https://github.com/mohshami/healthcheck.py.git
# For now, only the database path is defined, only needed if you want to run
# healthcheck.py without docker
cp .env.sample .env
# Update db_path if needed
docker compose up -d
```

## Usage
### Update check
```bash
curl -H "exitcode: 1" \
     -H "grace: 20" \
     -H "output: OK - Status" \
     http://localhost:3000/update/test1
```

### Status check
```bash
```bash
# All checks
$ curl http://localhost:3000/status

# Returns
# Success
{"status":"OK"}

# A service check expired or failed
{"status":"Error","Message":"At least one check failed or expired"}

# Single check
$ curl http://localhost:3000/status/test1

# Returns
{"lastupdate":1742664689,"grace":20,"output":"OK - Status","status":0,"expired":true}
```

### Remove a check
```bash
curl http://localhost:3000/delete/test1

# Returns
{"status":"ok"}
```

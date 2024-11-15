# healthcheck.py

healthcheck.py aims to be a simpler single-tenant alternative to healthcheck.io; a service for monitoring cron jobs and background tasks. It allows you to set up checks for scheduled tasks, receive alerts when those tasks fail to report within a specified time. It is very barebones by design, and assumes it is running on a secure network. It also lacks any dashboards or alerts, it assumes a tool such as Nagios/Icinga will be used for dashboards/alerts. It uses an SQLite database to keep everything running in a single container.

A sample docker-compose.yml file running Traefik as a reverse proxy with basic authentication is provided.

## Features
* Check Creation: Create and manage checks for cron jobs or background tasks.
* Ping Endpoints: Unique URLs to ping from your tasks to signal completion.
* Check Removal: Remove checks that are no longer needed

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

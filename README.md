# healthcheck.py

healthcheck.py aims to be a simpler single-tenant alternative to healthcheck.io; a service for monitoring cron jobs and background tasks. It allows you to set up checks for scheduled tasks, receive alerts when those tasks fail to report within a specified time. It is very barebones by design, and assumes it is running on a secure network. It also lacks any dashboards or alerts, it assumes a tool such as Nagios/Icinga will be used for dashboards/alerts. It uses an SQLite database to keep everything running in a single container.

A sample docker-compose.yml file running Traefik as a reverse proxy with basic authentication is provided.

## Features
* Check Creation: Create and manage checks for cron jobs or background tasks.
* Ping Endpoints: Unique URLs to ping from your tasks to signal completion.
* Check Removal: Remove checks that are no longer needed

## Getting Started
* Clone the repo
* cp .env.sample .env
* set variables in .env
* run docker compose up -d

## Usage
```
# Status check, returns 503 when at least one check expires, 200 otherwise
$ curl http://localhost:8000/status
# Success
{"status":"healthy"}
# Check(s) expired
{"status_code":503,"detail":"test1 expired","headers":null}

# Status check, returns 503 if the check in question expired or does not exist
$ curl http://localhost:8000/status/test1
# Success
{"status":"healthy"}
# Check expired
{"status_code":503,"detail":"test1 expired","headers":null}
# Check does not exist
{"status_code":503,"detail":"Check test2 does not exist","headers":null}

# "Ping" service
# "ttl" is the time in seconds before the check expires, defaults to 3600
curl -H "ttl: 300" http://localhost:8000/ping/test1

# Remove a check
curl -X DELETE http://localhost:8000/ping/test1
```

# healthcheck.py

healthcheck.py aims to be a simpler single-tenant alternative to healthcheck.io; a service for monitoring cron jobs and background tasks. It allows you to set up checks for scheduled tasks, receive alerts when those tasks fail to report within a specified time. It is very barebones by design, and assumes it is running on a secure network. It also lacks any dashboards or alerts, it assumes a tool such as Nagios/Icinga will be used for dashboards/alerts. It uses an SQLite database to keep everything running in a single container.

## Features
* Check Creation: Create and manage checks for cron jobs or background tasks.
* Ping Endpoints: Unique URLs to ping from your tasks to signal completion.

## Getting Started

* Clone the repo
* docker build -t healthcheck .
* docker run -d --rm -it -p 3000:3000 healthcheck

## Usage
```
# Status check, returns 503 when at least one check expires, 200 otherwise
$ curl http://localhost:8000/status
{"status":"healthy"}

# "Ping" service
# "ttl" is the time in seconds before the check expires, defaults to 3600
curl -H "ttl: 300" http://localhost:8000/ping/something
```

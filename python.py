<#
.SYNOPSIS
Creates a Docker ELK stack project with 50 commits (Oct-Dec 2022) on alternate days
#>

# Configuration - UPDATE WITH YOUR DETAILS
$REPO_DIR = "C:\Users\SRILUCKY\OneDrive\Desktop\my_github_projects\Docker_elk_projects"
$USER_NAME = "srikanth5451"
$USER_EMAIL = "91301139+srikanth5451@users.noreply.github.com"
$START_DATE = [datetime]"2022-10-01"
$END_DATE = [datetime]"2022-12-31"
$TOTAL_COMMITS = 50

# Initialize repository
Remove-Item $REPO_DIR -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $REPO_DIR -Force
Set-Location $REPO_DIR
git init
git config user.name $USER_NAME
git config user.email $USER_EMAIL

# Create ELK stack Docker project files
$projectFiles = @{
    "docker-compose.yml" = @'
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    ports:
      - "5000:5000"
    volumes:
      - ./logstash/config:/usr/share/logstash/config
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  es_data:
    driver: local
'@

    "logstash/pipeline/logstash.conf" = @'
input {
  beats {
    port => 5044
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:loglevel} %{GREEDYDATA:message}" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
'@

    "README.md" = @'
# Docker ELK Stack Project

## Project Description
Complete ELK (Elasticsearch, Logstash, Kibana) stack deployment using Docker

## Features
- Elasticsearch 8.5.0 with single-node configuration
- Logstash with custom pipeline configuration
- Kibana for visualization
- Docker Compose for easy deployment

## Quick Start
```bash
docker-compose up -d
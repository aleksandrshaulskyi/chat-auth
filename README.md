Chat-Logging

Logging microservice for the distributed chat system

Overview

This microservice provides centralized logging via the classic ELK stack (Elasticsearch, Logstash, Kibana), with Filebeat used as the log shipper.

It includes pre-built Kibana dashboards with both list-style log views and graphical visualizations.
All dashboards are located in the /kibana_dashboards/ directory and can be imported directly into Kibana.

Note: In ~90% of practical cases I would choose a modern, lightweight stack like OpenTelemetry + Prometheus + Grafana + Loki.
It’s simpler, more lightweight, and you'll likely use Prometheus/Grafana for metrics anyway.

Development Stage

Active development.
Updates are released several times a week.

Features

Centralized logging for all services in the distributed chat system

Pre-built Kibana dashboards

Filebeat-based log transportation

Fully containerized environment

Usage
1. Clone the repository
git clone <your-repo-url>

2. Create an .env file

Use env_example.txt located in the backend directory.
You can simply copy it as-is — it contains no project-specific secrets.

3. Run the stack
docker-compose up --build

4. Open Kibana

Kibana will be available at:

http://localhost:5601

Dashboards

All dashboards are located in:

/kibana_dashboards/


You can import them through Kibana → Stack Management → Saved Objects → Import.

Recent Updates

No released updates yet.

Root Repository

The index repository for the entire distributed chat system:

https://github.com/aleksandrshaulskyi/chat-index
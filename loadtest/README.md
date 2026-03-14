# Load Testing with Locust

## Quick Start

### Run locally (against local backend)
```bash
pip install locust
cd loadtest
locust -f locustfile.py --host=http://localhost:8000
```
Then open http://localhost:8089 for the web UI.

### Run headless (1,000+ concurrent users)
```bash
cd loadtest
locust -f locustfile.py \
  --headless \
  --host=http://localhost:8000 \
  --users 1100 \
  --spawn-rate 50 \
  --run-time 120s \
  --csv=results \
  --html=report.html
```

### Run against Docker stack
```bash
# Start the full stack
docker compose up -d --build

# Wait for it to be ready, then run load test
cd loadtest
locust -f locustfile.py --headless --host=http://localhost:8000 --users 1100 --spawn-rate 50 --run-time 120s
```

## User Profiles

| User Type         | Weight | Description                              |
| ----------------- | ------ | ---------------------------------------- |
| HealthCheckUser   | 10%    | Hits health endpoint                     |
| AnonymousBrowsing | 50%    | Browses products, doctors, hospitals     |
| AuthenticatedUser | 40%    | Registers, logs in, browses & uses cart  |

## Success Criteria

- **Error rate** < 5%
- **P99 latency** < 10 seconds
- System remains responsive under 1,000+ concurrent users

# Deployment Savant

A baseball pitcher deployment analyzer inspired by Baseball Savant and mlbpitchprofiler.com.

## Functionality

Deployment Savant evaluates a pitcher's deployment tendencies using:

- Pitch-tunneling frequencies (ABtunnel%)
- Pitch-location frequencies (Azone%)
- Other characteristics (e.g., arm-angle)

It outputs:

- Normalized (percentalized) deployment tendencies

## Motivation

I wanted to build a web-application to view percentalized pitcher profiles (à la Baseball Savant, mlbpitchprofiler.com), but in terms of deployment-metrics (i.e., the "how") rather than performance-metrics (i.e., the "what").

## Tech stack

### Languages

- CSS
- JavaScript (JSX)
- Python
- SQL

### Frameworks

- pytest
  - unittest.mock

### Python Libraries

- pandas

## Challenges

- SQL and JSX learning curves

## Live demo

- coming soon...

**Notes:**

- This project is currently in-development (pre-deployment)

## Project Structure

backend/
├── source_data.py
├── parse_data.py
├── profiler.py
├── processer.py
├── comparer.py
├── static/
├──── ...
├── data/
├──── parse_data.sql
├──── ...
├── tests/
├──── ...
...

## Future improvements

- Build machine learning model to model pitcher deployment similarity

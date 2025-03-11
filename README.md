# Agent Framework

A framework for building intelligent agents.

## Features

- AI-powered assistant for apartment complex administration
- Built with FastAPI for high performance
- Uses Gemini 2.0 Flash model for intelligent responses
- Includes calculator tool functionality

## Installation

### Prerequisites

- Python 3.8+
- Redis
- Make utility

### Setup

1. Clone the repository
2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies using Make:

```bash
make install
```

## Running the Application

To run the application, use the following command:

```bash
make run-services
```
This will start the FastAPI server, Redis server, and the Celery worker in http://localhost:8000.

## Documentation

The API documentation can be accessed at http://localhost:8000/docs.
# Full stack app boilerplate

## Overview

This repository contains a full-stack application that includes a Flask backend, a frontend, MongoDB, Storybook for UI development, and Mongo Express for MongoDB GUI.

## Requirements

- Docker
- Docker Compose

## Architecture

- **Backend**: Python (Flask)
- **Frontend**: React
- **Database**: MongoDB
- **UI Development**: Storybook
- **Database GUI**: Mongo Express

## Setup

### Clone the Repository

```bash
git clone [your_repository_link]
cd [your_repository_folder]
```

### Run Docker Compose

```bash
docker-compose up --build
```

## Services

### Backend

- Flask-based backend
- Exposed on port 5000
- Connects to MongoDB on port 12000

### Frontend

- Exposed on port 11000

### Storybook

- UI development environment
- Exposed on port 13000

### MongoDB

- NoSQL database
- Exposed on port 12000

### Mongo Express

- Web-based MongoDB admin interface
- Exposed on port [your_port]

## Logging

- Backend service is set up with Python's built-in logging for debugging and monitoring

## Volumes

- MongoDB data is persistent and stored in a Docker volume

## Network

- All services are connected on a custom Docker network `boilerplate-network`

## Troubleshooting

For any issues, please refer to the respective logs of the Docker containers.

## Contributing

To contribute to this project, please follow the standard fork-and-pull request workflow.

Feel free to customize the README to better match your project's specific requirements.

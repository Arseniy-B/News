# News Aggregator

## Description

News Aggregator is a simple web application for aggregating news from a third-party API (currently only "NewsAPI"). The application does not store the news content itself, but only user data. Authentication is implemented via email and password.

## Technologies

- **Backend**: Python, FastAPI, pydantic, pydantic-settings, sqlalchemy, aiohttp, redis, alembic
- **Frontend**: TypeScript, React, shadcn/ui
- **Databases**: PostgreSQL, Redis
- **APIs**: NewsAPI, and any SMTP server for sending email messages
- **Authentication**: JWT
- **Deployment**: Docker, Docker Compose

## Installation and Setup

1. Clone the repository:
```
	git clone https://github.com/Arseniy-B/News.git
	cd news-aggregator
```

2. Create a .env file in the back/ directory:
```
    REDIS_HOST=redis
    REDIS_PORT=6379
    DB_HOST=db
    DB_PORT=5432
	
    # NewsAPI secret key for authorization (you can get it from https://newsapi.org)
    API_KEY=your_newsapi_key
	
    # Database variables
    DB_USER=your_db_user
    DB_PASS=your_db_pass
    DB_NAME=your_db_name
	
    # Email sending variables
    # Some SMTP servers require a separate password for automated sending. Check the specifics on your SMTP server's website.
    EMAIL_ADDRESS=your_email@domain.com
    EMAIL_PASSWORD=your_email_password
    SMTP_SERVER=smtp.yourprovider.com
```

3. Launch with Docker Compose:
	`docker-compose up --build`

The application will be available at http://localhost:5173 (or your configured port). Ensure Docker and Docker Compose are installed on your system.



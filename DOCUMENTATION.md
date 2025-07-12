# EthIQ Documentation

## Overview

EthIQ is an ethical intelligence platform designed for content moderation at scale. This project was developed for the GenAI Hackathon 2025 by Team Nova.

## Project Structure

```
nova-hackathon/
├── agents/           # AI agent implementations
│   └── __init__.py
├── api/             # API endpoints and schemas
│   ├── main.py      # FastAPI application
│   └── schemas.py   # Pydantic models
├── tools/           # Utility tools and scripts
│   └── right-balancer.py
├── dashboard.py     # Web dashboard interface
├── requirements.txt # Python dependencies
├── README.md        # Project overview
└── DOCUMENTATION.md # This file
```

## Dependencies

### Core Dependencies

The project requires the following Python packages:

```txt
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
python-multipart>=0.0.6
jinja2>=3.1.2
aiofiles>=23.2.1
python-dotenv>=1.0.0
```

### Optional Dependencies

For development and testing:
```txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
```

## Setup Instructions

### Prerequisites

1. **Python 3.8+**: Ensure you have Python 3.8 or higher installed
2. **Virtual Environment**: Recommended to use a virtual environment

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd nova-hackathon
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database (if applicable)
DATABASE_URL=sqlite:///./ethiq.db

# External APIs (if applicable)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Security
SECRET_KEY=your_secret_key_here
```

## Usage

### Running the API Server

1. **Start the FastAPI server**:
   ```bash
   cd api
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access the API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running the Dashboard

1. **Start the dashboard**:
   ```bash
   python dashboard.py
   ```

2. **Access the dashboard**:
   - Web interface: http://localhost:8080

### Using the Tools

1. **Right Balancer Tool**:
   ```bash
   cd tools
   python right-balancer.py [options]
   ```

## API Endpoints

### Content Moderation

- `POST /api/moderate` - Submit content for ethical analysis
- `GET /api/analysis/{id}` - Retrieve analysis results
- `GET /api/history` - View moderation history

### Agent Management

- `GET /api/agents` - List available AI agents
- `POST /api/agents/configure` - Configure agent parameters
- `GET /api/agents/status` - Check agent status

### Analytics

- `GET /api/analytics/summary` - Get moderation statistics
- `GET /api/analytics/trends` - View trend analysis
- `POST /api/analytics/export` - Export data

## Development

### Code Style

- Use **Black** for code formatting
- Follow **PEP 8** guidelines
- Use type hints for all functions

### Testing

Run tests with pytest:
```bash
pytest tests/
```

### Code Quality

Check code quality:
```bash
flake8 .
black --check .
```

## Deployment

### Production Setup

1. **Environment Configuration**:
   - Set `DEBUG=False`
   - Configure production database
   - Set up proper logging

2. **Server Requirements**:
   - Use a production WSGI server (Gunicorn)
   - Set up reverse proxy (Nginx)
   - Configure SSL certificates

3. **Docker Deployment** (optional):
   ```bash
   docker build -t ethiq .
   docker run -p 8000:8000 ethiq
   ```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure virtual environment is activated
   - Check that all dependencies are installed

2. **API Connection Issues**:
   - Verify environment variables are set
   - Check API keys are valid

3. **Dashboard Not Loading**:
   - Ensure API server is running
   - Check port configurations

### Logs

- API logs: Check console output or log files
- Dashboard logs: Monitor browser console
- Error tracking: Implement proper error logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the FAQ section

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Team**: Nova 
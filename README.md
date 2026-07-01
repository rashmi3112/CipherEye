# CipherEye

CipherEye is an AI-powered cybersecurity analysis platform that combines a React frontend with a FastAPI backend to inspect URLs, text, images, and other inputs for threat indicators and privacy risks.

## Features
- Analyze URLs, text, and images
- Detect threat patterns and PII exposure
- Generate structured security reports with trust scoring
- Visualize agent-based analysis workflow

## Project Structure
- backend/: FastAPI server, agents, and analysis logic
- frontend/: React + Vite dashboard interface

## Getting Started

### Backend
1. Go to the backend directory
2. Create and activate a Python virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python main.py
   ```

### Frontend
1. Go to the frontend directory
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Notes
- Keep sensitive credentials out of the repository.
- Use environment variables or local secret files for service account configuration.

# Universal Text-to-JSON API

A powerful, AI-driven tool that extracts structured JSON data from raw, unstructured text using Google's Gemini model. It features a robust FastAPI backend and a modern, responsive frontend interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)

## Features

- **AI-Powered Extraction**: Uses Google Gemini 2.5 Flash for high-accuracy data extraction.
- **Flexible Schema**: Define any JSON schema you want, and the AI will map the text to it.
- **Modern Frontend**: Clean, responsive UI built with Tailwind CSS and Lucide icons.
- **RESTful API**: Fully documented API endpoints for easy integration with other services.
- **CORS Enabled**: Ready for cross-origin requests from other applications.
- **Static File Serving**: Integrated frontend serving directly from the backend.

## Prerequisites

- Python 3.9 or higher
- A Google Gemini API Key (Get one [here](https://aistudio.google.com/app/apikey))

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd text_to_json
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   Create a `.env` file in the root directory and add your API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Running the Server
Start the application using Python:
```bash
python main.py
```
The server will start at `http://0.0.0.0:8000`.

### Using the Frontend
Open your browser and navigate to:
```
http://localhost:8000
```
You will see the web interface where you can paste text, define a schema, and see the results in real-time.

### Using the API
You can interact with the API directly using tools like `curl` or Postman.

**Endpoint:** `POST /extract`

**Request Body:**
```json
{
  "text_content": "The iPhone 15 Pro costs $999 and features a titanium design.",
  "target_schema": {
    "type": "object",
    "properties": {
      "product_name": { "type": "string" },
      "price": { "type": "number" },
      "features": { "type": "array", "items": { "type": "string" } }
    }
  }
}
```

**Response:**
```json
{
  "product_name": "iPhone 15 Pro",
  "price": 999,
  "features": [
    "titanium design"
  ]
}
```

## Project Structure

```
text_to_json/
├── config.py               # Configuration management
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── services/
│   └── gemini_service.py   # Gemini API integration logic
└── static/
    └── index.html          # Frontend application
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.

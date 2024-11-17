# RAG-4-IRD

RAG-4-IRD is a FastAPI-based application designed to assist users with tax services, filing requirements, and regulations for the Inland Revenue Department (IRD) of Sri Lanka. The application uses web scraping, natural language processing, and vector databases to provide accurate and actionable information.

## Features

- **Web Scraping**: Collects data from specified URLs and processes it for further analysis.
- **Natural Language Processing**: Utilizes OpenAI's GPT-4o-mini model to generate descriptions and assist users with tax-related queries.
- **Vector Database**: Stores and retrieves document embeddings using ChromaDB for efficient information retrieval.
- **FastAPI Endpoints**: Provides RESTful endpoints for web scraping and chat functionalities.

## Installation

### Prerequisites

- Python 3.12
- Docker and Docker Compose
- Poetry for dependency management

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/rag-4-ird.git
   cd rag-4-ird
   ```

2. **Install Dependencies**

   Use Poetry to install the required dependencies:

   ```bash
   poetry install
   ```

3. **Environment Variables**

   Create a `.env` file in the root directory and add your API keys:

   ```plaintext
   LANGCHAIN_API_KEY=your_langchain_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Docker Setup**

   Build and run the Docker container:

   ```bash
   docker-compose up --build
   ```

## Usage

### Endpoints

- **GET /**: Test endpoint to verify the server is running.
- **POST /chat**: Accepts a JSON payload with a `question` and `thread_id` to provide tax-related assistance.
- **POST /web_scrape**: Accepts a JSON payload with `url` and `page_limit` to scrape and process web pages.

### Example `curl` Commands

- **Chat Endpoint**

  ```bash
  curl -X POST "http://localhost:8000/chat" \
       -H "Content-Type: application/json" \
       -d '{"question": "How do I file an income tax return?", "thread_id": "1234"}'
  ```

- **Web Scrape Endpoint**

  ```bash
  curl -X POST "http://localhost:8000/web_scrape" \
       -H "Content-Type: application/json" \
       -d '{"url": "http://www.ird.gov.lk/en", "page_limit": 5}'
  ```

## Code Structure

- **main.py**: Initializes the FastAPI application and defines the endpoints.

  ```python:main.py
  startLine: 1
  endLine: 73
  ```

- **vector_db/chroma.py**: Handles vector database operations using ChromaDB.

  ```python:vector_db/chroma.py
  startLine: 1
  endLine: 61
  ```

- **web_crawler_and_scraper/description_generator.py**: Generates descriptions from web page content using OpenAI.
  ```python:web_crawler_and_scraper/description_generator.py
  startLine: 1
  endLine: 123
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact Savith Panamgama at geethikasavith@gmail.com.

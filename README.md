# SciTranslate Service

This is a web app that translates scientific articles from Russian into English. It is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installing

1. Clone the repository:

2. Change into the project directory:
`cd SciTranslate_service`


3. Build the Docker image:
`docker build -t scitranslate .`


4. Run the Docker container:
`docker run -p 1111:1111 scitranslate`


5. Open your web browser and navigate to `http://127.0.0.1:1111/` to see the application in action.

## Usage

The application has two endpoints:

- `/translate/`: Accepts a POST request with a JSON payload containing a `text` field with the text to be translated. Returns a JSON response with the translated text.
- `/translate_article/`: Accepts a POST request with a file upload containing the scientific article to be translated. Returns a downloadable Excel file with the translated article.

The application also has a front-end interface that allows users to input text and see the translated output.

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework
- [Docker](https://www.docker.com/) - Containerization platform
- [Transformers](https://huggingface.co/transformers/) - State-of-the-art Natural Language Processing for TensorFlow 2.0 and PyTorch


# PDFChatBotApp
Simple app that allows you to aks questions about multiple pdf documents that were added to the app's 
knowledge base, It utilises OpenAI API for word embeddings.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/get-started)

## Getting Started

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository

First, clone the repository to your local machine using Git.

```sh
git clone https://github.com/BigQszak/PDFChatBotApp.git
```

### 2. Navigate to the Project Dirctory

```
cd PDFChatBotApp
```

### 3. Create '.env' file

```
echo. > .env
```

Open the .env file in your preferred text editor and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

Replace your_openai_api_key with your actual OpenAI API key.

### 4. Build and Run the Docker Container

```sh
docker build -t streamlitapp .
docker run -p 8501:8501 streamlitapp
```

The application will be available at http://localhost:8501


This project is licensed under the MIT License. See the LICENSE file for more details.
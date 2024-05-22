# PDFChatBotApp
Simple app that allows you to aks questions about multiple pdf documents that were added to the app's 
knowledge base, It utilises OpenAI API for word embeddings.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/get-started)

## Running the app with Docker image

### 1. Download Dockerfile to your local machine

Download provided Dockerfile 

### 2. Build and Run the Docker container

Run these commands in your terminal.

```sh
docker build --build-arg OPENAI_API_KEY={your_actual_openai_api_key} -t {name_of_your_image} .
docker run -d -p 8501:8501 {name_of_your_image} 
```
Replace {your_actual_openai_api_key} with your own OpenAI API key and {name_of_your_image} with the name of your choice

The application will be available at http://localhost:8501


## Running it locally

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

Create .env file that contains OpenAI API key. Run the following command:

```
echo "OPENAI_API_KEY={your_openai_api_key}" > .env
```

Replace {your_openai_api_key} with your actual OpenAI API key.

### 4. Create python virtual environment and install dependencies

Run the following commands:

```
python3.9.13 -m venv {myenv}

{myenv}/Scripts/activate

pip install -r requirements.txt

```

Replace {myenv} with the name of your choice.

### 5. Run the app

In order to run the app in your browser, run the following command:

```
streamlit run app.py 
```

This project is licensed under the MIT License. See the LICENSE file for more details.
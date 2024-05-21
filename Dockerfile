FROM python:3.9-slim

WORKDIR /app

# COPY requirements.txt /app/
# RUN pip install -r requirements.txt

# COPY . /app
# COPY .env /app/

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8501 

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENV NAME PDFChatBotApp

# CMD ["streamlit", "run", "app.py"]
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
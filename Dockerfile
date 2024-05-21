FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY .env /app/

EXPOSE 8080

ENV NAME PDFChatBotApp

CMD ["streamlit", "run", "app.py"]
FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install gunicorn
RUN pip install -r requirements.txt

COPY . .

# Executa a aplicação usando Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

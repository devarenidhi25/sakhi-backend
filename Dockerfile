FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    python -m spacy download en_core_web_sm

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

#user Python 
FROM python:3.11-slim

WORKDIR /Fraud_prediction

COPY  requirements.txt .
RUN pip install --no-cacher-dir -r requirements.txt

COPY  . .

EXPOSE 8000

CMD ["uvicorn", "Fraud_prediction:app", "--host", "0.0.0.0", "--port", "8000"]

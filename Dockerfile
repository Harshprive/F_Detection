#user Python 
FROM python:3.11-slim

# Set working Directory
WORKDIR /Fraud_prediction


#Copy requirements and install dependencies
COPY  requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application code
COPY  . .

EXPOSE 8000

# command to start FastAPI application
CMD ["uvicorn", "Fraud_prediction:app", "--host", "0.0.0.0", "--port", "8000"]

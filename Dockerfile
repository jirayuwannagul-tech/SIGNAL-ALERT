FROM python:3.11-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p data/logs storage

ENV PORT=8080
EXPOSE 8080

CMD ["python", "-m", "app.main"]

ENV GOOGLE_SHEETS_ID=1t715T22T8NhfaZRpjfR0zHDfcHqTq3EutG49xgGH8HU
ENV GOOGLE_SHEETS_CREDENTIALS=/app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json


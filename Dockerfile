FROM python:3.14

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY sql_scripts/ sql_scripts/
COPY clean_weather.parquet .

# Default command (you can override in cron)
CMD ["python3", "src/load.py"]

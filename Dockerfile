# Dockerfile

FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose both APIs and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Default command (just FastAPI for now)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

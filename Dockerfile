# 1. Use a lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only requirements first (this makes rebuilding faster)
COPY requirements.txt .

# 4. Install your libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your files (app.py, templates/, static/, etc.)
COPY app.py .
COPY cs2rcon.py .
COPY workshopmaps.py .
COPY templates/ ./templates/
COPY static/ ./static/

# 6. Tell Docker we are using port 5000
EXPOSE 5000

# 7. Start the Flask app
CMD ["python", "app.py"]
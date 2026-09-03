# 1. Use a lightweight Python image
FROM python:3.11-slim

# 2. Install git so we can clone from the repository
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Accept a build argument to force Docker to bypass cache and fetch fresh code
ARG CACHEBUST=1

# 5. Clone your repository directly into /app 
# (Replace with your actual GitHub/GitLab repository URL)
RUN git clone https://github.com/tmr2000/cs2-rcon-tool.git .

# 6. Install your libraries from the cloned requirements file
RUN pip install --no-cache-dir -r requirements.txt

# 7. Tell Docker we are using port 5000
EXPOSE 5000

# 8. Start the Flask app
CMD ["python", "app.py"]
# CS2 RCON Web Panel

A lightweight, web-based RCON administration panel for Counter-Strike 2 servers. This project allows you to manage your server console via a browser using a secure, dockerized Flask application. 

Project is still under development and should not be considered production ready. All features are subject to change

## Features
- **Real-time Console:** Send RCON commands and view server responses.
- **Dockerized:** Easy deployment and isolation.
- **Reverse Proxy Ready:** Optimized for use with Pangolin, Nginx Proxy Manager, or Traefik.
- **Mobile Friendly:** Manage your server on the go.
-  **More Coming Soon**

---

## Deployment with Docker Compose

This is the recommended way to run the panel on your Linux server. Use the following `docker-compose.yml` file:

```yaml
services:
  cs2-panel:
    container_name: cs2-panel
    image: tmr2000/cs2-panel:beta
    ports:
      - "5000:5000"
    restart: unless-stopped
    environment:
      RCON_SERVER: "SERVER IP"
      RCON_PORT: "SERVER PORT"
      RCON_PASSWORD: "SERVER PASSWORD"
      STEAM_WEB_API_KEY: "STEAM WEB API KEY - https://steamcommunity.com/dev/apikey"
    volumes:
      - "/pathtocs2installfolder/app/data:/app/data" 
```

Setup Instructions:

    Reverse Proxy: Point your domain (e.g., cs2panel.yourdomain.com) to the internal IP of your server on port 5000. (Always use https as Source RCON is an unencrypted protocol)

    Websockets: Ensure "Websockets Support" is enabled in your proxy settings to allow the console to update live.

    Firewall: Ensure port 5000 is open on your host machine if you are not using a Docker network for your proxy.

 Security Note

    Always run your CS2 server with a strong RCON password and if using via Reverse Proxy always use HTTPS

## Local Development & Build
Prerequisites

    Python 3.11+

    Docker Desktop (for building images)

Running Locally

    Clone the repository:

    git clone https://github.com/tmr2000/cs2-rcon-project.git
    cd cs2-rcon-project

    Create a .env file (ignored by Git) for local testing:

    RCON_IP: "CS2 Server IP Address"
    RCON_PORT: "27015"
    RCON_PASSWORD: "Your_RCON_Password"

    Install dependencies and run:

    pip install -r requirements.txt
    python app.py

Building the Image

To make changes to the code, use the included dockerbuild.bat (Windows) to rebuild and push the image to dockerhub:

```
docker build -t tmr2000/cs2-panel:beta .
docker push tmr2000/cs2-panel:beta
```

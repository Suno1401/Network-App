### Configuration pour l'application de test réseau ###

# Domaines à tester pour DNS
DNS_DOMAINS = [
    "www.google.com",
    "www.github.com",
    "www.cloudflare.com"
]

# Hosts à tester pour Ping
PING_HOSTS = [
    "8.8.8.8",      # Google DNS
    "1.1.1.1",      # Cloudflare DNS 
]

# Seuils de vitesse
SPEED_THRESHOLDS = {
    "min_download_mbps": 10,  # Minimum download speed in Mbps
    "min_upload_mbps": 5,   # Minimum upload speed in Mbps
}

# Configuration logging
LOGGING = {
    "filename": "network_app.log",
    "level": "INFO", # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL -> README
    "format": "[%(asctime)s] %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S"
}

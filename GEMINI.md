# Threat Intelligence Dashboard

A Python-based tool that monitors active network connections, geolocates remote IP addresses, and assesses their threat level using the AbuseIPDB API. The results are visualized on an interactive HTML map.

## Project Overview

- **Purpose**: Real-time monitoring and visualization of outgoing network connections with security reputation checks.
- **Core Technologies**:
    - **Python 3.14**: Main programming language.
    - **Folium**: For generating interactive maps (`mapa_siete.html`).
    - **Psutil**: To retrieve active network connections.
    - **Requests**: For interacting with geolocation and threat intelligence APIs.
    - **python-dotenv**: For managing configuration via `.env`.
- **Architecture**:
    - `main.py`: The entry point that orchestrates connection scanning, data retrieval, and map generation.
    - `ip_location.py`: Handles geolocation lookups using the `ip-api.com` service.
    - `ip_abuse.py`: Interfaces with the `AbuseIPDB` API to get reputation scores for IP addresses.

## Getting Started

### Prerequisites

- Python 3.x
- An API key from [AbuseIPDB](https://www.abuseipdb.com/) (optional but recommended for threat scores).

### Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your API key in a `.env` file:
   ```env
   ABUSEIPDB_API_KEY=your_actual_api_key_here
   ```

### Running the Dashboard

Execute the main script:
```bash
python main.py
```
After execution, open the generated `mapa_siete.html` file in any web browser to view the interactive map.

## Development Conventions

- **Modular Design**: Logic is split into specialized modules for geolocation and threat analysis.
- **Configuration**: Sensitive data and API keys must be stored in `.env` and never hardcoded.
- **Error Handling**: Basic try-except blocks are used to handle API failures gracefully.
- **Language**: Source code comments and print statements are currently in Slovak.

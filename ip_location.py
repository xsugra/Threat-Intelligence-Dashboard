import requests


def get_ip_location(ip):
    """Zistí GPS súradnice a mesto pre danú IP adresu."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response.get('status') == 'success' and 'lat' in response and 'lon' in response:
            return {
                'lat': response['lat'],
                'lon': response['lon'],
                'city': response.get('city', 'Unknown'),
                'country': response.get('country', 'Unknown')
            }
    except Exception:
        return None
    return None
import folium
import psutil
from ip_location import get_ip_location
from ip_abuse import check_ip_abuse

# Tvoja domáca poloha (Prednastavené napr. na strednú Európu/Slovensko)
MY_LAT = 48.6690
MY_LON = 19.6990


def main():
    print("Skenujem sieťové pripojenia...")
    try:
        connections = psutil.net_connections(kind='inet')
    except (psutil.AccessDenied, PermissionError):
        print("  [!] Chyba: Nedostatočné oprávnenia na prístup k sieťovým pripojeniam.")
        print("      Skús spustiť program s vyššími oprávneniami (napr. sudo python3 main.py).")
        return

    analyzed_ips = set()

    # Vytvorenie základnej mapy
    m = folium.Map(location=[MY_LAT, MY_LON], zoom_start=4, tiles="CartoDB dark_matter")

    # Pridáme bodku pre tvoj počítač
    folium.Marker([MY_LAT, MY_LON], popup="Tvoj Počítač", icon=folium.Icon(color="blue")).add_to(m)

    for conn in connections:
        if conn.raddr:
            ip = conn.raddr.ip

            # Ignorujeme lokálne a loopback IP adresy (IPv4 aj IPv6)
            is_local = (
                ip.startswith(('127.', '192.168.', '10.', '172.', '169.254.')) or
                ip in ('::1', '0.0.0.0', '::') or
                ip.startswith('fe80:')
            )

            if not is_local and ip not in analyzed_ips:
                analyzed_ips.add(ip)
                print(f"Analyzujem IP: {ip}...")

                location = get_ip_location(ip)
                if location:
                    # Kontrola hrozby
                    abuse_score = check_ip_abuse(ip)

                    # Logika farieb: Červená = nebezpečenstvo, Zelená = OK
                    if abuse_score > 20:
                        color = 'red'
                        print(f"  [!] POZOR: Hrozba detekovaná! Skóre: {abuse_score}/100")
                    else:
                        color = 'green'

                    # Pridanie bodu na mapu pre cieľový server
                    popup_text = f"{location['city']}, {location['country']}<br>IP: {ip}<br>Hrozba: {abuse_score}%"
                    folium.Marker(
                        [location['lat'], location['lon']],
                        popup=popup_text,
                        icon=folium.Icon(color=color)
                    ).add_to(m)

                    # Nakreslenie čiary z tvojho PC na server
                    folium.PolyLine(
                        locations=[[MY_LAT, MY_LON], [location['lat'], location['lon']]],
                        color=color,
                        weight=2,
                        opacity=0.5
                    ).add_to(m)

    # Uloženie mapy do súboru
    map_file = "mapa_siete.html"
    m.save(map_file)
    print("-" * 40)
    print(f"Hotovo! Otvor si súbor '{map_file}' vo svojom prehliadači.")


if __name__ == "__main__":
    main()




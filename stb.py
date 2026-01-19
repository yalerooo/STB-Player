"""
STB Checker & Player - Verificador y reproductor de canales IPTV
"""
import requests
import random
import string
import json
import re
import subprocess
import os
from urllib.parse import urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

# Traducciones
LANG = {
    'es': {
        'title': 'STB Checker & Player',
        'enter_url': 'URL del portal (ej: http://server.com:8080/c/): ',
        'enter_mac': 'Dirección MAC (ej: 00:1A:79:00:00:00): ',
        'error_empty': '[!] Debes introducir URL y MAC',
        'error_mac': '[!] Formato MAC inválido',
        'connecting': '[*] Conectando...',
        'connected': '[+] Conectado!',
        'error_connect': '[!] No se pudo conectar al portal',
        'user': '[+] Usuario: ',
        'categories': '[+] Categorías: ',
        'categories_title': 'CATEGORÍAS DISPONIBLES',
        'select_category': 'Escribe el número de la categoría o busca por nombre',
        'category_not_found': '[!] Categoría no encontrada',
        'selected_category': '[+] Categoría seleccionada: ',
        'getting_channels': '[*] Obteniendo canales...',
        'channels_count': ' canales',
        'menu': 'MENÚ',
        'opt_list': '1. Ver lista de canales',
        'opt_play': '2. Reproducir canal',
        'opt_search': '3. Buscar canal',
        'opt_category': '4. Cambiar categoría',
        'opt_exit': '5. Salir',
        'option': 'Opción: ',
        'channel_num': 'Número de canal: ',
        'invalid_num': '[!] Número inválido',
        'enter_num': '[!] Introduce un número',
        'search': 'Buscar: ',
        'not_found': 'No encontrado',
        'no_url': '[!] No se pudo obtener URL',
        'playing': '[+] Reproduciendo en VLC...',
        'vlc_not_found': '[!] VLC no encontrado. Copia esta URL:',
        'category': '[+] Categoría: ',
    },
    'en': {
        'title': 'STB Checker & Player',
        'enter_url': 'Portal URL (e.g.: http://server.com:8080/c/): ',
        'enter_mac': 'MAC Address (e.g.: 00:1A:79:00:00:00): ',
        'error_empty': '[!] You must enter URL and MAC',
        'error_mac': '[!] Invalid MAC format',
        'connecting': '[*] Connecting...',
        'connected': '[+] Connected!',
        'error_connect': '[!] Could not connect to portal',
        'user': '[+] User: ',
        'categories': '[+] Categories: ',
        'categories_title': 'AVAILABLE CATEGORIES',
        'select_category': 'Enter category number or search by name',
        'category_not_found': '[!] Category not found',
        'selected_category': '[+] Selected category: ',
        'getting_channels': '[*] Getting channels...',
        'channels_count': ' channels',
        'menu': 'MENU',
        'opt_list': '1. View channel list',
        'opt_play': '2. Play channel',
        'opt_search': '3. Search channel',
        'opt_category': '4. Change category',
        'opt_exit': '5. Exit',
        'option': 'Option: ',
        'channel_num': 'Channel number: ',
        'invalid_num': '[!] Invalid number',
        'enter_num': '[!] Enter a number',
        'search': 'Search: ',
        'not_found': 'Not found',
        'no_url': '[!] Could not get URL',
        'playing': '[+] Playing in VLC...',
        'vlc_not_found': '[!] VLC not found. Copy this URL:',
        'category': '[+] Category: ',
    }
}


class STBPlayer:
    def __init__(self, portal_url, mac_address):
        self.portal_url = portal_url.rstrip('/')
        self.mac = mac_address.upper()
        self.token = None
        self.active_url = None
        self.session = requests.Session()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3',
            'X-User-Agent': 'Model: MAG250; Link: WiFi',
            'Accept': '*/*',
        }
        
        self.serial = ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))
        self.device_id = ''.join(random.choices(string.hexdigits.upper(), k=32))

    def connect(self):
        """Conecta al portal y obtiene token"""
        parsed = urlparse(self.portal_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        urls = [base + '/c', base + '/portal.php', base + '/stalker_portal/c']
        
        for url in urls:
            self.active_url = url
            params = {'type': 'stb', 'action': 'handshake', 'token': '', 'JsHttpRequest': '1-xml'}
            self.headers['Cookie'] = f'mac={self.mac}; stb_lang=en; timezone=Europe/Madrid'
            
            try:
                response = self.session.get(url, params=params, headers=self.headers, timeout=15, verify=False)
                data = response.json()
                
                if 'js' in data and 'token' in data['js']:
                    self.token = data['js']['token']
                    self.headers['Authorization'] = f'Bearer {self.token}'
                    return True
            except:
                continue
        return False

    def get_profile(self):
        """Obtiene info del perfil"""
        params = {
            'type': 'stb', 'action': 'get_profile', 'hd': '1',
            'sn': self.serial, 'stb_type': 'MAG250', 'device_id': self.device_id,
            'JsHttpRequest': '1-xml'
        }
        try:
            response = self.session.get(self.active_url, params=params, headers=self.headers, timeout=15, verify=False)
            return response.json().get('js', {})
        except:
            return {}

    def get_categories(self):
        """Obtiene categorías de canales"""
        params = {'type': 'itv', 'action': 'get_genres', 'JsHttpRequest': '1-xml'}
        try:
            response = self.session.get(self.active_url, params=params, headers=self.headers, timeout=15, verify=False)
            return response.json().get('js', [])
        except:
            return []

    def get_channels(self, genre_id='*', page=1):
        """Obtiene lista de canales"""
        params = {
            'type': 'itv', 'action': 'get_ordered_list', 'genre': genre_id,
            'sortby': 'number', 'p': page, 'JsHttpRequest': '1-xml'
        }
        try:
            response = self.session.get(self.active_url, params=params, headers=self.headers, timeout=30, verify=False)
            return response.json().get('js', {})
        except:
            return {}

    def get_all_channels_from_category(self, genre_id):
        """Obtiene todos los canales de una categoría"""
        channels = []
        page = 1
        while page <= 30:
            result = self.get_channels(genre_id=genre_id, page=page)
            if not result or not result.get('data'):
                break
            channels.extend(result['data'])
            if len(channels) >= int(result.get('total_items', 0)):
                break
            page += 1
        return channels

    def get_stream_url(self, cmd):
        """Obtiene URL de streaming real"""
        params = {
            'type': 'itv', 'action': 'create_link', 'cmd': cmd,
            'JsHttpRequest': '1-xml'
        }
        try:
            response = self.session.get(self.active_url, params=params, headers=self.headers, timeout=15, verify=False)
            data = response.json()
            
            if 'js' in data and 'cmd' in data['js']:
                stream_cmd = data['js']['cmd']
                if stream_cmd.startswith('ffmpeg '):
                    return stream_cmd[7:]
                elif stream_cmd.startswith('ffrt '):
                    return stream_cmd[5:]
                for part in stream_cmd.split():
                    if part.startswith('http'):
                        return part
        except:
            pass
        return None

    def play_vlc(self, stream_url, name, lang='es'):
        """Reproduce en VLC"""
        t = LANG[lang]
        if not os.path.exists(VLC_PATH):
            print(f"\n{t['vlc_not_found']}")
            print(f"    {stream_url}")
            return
        
        args = [
            VLC_PATH, stream_url,
            '--http-user-agent=Mozilla/5.0 (QtEmbedded; U; Linux; C)',
            f'--http-referrer={self.portal_url}',
            '--network-caching=1000',
            f'--meta-title={name}',
        ]
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(t['playing'])

    def find_spain_category(self, categories):
        """Busca categoría de España"""
        for cat in categories:
            title = cat.get('title', '').lower()
            if 'spain' in title or 'españa' in title or 'espana' in title:
                return cat
        return None

    def filter_channels(self, channels):
        """Filtra separadores y canales vacíos"""
        return [ch for ch in channels 
                if ch.get('cmd') and '===' not in ch.get('name', '') and '###' not in ch.get('name', '')]


def main():
    print("="*60)
    print("  Language / Idioma")
    print("="*60)
    print("1. English")
    print("2. Español")
    lang_choice = input("\n> ").strip()
    lang = 'en' if lang_choice == '1' else 'es'
    t = LANG[lang]
    
    print("\n" + "="*60)
    print(f"  {t['title']}")
    print("="*60)
    
    # Pedir datos
    portal = input(f"\n{t['enter_url']}").strip()
    mac = input(t['enter_mac']).strip()
    
    if not portal or not mac:
        print(t['error_empty'])
        return
    
    # Validar MAC
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$', mac):
        print(t['error_mac'])
        return
    
    player = STBPlayer(portal, mac)
    
    # Conectar
    print(f"\n{t['connecting']}")
    if not player.connect():
        print(t['error_connect'])
        return
    
    print(t['connected'])
    
    # Perfil
    profile = player.get_profile()
    if profile:
        print(f"{t['user']}{profile.get('name', 'N/A')}")
    
    # Categorías
    categories = player.get_categories()
    print(f"{t['categories']}{len(categories)}")
    
    # Mostrar categorías para elegir
    print("\n" + "="*60)
    print(t['categories_title'])
    print("="*60)
    
    # Filtrar la categoría "All"
    cats_to_show = [c for c in categories if c.get('id') != '*']
    
    for i, cat in enumerate(cats_to_show, 1):
        print(f"{i:3}. {cat.get('title')}")
    
    # Elegir categoría
    print(f"\n{t['select_category']}")
    choice = input("> ").strip().lower()
    
    selected_cat = None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(cats_to_show):
            selected_cat = cats_to_show[idx]
    except ValueError:
        # Buscar por nombre
        for cat in cats_to_show:
            if choice in cat.get('title', '').lower():
                selected_cat = cat
                break
    
    if not selected_cat:
        print(t['category_not_found'])
        return
    
    print(f"\n{t['selected_category']}{selected_cat.get('title')}")
    
    # Obtener canales
    print(t['getting_channels'])
    all_channels = player.get_all_channels_from_category(selected_cat.get('id'))
    channels = player.filter_channels(all_channels)
    print(f"[+] {len(channels)}{t['channels_count']}")
    
    # Menú principal
    while True:
        print(f"\n{'='*60}")
        print(t['menu'])
        print("="*60)
        print(t['opt_list'])
        print(t['opt_play'])
        print(t['opt_search'])
        print(t['opt_category'])
        print(t['opt_exit'])
        
        opt = input(f"\n{t['option']}").strip()
        
        if opt == '1':
            for i, ch in enumerate(channels, 1):
                print(f"{i:3}. {ch.get('name')}")
        
        elif opt == '2':
            num = input(t['channel_num']).strip()
            try:
                idx = int(num) - 1
                if 0 <= idx < len(channels):
                    ch = channels[idx]
                    print(f"\n[*] {ch.get('name')}")
                    url = player.get_stream_url(ch.get('cmd'))
                    if url:
                        player.play_vlc(url, ch.get('name'), lang)
                    else:
                        print(t['no_url'])
                else:
                    print(t['invalid_num'])
            except:
                print(t['enter_num'])
        
        elif opt == '3':
            query = input(t['search']).strip().lower()
            found = [(i, ch) for i, ch in enumerate(channels, 1) 
                    if query in ch.get('name', '').lower()]
            if found:
                for i, ch in found:
                    print(f"{i:3}. {ch.get('name')}")
            else:
                print(t['not_found'])
        
        elif opt == '4':
            # Cambiar categoría
            print("\n" + "="*60)
            print(t['categories_title'])
            print("="*60)
            for i, cat in enumerate(cats_to_show, 1):
                print(f"{i:3}. {cat.get('title')}")
            
            choice = input("\n> ").strip().lower()
            new_cat = None
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(cats_to_show):
                    new_cat = cats_to_show[idx]
            except ValueError:
                for cat in cats_to_show:
                    if choice in cat.get('title', '').lower():
                        new_cat = cat
                        break
            
            if new_cat:
                selected_cat = new_cat
                print(f"\n{t['category']}{selected_cat.get('title')}")
                print(t['getting_channels'])
                all_channels = player.get_all_channels_from_category(selected_cat.get('id'))
                channels = player.filter_channels(all_channels)
                print(f"[+] {len(channels)}{t['channels_count']}")
            else:
                print(t['category_not_found'])
        
        elif opt == '5':
            break


if __name__ == "__main__":
    main()

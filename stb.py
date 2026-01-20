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
from datetime import datetime
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

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
        'opt_verify_channels': '5. Verificar canales',
        'opt_exit': '6. Salir',
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
        'verifying_channels': '[*] Verificando canales...',
        'channel_ok': '[OK]',
        'channel_fail': '[FAIL]',
        'channels_verified': '\n[+] Verificación completada',
        'working_channels': 'Canales funcionando',
        'broken_channels': 'Canales rotos',
        'save_working': '¿Guardar lista de canales funcionando? (s/n): ',
        # Batch checker
        'main_menu': 'MENÚ PRINCIPAL',
        'opt_single': '1. Verificar portal individual',
        'opt_batch': '2. Verificar lista de portales',
        'paste_list': 'Pega la lista (escribe END en una línea vacía para terminar):',
        'parsing': '[*] Parseando lista...',
        'found_portals': '[+] Encontrados {} portales',
        'checking': '[*] Verificando {}/{}...',
        'check_ok': '[OK]',
        'check_fail': '[FAIL]',
        'results_title': 'RESULTADOS',
        'working': 'FUNCIONANDO',
        'not_working': 'NO FUNCIONAN',
        'filter_country': 'Filtrar por país (ej: spain, germany) o ENTER para todos: ',
        'channels_in_country': ' canales en ',
        'no_channels_country': 'Sin canales en ese país',
        'expiry': 'Expira: ',
        'save_results': '¿Guardar resultados? (s/n): ',
        'saved_to': '[+] Guardado en: ',
        'no_portals': '[!] No se encontraron portales válidos',
        'select_working': 'Selecciona un portal para usar (número) o ENTER para salir: ',
        'opt_batch_folder': '3. Verificar todos los .txt de la carpeta',
        'opt_verify_country': '4. Verificar canales de un país',
        'scanning_folder': '[*] Buscando archivos .txt...',
        'found_txt_files': '[+] Encontrados {} archivos .txt',
        'no_txt_files': '[!] No se encontraron archivos .txt en la carpeta',
        'processing_file': '\n[*] Procesando: {}',
        'portals_in_file': '[+] {} portales en este archivo',
        'no_portals_in_file': '[-] Sin portales válidos',
        'total_portals': '[+] Total de portales encontrados: {}',
        'batch_complete': '\n[+] Verificación completada',
        'num_threads': 'Número de threads (1-20, por defecto 5): ',
        'using_threads': '[*] Usando {} threads',
        'progress': '[*] Progreso: {}/{} ({:.1f}%)',
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
        'opt_verify_channels': '5. Verify channels',
        'opt_exit': '6. Exit',
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
        'verifying_channels': '[*] Verifying channels...',
        'channel_ok': '[OK]',
        'channel_fail': '[FAIL]',
        'channels_verified': '\n[+] Verification complete',
        'working_channels': 'Working channels',
        'broken_channels': 'Broken channels',
        'save_working': 'Save list of working channels? (y/n): ',
        # Batch checker
        'main_menu': 'MAIN MENU',
        'opt_single': '1. Check single portal',
        'opt_batch': '2. Check portal list',
        'paste_list': 'Paste the list (type END on empty line to finish):',
        'parsing': '[*] Parsing list...',
        'found_portals': '[+] Found {} portals',
        'checking': '[*] Checking {}/{}...',
        'check_ok': '[OK]',
        'check_fail': '[FAIL]',
        'results_title': 'RESULTS',
        'working': 'WORKING',
        'not_working': 'NOT WORKING',
        'filter_country': 'Filter by country (e.g.: spain, germany) or ENTER for all: ',
        'channels_in_country': ' channels in ',
        'no_channels_country': 'No channels in that country',
        'expiry': 'Expires: ',
        'save_results': 'Save results? (y/n): ',
        'saved_to': '[+] Saved to: ',
        'no_portals': '[!] No valid portals found',
        'select_working': 'Select a portal to use (number) or ENTER to exit: ',
        'opt_batch_folder': '3. Check all .txt files in folder',
        'opt_verify_country': '4. Verify channels by country',
        'scanning_folder': '[*] Scanning for .txt files...',
        'found_txt_files': '[+] Found {} .txt files',
        'no_txt_files': '[!] No .txt files found in folder',
        'processing_file': '\n[*] Processing: {}',
        'portals_in_file': '[+] {} portals in this file',
        'no_portals_in_file': '[-] No valid portals',
        'total_portals': '[+] Total portals found: {}',
        'batch_complete': '\n[+] Check complete',
        'num_threads': 'Number of threads (1-20, default 5): ',
        'using_threads': '[*] Using {} threads',
        'progress': '[*] Progress: {}/{} ({:.1f}%)',
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

    def get_stream_url(self, cmd, debug=False):
        """Obtiene URL de streaming real"""
        if not cmd:
            if debug:
                print("[DEBUG] CMD vacío")
            return None
        
        # Primero intentar extraer URL directamente del CMD
        # Algunos servidores tienen el stream completo en el CMD
        if cmd.startswith('ffmpeg '):
            direct_url = cmd[7:].strip()
        elif cmd.startswith('ffrt '):
            direct_url = cmd[5:].strip()
        else:
            # Buscar URL en el CMD
            direct_url = None
            for part in cmd.split():
                if part.startswith('http'):
                    direct_url = part
                    break
        
        # Verificar si el CMD directo tiene stream ID válido
        has_valid_stream_in_cmd = False
        if direct_url and 'stream=' in direct_url:
            match = re.search(r'stream=([^&]+)', direct_url)
            if match and match.group(1):
                has_valid_stream_in_cmd = True
                if debug:
                    print(f"[DEBUG] CMD original tiene stream válido: {match.group(1)}")
            
        params = {
            'type': 'itv', 'action': 'create_link', 'cmd': cmd,
            'JsHttpRequest': '1-xml'
        }
        try:
            response = self.session.get(self.active_url, params=params, headers=self.headers, timeout=15, verify=False)
            data = response.json()
            
            if debug:
                print(f"[DEBUG] Response: {json.dumps(data, indent=2)[:500]}")
            
            if 'js' in data and 'cmd' in data['js']:
                stream_cmd = data['js']['cmd']
                
                if debug:
                    print(f"[DEBUG] Stream CMD: {stream_cmd[:200]}")
                
                # Si el cmd está vacío o es inválido
                if not stream_cmd or stream_cmd.strip() == '':
                    if debug:
                        print("[DEBUG] Stream CMD vacío, usando CMD original")
                    # Usar CMD original si estaba disponible
                    return direct_url if has_valid_stream_in_cmd else None
                
                # Extraer URL del stream
                if stream_cmd.startswith('ffmpeg '):
                    url = stream_cmd[7:].strip()
                elif stream_cmd.startswith('ffrt '):
                    url = stream_cmd[5:].strip()
                else:
                    # Buscar cualquier URL http en el comando
                    for part in stream_cmd.split():
                        if part.startswith('http'):
                            url = part
                            break
                    else:
                        url = stream_cmd.strip()
                
                # Verificar que la URL tenga un stream ID válido
                if url and 'stream=' in url:
                    # Verificar que stream= tenga un valor
                    match = re.search(r'stream=([^&]+)', url)
                    if match and match.group(1):
                        if debug:
                            print(f"[DEBUG] URL válida: {url[:100]}")
                        return url
                    else:
                        # Stream vacío en respuesta, usar CMD original si tiene stream
                        if debug:
                            print(f"[DEBUG] Stream= vacío en respuesta, usando CMD original")
                        return direct_url if has_valid_stream_in_cmd else None
                elif url and url.startswith('http'):
                    if debug:
                        print(f"[DEBUG] URL sin stream=: {url[:100]}")
                    return url
            else:
                if debug:
                    print("[DEBUG] No hay 'js' o 'cmd' en respuesta, usando CMD original")
                return direct_url if has_valid_stream_in_cmd else None
                    
        except Exception as e:
            if debug:
                print(f"[DEBUG] Exception: {str(e)}, usando CMD original")
            return direct_url if has_valid_stream_in_cmd else None
        
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

    def find_country_category(self, categories, country):
        """Busca categoría de un país con variantes de nombres"""
        country = country.lower().strip()
        
        # Diccionario de variantes para países comunes
        # Los patrones cortos (2-3 letras) usan regex con delimitadores
        country_aliases = {
            'spain': {
                'words': ['spain', 'españa', 'espana', 'spanish', 'espanol', 'español'],
                'codes': ['es', 'esp']  # Códigos cortos que necesitan delimitadores
            },
            'germany': {
                'words': ['germany', 'german', 'alemania', 'deutschland', 'deutsch'],
                'codes': ['de', 'ger', 'deu']
            },
            'france': {
                'words': ['france', 'french', 'francia', 'francais', 'français'],
                'codes': ['fr', 'fra']
            },
            'italy': {
                'words': ['italy', 'italian', 'italia', 'italiano'],
                'codes': ['it', 'ita']
            },
            'portugal': {
                'words': ['portugal', 'portuguese', 'portugues', 'português'],
                'codes': ['pt', 'por']
            },
            'uk': {
                'words': ['united kingdom', 'england', 'english', 'britain', 'british'],
                'codes': ['uk', 'gb', 'eng']
            },
            'usa': {
                'words': ['united states', 'america', 'american', 'estados unidos'],
                'codes': ['usa', 'us', 'eeuu']
            },
            'mexico': {
                'words': ['mexico', 'méxico', 'mexican', 'mexicano'],
                'codes': ['mx', 'mex']
            },
            'argentina': {
                'words': ['argentina', 'argentino'],
                'codes': ['ar', 'arg']
            },
            'brazil': {
                'words': ['brazil', 'brasil', 'brazilian', 'brasileiro'],
                'codes': ['br', 'bra']
            },
            'netherlands': {
                'words': ['netherlands', 'dutch', 'holland', 'holanda'],
                'codes': ['nl', 'ned']
            },
            'poland': {
                'words': ['poland', 'polish', 'polska', 'polaco'],
                'codes': ['pl', 'pol']
            },
            'russia': {
                'words': ['russia', 'russian', 'rusia'],
                'codes': ['ru', 'rus']
            },
            'turkey': {
                'words': ['turkey', 'turkish', 'turquia', 'türkiye'],
                'codes': ['tr', 'tur']
            },
            'arab': {
                'words': ['arab', 'arabic', 'arabe', 'árabe', 'middle east'],
                'codes': ['arb']
            },
            'latin': {
                'words': ['latin', 'latino', 'latina', 'latam', 'latinoamerica', 'latinoamérica'],
                'codes': ['lat']
            },
        }
        
        # Buscar qué variantes usar
        search_words = [country]  # Siempre incluir el término original
        search_codes = []
        
        for key, aliases in country_aliases.items():
            all_terms = aliases['words'] + aliases['codes']
            if country in all_terms or country == key:
                search_words = aliases['words']
                search_codes = aliases['codes']
                break
        
        # Buscar TODAS las categorías que coincidan
        found_categories = []
        
        for cat in categories:
            title = cat.get('title', '').lower()
            matched = False
            
            # Primero buscar palabras completas
            for word in search_words:
                if word in title:
                    matched = True
                    break
            
            # Luego buscar códigos con delimitadores (|ES|, (ES), [ES], -ES-, etc.)
            if not matched:
                for code in search_codes:
                    # Patrón que busca el código rodeado de caracteres no alfabéticos
                    pattern = r'(?:^|[^a-zA-Z])' + re.escape(code) + r'(?:[^a-zA-Z]|$)'
                    if re.search(pattern, title):
                        matched = True
                        break
            
            if matched:
                found_categories.append(cat)
        
        return found_categories if found_categories else None

    def count_channels_in_country(self, country):
        """Cuenta canales en todas las categorías de un país"""
        categories = self.get_categories()
        found_cats = self.find_country_category(categories, country)
        if found_cats:
            total_channels = 0
            cat_names = []
            for cat in found_cats:
                channels = self.get_all_channels_from_category(cat.get('id'))
                total_channels += len(self.filter_channels(channels))
                cat_names.append(cat.get('title'))
            return total_channels, f"{len(found_cats)} categorías"
        return 0, None

    def filter_channels(self, channels):
        """Filtra separadores y canales vacíos"""
        return [ch for ch in channels 
                if ch.get('cmd') and '===' not in ch.get('name', '') and '###' not in ch.get('name', '')]

    def get_expiry_date(self):
        """Obtiene fecha de expiración del servidor"""
        params = {
            'type': 'account_info', 'action': 'get_main_info',
            'JsHttpRequest': '1-xml'
        }
        try:
            response = self.session.get(self.active_url, params=params, headers=self.headers, timeout=15, verify=False)
            data = response.json()
            if 'js' in data:
                js = data['js']
                # Buscar fecha de expiración en diferentes campos
                expiry = js.get('phone') or js.get('expiry') or js.get('exp_date') or js.get('expire_billing_date')
                if expiry:
                    return expiry
        except:
            pass
        
        # Intentar desde el perfil
        try:
            profile = self.get_profile()
            if profile:
                expiry = profile.get('phone') or profile.get('expiry') or profile.get('exp_date')
                if expiry:
                    return expiry
        except:
            pass
        
        return None


def parse_portal_list(text):
    """Parsea diferentes formatos de listas de portales"""
    portals = []
    
    # Patrón MAC simple (sin prefijo)
    simple_mac_pattern = r'^([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})$'
    # Patrón MAC con prefijo
    mac_pattern = r'[Mm]a[cᴄ][➛➨:\s]+\s*([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})'
    # Patrón URL simple (con o sin /c/)
    simple_url_pattern = r'^(https?://[^\s]+)$'
    
    # Primero intentar formato simple: URL seguida de MACs
    lines = text.strip().split('\n')
    current_url = None
    simple_format_found = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Verificar si es una URL
        url_match = re.match(simple_url_pattern, line)
        if url_match and '://' in line:
            url = url_match.group(1).rstrip('/')
            # Asegurar que termina en /c
            if not url.endswith('/c'):
                if '/c/' in url:
                    url = url.split('/c/')[0] + '/c'
                else:
                    url = url + '/c'
            current_url = url
            continue
        
        # Verificar si es una MAC simple (solo la MAC en la línea)
        mac_match = re.match(simple_mac_pattern, line)
        if mac_match and current_url:
            mac = mac_match.group(1).upper().replace('-', ':')
            portals.append({
                'portal': current_url,
                'mac': mac,
                'expiry': None
            })
            simple_format_found = True
    
    # Si encontró portales con formato simple, retornar
    if simple_format_found and portals:
        # Eliminar duplicados
        seen = set()
        unique_portals = []
        for p in portals:
            key = (p['portal'], p['mac'])
            if key not in seen:
                seen.add(key)
                unique_portals.append(p)
        return unique_portals
    
    # Si no, intentar formato complejo (HIT INFO, etc.)
    portals = []
    
    # Dividir por bloques (cada HIT INFO o bloque Panel/Mac)
    blocks = re.split(r'(?:╭─➨\s*HIT INFO|MAC FINDER|www\.linuxsat)', text, flags=re.IGNORECASE)
    
    # También intentar dividir por líneas vacías múltiples si no hay bloques claros
    if len(blocks) <= 1:
        blocks = re.split(r'\n\s*\n\s*\n', text)
    
    # Si aún no hay bloques, procesar todo como un solo bloque
    if len(blocks) <= 1:
        blocks = [text]
    
    # Patrones de URL en orden de preferencia (Real primero, luego Panel, luego Host)
    url_patterns_ordered = [
        (r'[Rr]eal[➛➨:\s]+\s*(https?://[^\s]+)', 'real'),
        (r'[Pp]a[nɴ]el[➛➨:\s]+\s*(https?://[^\s]+)', 'panel'),
        (r'[Hh]ost[➛➨:\s]+\s*(https?://[^\s]+)', 'host'),
        (r'[Pp]ᴀɴᴇʟ[➛➨:\s]+\s*(https?://[^\s]+)', 'panel2'),
    ]
    
    expiry_patterns = [
        r'[Ee]xp(?:ira|iry|ir[yʏ]|)[➛➨:\s]+\s*([A-Za-z]+ \d+, \d{4}[^│\n]*)',
        r'[Ee]xᴘɪʀᴀ[➛➨:\s]+\s*([A-Za-z]+ \d+, \d{4}[^│\n]*)',
        r'[Ee]xp[➛➨:\s]+\s*(\d{2}-\d{2}-\d{4}[^│\n]*)',
    ]
    
    for block in blocks:
        if not block.strip():
            continue
        
        # Buscar MAC en este bloque
        mac_match = re.search(mac_pattern, block)
        if not mac_match:
            continue
        
        mac = mac_match.group(1).upper().replace('-', ':')
        
        # Buscar URL (preferir Real > Panel > Host)
        url = None
        for pattern, url_type in url_patterns_ordered:
            url_match = re.search(pattern, block)
            if url_match:
                url = url_match.group(1)
                break
        
        # Si no encontró con patrones específicos, buscar cualquier URL con /c/
        if not url:
            generic_url = re.search(r'(https?://[^\s]+/c/?)', block)
            if generic_url:
                url = generic_url.group(1)
        
        if not url:
            continue
        
        # Limpiar URL
        url = url.rstrip('/')
        # Remover trailing characters no deseados
        url = re.sub(r'[,\s]+$', '', url)
        
        if not url.endswith('/c'):
            if '/c/' in url:
                url = url.split('/c/')[0] + '/c'
            else:
                url = url + '/c'
        
        # Buscar fecha de expiración
        expiry = None
        for pattern in expiry_patterns:
            exp_match = re.search(pattern, block)
            if exp_match:
                expiry = exp_match.group(1).strip()
                # Limpiar días al final
                expiry = re.sub(r'\s+\d+\s*[Dd]ays.*$', '', expiry).strip()
                break
        
        portals.append({
            'portal': url,
            'mac': mac,
            'expiry': expiry
        })
    
    # Si no encontró nada con bloques, intentar método línea por línea
    if not portals:
        lines = text.split('\n')
        current_urls = {}  # Guardar todas las URLs encontradas
        current_mac = None
        current_expiry = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Buscar URLs por tipo
            for pattern, url_type in url_patterns_ordered:
                match = re.search(pattern, line)
                if match:
                    current_urls[url_type] = match.group(1)
            
            # Buscar MAC
            mac_match = re.search(mac_pattern, line)
            if mac_match:
                # Si ya teníamos un MAC, guardar el portal anterior
                if current_mac and current_urls:
                    # Preferir: real > panel > host
                    url = current_urls.get('real') or current_urls.get('panel') or current_urls.get('panel2') or current_urls.get('host')
                    if url:
                        url = url.rstrip('/')
                        if not url.endswith('/c'):
                            url = url + '/c' if '/c' not in url else url.split('/c')[0] + '/c'
                        portals.append({
                            'portal': url,
                            'mac': current_mac,
                            'expiry': current_expiry
                        })
                
                current_mac = mac_match.group(1).upper().replace('-', ':')
                current_urls = {}  # Reset URLs for new entry
                current_expiry = None
            
            # Buscar expiración
            for pattern in expiry_patterns:
                exp_match = re.search(pattern, line)
                if exp_match:
                    current_expiry = re.sub(r'\s+\d+\s*[Dd]ays.*$', '', exp_match.group(1)).strip()
                    break
        
        # Agregar el último
        if current_mac and current_urls:
            url = current_urls.get('real') or current_urls.get('panel') or current_urls.get('panel2') or current_urls.get('host')
            if url:
                url = url.rstrip('/')
                if not url.endswith('/c'):
                    url = url + '/c' if '/c' not in url else url.split('/c')[0] + '/c'
                portals.append({
                    'portal': url,
                    'mac': current_mac,
                    'expiry': current_expiry
                })
    
    # Eliminar duplicados
    seen = set()
    unique_portals = []
    for p in portals:
        key = (p['portal'], p['mac'])
        if key not in seen:
            seen.add(key)
            unique_portals.append(p)
    
    return unique_portals


# Lock para impresión thread-safe
print_lock = threading.Lock()

# Diccionario de semáforos por servidor (máx 3 conexiones simultáneas por servidor)
server_semaphores = {}
server_semaphores_lock = threading.Lock()

def get_server_semaphore(portal_url, max_per_server=3):
    """Obtiene o crea un semáforo para limitar conexiones por servidor"""
    from urllib.parse import urlparse
    server = urlparse(portal_url).netloc
    
    with server_semaphores_lock:
        if server not in server_semaphores:
            server_semaphores[server] = threading.Semaphore(max_per_server)
        return server_semaphores[server]

def check_single_portal(portal_info, country_filter, t, retry=True):
    """Verifica un portal individual (thread-safe)"""
    portal = portal_info['portal']
    mac = portal_info['mac']
    expiry = portal_info.get('expiry')
    source = portal_info.get('source_file', '')
    
    # Limitar conexiones por servidor
    semaphore = get_server_semaphore(portal)
    
    with semaphore:
        # Pequeño delay aleatorio para evitar saturar
        time.sleep(random.uniform(0.1, 0.5))
        
        try:
            player = STBPlayer(portal, mac)
            if player.connect():
                profile = player.get_profile()
                user_name = profile.get('name', 'N/A') if profile else 'N/A'
                
                if not expiry:
                    expiry = player.get_expiry_date()
                
                result = {
                    'portal': portal,
                    'mac': mac,
                    'expiry': expiry,
                    'user': user_name,
                    'player': player,
                    'source_file': source,
                    'success': True
                }
                
                if country_filter:
                    count, cat_name = player.count_channels_in_country(country_filter)
                    result['country_channels'] = count
                    result['country_name'] = cat_name
                    
                    if count > 0:
                        with print_lock:
                            print(f"  {t['check_ok']} {portal} - {mac[:11]}... - {user_name} - {count} ch")
                        return result
                    else:
                        result['success'] = False
                        with print_lock:
                            print(f"  {t['check_fail']} {portal} - {mac[:11]}... - {t['no_channels_country']}")
                        return result
                else:
                    categories = player.get_categories()
                    result['categories'] = len(categories)
                    with print_lock:
                        print(f"  {t['check_ok']} {portal} - {mac[:11]}... - {user_name} - {len(categories)} cats")
                    return result
            else:
                # Si falla conexión, reintentar una vez
                if retry:
                    time.sleep(1)
                    return check_single_portal(portal_info, country_filter, t, retry=False)
                    
                with print_lock:
                    print(f"  {t['check_fail']} {portal} - {mac[:11]}... - {t['error_connect']}")
                return {
                    'portal': portal,
                    'mac': mac,
                    'expiry': expiry,
                    'source_file': source,
                    'error': 'Connection failed',
                    'success': False
                }
        except Exception as e:
            # Reintentar una vez en caso de error
            if retry:
                time.sleep(1)
                return check_single_portal(portal_info, country_filter, t, retry=False)
                
            with print_lock:
                print(f"  {t['check_fail']} {portal} - {mac[:11]}... - {str(e)[:30]}")
            return {
                'portal': portal,
                'mac': mac,
                'expiry': expiry,
                'source_file': source,
                'error': str(e)[:50],
                'success': False
            }


def get_num_threads(t):
    """Pide al usuario el número de threads"""
    threads_input = input(t['num_threads']).strip()
    try:
        num_threads = int(threads_input)
        if num_threads < 1:
            num_threads = 1
        elif num_threads > 20:
            num_threads = 20  # Máximo 20 para evitar bloqueos
    except:
        num_threads = 5
    print(t['using_threads'].format(num_threads))
    return num_threads


def batch_check(lang='es'):
    """Verifica una lista de portales"""
    t = LANG[lang]
    
    print("\n" + "="*60)
    print(t['paste_list'])
    print("="*60)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    text = '\n'.join(lines)
    print(f"\n{t['parsing']}")
    
    portals = parse_portal_list(text)
    
    if not portals:
        print(t['no_portals'])
        return None
    
    print(t['found_portals'].format(len(portals)))
    
    # Preguntar por filtro de país
    country_filter = input(f"\n{t['filter_country']}").strip().lower()
    
    # Preguntar número de threads
    num_threads = get_num_threads(t)
    
    working = []
    not_working = []
    completed = [0]  # Usar lista para poder modificar en closure
    total = len(portals)
    
    print(f"\n[*] Verificando {total} portales...")
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(check_single_portal, p, country_filter, t): p for p in portals}
        
        for future in as_completed(futures):
            result = future.result()
            completed[0] += 1
            
            if result.get('success'):
                working.append(result)
            else:
                not_working.append(result)
            
            # Mostrar progreso cada 10 verificaciones
            if completed[0] % 10 == 0 or completed[0] == total:
                with print_lock:
                    print(t['progress'].format(completed[0], total, (completed[0]/total)*100))
    
    # Mostrar resultados
    print("\n" + "="*60)
    print(f"  {t['results_title']}")
    print("="*60)
    
    print(f"\n[+] {t['working']}: {len(working)}")
    for i, w in enumerate(working, 1):
        exp_str = f" | {t['expiry']}{w['expiry']}" if w.get('expiry') else ""
        country_str = f" | {w.get('country_channels', 0)} ch {w.get('country_name', '')}" if country_filter else ""
        print(f"  {i:2}. {w['portal']}")
        print(f"      MAC: {w['mac']} | User: {w.get('user', 'N/A')}{exp_str}{country_str}")
    
    print(f"\n[-] {t['not_working']}: {len(not_working)}")
    for w in not_working:
        print(f"  - {w['portal']} | {w['mac']}")
    
    # Guardar resultados
    save = input(f"\n{t['save_results']}").strip().lower()
    if save in ['s', 'y', 'si', 'yes']:
        filename = f"stb_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"STB Check Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(f"WORKING ({len(working)}):\n")
            for w in working:
                f.write(f"Portal: {w['portal']}\n")
                f.write(f"MAC: {w['mac']}\n")
                f.write(f"User: {w.get('user', 'N/A')}\n")
                if w.get('expiry'):
                    f.write(f"Expiry: {w['expiry']}\n")
                if country_filter and w.get('country_channels'):
                    f.write(f"Channels in {w.get('country_name', country_filter)}: {w['country_channels']}\n")
                f.write("\n")
            
            f.write(f"\nNOT WORKING ({len(not_working)}):\n")
            for w in not_working:
                f.write(f"Portal: {w['portal']} | MAC: {w['mac']}\n")
        
        print(f"{t['saved_to']}{filename}")
    
    # Opción para usar un portal que funciona
    if working:
        choice = input(f"\n{t['select_working']}").strip()
        if choice:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(working):
                    return working[idx]
            except:
                pass
    
    return None


def batch_check_folder(lang='es'):
    """Verifica todos los archivos .txt de la carpeta actual"""
    t = LANG[lang]
    
    print("\n" + "="*60)
    print(t['scanning_folder'])
    print("="*60)
    
    # Buscar en la subcarpeta 'stb' del directorio de trabajo
    script_dir = os.path.join(os.getcwd(), 'stb')
    
    if not os.path.exists(script_dir):
        print(f"[!] No existe la carpeta: {script_dir}")
        return None
    
    print(f"[*] Carpeta: {script_dir}")
    
    # Buscar todos los .txt
    txt_files = [f for f in os.listdir(script_dir) 
                 if f.endswith('.txt') and os.path.isfile(os.path.join(script_dir, f))]
    
    if not txt_files:
        print(t['no_txt_files'])
        return None
    
    print(t['found_txt_files'].format(len(txt_files)))
    for f in txt_files:
        print(f"  - {f}")
    
    # Parsear todos los archivos
    all_portals = []
    
    for txt_file in txt_files:
        filepath = os.path.join(script_dir, txt_file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            portals = parse_portal_list(content)
            
            if portals:
                print(t['processing_file'].format(txt_file))
                print(t['portals_in_file'].format(len(portals)))
                # Añadir origen del archivo
                for p in portals:
                    p['source_file'] = txt_file
                all_portals.extend(portals)
            else:
                print(t['processing_file'].format(txt_file))
                print(t['no_portals_in_file'])
        except Exception as e:
            print(f"[!] Error leyendo {txt_file}: {e}")
    
    if not all_portals:
        print(t['no_portals'])
        return None
    
    print(f"\n{t['total_portals'].format(len(all_portals))}")
    
    # Preguntar por filtro de país
    country_filter = input(f"\n{t['filter_country']}").strip().lower()
    
    # Preguntar número de threads
    num_threads = get_num_threads(t)
    
    working = []
    not_working = []
    completed = [0]
    total = len(all_portals)
    
    print(f"\n[*] Verificando {total} portales...")
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(check_single_portal, p, country_filter, t): p for p in all_portals}
        
        for future in as_completed(futures):
            result = future.result()
            completed[0] += 1
            
            if result.get('success'):
                working.append(result)
            else:
                not_working.append(result)
            
            # Mostrar progreso cada 10 verificaciones
            if completed[0] % 10 == 0 or completed[0] == total:
                with print_lock:
                    print(t['progress'].format(completed[0], total, (completed[0]/total)*100))
    
    print(t['batch_complete'])
    
    # Mostrar resultados
    print("\n" + "="*60)
    print(f"  {t['results_title']}")
    print("="*60)
    
    print(f"\n[+] {t['working']}: {len(working)}")
    for i, w in enumerate(working, 1):
        exp_str = f" | {t['expiry']}{w['expiry']}" if w.get('expiry') else ""
        country_str = f" | {w.get('country_channels', 0)} ch {w.get('country_name', '')}" if country_filter else ""
        print(f"  {i:2}. {w['portal']}")
        print(f"      MAC: {w['mac']} | User: {w.get('user', 'N/A')}{exp_str}{country_str}")
        print(f"      Archivo: {w.get('source_file', 'N/A')}")
    
    print(f"\n[-] {t['not_working']}: {len(not_working)}")
    for w in not_working:
        print(f"  - {w['portal']} | {w['mac']} | {w.get('source_file', 'N/A')}")
    
    # Guardar resultados
    save = input(f"\n{t['save_results']}").strip().lower()
    if save in ['s', 'y', 'si', 'yes']:
        filename = f"stb_folder_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"STB Folder Check Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Archivos procesados: {len(txt_files)}\n")
            f.write("="*60 + "\n\n")
            f.write(f"WORKING ({len(working)}):\n")
            for w in working:
                f.write(f"Portal: {w['portal']}\n")
                f.write(f"MAC: {w['mac']}\n")
                f.write(f"User: {w.get('user', 'N/A')}\n")
                f.write(f"Source: {w.get('source_file', 'N/A')}\n")
                if w.get('expiry'):
                    f.write(f"Expiry: {w['expiry']}\n")
                if country_filter and w.get('country_channels'):
                    f.write(f"Channels in {w.get('country_name', country_filter)}: {w['country_channels']}\n")
                f.write("\n")
            
            f.write(f"\nNOT WORKING ({len(not_working)}):\n")
            for w in not_working:
                f.write(f"Portal: {w['portal']} | MAC: {w['mac']} | Source: {w.get('source_file', 'N/A')}\n")
        
        print(f"{t['saved_to']}{filename}")
    
    # Opción para usar un portal que funciona
    if working:
        choice = input(f"\n{t['select_working']}").strip()
        if choice:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(working):
                    return working[idx]
            except:
                pass
    
    return None


def verify_country_channels(lang='es'):
    """Verifica canales de un país específico"""
    t = LANG[lang]
    
    print("\n" + "="*60)
    print("  Verificar Canales por País" if lang == 'es' else "  Verify Channels by Country")
    print("="*60)
    
    # Pedir país
    country = input("\nPaís a verificar (ej: spain, germany): ").strip().lower()
    if not country:
        print("[!] País requerido")
        return
    
    # Pedir portal y MAC
    portal = input(f"\n{t['enter_url']}").strip()
    mac = input(t['enter_mac']).strip()
    
    if not portal or not mac:
        print(t['error_empty'])
        return
    
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$', mac):
        print(t['error_mac'])
        return
    
    # Conectar
    print(f"\n{t['connecting']}")
    player = STBPlayer(portal, mac)
    
    if not player.connect():
        print(t['error_connect'])
        return
    
    print(t['connected'])
    
    # Buscar categorías del país
    categories = player.get_categories()
    country_cats = player.find_country_category(categories, country)
    
    if not country_cats:
        print(f"[!] No se encontraron categorías para {country}")
        return
    
    print(f"\n[+] Encontradas {len(country_cats)} categorías de {country}:")
    for cat in country_cats:
        print(f"  - {cat.get('title')}")
    
    # Confirmar
    confirm = input("\n¿Continuar con la verificación? (s/n): ").strip().lower()
    if confirm not in ['s', 'y', 'si', 'yes']:
        return
    
    # Verificar canales de todas las categorías
    all_working = []
    all_broken = []
    total_channels = 0
    
    for cat in country_cats:
        print(f"\n{'='*60}")
        print(f"Verificando: {cat.get('title')}")
        print("="*60)
        
        channels = player.get_all_channels_from_category(cat.get('id'))
        channels = player.filter_channels(channels)
        total_channels += len(channels)
        
        print(f"[*] {len(channels)} canales en esta categoría\n")
        
        for i, ch in enumerate(channels, 1):
            name = ch.get('name', 'Sin nombre')
            cmd = ch.get('cmd')
            
            url = player.get_stream_url(cmd)
            
            if url:
                print(f"  {t['channel_ok']} {name}")
                all_working.append({
                    'name': name,
                    'cmd': cmd,
                    'url': url,
                    'category': cat.get('title')
                })
            else:
                print(f"  {t['channel_fail']} {name}")
                all_broken.append({
                    'name': name,
                    'cmd': cmd,
                    'category': cat.get('title')
                })
            
            # Progreso cada 20
            if i % 20 == 0:
                print(f"\n  {t['progress'].format(i, len(channels), (i/len(channels))*100)}\n")
    
    # Resultados finales
    print("\n" + "="*60)
    print(f"  {t['results_title']} - {country.upper()}")
    print("="*60)
    print(f"\nTotal canales verificados: {total_channels}")
    print(f"[+] {t['working_channels']}: {len(all_working)} ({(len(all_working)/total_channels*100):.1f}%)")
    print(f"[-] {t['broken_channels']}: {len(all_broken)} ({(len(all_broken)/total_channels*100):.1f}%)")
    
    # Guardar
    save = input(f"\n{t['save_working']}").strip().lower()
    if save in ['s', 'y', 'si', 'yes']:
        filename = f"channels_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Working Channels - {country.upper()}\n")
            f.write(f"Portal: {portal}\n")
            f.write(f"MAC: {mac}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(f"WORKING ({len(all_working)}):\n\n")
            
            current_cat = None
            for i, ch in enumerate(all_working, 1):
                if ch['category'] != current_cat:
                    current_cat = ch['category']
                    f.write(f"\n## {current_cat} ##\n")
                f.write(f"{i:3}. {ch['name']}\n")
            
            f.write(f"\n\nBROKEN ({len(all_broken)}):\n\n")
            current_cat = None
            for i, ch in enumerate(all_broken, 1):
                if ch['category'] != current_cat:
                    current_cat = ch['category']
                    f.write(f"\n## {current_cat} ##\n")
                f.write(f"{i:3}. {ch['name']}\n")
        
        print(f"{t['saved_to']}{filename}")


def single_portal_mode(portal, mac, lang='es'):
    """Modo de portal individual"""
    t = LANG[lang]
    
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
        print(t['opt_verify_channels'])
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
                    print(f"[*] Obteniendo stream...")
                    url = player.get_stream_url(ch.get('cmd'), debug=True)
                    if url:
                        player.play_vlc(url, ch.get('name'), lang)
                    else:
                        print(t['no_url'])
                        print(f"[DEBUG] CMD: {ch.get('cmd')}")
                else:
                    print(t['invalid_num'])
            except Exception as e:
                print(t['enter_num'])
                print(f"[DEBUG] Error: {e}")
        
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
            # Verificar canales
            print(f"\n{t['verifying_channels']}")
            print(f"[*] Total: {len(channels)} canales\n")
            
            working_ch = []
            broken_ch = []
            
            for i, ch in enumerate(channels, 1):
                name = ch.get('name', 'Sin nombre')
                cmd = ch.get('cmd')
                
                # Intentar obtener URL
                url = player.get_stream_url(cmd)
                
                if url:
                    print(f"  {t['channel_ok']} {i:3}. {name}")
                    working_ch.append({'name': name, 'cmd': cmd, 'url': url})
                else:
                    print(f"  {t['channel_fail']} {i:3}. {name}")
                    broken_ch.append({'name': name, 'cmd': cmd})
                
                # Mostrar progreso cada 20 canales
                if i % 20 == 0:
                    print(f"\n  {t['progress'].format(i, len(channels), (i/len(channels))*100)}\n")
            
            # Resultados
            print(t['channels_verified'])
            print(f"\n[+] {t['working_channels']}: {len(working_ch)}")
            print(f"[-] {t['broken_channels']}: {len(broken_ch)}")
            
            # Guardar resultados
            save = input(f"\n{t['save_working']}").strip().lower()
            if save in ['s', 'y', 'si', 'yes']:
                cat_name = selected_cat.get('title', 'unknown').replace(' ', '_').replace('|', '')
                filename = f"channels_{cat_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Working Channels - {selected_cat.get('title')}\n")
                    f.write(f"Portal: {player.portal_url}\n")
                    f.write(f"MAC: {player.mac}\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*60 + "\n\n")
                    f.write(f"WORKING ({len(working_ch)}):\n")
                    for i, ch in enumerate(working_ch, 1):
                        f.write(f"{i:3}. {ch['name']}\n")
                    
                    f.write(f"\n\nBROKEN ({len(broken_ch)}):\n")
                    for i, ch in enumerate(broken_ch, 1):
                        f.write(f"{i:3}. {ch['name']}\n")
                
                print(f"{t['saved_to']}{filename}")
        
        elif opt == '6':
            break


def main():
    print("="*60)
    print("  Language / Idioma")
    print("="*60)
    print("1. English")
    print("2. Español")
    lang_choice = input("\n> ").strip()
    lang = 'en' if lang_choice == '1' else 'es'
    t = LANG[lang]
    
    while True:
        print("\n" + "="*60)
        print(f"  {t['title']}")
        print("="*60)
        print(t['opt_single'])
        print(t['opt_batch'])
        print(t['opt_batch_folder'])
        print(t['opt_verify_country'])
        print("5. Salir" if lang == 'es' else "5. Exit")
        
        mode = input(f"\n{t['option']}").strip()
        
        if mode == '1':
            # Modo individual
            portal = input(f"\n{t['enter_url']}").strip()
            mac = input(t['enter_mac']).strip()
            
            if not portal or not mac:
                print(t['error_empty'])
                continue
            
            if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$', mac):
                print(t['error_mac'])
                continue
            
            single_portal_mode(portal, mac, lang)
        
        elif mode == '2':
            # Modo batch
            result = batch_check(lang)
            if result and result.get('player'):
                # Usar el portal seleccionado
                single_portal_mode(result['portal'], result['mac'], lang)
        
        elif mode == '3':
            # Modo batch desde carpeta
            result = batch_check_folder(lang)
            if result and result.get('player'):
                single_portal_mode(result['portal'], result['mac'], lang)
        
        elif mode == '4':
            # Verificar canales por país
            verify_country_channels(lang)
        
        elif mode == '5':
            break


if __name__ == "__main__":
    main()

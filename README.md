# STB Checker & Player

A powerful Python tool to check, verify, and play IPTV channels from STB (Stalker Portal) servers. Connect to MAC-based IPTV portals, batch verify multiple accounts, check channel availability, and stream directly to VLC.

## ✨ Features

### Portal Management
- Connect to Stalker/Ministra portals using MAC address authentication
- **Batch verification** of portal lists (paste format or from files)
- **Multi-threaded checking** (1-20 threads) for fast verification
- **Automatic expiry date detection** from server
- Support for multiple input formats (MAC FINDER PRO, simple URL+MAC lists)

### Channel Operations
- Browse all available channel categories (countries/genres)
- **Verify all channels** in a category to find broken streams
- **Verify channels by country** across all categories
- Search channels by name
- Stream channels directly to VLC media player
- **Smart URL fallback** - uses original CMD when server returns empty streams

### Country Filtering
- **Advanced country aliases** - search "spain" and find "ES", "España", "Español", etc.
- Filter portals by country with channel count
- Support for 16+ country variations (Spain, Germany, France, Italy, UK, USA, Mexico, etc.)

### Batch Operations
- Verify portal lists (manual paste with END marker)
- **Verify all .txt files** in `/stb` folder automatically
- Save results with expiry dates and channel counts
- Select working portal to use directly from results

### Interface
- Bilingual interface (English/Spanish)
- Progress indicators for long operations
- Thread-safe concurrent operations
- Debug mode for troubleshooting

## 📋 Requirements

- Python 3.6+
- VLC Media Player
- Required libraries:
  ```bash
  pip install requests
  ```

## 🚀 Installation

```bash
git clone <repository-url>
cd stbChecker
pip install requests
```

## 📖 Usage

```bash
python stb.py
```

### Main Menu Options

| Option | Description |
|--------|-------------|
| **1** | **Single Portal Mode** - Enter URL & MAC to browse/play channels |
| **2** | **Batch Verification** - Paste portal list to check multiple accounts |
| **3** | **Folder Verification** - Check all .txt files in `/stb` folder |
| **4** | **Verify Country Channels** - Check all channels for a specific country |
| **5** | Exit |

### Single Portal Mode

Once connected, you can:

| Option | Description |
|--------|-------------|
| 1 | View channel list |
| 2 | Play channel in VLC |
| 3 | Search channels |
| 4 | Change category |
| **5** | **Verify all channels** - Find broken/working streams |
| 6 | Exit |

## 🔧 Advanced Features

### Multi-threaded Verification

When using batch verification, you'll be asked:
```
Number of threads (1-20, default 5):
```
- **Recommended**: 5-10 threads for balanced speed/reliability
- **Maximum**: 20 threads (automatic rate limiting per server)
- **Features**: Automatic retry on failure, random delays to avoid blocking

### Input Format Support

**MAC FINDER PRO Format:**
```
=== HIT INFO ===
URL: http://portal.com/c
Real URL: http://real-portal.com/c
MAC: 00:1A:79:00:00:00
Expiry: 2026-12-31 23:59:59
```

**Simple Format:**
```
http://portal.com/c
00:1A:79:00:00:00
00:1A:79:00:00:01
00:1A:79:00:00:02
```

**End with:** Type `END` on empty line

### Country Aliases

The tool recognizes multiple variations:

| Country | Aliases |
|---------|---------|
| Spain | spain, españa, espana, spanish, es, esp, español |
| Germany | germany, german, alemania, deutschland, de, ger, deu, deutsch |
| France | france, french, francia, fr, fra, français |
| Italy | italy, italian, italia, it, ita, italiano |
| Portugal | portugal, portuguese, portugues, pt, por, português |
| UK | united kingdom, uk, england, english, gb, eng, britain |
| USA | united states, usa, us, america, american, eeuu |

*...and more for Mexico, Argentina, Brazil, Netherlands, Poland, Russia, Turkey, Arab, Latin*

### File Organization

For batch folder verification, organize your files:
```
stbChecker/
├── stb.py
├── stb/
│   ├── portal1.txt
│   ├── portal2.txt
│   └── portal3.txt
```

### Output Files

**Portal Verification Results:**
```
stb_results_YYYYMMDD_HHMMSS.txt
stb_folder_results_YYYYMMDD_HHMMSS.txt
```

**Channel Verification Results:**
```
channels_spain_YYYYMMDD_HHMMSS.txt
channels_|ES|_DEPORTES_YYYYMMDD_HHMMSS.txt
```

## 🎯 Example Workflows

### Quick Single Portal Check
1. Run `python stb.py`
2. Select language
3. Choose option **1** (Single Portal)
4. Enter portal URL and MAC
5. Browse categories and play channels

### Verify Portal List
1. Run `python stb.py`
2. Choose option **2** (Batch Verification)
3. Paste your portal list
4. Type `END` on empty line
5. Enter country filter (e.g., "spain") or press ENTER for all
6. Enter thread count (default 5)
7. Review results and save to file

### Check All Portals from Files
1. Place .txt files with portals in `/stb` folder
2. Run `python stb.py`
3. Choose option **3** (Folder Verification)
4. Enter country filter
5. Enter thread count
6. Results show source file for each portal

### Verify Country Channels
1. Run `python stb.py`
2. Choose option **4** (Verify Country Channels)
3. Enter country (e.g., "spain")
4. Enter portal URL and MAC
5. Tool finds all Spain categories automatically
6. Verifies all channels and shows working percentage
7. Save list of working channels

## 🐛 Troubleshooting

### "No se pudo obtener URL" but verification showed OK

This happens when the server returns empty `stream=` parameter. The tool now automatically falls back to the original CMD URL. Enable debug output to see details.

### Too many connections failing with high thread count

Reduce threads to 5-10. The tool limits 3 concurrent connections per server, but some servers may still rate-limit.

### VLC not opening

Check VLC path in `stb.py`:
```python
VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
```

Adjust for your installation path (Linux: `/usr/bin/vlc`, macOS: `/Applications/VLC.app/Contents/MacOS/VLC`)

## ⚙️ Configuration

Edit these variables in `stb.py`:

```python
# VLC installation path
VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

# Thread limits (in get_num_threads function)
max_threads = 20  # Maximum allowed
default_threads = 5  # Default value

# Server connection limits (in get_server_semaphore)
max_per_server = 3  # Max concurrent connections per server
```

## Note

This tool is for educational and testing purposes only. Ensure you have proper authorization to access any portals you connect to. Respect service provider terms and conditions.

---

# STB Checker & Player (Español)

Herramienta avanzada en Python para verificar y reproducir canales IPTV de servidores STB (Stalker Portal). Verifica múltiples portales en lote, comprueba disponibilidad de canales y reproduce en VLC.

## ✨ Características

### Gestión de Portales
- Conexión a portales Stalker/Ministra usando autenticación MAC
- **Verificación por lotes** de listas de portales
- **Verificación multi-hilo** (1-20 hilos) para rapidez
- **Detección automática de fecha de expiración**
- Soporte para múltiples formatos de entrada

### Operaciones con Canales
- Navegación por categorías (países/géneros)
- **Verificar todos los canales** de una categoría
- **Verificar canales por país** en todas las categorías
- Búsqueda de canales por nombre
- Reproducción directa en VLC
- **Respaldo inteligente de URL** cuando el servidor falla

### Filtrado por País
- **Sistema de alias avanzado** - busca "spain" y encuentra "ES", "España", "Español"
- Filtrar portales por país con conteo de canales
- Soporte para 16+ variaciones de países

### Operaciones por Lotes
- Verificar listas de portales (pegado manual)
- **Verificar todos los .txt** en carpeta `/stb` automáticamente
- Guardar resultados con fechas y conteos
- Seleccionar portal funcionando directamente

## 📋 Requisitos

- Python 3.6+
- VLC Media Player
- Librerías:
  ```bash
  pip install requests
  ```

## 🚀 Instalación

```bash
git clone <repository-url>
cd stbChecker
pip install requests
```

## 📖 Uso

```bash
python stb.py
```

### Menú Principal

| Opción | Descripción |
|--------|-------------|
| **1** | **Portal Individual** - Introducir URL y MAC para navegar |
| **2** | **Verificación por Lotes** - Pegar lista de portales |
| **3** | **Verificar Carpeta** - Verificar todos los .txt de `/stb` |
| **4** | **Verificar Canales por País** - Verificar canales de un país |
| **5** | Salir |

### Modo Portal Individual

Una vez conectado:

| Opción | Descripción |
|--------|-------------|
| 1 | Ver lista de canales |
| 2 | Reproducir canal en VLC |
| 3 | Buscar canales |
| 4 | Cambiar categoría |
| **5** | **Verificar canales** - Encontrar rotos/funcionando |
| 6 | Salir |

## 🔧 Características Avanzadas

### Verificación Multi-hilo

Al usar verificación por lotes:
```
Número de threads (1-20, por defecto 5):
```
- **Recomendado**: 5-10 hilos para equilibrio velocidad/fiabilidad
- **Máximo**: 20 hilos (limitación automática por servidor)

### Formatos Soportados

**Formato MAC FINDER PRO:**
```
=== HIT INFO ===
URL: http://portal.com/c
Real URL: http://real-portal.com/c
MAC: 00:1A:79:00:00:00
Expiry: 2026-12-31 23:59:59
```

**Formato Simple:**
```
http://portal.com/c
00:1A:79:00:00:00
00:1A:79:00:00:01
```

**Finalizar con:** Escribe `END` en línea vacía

### Alias de Países

| País | Alias reconocidos |
|------|-------------------|
| España | spain, españa, espana, spanish, es, esp, español |
| Alemania | germany, german, alemania, deutschland, de, ger, deu |
| Francia | france, french, francia, fr, fra, français |
| Italia | italy, italian, italia, it, ita, italiano |

*...y más para Portugal, UK, USA, México, Argentina, Brasil, etc.*

### Archivos de Salida

**Resultados de Portales:**
```
stb_results_YYYYMMDD_HHMMSS.txt
stb_folder_results_YYYYMMDD_HHMMSS.txt
```

**Resultados de Canales:**
```
channels_spain_YYYYMMDD_HHMMSS.txt
channels_|ES|_DEPORTES_YYYYMMDD_HHMMSS.txt
```

## 🎯 Flujos de Trabajo

### Verificar Portal Individual
1. Ejecutar `python stb.py`
2. Opción **1** (Portal Individual)
3. Introducir URL y MAC
4. Navegar y reproducir

### Verificar Lista de Portales
1. Ejecutar `python stb.py`
2. Opción **2** (Verificación por Lotes)
3. Pegar lista de portales
4. Escribir `END`
5. Filtrar por país (ej: "spain") o ENTER para todos
6. Elegir número de hilos (defecto 5)
7. Guardar resultados

### Verificar Carpeta Completa
1. Colocar archivos .txt en carpeta `/stb`
2. Ejecutar `python stb.py`
3. Opción **3** (Verificar Carpeta)
4. Filtrar por país
5. Elegir hilos
6. Ver origen de cada portal

### Verificar Canales por País
1. Ejecutar `python stb.py`
2. Opción **4** (Verificar Canales por País)
3. Introducir país (ej: "spain")
4. Introducir portal y MAC
5. Verifica automáticamente todas las categorías
6. Muestra porcentaje de canales funcionando
7. Guardar lista

## 🐛 Solución de Problemas

### "No se pudo obtener URL" pero verificación mostró OK

El servidor devuelve `stream=` vacío. La herramienta ahora usa automáticamente la URL original del CMD.

### Muchas conexiones fallan con muchos hilos

Reducir a 5-10 hilos. Algunos servidores limitan conexiones.

### VLC no abre

Verificar ruta en `stb.py`:
```python
VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
```

##  Nota

Esta herramienta es solo para fines educativos y de prueba. Asegúrate de tener autorización adecuada para acceder a cualquier portal. Respeta los términos y condiciones del proveedor.



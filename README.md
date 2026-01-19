# STB Checker & Player

A Python tool to check and play IPTV channels from STB (Stalker Portal) servers. Connect to MAC-based IPTV portals, browse channel categories by country, and stream directly to VLC.

## Features

- Connect to Stalker/Ministra portals using MAC address authentication
- Browse all available channel categories (countries/genres)
- Search channels by name
- Stream channels directly to VLC media player
- Bilingual interface (English/Spanish)

## Requirements

- Python 3.6+
- VLC Media Player
- `requests` library

## Installation

```bash
pip install requests
```

## Usage

```bash
python stb.py
```

1. Select language (English/Spanish)
2. Enter portal URL (e.g., `http://example.com:8080/c/`)
3. Enter MAC address (e.g., `00:1A:79:00:00:00`)
4. Select a category/country
5. Browse and play channels

## Menu Options

| Option | Description |
|--------|-------------|
| 1 | View channel list |
| 2 | Play channel in VLC |
| 3 | Search channels |
| 4 | Change category |
| 5 | Exit |

## Note

This tool is for educational purposes only. Make sure you have authorization to access the portals you connect to.

---

# STB Checker & Player (Español)

Herramienta en Python para verificar y reproducir canales IPTV de servidores STB (Stalker Portal). Conéctate a portales IPTV basados en MAC, navega por categorías de canales por país y reproduce directamente en VLC.

## Características

- Conexión a portales Stalker/Ministra usando autenticación MAC
- Navegación por todas las categorías disponibles (países/géneros)
- Búsqueda de canales por nombre
- Reproducción directa en VLC
- Interfaz bilingüe (Inglés/Español)

## Requisitos

- Python 3.6+
- VLC Media Player
- Librería `requests`

## Instalación

```bash
pip install requests
```

## Uso

```bash
python stb.py
```

1. Selecciona idioma (Inglés/Español)
2. Introduce la URL del portal (ej: `http://ejemplo.com:8080/c/`)
3. Introduce la dirección MAC (ej: `00:1A:79:00:00:00`)
4. Selecciona una categoría/país
5. Navega y reproduce canales

## Opciones del Menú

| Opción | Descripción |
|--------|-------------|
| 1 | Ver lista de canales |
| 2 | Reproducir canal en VLC |
| 3 | Buscar canales |
| 4 | Cambiar categoría |
| 5 | Salir |

## Nota

Esta herramienta es solo para fines educativos. Asegúrate de tener autorización para acceder a los portales que uses.

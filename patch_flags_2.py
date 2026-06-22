import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

lookup_code = """
const ISO3_TO_ALPHA2 = {
  // Group A
  "MEX": "mx",
  "USA": "us",
  "CAN": "ca",
  "URU": "uy",
  // Group B
  "SUI": "ch",   // Switzerland — FIFA uses SUI, alpha-2 is ch
  "BIH": "ba",   // Bosnia and Herzegovina
  "QAT": "qa",
  // Group C
  "BRA": "br",
  "MAR": "ma",
  "SCO": "gb-sct",  // Scotland — flagcdn supports gb-sct
  "HAI": "ht",
  // Group D
  "AUS": "au",
  "PRY": "py",   // Paraguay
  "TUR": "tr",   // Türkiye
  // Group E
  "GER": "de",
  "CIV": "ci",   // Côte d'Ivoire
  "ECU": "ec",
  "CUW": "cw",   // Curaçao — NOT cu (Cuba)
  // Group F
  "NED": "nl",   // Netherlands — FIFA uses NED
  "JPN": "jp",
  "SWE": "se",
  "TUN": "tn",
  // Group G
  "EGY": "eg",
  "BEL": "be",
  "IRN": "ir",   // IR Iran
  "NZL": "nz",
  // Group H
  "ESP": "es",
  "CPV": "cv",   // Cabo Verde — NOT cp
  "KSA": "sa",   // Saudi Arabia
  // Group I
  "NOR": "no",
  "FRA": "fr",
  "SEN": "sn",
  "IRQ": "iq",
  // Group J
  "ARG": "ar",
  "AUT": "at",
  "JOR": "jo",
  "ALG": "dz",   // Algeria — alpha-2 is dz
  // Group K
  "COL": "co",
  "COD": "cd",   // Congo DR — NOT co (Colombia)
  "POR": "pt",
  "UZB": "uz",
  // Group L
  "KOR": "kr",   // Korea Republic — NOT ko
  "GHA": "gh",
  "GER": "de",
  "ENG": "gb-eng",  // England — flagcdn supports gb-eng
  "CRO": "hr",   // Croatia
  "CZE": "cz",
  "PAN": "pa",
  "RSA": "za",   // South Africa
  "SCT": "gb-sct",
  "SEN": "sn",
};

function getAlpha2(code) {
  const alpha2 = ISO3_TO_ALPHA2[code?.toUpperCase()];
  if (!alpha2) {
    console.warn(`[flags] No alpha-2 mapping found for code: "${code}" — falling back to UN flag`);
    return "un";
  }
  return alpha2;
}

"""

# Inject after <script>
if "const ISO3_TO_ALPHA2" not in html:
    html = re.sub(r'<script>', f'<script>\n{lookup_code}', html, count=1)

# Replace the .slice calls
html = re.sub(r'\(([\w\.]+) \|\| [\'"]un[\'"]\)\.slice\(0,\s*2\)\.toLowerCase\(\)', r'getAlpha2(\1)', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Patched flags logic.")

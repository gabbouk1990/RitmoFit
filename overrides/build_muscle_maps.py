"""Precompila viste muscolari statiche da Anatome (Apache 2.0 / MIT SVG paths).

Le immagini rimangono in GitHub Pages: dopo la pubblicazione l'app funziona
senza richieste a servizi di terzi. Non usa account o API a pagamento.
"""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError
from xml.etree import ElementTree as ET
import json
import time

TARGET=Path("_site/assets/muscles")
TARGET.mkdir(parents=True,exist_ok=True)
BASE="https://api.anatome.dev/generateImage"
# Il renderer evidenzia in rosso i muscoli principali e in ambra i sinergici.
# Esempi fisiologici semplificati: non sono mappe EMG o una quantificazione.
PRESETS={
 "squat":       (["quadriceps","gluteal"], ["adductors","hamstring","abs"]),
 "hinge":       (["hamstring","gluteal"], ["lower-back","upper-back","forearm"]),
 "glutes":      (["gluteal"], ["hamstring","abs"]),
 "chest":       (["chest"], ["triceps","deltoids"]),
 "incline":     (["chest","deltoids"], ["triceps"]),
 "vertical":    (["upper-back"], ["biceps","trapezius","forearm"]),
 "row":         (["upper-back","trapezius"], ["biceps","deltoids"]),
 "pullover":    (["upper-back"], ["triceps","abs"]),
 "shoulders":   (["deltoids"], ["triceps","trapezius"]),
 "lateral":     (["deltoids"], ["trapezius"]),
 "plank":       (["abs"], ["obliques","deltoids","gluteal"]),
 "core":        (["obliques","abs"], ["deltoids","gluteal"]),
 "carry":       (["obliques","forearm"], ["trapezius","abs"]),
 "swimming":    (["upper-back","deltoids"], ["chest","triceps","abs"]),
 "walking":     (["gluteal","quadriceps"], ["hamstring","calves"]),
 "cycling":     (["quadriceps"], ["gluteal","calves"]),
}
def make_url(primary,secondary):
 params={
  "gender":"male",
  "view":"dual",
  "width":480,
  "layers":"EF5350:"+",".join(primary)+"|F4B860:"+",".join(secondary),
  "output":"raw",
 }
 return BASE+"?"+urlencode(params)
def save_one(key,primary,secondary):
 dst=TARGET/(key+".svg")
 if dst.exists() and '<svg' in dst.read_text(encoding='utf-8'):
  return key
 req=Request(make_url(primary,secondary),headers={
  "Accept":"image/svg+xml","User-Agent":"RitmoFit/1.0 personal offline muscle map"
 })
 for attempt in range(3):
  try:
   with urlopen(req,timeout=24) as response:
    content=response.read(2_000_000)
    mime=response.headers.get("Content-Type","")
   decoded=content.decode("utf-8")
   root=ET.fromstring(decoded)
   if not root.tag.endswith("svg") or len(content)<2000:
    raise RuntimeError(f"Risposta non valida per {key}, {len(content)} bytes, {mime}")
   if 'EF5350' not in decoded.upper() and '#ef5350' not in decoded.lower():
    raise RuntimeError(f"Colore muscoli principali assente da {key}")
   dst.write_text(decoded,encoding="utf-8")
   return key
  except (URLError,OSError,RuntimeError,ET.ParseError,UnicodeError) as exc:
   if attempt>=2:
    raise RuntimeError(f"Impossibile creare mappa {key}: {exc}") from exc
   time.sleep(1.2*(attempt+1))
for i,(key,(primary,secondary)) in enumerate(PRESETS.items(),1):
 print(f"[{i}/{len(PRESETS)}] Anatomia: {key}",flush=True)
 save_one(key,primary,secondary)
(TARGET/"LICENSE.txt").write_text(
 "Anatomical SVG diagrams produced with Anatome by NextSolutions "
 "(https://github.com/Rippy1911/anatome), Apache License 2.0. "
 "Underlying SVG muscle path artwork by Hicham El Boussarghini "
 "(react-native-body-highlighter), MIT. "
 "Muscle highlighting, preset selection and color adaptations by Ritmo Fit. "
 "Primary: #EF5350; secondary: #F4B860. "
 "https://www.apache.org/licenses/LICENSE-2.0 "
 "https://opensource.org/license/mit\n",
 encoding="utf-8")
(TARGET/"mapping.json").write_text(json.dumps(
 {key:{"primary":pr,"secondary":se} for key,(pr,se) in PRESETS.items()},
 indent=2),encoding="utf-8")
print(f"{len(PRESETS)} mappe muscolari create e salvate nel sito.",flush=True)

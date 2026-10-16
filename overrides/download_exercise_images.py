"""Copia le miniature CC BY-SA 4.0 negli asset della build statica.

L'app serve solo file locali: nessuna dipendenza visiva dal sito di origine.
La provenienza è fissata a un commit upstream, per risultati riproducibili.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import URLError
import time

UPSTREAM = "aac599224bb9780305239607ef98540b7e0ce389"
SOURCE = ("https://raw.githubusercontent.com/bryllim/workout-guide/"
          + UPSTREAM + "/packages/workout-guide/assets/")
DEST = Path("_site/assets/exercises")
# Solo movimenti validati nel catalogo pubblicato. Nessuna immagine dell'app bici/gravel.
SLUGS = (
    "arm-circles", "cycling", "walking", "treadmill-incline-walk",
    "squat", "goblet-squat", "romanian-deadlift", "dumbbell-romanian-deadlift",
    "bench-press", "dumbbell-bench-press", "incline-dumbbell-press",
    "lat-pulldown", "close-grip-lat-pulldown",
    "one-arm-dumbbell-row", "chest-supported-row", "machine-row",
    "barbell-row", "seated-row", "cable-lateral-raise", "lateral-raise",
    "hip-thrust", "dumbbell-hip-thrust", "glute-bridge",
    "straight-arm-pulldown", "pallof-press", "plank", "side-plank",
    "swimming", "farmer-carry", "push-up", "machine-chest-press",
    "seated-dumbbell-press", "machine-shoulder-press", "assisted-dip",
)
DEST.mkdir(parents=True, exist_ok=True)

def download(slug, frame):
    name = f"{slug}-{frame}.png"
    target = DEST / name
    url = SOURCE + slug + f"/frame-{frame}.png"
    if target.exists() and target.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n":
        return name
    for attempt in range(3):
        try:
            request = Request(url, headers={"User-Agent":"RitmoFit-GitHub-Pages/1.0"})
            with urlopen(request, timeout=25) as response:
                data = response.read()
            if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data)<200:
                raise RuntimeError(f"Risorsa non valida: {url}")
            target.write_bytes(data)
            return name
        except (OSError, URLError, RuntimeError):
            if attempt==2:
                raise
            time.sleep(1+attempt)

with ThreadPoolExecutor(max_workers=8) as pool:
    jobs=[pool.submit(download,slug,frame) for slug in SLUGS for frame in (1,2)]
    completed=[job.result() for job in as_completed(jobs)]

(DEST/"ATTRIBUTION.txt").write_text(
    "Workout Guide visual assets (c) 2026 Bryl Lim; based in part on original "
    "Everkinetic pose artwork. CC BY-SA 4.0. Unmodified original frames (only "
    "selected and renamed for use in Ritmo Fit). "
    "Source: https://github.com/bryllim/workout-guide "
    "Upstream: https://github.com/everkinetic/data "
    "License: https://creativecommons.org/licenses/by-sa/4.0/ "
    "See the original ATTRIBUTION.md and LICENSE-ASSETS files.\n",
    encoding="utf-8",
)
print(f"Immagini installate sul sito: {len(completed)} file, {len(SLUGS)} esercizi.")

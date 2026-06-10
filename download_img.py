#!/usr/bin/env python3
"""
Télécharge toutes les images du QCM CCNA 3 depuis ccnareponses.com.
À lancer une seule fois depuis le dossier ccna3_final/ :
 
    python3 download_images.py
 
Les images sont sauvegardées dans images/.
Si une image existe déjà, elle est ignorée (relançable sans risque).
"""
import json, os, sys, time
from pathlib import Path
 
try:
    import requests
except ImportError:
    print("❌ Module 'requests' manquant.")
    print("   Installe-le : pip install requests  ou  sudo apt install python3-requests")
    sys.exit(1)
 
BASE = "https://ccnareponses.com/wp-content/uploads"
 
IMAGE_URLS = {
    "2020-07-11_174231a.jpg":        f"{BASE}/2021/12/2020-07-11_174231a.jpg",
    "iqw386473n1v31.png":            f"{BASE}/2021/12/iqw386473n1v31.png",
    "i386046n1v2-1613220070.9736.gif": f"{BASE}/2022/05/i386046n1v2-1613220070.9736.gif",
    "2020-06-28_210428.jpg":         f"{BASE}/2022/05/2020-06-28_210428.jpg",
    "2024-10-17_100331.jpg":         f"{BASE}/2021/12/2024-10-17_100331.jpg",
    "ccna-5.0-s2-43.jpg":            f"{BASE}/2022/05/ccna-5.0-s2-43.jpg",
    "i350679v1n1_C3M4-Diagram.jpg":  f"{BASE}/2022/05/i350679v1n1_C3M4-Diagram.jpg",
    "Match-each-component-of-a-WAN-connection-to-its-description.jpg": f"{BASE}/2022/05/Match-each-component-of-a-WAN-connection-to-its-description.jpg",
    "i285134v1n1_285134.png":        f"{BASE}/2022/05/i285134v1n1_285134.png",
    "i286191v1n1_15178.jpg":         f"{BASE}/2022/05/i286191v1n1_15178.jpg",
    "Q48-CCNA-3-Examen-Final-ENSAv7.jpg": f"{BASE}/2022/05/Q48-CCNA-3-Examen-Final-ENSAv7.jpg",
    "i282155v1n2_282152.png":        f"{BASE}/2022/05/i282155v1n2_282152.png",
    "i212256v1n3_212256.png":        f"{BASE}/2022/05/i212256v1n3_212256.png",
    "2017-06-26_224429.jpg":         f"{BASE}/2022/05/2017-06-26_224429.jpg",
    "p53-1-1.png":                   f"{BASE}/2022/05/p53-1-1.png",
    "49.png":                        f"{BASE}/2022/05/49.png",
    "i212860v1n1_212860-1.png":      f"{BASE}/2022/05/i212860v1n1_212860-1.png",
    "Q62-CCNA-3-Examen-Final-ENSAv7.jpg": f"{BASE}/2022/05/Q62-CCNA-3-Examen-Final-ENSAv7.jpg",
    "i350680v1n1_C3M4-Diagram.jpg":  f"{BASE}/2022/05/i350680v1n1_C3M4-Diagram.jpg",
    "a2221i386513n1v3.png":          f"{BASE}/2021/12/a2221i386513n1v3.png",
    "2020-07-11_172005.jpg":         f"{BASE}/2022/05/2020-07-11_172005.jpg",
    "i282157v1n1_282156.png":        f"{BASE}/2022/05/i282157v1n1_282156.png",
    "i255837v1n1_255837.gif":        f"{BASE}/2022/05/i255837v1n1_255837.gif",
    "2022-05-09_165502.jpg":         f"{BASE}/2021/12/2022-05-09_165502.jpg",
    "41.jpg":                        f"{BASE}/2022/05/41.jpg",
    "2017-06-26_224149.jpg":         f"{BASE}/2022/05/2017-06-26_224149.jpg",
    "i208382v1n1_208382-1.png":      f"{BASE}/2022/05/i208382v1n1_208382-1.png",
    "i212258v1n1_212258-2-1.jpg":    f"{BASE}/2022/05/i212258v1n1_212258-2-1.jpg",
    "asdiasd305772n1v2.png":         f"{BASE}/2021/12/asdiasd305772n1v2.png",
    "12i300534n1v2.png":             f"{BASE}/2021/12/12i300534n1v2.png",
    "123i292427n1v3.jpg":            f"{BASE}/2021/12/123i292427n1v3.jpg",
    "2024-10-17_095512.jpg":         f"{BASE}/2021/12/2024-10-17_095512.jpg",
    "11i386750n1v3.jpg":             f"{BASE}/2021/12/11i386750n1v3.jpg",
    "ai386471n1v3.png":              f"{BASE}/2021/12/ai386471n1v3.png",
    "aa1i305927n1v2.png":            f"{BASE}/2021/12/aa1i305927n1v2.png",
    "112i238703n1v2.png":            f"{BASE}/2021/12/112i238703n1v2.png",
    "i239075n1v1.png":               f"{BASE}/2021/12/i239075n1v1.png",
    "i300450n1v2.png":               f"{BASE}/2021/12/i300450n1v2.png",
    "i290000v1n1_Trust-Boundary2-1.jpg": f"{BASE}/2022/05/i290000v1n1_Trust-Boundary2-1.jpg",
    "i349058v2n1_347058-1.png":      f"{BASE}/2022/05/i349058v2n1_347058-1.png",
    "i255837v1n1_255837-2.gif":      f"{BASE}/2022/05/i255837v1n1_255837-2.gif",
    "i208111v6n1_Question-8-1.png":  f"{BASE}/2022/05/i208111v6n1_Question-8-1.png",
    "2021-11-22_102145-1.jpg":       f"{BASE}/2022/05/2021-11-22_102145-1.jpg",
    "temp-1593110686.3832-1.png":    f"{BASE}/2022/05/temp-1593110686.3832-1.png",
    "Match-the-HTTP-method-with-the-RESTful-operation.-1.jpg": f"{BASE}/2022/05/Match-the-HTTP-method-with-the-RESTful-operation.-1.jpg",
    "i350786v1n1_C3M4-Diagram-1.jpg": f"{BASE}/2022/05/i350786v1n1_C3M4-Diagram-1.jpg",
    "i282155v1n2_282152-1.png":      f"{BASE}/2022/05/i282155v1n2_282152-1.png",
    "2020-10-25_185415-1.jpg":       f"{BASE}/2022/05/2020-10-25_185415-1.jpg",
    "i350685v1n1_C3M4-Diagram-1.jpg": f"{BASE}/2022/05/i350685v1n1_C3M4-Diagram-1.jpg",
}
 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
    "Referer": "https://ccnareponses.com/",
}
 
def download(url, dest, retries=3):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20, stream=True)
            if r.status_code == 200:
                dest.write_bytes(r.content)
                return True, f"{len(r.content)/1024:.1f} Ko"
            elif r.status_code == 404:
                return False, "404 introuvable"
            else:
                if attempt < retries:
                    time.sleep(1.5 * attempt)
        except Exception as e:
            if attempt < retries:
                time.sleep(1.5 * attempt)
            else:
                return False, str(e)
    return False, f"HTTP {r.status_code}"
 
def main():
    images_dir = Path(__file__).parent / "images"
    images_dir.mkdir(exist_ok=True)
 
    # Collect only images referenced in questions.json
    qfile = Path(__file__).parent / "questions.json"
    if qfile.exists():
        qs = json.loads(qfile.read_text(encoding="utf-8"))
        needed = {q["image"] for q in qs if q.get("image")}
    else:
        needed = set(IMAGE_URLS.keys())
 
    total = len(needed)
    print(f"╔══════════════════════════════════════════╗")
    print(f"║  Téléchargement images QCM CCNA 3        ║")
    print(f"╚══════════════════════════════════════════╝")
    print(f"\nImages à télécharger : {total}\n")
 
    ok_count, skip_count, fail = 0, 0, []
 
    for i, name in enumerate(sorted(needed), 1):
        dest = images_dir / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"[{i:>2}/{total}] ⏭  {name}")
            skip_count += 1
            continue
        url = IMAGE_URLS.get(name)
        if not url:
            print(f"[{i:>2}/{total}] ⚠  {name} (URL inconnue)")
            fail.append(name)
            continue
        print(f"[{i:>2}/{total}] ↓  {name}...", end=" ", flush=True)
        ok, msg = download(url, dest)
        if ok:
            print(f"✓ {msg}")
            ok_count += 1
        else:
            print(f"✗ {msg}")
            fail.append(name)
        time.sleep(0.4)
 
    print(f"\n{'='*45}")
    print(f"  Téléchargées  : {ok_count}")
    print(f"  Déjà présentes: {skip_count}")
    print(f"  Échecs        : {len(fail)}")
    if fail:
        print("\nÉchecs :")
        for f in fail: print(f"  - {f}")
        print("\n💡 Relance le script pour réessayer.")
    else:
        print("\n✅ Tout bon ! Lance : python3 -m http.server 8000")
        print("   puis ouvre http://localhost:8000 dans ton navigateur.")
    print("="*45)
 
if __name__ == "__main__":
    main()
 

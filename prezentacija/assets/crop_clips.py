"""Isece 'cisti' deo (3D viewport, bez debug panela) iz sirovih GIF snimaka
i uveca ih visokokvalitetnim (Lanczos + blago izostravanje) upscale-om,
buduci da je izvorna rezolucija snimaka svega 854x480 (fizicki maksimum
dostupnog materijala) pa ih PowerPoint inace steze default (mutnijim)
skaliranjem kad se prikazu preko 5+ inca visine na slajdu."""
import os
from PIL import Image, ImageSequence, ImageFilter

SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "videos")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips")
os.makedirs(OUT_DIR, exist_ok=True)

BOX = (4, 68, 276, 455)  # levi 3D viewport, bez UI panela/dugmadi/ikonica
SCALE = 1.8  # Lanczos upscale faktor pre ugradnje u slajd

FILES = {
    "cheat_code_policy (1).gif": "clip_cheat.gif",
    "run_act_policy (1).gif": "clip_act.gif",
    "wave_arm_policy (1).gif": "clip_wave.gif",
}

for src_name, out_name in FILES.items():
    src_path = os.path.join(SRC_DIR, src_name)
    im = Image.open(src_path)
    w, h = BOX[2] - BOX[0], BOX[3] - BOX[1]
    new_size = (int(w * SCALE), int(h * SCALE))
    frames = []
    durations = []
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        if i % 2 == 1:  # preskoci svaki drugi frejm - upola manji fajl, pokret ostaje gladak
            continue
        f = frame.convert("RGB").crop(BOX)
        f = f.resize(new_size, Image.LANCZOS)
        f = f.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
        f = f.convert("P", palette=Image.ADAPTIVE, colors=110)
        frames.append(f)
        durations.append(frame.info.get("duration", 80) * 2)
    out_path = os.path.join(OUT_DIR, out_name)
    frames[0].save(out_path, save_all=True, append_images=frames[1:],
                    duration=durations, loop=0, optimize=True)
    print(out_name, len(frames), "frames @", new_size, "->", os.path.getsize(out_path) // 1024, "KB")

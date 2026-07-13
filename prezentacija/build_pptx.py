"""Sklapa template prezentacije za odbranu diplomskog (.pptx)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
CLIPS = os.path.join(ASSETS, "clips")
IMAGES = os.path.join(HERE, "..", "images")

# --- Paleta ---
BG = RGBColor(0x14, 0x17, 0x1F)
FG = RGBColor(0xF5, 0xF6, 0xF8)
MUTED = RGBColor(0x9C, 0xA3, 0xAF)
ACCENT = RGBColor(0xFF, 0x7A, 0x45)
BLUE = RGBColor(0x5B, 0x8D, 0xEF)
ORANGE = RGBColor(0xFF, 0x7A, 0x45)
GREEN = RGBColor(0x34, 0xD3, 0x99)
RED = RGBColor(0xE5, 0x55, 0x5A)

FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_slide(notes=None):
    slide = prs.slides.add_slide(BLANK)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG
    bg.line.fill.background()
    bg.shadow.inherit = False
    spTree = slide.shapes._spTree
    spTree.remove(bg._element)
    spTree.insert(2, bg._element)
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def add_text(slide, runs, left, top, width, height,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15,
             wrap=True):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, para_runs in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        for text, size, color, bold, italic in para_runs:
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic
            r.font.name = FONT
    return box


def add_image_centered(slide, path, cx, cy, width=None, height=None):
    if width is not None:
        pic = slide.shapes.add_picture(path, 0, 0, width=width)
    elif height is not None:
        pic = slide.shapes.add_picture(path, 0, 0, height=height)
    else:
        pic = slide.shapes.add_picture(path, 0, 0)
    pic.left = int(cx - pic.width / 2)
    pic.top = int(cy - pic.height / 2)
    return pic


def corner_mark(slide):
    p = os.path.join(ASSETS, "symbol_ring_small.png")
    pic = slide.shapes.add_picture(p, 0, 0, height=Inches(0.55))
    pic.left = SW - pic.width - Inches(0.45)
    pic.top = Inches(0.4)
    return pic


def footer(slide, text, left=Inches(0.6), color=MUTED, size=13):
    add_text(slide, [[(text, size, color, False, False)]],
              left, SH - Inches(0.6), Inches(11.5), Inches(0.4),
              align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)


R = lambda t, s, c=FG, b=False, i=False: (t, s, c, b, i)

# =====================================================================
# SLIDE 1 -- HOOK deo I: promasaji (stvarni snimci)
# =====================================================================
s = add_slide(notes=(
    "[Gledaj publiku, ne slajd.] Ovo su stvarni snimci iz nase simulacije - "
    "robot pokusava da umetne konektor u port.\n"
    "OBECANJE (izgovoriti polako, kontakt ocima): 'Do kraja ovih deset minuta znacete tacno "
    "gde vestacka inteligencija staje - i zasto uvek staje na istom mestu, bez obzira na model.'"
))
fail_clips = ["clip_act.gif", "clip_wave.gif"]
panel_h = Inches(5.4)
gap = Inches(0.4)
pics = []
total_w = 0
for name in fail_clips:
    pic = s.shapes.add_picture(os.path.join(CLIPS, name), 0, 0, height=panel_h)
    pics.append(pic)
    total_w += pic.width
total_w += gap
start_x = int((SW - total_w) / 2)
y = Inches(0.75)
x = start_x
for pic in pics:
    pic.left = x
    pic.top = y
    x += pic.width + gap
footer(s, "Лабораторија за роботику ЕТФ  ·  Intrinsic AI for Industry Challenge")

# =====================================================================
# SLIDE 2 -- HOOK deo II: uspeh (reveal)
# =====================================================================
s = add_slide(notes=(
    "[Pauza 1-2 sekunde pre nego sto pustis ovaj slajd da progovori.] "
    "A evo i snimka gde uspeva.\n"
    "PITANJE PUBLICI (zastani, sacekaj 2-3 odgovora, ne otkrivaj broj jos): "
    "'Koliko demonstracija mislite da je robotu bilo potrebno da ovo nauci?'"
))
add_image_centered(s, os.path.join(CLIPS, "clip_cheat.gif"),
                    cx=SW / 2, cy=Inches(3.5), height=Inches(6.2))

# =====================================================================
# SLIDE 3-6 -- NASA ULOGA (pipeline, progresivan build klik-po-klik)
# =====================================================================
CREDIT = ("Демонстрације: Добрица Јанковић   ·   "
          "Ментори: проф. др Коста Јовановић, Давид Сеничић, др Филип Бечановић")
pipeline_notes = {
    1: "Oracle politika - skriptovani agent sa privilegovanim pristupom koordinatama porta.",
    2: "Iz uspesnih epizoda oracle-a gradi se skup demonstracija.",
    3: "Ovde je nasa podela rada - Dobrica demonstracije, mi trening.",
    4: "Mi treniramo i evaluiramo - politika vise NEMA privilegovan pristup, uci samo iz slike i pozicije.",
}
for step in range(1, 5):
    s = add_slide(notes=pipeline_notes[step])
    add_image_centered(s, os.path.join(ASSETS, f"pipeline_{step}.png"),
                        cx=SW / 2, cy=Inches(2.9), width=Inches(11.2))
    if step == 4:
        add_text(s, [
            [R("Ми учимо машину да сама пронађе пут.", 44, ACCENT, True)],
        ], Inches(0.8), Inches(4.85), Inches(11.7), Inches(1.2))
    footer(s, CREDIT)

# =====================================================================
# SLIDE 7 -- GRANICA + GLAVNI SIMBOL (rec iz naslova rada)
# =====================================================================
s = add_slide(notes=(
    "[Kontakt ocima, pauza pre reci 'GRANICA'.] Naslov rada kaze: ispitujemo GRANICU ucenja "
    "imitacijama. Ovo je ta granica koju cemo danas pronaci zajedno - zovem je 'poslednji milimetar'."
))
add_image_centered(s, os.path.join(ASSETS, "symbol_ring.png"),
                    cx=SW / 2, cy=Inches(2.75), width=Inches(3.5))
add_text(s, [
    [R("ГРАНИЦА.", 50, ACCENT, True)],
], Inches(0.8), Inches(4.4), Inches(11.7), Inches(1.05))
add_text(s, [
    [R("„последњи милиметар”", 26, MUTED, False, True)],
], Inches(0.8), Inches(5.5), Inches(11.7), Inches(0.7))

# =====================================================================
# SLIDE 8 -- VIZIJA: problem (krut vs deformabilan)
# =====================================================================
s = add_slide(notes="DLO problem - kabl nema fiksnu geometriju, za razliku od krutog umetka.")
corner_mark(s)
add_image_centered(s, os.path.join(ASSETS, "rigid_vs_deformable.png"),
                    cx=SW / 2, cy=Inches(2.85), width=Inches(9.2))
add_text(s, [
    [R("Кабл није крут.", 44, FG, True)],
    [R("Свака грешка изнад милиметра је промашај.", 40, MUTED)],
], Inches(0.8), Inches(5.35), Inches(11.7), Inches(1.7), line_spacing=1.2)

# =====================================================================
# SLIDE 9 -- MOJ PRISTUP / INOVACIJA: ACT vs DP (jednostavno)
# =====================================================================
s = add_slide(notes=(
    "Ovde je moja specificna kontribucija - ne izum novih metoda, vec prva kontrolisana "
    "uporedna studija ove dve arhitekture bas na ovom zadatku."
))
corner_mark(s)
add_image_centered(s, os.path.join(ASSETS, "act_vs_dp.png"),
                    cx=SW / 2, cy=Inches(2.3), width=Inches(9.2))
add_text(s, [
    [R("Прва контролисана студија", 40, FG, True)],
    [R("ACT", 40, BLUE, True), R(" и ", 40, FG, True), R("Diffusion Policy", 40, ORANGE, True)],
    [R("на задатку милиметарске прецизности.", 40, FG, True)],
], Inches(0.6), Inches(4.35), Inches(12.1), Inches(2.35), line_spacing=1.05)
footer(s, "Иста симулација  ·  исте демонстрације  ·  исти протокол евалуације")

# =====================================================================
# SLIDE 10 -- ARHITEKTURE (namerno gust/tehnicki slajd)
# =====================================================================
s = add_slide(notes=(
    "[Namerno gust slajd - ne ocekujte da svi prate svaki detalj, samo pokazite strukturu, "
    "publika treba da OSETI kompleksnost, ne da je razume do kraja.]\n\n"
    "ACT (gore): 4 kamere -> CNN izvlaci vizuelne odlike -> transformer enkoder ih kombinuje sa "
    "pozicijom zglobova -> dekoder predvidja CEO BLOK buducih akcija odjednom (ne jednu po jednu). "
    "CVAE (stil 'z') levo postoji samo tokom treninga da uhvati razlicite stilove izvodjenja iz "
    "demonstracija.\n\n"
    "Diffusion Policy (dole): suprotna logika - krene od CISTOG SUMA (A^K, levo dole u tackicama) "
    "i iterativno ga 'ocisti' u K koraka do glatke putanje akcija (A^0, desno, uokvireno). Svaki "
    "korak ciscenja je uslovljen slikom kamere - FiLM (CNN varijanta, b) ili unakrsna paznja "
    "(transformer varijanta, c).\n\n"
    "Poenta za publiku: ACT donosi ODLUKU odjednom (jedan blok), DP je PROCES prociscavanja kroz "
    "vreme - dva potpuno razlicita nacina da se dodje do iste akcije."
))
add_text(s, [[R("ACT", 26, BLUE, True)]], Inches(0.8), Inches(0.35), Inches(3.0), Inches(0.5),
          align=PP_ALIGN.LEFT)
add_image_centered(s, os.path.join(ASSETS, "act_arhitektura_dark.png"),
                    cx=SW / 2, cy=Inches(2.35), width=Inches(10.6))
add_text(s, [[R("Diffusion Policy", 26, ORANGE, True)]], Inches(0.8), Inches(4.15), Inches(4.5), Inches(0.5),
          align=PP_ALIGN.LEFT)
add_image_centered(s, os.path.join(ASSETS, "dp_arhitektura_dark.png"),
                    cx=SW / 2, cy=Inches(5.95), width=Inches(10.2))

# =====================================================================
# SLIDE 11-14 -- KAKO JE URADJENO: koraci u krugu (progresivan build)
# =====================================================================
steps = [
    ("ШТА треба урадити", "задатак: уметање конектора"),
    ("ПОНАШАЊЕ система", "прилазак → поравнање → уметање"),
    ("УСЛОВИ", "прецизност < 3mm, деформабилан кабл"),
    ("ИМПЛЕМЕНТАЦИЈА", "изградити и демонстрирати"),
]
for i, (title, sub) in enumerate(steps, start=1):
    s = add_slide()
    add_text(s, [[R("КАКО ИЗГЛЕДА ИНЖЕЊЕРСКИ ПОСТУПАК.", 34, FG, True)]],
              Inches(0.8), Inches(0.55), Inches(11.7), Inches(0.9), align=PP_ALIGN.LEFT)
    add_image_centered(s, os.path.join(ASSETS, f"steps_circle_{i}.png"),
                        cx=Inches(3.75), cy=Inches(4.5), height=Inches(4.3))
    add_text(s, [[R(f"{i}  {title}", 40, ACCENT, True)]],
              Inches(6.75), Inches(3.35), Inches(6.1), Inches(1.1),
              align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.BOTTOM)
    add_text(s, [[R(sub, 28, MUTED, False, True)]],
              Inches(6.75), Inches(4.5), Inches(6.1), Inches(0.7),
              align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
    if i == 4:
        add_text(s, [
            [R("Ми смо инжењери — не верујемо да нешто знамо", 26, MUTED, False, True)],
            [R("док га не направимо и не покажемо.", 26, MUTED, False, True)],
        ], Inches(0.8), Inches(6.35), Inches(11.7), Inches(1.0), align=PP_ALIGN.LEFT, line_spacing=1.2)

# =====================================================================
# SLIDE 15 -- REZULTATI I: bocna greska (blizu ose)
# =====================================================================
s = add_slide(notes="Prvo dobra vest - bocno smo skoro tacno na osi porta.")
corner_mark(s)
add_text(s, [
    [R("9,1 mm", 48, ACCENT, True), R("  бочно одступање.", 40, FG, True)],
], Inches(0.7), Inches(0.55), Inches(12.0), Inches(1.1))
add_image_centered(s, os.path.join(ASSETS, "lateral_target.png"),
                    cx=SW / 2, cy=Inches(4.35), height=Inches(4.7))
add_text(s, [
    [R("Скоро на оси порта.", 40, MUTED)],
], Inches(0.8), Inches(6.75), Inches(11.7), Inches(0.65))

# =====================================================================
# SLIDE 16 -- REZULTATI II: ukupna (dubinska) greska - plato
# =====================================================================
s = add_slide(notes=(
    "OVDE JE ODGOVOR na pitanje sa pocetka: 30.290 demonstracija. I dalje ispod 1% uspesnosti. "
    "Sad zastani - ovo je twist pre iznenadjenja."
))
corner_mark(s)
add_text(s, [
    [R("Али укупно застанемо на ", 40, FG, True), R("47 mm", 40, ACCENT, True), R(".", 40, FG, True)],
], Inches(0.6), Inches(0.4), Inches(12.1), Inches(1.0))
add_image_centered(s, os.path.join(ASSETS, "plateau_chart.png"),
                    cx=SW / 2, cy=Inches(4.15), width=Inches(9.6))
add_text(s, [
    [R("0,7–1,3", 34, ACCENT, True), R(" % успешности.", 34, MUTED)],
], Inches(0.8), Inches(6.85), Inches(11.7), Inches(0.6))

# =====================================================================
# SLIDE 17 -- IZNENADJENJE
# =====================================================================
s = add_slide(notes="[Pusti ovo da 'legne' - napravi pauzu posle citanja poslednje recenice.]")
add_image_centered(s, os.path.join(ASSETS, "surprise_wall.png"),
                    cx=Inches(4.5), cy=SH / 2, height=Inches(6.6))
add_text(s, [
    [R("ИЗНЕНАЂЕЊЕ", 20, RED, True)],
], Inches(7.5), Inches(1.3), Inches(5.2), Inches(0.55), align=PP_ALIGN.LEFT)
add_text(s, [
    [R("Различите архитектуре.", 40, FG, True)],
    [R("Исти зид.", 40, ACCENT, True)],
], Inches(7.5), Inches(1.85), Inches(5.4), Inches(2.0), align=PP_ALIGN.LEFT, line_spacing=1.15)
add_text(s, [
    [R("ACT", 26, BLUE, True), R(" и ", 26, MUTED), R("Diffusion Policy", 26, ORANGE, True),
     R(", учене одвојено —", 26, MUTED)],
    [R("стану на истих ", 26, MUTED), R("~47mm", 26, FG, True), R(".", 26, MUTED)],
    [R("Проблем није модел. Проблем је задатак.", 26, FG, True)],
], Inches(7.5), Inches(4.25), Inches(5.5), Inches(2.4), align=PP_ALIGN.LEFT, line_spacing=1.3)

# =====================================================================
# SLIDE 18 -- VIDEO DOKAZ (pusti se 2x) + QR za posle
# =====================================================================
s = add_slide(notes=(
    "[Cutis dok se ovo pusta - ne pricaj preko snimka. Pusti da odigra dva puta pa nastavi.] "
    "Ovo je dokaz da uspeh nije nemoguc - samo krajnje redak."
))
add_image_centered(s, os.path.join(CLIPS, "clip_cheat_loop2.gif"),
                    cx=Inches(5.4), cy=SH / 2, height=Inches(6.6))
qr_path = os.path.join(ASSETS, "qr_video.png")
if os.path.exists(qr_path):
    add_image_centered(s, qr_path, cx=Inches(10.9), cy=Inches(3.3), height=Inches(2.3))
add_text(s, [[R("гледај поново", 22, MUTED)]], Inches(9.6), Inches(4.75), Inches(2.6), Inches(0.5))

# =====================================================================
# SLIDE 19 -- DOPRINOS (zavrsni slajd)
# =====================================================================
s = add_slide(notes="Zavrsna rec - hvala se kaze usmeno, slajd ostaje otvoren dok traju pitanja.")
contrib = [
    "Систематска студија граница ACT и Diffusion Policy.",
    "Поређење скалабилности две архитектуре.",
    "Карактеризација платоа перформанси.",
]
top0 = Inches(1.0)
for i, text in enumerate(contrib):
    top = top0 + Inches(1.35) * i
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.85), top + Inches(0.18), Inches(0.3), Inches(0.3))
    dot.fill.solid(); dot.fill.fore_color.rgb = ACCENT
    dot.line.fill.background(); dot.shadow.inherit = False
    add_text(s, [[R(text, 34, FG, True)]], Inches(1.45), top, Inches(11.0), Inches(1.1),
              align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.2)

add_image_centered(s, os.path.join(ASSETS, "symbol_ring_small.png"),
                    cx=Inches(1.55), cy=Inches(6.55), height=Inches(0.85))
add_text(s, [[R("ГРАНИЦА", 30, ACCENT, True)]],
          Inches(2.2), Inches(6.15), Inches(8.5), Inches(0.85),
          align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

out_path = os.path.join(HERE, "Odbrana_Template.pptx")
prs.save(out_path)
print("saved:", out_path)

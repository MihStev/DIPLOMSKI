"""Generise minimalisticke SVG-like PNG ilustracije za prezentaciju odbrane."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# --- Paleta ---
BG = "#14171F"
FG = "#F5F6F8"
MUTED = "#6B7280"
ACCENT = "#FF7A45"      # amber - simbol / port / preciznost
BLUE = "#5B8DEF"        # ACT
ORANGE = "#FF7A45"      # DP (isti kao accent - dosledno)
GREEN = "#34D399"       # uspeh / zona
RED = "#E5555A"         # neuspeh

plt.rcParams["font.family"] = "DejaVu Sans"


def new_fig(w=10, h=10, transparent=True):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")
    if not transparent:
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
    else:
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# =====================================================================
# 1. GLAVNI SIMBOL: prsten (port) + tacka koja se priblizava ali ne ulazi
# =====================================================================
def symbol_ring(big=True, label=True):
    fig, ax = new_fig(10, 10)
    cx, cy, r = 50, 50, 32
    ring = plt.Circle((cx, cy), r, fill=False, edgecolor=ACCENT, linewidth=7)
    ax.add_patch(ring)
    # unutrasnji "port" prsten tanji
    ring2 = plt.Circle((cx, cy), r - 9, fill=False, edgecolor=ACCENT, linewidth=2.2, alpha=0.35)
    ax.add_patch(ring2)
    # isprekidana putanja prilaska, zaustavljena TESNO PRE ivice
    theta = np.linspace(200, 250, 40) * np.pi / 180
    path_r = np.linspace(85, r + 6, 40)
    px = cx + path_r * np.cos(theta)
    py = cy + path_r * np.sin(theta)
    ax.plot(px, py, linestyle=(0, (2, 3)), color=FG, linewidth=2.4, alpha=0.85)
    # tacka (vrh konektora) zaustavljena na ivici prstena
    ax.plot(px[-1], py[-1], marker="o", markersize=17, color=FG, zorder=5)
    ax.plot(px[-1], py[-1], marker="o", markersize=17, markerfacecolor="none",
            markeredgecolor=ACCENT, markeredgewidth=2, zorder=6)
    save(fig, "symbol_ring.png")


def symbol_ring_small():
    """Sitan brend-marker za uglove slajdova."""
    fig, ax = new_fig(4, 4)
    cx, cy, r = 50, 50, 34
    ring = plt.Circle((cx, cy), r, fill=False, edgecolor=ACCENT, linewidth=6, alpha=0.9)
    ax.add_patch(ring)
    ax.plot(cx + r, cy, marker="o", markersize=13, color=ACCENT, zorder=5)
    save(fig, "symbol_ring_small.png")


# =====================================================================
# 2. HOOK: robot promasuje port - vise isprekidanih putanja, promasaji
# =====================================================================
def hook_misses():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect("equal"); ax.axis("off")
    fig.patch.set_alpha(0); ax.patch.set_alpha(0)

    cx, cy = 76, 50
    r = 14
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, edgecolor=FG, linewidth=5))
    ax.add_patch(plt.Circle((cx, cy), r - 5, fill=False, edgecolor=FG, linewidth=1.6, alpha=0.4))

    # cetiri mirna, paralelna promasaja - dolaze sa leve strane, na razlicitim visinama
    starts_y = [20, 38, 62, 80]
    end_angles = [150, 195, 165, 210]  # gde oko porta promasuju
    for sy, ea in zip(starts_y, end_angles):
        ex = cx + (r + 6) * np.cos(ea * np.pi / 180)
        ey = cy + (r + 6) * np.sin(ea * np.pi / 180)
        t = np.linspace(0, 1, 30)
        xs = 6 + (ex - 6) * t
        ys = sy + (ey - sy) * t
        ax.plot(xs, ys, linestyle=(0, (1, 2.6)), color=MUTED, linewidth=2.2, alpha=0.65)
        ax.plot(ex, ey, marker="x", markersize=15, markeredgewidth=3.4, color=RED, alpha=0.9)

    # jedna putanja - blizu, ali stala tik uz ivicu (najavljuje temu)
    theta = np.linspace(195, 232, 30) * np.pi / 180
    path_r = np.linspace(58, r + 2, 30)
    px = cx + path_r * np.cos(theta)
    py = cy + path_r * np.sin(theta)
    ax.plot(px, py, linestyle=(0, (2, 3)), color=ACCENT, linewidth=3)
    ax.plot(px[-1], py[-1], marker="o", markersize=17, color=FG, zorder=6)
    save(fig, "hook_misses.png")


# =====================================================================
# 3. PIPELINE: Oracle -> Demonstracije -> Trening -> Evaluacija
# =====================================================================
def pipeline(step=4):
    """step = koliko kutija (1-4) je vec 'otkriveno' (za progresivan build klik-po-klik)."""
    fig, ax = plt.subplots(figsize=(18, 5.5), dpi=200)
    ax.set_xlim(0, 100); ax.set_ylim(0, 30); ax.set_aspect("auto"); ax.axis("off")
    fig.patch.set_alpha(0); ax.patch.set_alpha(0)

    labels = ["ORACLE\nполитика", "ДЕМОНСТРАЦИЈЕ", "ТРЕНИНГ\nполитике", "ЕВАЛУАЦИЈА"]
    highlight = [False, False, True, True]
    xs = [13, 38, 63, 88]
    y = 15
    w, h = 20, 18
    for idx, (x, lab, hi) in enumerate(zip(xs, labels, highlight)):
        if idx >= step:
            break
        active = idx == step - 1
        color = ACCENT if hi else MUTED
        lw = 4.2 if active else 3
        alpha = 1.0 if active else 0.55
        box = mpatches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                       boxstyle="round,pad=0.6,rounding_size=2.4",
                                       linewidth=lw, edgecolor=color, facecolor="none", alpha=alpha)
        ax.add_patch(box)
        txt_color = (FG if hi else MUTED)
        ax.text(x, y, lab, ha="center", va="center", color=txt_color,
                 fontsize=15, fontweight="bold" if hi else "normal", linespacing=1.5, alpha=alpha)
    for i, (x0, x1) in enumerate(zip(xs[:-1], xs[1:])):
        if i + 1 >= step:
            break
        ax.annotate("", xy=(x1 - w / 2 - 1, y), xytext=(x0 + w / 2 + 1, y),
                     arrowprops=dict(arrowstyle="-|>", color=FG, lw=2.4, alpha=0.85))
    save(fig, f"pipeline_{step}.png")


# =====================================================================
# 4. KRUT vs DEFORMABILAN (reseno vs otvoren problem)
# =====================================================================
def rigid_vs_deformable():
    fig, axs = plt.subplots(1, 2, figsize=(14, 7), dpi=200)
    for ax in axs:
        ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect("equal"); ax.axis("off")
        ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)

    # levo: kruto telo - resen problem
    ax = axs[0]
    ax.plot([20, 20], [30, 70], color=FG, linewidth=10, solid_capstyle="round")
    ax.add_patch(plt.Circle((20, 20), 12, fill=False, edgecolor=GREEN, linewidth=5))
    ax.plot([20, 20], [20, 30], color=GREEN, linewidth=8)
    ax.text(20, 85, "КРУТ УМЕТАК", ha="center", color=FG, fontsize=17, fontweight="bold")
    ax.text(20, 5, "решен проблем", ha="center", color=GREEN, fontsize=14)

    # desno: deformabilan kabl - otvoren problem
    ax = axs[1]
    t = np.linspace(0, 1, 60)
    xs = 20 + 6 * np.sin(t * 4 * np.pi)
    ys = 30 + t * 40
    ax.plot(xs, ys, color=FG, linewidth=9, solid_capstyle="round")
    ax.add_patch(plt.Circle((20, 20), 12, fill=False, edgecolor=ACCENT, linewidth=5))
    ax.plot([22, 18], [24, 30], color=RED, linewidth=3)
    ax.plot([18, 22], [24, 30], color=RED, linewidth=3)
    ax.text(20, 85, "ДЕФОРМАБИЛАН КАБЛ", ha="center", color=FG, fontsize=17, fontweight="bold")
    ax.text(20, 5, "отворен проблем", ha="center", color=ACCENT, fontsize=14)

    save(fig, "rigid_vs_deformable.png")


# =====================================================================
# 5. ACT vs Diffusion Policy - dva jednostavna piktograma
# =====================================================================
def act_vs_dp():
    fig, axs = plt.subplots(1, 2, figsize=(14, 8), dpi=200)
    for ax in axs:
        ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_aspect("equal"); ax.axis("off")
        ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)

    # ACT - blokovi akcija (chunking)
    ax = axs[0]
    xs = [15, 32, 49, 66, 83]
    for i, x in enumerate(xs):
        h = 20 + 6 * np.sin(i)
        ax.add_patch(mpatches.FancyBboxPatch((x - 7, 40 - h / 2), 14, h,
                     boxstyle="round,pad=0.3,rounding_size=2",
                     facecolor=BLUE, edgecolor="none", alpha=0.85))
    ax.annotate("", xy=(90, 40), xytext=(8, 40),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.8))
    ax.text(50, 75, "ACT", ha="center", color=BLUE, fontsize=26, fontweight="bold")
    ax.text(50, 15, "блок акција одједном", ha="center", color=FG, fontsize=13)

    # DP - sum -> signal (difuzija)
    ax = axs[1]
    rng = np.random.default_rng(3)
    t = np.linspace(0, 100, 200)
    clean = 40 + 12 * np.sin(t / 10)
    for noise_amt, alpha in zip([18, 10, 4, 0], [0.25, 0.4, 0.6, 1.0]):
        y = clean + rng.normal(0, noise_amt, size=t.shape) if noise_amt else clean
        ax.plot(t * 0.8 + 5, y * 0.6 + (10 if noise_amt else 10), color=ORANGE, alpha=alpha, linewidth=2.2)
    ax.text(50, 75, "Diffusion\nPolicy", ha="center", color=ORANGE, fontsize=22, fontweight="bold", linespacing=1.3)
    ax.text(50, 8, "шум → путања", ha="center", color=FG, fontsize=13)

    save(fig, "act_vs_dp.png")


# =====================================================================
# 6. KORACI U KRUGU (4 koraka, kruzno - motiv prstena)
# =====================================================================
def steps_circle(active=None):
    """active = 1..4: istakni samo taj korak (accent), ostali priguseni. None = svi accent."""
    fig, ax = new_fig(11, 11)
    cx, cy, r = 50, 50, 34
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, edgecolor=MUTED, linewidth=2, alpha=0.5))
    steps = ["1", "2", "3", "4"]
    angles = [90, 0, 270, 180]
    for s, a in zip(steps, angles):
        is_active = (active is None) or (int(s) == active)
        x = cx + r * np.cos(a * np.pi / 180)
        y = cy + r * np.sin(a * np.pi / 180)
        color = ACCENT if is_active else "#3A3F4B"
        txtcolor = BG if is_active else MUTED
        radius = 9.5 if (active is not None and int(s) == active) else 8.5
        ax.add_patch(plt.Circle((x, y), radius, facecolor=color, edgecolor="none"))
        ax.text(x, y, s, ha="center", va="center", color=txtcolor, fontsize=22, fontweight="bold")
    # strelice u krug
    for a0, a1 in zip(angles, angles[1:] + angles[:1]):
        t = np.linspace(a0, a1 - (360 if a1 > a0 else 0), 30) * np.pi / 180
        xs = cx + r * np.cos(t)
        ys = cy + r * np.sin(t)
        ax.plot(xs[3:-3], ys[3:-3], color=MUTED, linewidth=1.6, alpha=0.6)
    name = "steps_circle.png" if active is None else f"steps_circle_{active}.png"
    save(fig, name)


# =====================================================================
# 9. BOCNA GRESKA: pogled "iz cevi" - tacke blizu ose
# =====================================================================
def lateral_target():
    fig, ax = new_fig(10, 10)
    cx, cy, r = 50, 50, 32
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, edgecolor=FG, linewidth=5))
    ax.add_patch(plt.Circle((cx, cy), r - 9, fill=False, edgecolor=FG, linewidth=1.6, alpha=0.35))
    rng = np.random.default_rng(11)
    n = 14
    ang = rng.uniform(0, 2 * np.pi, n)
    rad = np.abs(rng.normal(0, 7, n))
    rad = np.clip(rad, 0, 22)
    xs = cx + rad * np.cos(ang)
    ys = cy + rad * np.sin(ang)
    ax.scatter(xs, ys, s=170, color=ACCENT, alpha=0.85, zorder=5, edgecolors="none")
    ax.scatter([cx], [cy], s=60, color=FG, zorder=6)
    save(fig, "lateral_target.png")


# =====================================================================
# 7. PLATO - distribucija d_min, jasan zid oko 47mm
# =====================================================================
def plateau_chart():
    fig, ax = plt.subplots(figsize=(13, 7), dpi=200)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    bins_c = [15, 25, 35, 45, 55, 65, 75]
    counts = [1, 3, 2, 39, 3, 1, 1]
    colors = [MUTED] * 6
    colors[3] = ACCENT
    bars = ax.bar(bins_c, counts, width=8.5, color=colors, edgecolor="none")
    ax.axvline(3, color=GREEN, linewidth=3, linestyle="--")
    ax.text(3, max(counts) * 1.05, "циљ: 3mm", color=GREEN, fontsize=13, ha="left")
    for x, c in zip(bins_c, counts):
        if c >= 10:
            ax.text(x, c + 1.2, f"{c}/50", ha="center", color=FG, fontsize=15, fontweight="bold")
    ax.set_xlim(-2, 82)
    ax.set_ylim(0, 46)
    ax.set_xlabel("растојање врха од порта  [mm]", color=FG, fontsize=14)
    ax.tick_params(colors=MUTED, labelsize=11)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.set_yticks([])
    ax.xaxis.label.set_color(FG)
    save(fig, "plateau_chart.png")


# =====================================================================
# 8. IZNENADJENJE: dve razlicite arhitekture, isti zid
# =====================================================================
def surprise_wall():
    fig, ax = new_fig(12, 12)
    cx, cy, r = 50, 50, 32
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, edgecolor=MUTED, linewidth=2, alpha=0.4))
    # "zid" - deblji luk tik uz prsten
    wall_theta = np.linspace(160, 260, 60) * np.pi / 180
    wx = cx + (r + 4) * np.cos(wall_theta)
    wy = cy + (r + 4) * np.sin(wall_theta)
    ax.plot(wx, wy, color=RED, linewidth=10, solid_capstyle="round", alpha=0.85)

    for color, ang0, label in [(BLUE, 205, "ACT"), (ORANGE, 235, "DP")]:
        theta = np.linspace(ang0 - 25, ang0, 30) * np.pi / 180
        path_r = np.linspace(85, r + 9, 30)
        px = cx + path_r * np.cos(theta)
        py = cy + path_r * np.sin(theta)
        ax.plot(px, py, linestyle=(0, (2, 3)), color=color, linewidth=3)
        ax.plot(px[-1], py[-1], marker="o", markersize=15, color=color, zorder=6)

    ax.text(cx, cy - 4, "47mm", ha="center", va="center", color=FG, fontsize=26, fontweight="bold")
    ax.text(cx, cy - 14, "исти зид", ha="center", va="center", color=RED, fontsize=15)
    save(fig, "surprise_wall.png")


if __name__ == "__main__":
    symbol_ring()
    symbol_ring_small()
    hook_misses()
    for k in range(1, 5):
        pipeline(k)
    rigid_vs_deformable()
    act_vs_dp()
    steps_circle()
    for k in range(1, 5):
        steps_circle(k)
    plateau_chart()
    lateral_target()
    surprise_wall()
    print("done")

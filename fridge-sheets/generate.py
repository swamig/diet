#!/usr/bin/env python3
"""Fridge reference cards — Paragraph-based cells, QR footer."""

import io
import os
import tempfile

import qrcode
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (HRFlowable, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

# ── Colours ──────────────────────────────────────────────────────────────────
TEAL  = colors.HexColor("#1a6b5a")
CREAM = colors.HexColor("#fdf8f0")
GOLD  = colors.HexColor("#c9a846")
LIGHT = colors.HexColor("#e8f4f0")
DARK  = colors.HexColor("#1a2e2a")
WARN  = colors.HexColor("#8b2020")
AMBER = colors.HexColor("#fff3cd")
MINT  = colors.HexColor("#d4edda")

# ── Section styles ────────────────────────────────────────────────────────────
def _s(name, **kw): return ParagraphStyle(name, **kw)

TITLE = _s("T",  fontSize=32, fontName="Helvetica-Bold", textColor=TEAL,
            alignment=TA_CENTER, spaceAfter=6)
SUB   = _s("S",  fontSize=14, fontName="Helvetica", textColor=DARK,
            alignment=TA_CENTER, spaceAfter=18)
H2    = _s("H2", fontSize=20, fontName="Helvetica-Bold", textColor=TEAL,
            spaceBefore=14, spaceAfter=6)
BODY  = _s("B",  fontSize=14, fontName="Helvetica", textColor=DARK, leading=22)
NOTE  = _s("N",  fontSize=11, fontName="Helvetica-Oblique",
            textColor=colors.HexColor("#555555"), leading=17)
WARN_S= _s("W",  fontSize=13, fontName="Helvetica-Bold", textColor=WARN, leading=20)

# ── Cell paragraph styles ─────────────────────────────────────────────────────
_TCH  = _s("TCH",  fontSize=13, fontName="Helvetica-Bold",
            textColor=colors.white, leading=18)
_TC   = _s("TC",   fontSize=13, fontName="Helvetica",
            textColor=DARK, leading=18)
_TCB  = _s("TCB",  fontSize=13, fontName="Helvetica-Bold",
            textColor=DARK, leading=18)
_TCSM = _s("TCSM", fontSize=11, fontName="Helvetica",
            textColor=DARK, leading=16)
_TCSMB= _s("TCSMB",fontSize=11, fontName="Helvetica-Bold",
            textColor=DARK, leading=16)
_TCW  = _s("TCW",  fontSize=12, fontName="Helvetica-Bold",
            textColor=WARN, leading=17)

# ── Cell helpers ──────────────────────────────────────────────────────────────
def _p(t, s): return Paragraph(str(t).replace("\n", "<br/>"), s)
def c(t):   return _p(t, _TC)
def b(t):   return _p(t, _TCB)
def sm(t):  return _p(t, _TCSM)
def smb(t): return _p(t, _TCSMB)
def w(t):   return _p(t, _TCW)

def tbl(rows, col_widths, cmds=None):
    """Build a Table; all string cells become Paragraphs for correct alignment."""
    def wrap(cell, hdr):
        if isinstance(cell, str):
            return _p(cell, _TCH if hdr else _TC)
        return cell
    data = [[wrap(cell, r == 0) for cell in row] for r, row in enumerate(rows)]
    base = [
        ("ROWBACKGROUNDS",  (0,0), (-1,-1), [CREAM, LIGHT]),
        ("BACKGROUND",      (0,0), (-1,0),  TEAL),
        ("GRID",            (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN",          (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",      (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",   (0,0), (-1,-1), 7),
        ("LEFTPADDING",     (0,0), (-1,-1), 8),
        ("RIGHTPADDING",    (0,0), (-1,-1), 8),
    ]
    if cmds:
        base += cmds
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(base))
    return t

# ── QR code + footer ──────────────────────────────────────────────────────────
GITHUB_URL = "https://github.com/swamig/bluevedaprotocol"

def _build_qr_file():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=1,
    )
    qr.add_data(GITHUB_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name)
    tmp.close()
    return tmp.name

_QR_PATH = _build_qr_file()

def _footer(canvas, doc):
    canvas.saveState()
    w_page = doc.pagesize[0]
    lm = doc.leftMargin
    rm = doc.rightMargin
    qr_size = 0.48 * inch
    footer_y = 0.22 * inch
    line_y   = 0.42 * inch
    canvas.setStrokeColor(colors.HexColor("#bbbbbb"))
    canvas.setLineWidth(0.5)
    canvas.line(lm, line_y, w_page - rm, line_y)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(lm, footer_y, GITHUB_URL)
    canvas.drawImage(
        _QR_PATH,
        w_page - rm - qr_size,
        0.04 * inch,
        width=qr_size, height=qr_size,
        preserveAspectRatio=True,
    )
    canvas.restoreState()

def mk_doc(path, margins=0.55):
    m = margins * inch
    return SimpleDocTemplate(path, pagesize=letter,
                             leftMargin=m, rightMargin=m,
                             topMargin=m, bottomMargin=0.65 * inch)

def _build(doc, story):
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)

# ─────────────────────────────────────────────────────────────────────────────
# CARD 1 — Produce Cleaning
# ─────────────────────────────────────────────────────────────────────────────
def card_produce():
    d = mk_doc("fridge-sheets/01-produce-cleaning.pdf")
    s = []
    s.append(Paragraph("Produce Cleaning", TITLE))
    s.append(Paragraph("Mandatory before every batch — both baths single-use only", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    s.append(Paragraph("① Alkaline Soak", H2))
    s.append(tbl([
        ["Water",    "Baking Soda", "Soak Time"],
        ["1 gallon", "1 tbsp",      "12–15 min"],
        ["1 quart",  "¾ tsp",       "12–15 min"],
        ["1 cup",    "¼ tsp",       "12–15 min"],
    ], [2.2*inch, 2.2*inch, 2.2*inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Use cold water. Fully submerge. Removes up to 96% of surface pesticides.", NOTE))

    s.append(Paragraph("② Acid Rinse (fresh bowl, fresh water)", H2))
    s.append(tbl([
        ["Water",   "Vinegar",   "Rinse Time"],
        ["1 cup",   "1–2 tbsp",  "2–3 min"],
        ["1 quart", "4–8 tbsp",  "2–3 min"],
    ], [2.2*inch, 2.2*inch, 2.2*inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph(
        "White vinegar or ACV. Kills residual bacteria; neutralises baking soda residue. "
        "Minimum 2 min at this dilution — do not shorten.", NOTE))

    s.append(Paragraph("③ Plain Cold Water Rinse", H2))
    s.append(Paragraph("30-second rinse to remove vinegar taste.", BODY))

    s.append(Paragraph("④ Dry — Mandatory", H2))
    s.append(Paragraph("Spin dry or pat with paper towels. Storing wet causes rapid oxidation.", BODY))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  BOTH BATHS ARE SINGLE-USE — discard after every batch. "
        "Reusing recontaminates the next batch.", WARN_S))

    s.append(Spacer(1, 12))
    s.append(Paragraph("Buy Organic for the Dirty Dozen", H2))
    s.append(Paragraph(
        "Kale · Arugula · Spinach · Blueberries · Strawberries · Peaches · "
        "Pears · Nectarines · Apples · Grapes · Bell Peppers · Cherries", BODY))

    _build(d, s)
    print("✓ 01-produce-cleaning.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 2 — Salad Dressing
# ─────────────────────────────────────────────────────────────────────────────
def card_dressing():
    d = mk_doc("fridge-sheets/02-salad-dressing.pdf")
    s = []
    s.append(Paragraph("Master Salad Dressing", TITLE))
    s.append(Paragraph("7-day batch — make every Sunday", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=18))

    s.append(Paragraph("Sunday Batch (glass mason jar)", H2))
    s.append(tbl([
        ["Ingredient",        "Amount",  "Notes"],
        [b("Olive Oil"),        b("14 tbsp"), "Or: 7 tbsp Terra Delyssa + 7 tbsp Snake Oil"],
        [b("Balsamic Vinegar"), b("7 tbsp"),  "Just under ½ cup"],
        [b("Tomato Puree"),     b("7 tbsp"),  "Just under ½ cup"],
        [b("Dijon Mustard"),    b("7 tsp"),   "Sugar-free"],
    ], [2.6*inch, 1.4*inch, 3.0*inch]))
    s.append(Spacer(1, 6))
    s.append(Paragraph(
        "Whisk or shake vigorously until fully emulsified. "
        "Store in a dark spot in the fridge if using Snake Oil.", NOTE))

    s.append(Spacer(1, 16))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))

    s.append(Paragraph("Daily Use (at 14:30 — each serving)", H2))
    s.append(tbl([
        ["What",                 "Amount",    "How"],
        [b("Dressing from jar"),  b("4 tbsp"),  "Pour over assembled greens"],
        [b("Turmeric (ground)"),  b("½ tsp"),   "Sprinkle on WET dressing before tossing"],
        [b("Black Pepper"),       b("¼ tsp"),   "Grind FRESH — sprinkle on wet dressing"],
    ], [2.6*inch, 1.4*inch, 3.0*inch],
    [("BACKGROUND", (0,3), (-1,3), AMBER)]))
    s.append(Spacer(1, 8))
    s.append(Paragraph(
        "Turmeric and pepper go on the wet dressing — never pre-mixed into the jar.", NOTE))

    s.append(Spacer(1, 14))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  Do NOT add Turmeric or Black Pepper to the master jar — "
        "they go on fresh at eating time only.", WARN_S))

    s.append(Spacer(1, 16))
    s.append(Paragraph("Lipid Lever (Coconut Milk days)", H2))
    s.append(Paragraph(
        "If you add Coconut Milk to your 12:00 Chaas, subtract 1–2 tbsp oil from "
        "the 14:30 dressing to keep total lipid load balanced.", BODY))

    _build(d, s)
    print("✓ 02-salad-dressing.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 3 — Salad Assembly + Seed Rotation
# ─────────────────────────────────────────────────────────────────────────────
def card_salad():
    d = mk_doc("fridge-sheets/03-salad-assembly.pdf")
    s = []
    s.append(Paragraph("14:30 Salad Assembly", TITLE))
    s.append(Paragraph("Build in a 56 oz glass container", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    s.append(Paragraph("Assembly Order", H2))
    s.append(tbl([
        ["Layer",             "What",                              "Amount"],
        [b("① Bitter Green"), "Arugula / Watercress / Kale*",     "2 cups"],
        [b("② Anchors"),      b("Broccoli Microgreens"),           "1 cup"],
        ["",                  "Fresh Cilantro",                    "¼ cup"],
        [b("③ Probiotic"),    "Sauerkraut or Kimchi (raw/unpast.)","¼ cup"],
        [b("④ Seed"),         "Day's seed (see table below)",      "1 tbsp"],
        [b("⑤ Dressing"),     "Master dressing from fridge jar",   "4 tbsp"],
        [w("⑥ Activate"),     w("Turmeric (ground)"),              w("½ tsp")],
        ["",                  w("Black Pepper — grind FRESH"),     w("¼ tsp")],
    ], [1.3*inch, 3.3*inch, 1.8*inch],
    [("BACKGROUND", (0,7), (-1,8), AMBER)]))
    s.append(Spacer(1, 5))
    s.append(Paragraph("* Kale: massage with lemon + salt 60 sec to break cell walls.", NOTE))
    s.append(Paragraph(
        "⑥ Sprinkle turmeric and fresh-ground pepper on the wet dressing before tossing.", NOTE))

    s.append(Spacer(1, 14))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))

    s.append(Paragraph("Weekly Seed Rotation (1 tbsp each)", H2))
    s.append(tbl([
        ["Mon",          "Tue",    "Wed",          "Thu",     "Fri",          "Sat",     "Sun"],
        [b("Basil\nSeeds"),b("Sesame"),b("Basil\nSeeds"),b("Walnuts"),b("Basil\nSeeds"),b("Pumpkin"),b("Hemp")],
        [sm("Iron/\nCooling"),sm("Mineral"),sm("Iron/\nCooling"),sm("Omega-3"),sm("Iron/\nCooling"),sm("Zinc"),sm("Protein")],
    ], [0.93*inch]*7,
    [
        ("BACKGROUND", (0,1), (0,1), MINT),
        ("BACKGROUND", (2,1), (2,1), MINT),
        ("BACKGROUND", (4,1), (4,1), MINT),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Green = workout days (Mon/Wed/Fri).", NOTE))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  Never put seeds in the 17:30 post-workout shake — "
        "mucilage gel slows protein absorption.", WARN_S))

    _build(d, s)
    print("✓ 03-salad-assembly.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 4 — Daily Timing
# ─────────────────────────────────────────────────────────────────────────────
def card_timing():
    d = mk_doc("fridge-sheets/04-daily-timing.pdf")
    s = []
    s.append(Paragraph("Daily Rhythm", TITLE))
    s.append(Paragraph("Protocol at a glance", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    s.append(tbl([
        ["Time",     "Action",            "Key Detail"],
        [b("06:30"), b("Morning Anchor"),  "Cold Plunge — swap Yoga if exhausted"],
        [b("09:15"), b("Morning Hydration"),"Warm Ajwain / Jeera / Matcha"],
        [b("10:00"), b("Tannin Deadline"), "Stop all tea & caffeine"],
        [b("12:00"), b("Main Meal"),       "Protein + starch + spice stack + Jaljeera"],
        [b("13:00"), b("Enzyme Pulse"),    "Papaya ½ cup — must follow heavy meal"],
        [b("14:30"), b("Salad Layer"),     "Greens + ferment + seeds + dressing"],
        [b("16:30"), b("Training"),        "Lift (M/W/F) · VO2 Max (Tue) · Rest (Thu/Sat)"],
        [b("17:30"), b("Post-Workout"),    "Whey isolate + creatine"],
        [b("17:50"), b("Recovery Bowl"),   "Yogurt + blueberries + casein"],
        [b("18:30"), b("Heat Rotation"),   "Sauna (Tue/Thu/Sat) · Epsom Bath (M/W/F)"],
        [b("21:00"), b("Night Infusion"),  "Tulsi / Saffron / Ashwagandha"],
    ], [0.75*inch, 1.7*inch, 5.1*inch],
    [
        ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#e3f2fd")),
        ("BACKGROUND", (0,6), (-1,6), MINT),
    ]))

    s.append(Spacer(1, 14))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))
    s.append(Paragraph("Macro Adjustments by Day Type", H2))
    s.append(tbl([
        ["Day Type",        "Quinoa (12:00)", "Casein (17:50)", "Salad Dressing"],
        [b("Heavy Lift"),    "½ cup",          "1 scoop",         "4 tbsp"],
        [b("VO2 Max (Tue)"), "¾ cup",          "1 scoop",         "4 tbsp"],
        [b("Rest / Cardio"), "¼ cup",          w("SKIP"),         "2–4 tbsp"],
    ], [2.0*inch, 1.6*inch, 1.6*inch, 2.2*inch]))

    s.append(Spacer(1, 12))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  NEVER cold plunge immediately after a heavy lift — "
        "blunts mTOR / growth signal. Keep cold exposure to 06:30 AM only.", WARN_S))

    _build(d, s)
    print("✓ 04-daily-timing.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 5 — Morning Drink
# ─────────────────────────────────────────────────────────────────────────────
def card_morning_drink():
    d = mk_doc("fridge-sheets/05-morning-drink.pdf")
    s = []
    s.append(Paragraph("Morning Drink", TITLE))
    s.append(Paragraph("09:15 — must be warm/hot — finish by 10:00 AM", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=18))

    s.append(tbl([
        ["Day",                       "Base Spice",              "Amount",   "Method"],
        [b("Odd days\n(1 · 3 · 5 · 7)"), b("Ajwain seeds"),     b("¼ tsp"), "Boil 1–2 cups water · add seeds · steep 5 min · strain"],
        [b("Even days\n(2 · 4 · 6)"),    b("Whole Jeera\n(cumin seeds)"), b("½ tsp"), "Boil 1–2 cups water · add seeds · steep 5 min"],
    ], [1.5*inch, 1.6*inch, 0.9*inch, 3.55*inch]))

    s.append(Spacer(1, 18))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))
    s.append(Paragraph("Optional Upgrades", H2))
    s.append(tbl([
        ["Add-on",                    "Amount",   "When",                      "How"],
        [b("Matcha powder"),           "1 tsp",    "Any day",                   "Whisk into warm (not boiling) water separately, stir in after steeping"],
        [b("Whole Clove"),             "1 clove",  "Week 2 only\n(replace Jeera day)", "Add to water with seeds, steep together"],
        [b("Cardamom pod (crushed)"),  "1 pod",    "Any day\n(rotator)",        "Crush pod, add to steep"],
        [b("Star Anise"),              "1 whole",  "Antiviral pulse\n(rotator)","Add to steep — strong flavour, use sparingly"],
    ], [1.8*inch, 0.9*inch, 1.4*inch, 3.45*inch]))

    s.append(Spacer(1, 14))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  TANNIN DEADLINE — 10:00 AM. Matcha catechins block iron absorption by up to 3×. "
        "All tea/caffeine must be finished 2 hours before the 12:00 main meal.", WARN_S))

    s.append(Spacer(1, 12))
    s.append(Paragraph("The Warm Start Rule", H2))
    s.append(Paragraph(
        "Must be consumed warm to hot — never cold before 10:00. "
        "Do NOT use alkaline water — it neutralises the acids needed for Agni.", BODY))

    s.append(Spacer(1, 14))
    s.append(Paragraph("Sunday Prep Shortcut", H2))
    s.append(Paragraph(
        "Pre-portion 7 small containers on Sunday — each holds one day's base spice. "
        "Alternates automatically. Add 1 tsp Matcha to each pack if using.", BODY))

    _build(d, s)
    print("✓ 05-morning-drink.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 6 — Batch Session Flip (front=3-week, back=3-month)
# ─────────────────────────────────────────────────────────────────────────────
def card_batch_flip():
    d = mk_doc("fridge-sheets/06-batch-session.pdf")
    s = []

    s.append(Paragraph("3-Week Batch Session", TITLE))
    s.append(Paragraph("Run every 3 weeks · ~85 min · one person · no cooking after tadka", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Night Before", H2))
    s.append(Paragraph("Soak 4 tbsp fenugreek seeds in water overnight.", BODY))

    s.append(Paragraph("Session Timeline", H2))
    s.append(tbl([
        ["Time",      "Step",                                                  "Output"],
        ["T+0:00",    "Setup — ingredients out, start water boiling",           "—"],
        ["T+0:05",    "Pre-chop: curry leaves (½\" pieces), break chili to flakes","—"],
        [b("T+0:08"), w("Tadka — mustard seeds pop → curry leaves + chili + hing\n→ BLOOM 15–20 SEC EXACTLY → off heat → cool 5 min"), w("~21 cubes")],
        ["T+0:15",    "Blanch mint + cilantro together — 10–15 SEC, ice bath, squeeze, separate into two piles","—"],
        ["T+0:20",    "Pour cooled tadka into mini tray (1 tsp per cell)",      "21 cubes"],
        ["T+0:22",    "Blend Jaljeera concentrate → pour into tray",            "21 cubes"],
        ["T+0:27",    "Blend cilantro chutney → pour into tray",               "17–18 cubes"],
        ["T+0:32",    "Blend coconut chutney — 2 Vitamix runs × 6 min",        "48 cubes"],
        ["T+0:44",    "Blend mint muddle → pour into mini tray",               "21 cubes"],
        ["T+0:54",    "Fenugreek paste — drain seeds, blend immersion, pour",   "12–14 cubes"],
        ["T+1:04",    "Aloe topical refresh (only if running low)",             "~14–28 cubes"],
        ["T+1:19",    "Label all trays, freeze flat — do NOT stack until frozen","—"],
        ["T+1:24",    "Cleanup",                                                "Done"],
    ], [0.7*inch, 4.3*inch, 1.5*inch],
    [("BACKGROUND", (0,3), (-1,4), AMBER)]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("Key Ratios & Rules", H2))
    s.append(tbl([
        ["Item",                    "Critical Number",     "Rule"],
        [b("Tadka bloom"),           b("15–20 sec exactly"),"Beyond 30 sec → alkaloids degrade. Use a timer."],
        [b("Blanch time"),           b("10–15 sec"),        "Set timer. Ice bath ≥1:1 ice:water ratio."],
        [b("Coconut per Vitamix"),   b("4 cups max"),       "One run = 4 cups → ~24 cubes. 2 runs = 48."],
        [b("Mini cube size"),        b("1 tsp per cell"),   "Tadka, mint muddle, fenugreek, ginger cubes."],
        [b("Regular cube size"),     b("~2 tbsp per cell"), "Jaljeera, cilantro chutney, coconut chutney."],
        [b("Freeze stability"),      b("3 weeks"),          "Cilantro, coconut, Jaljeera, mint muddle."],
    ], [1.6*inch, 1.6*inch, 4.3*inch]))

    s.append(PageBreak())

    s.append(Paragraph("3-Month Big Session", TITLE))
    s.append(Paragraph("Run every 3 months · ~half day across 2 days · RS3 chill is the bottleneck", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Night Before Day 1", H2))
    s.append(Paragraph(
        "Clear chest freezer. Soak chickpeas (5 kg) and black beans (4.5 kg) separately overnight.", BODY))

    s.append(Paragraph("Day 1 — Cook & Chill (~4h active)", H2))
    s.append(tbl([
        ["Order", "Task",                                                          "RS3 Rule"],
        [b("1st"), "Cook chickpeas + black beans — pressure cook or boil until tender", w("CHILL 24h in fridge before freezing")],
        [b("2nd"), "Cook quinoa — 1 cup dry : 1.75 cups water, simmer 12 min, spread thin in 88oz Pyrex", w("CHILL 24h in fridge before freezing")],
        [b("3rd"), "Cook lentils — simmer 20–25 min, spread thin to cool",         w("Chill 12–24h")],
        [b("4th"), "Freeze tofu slabs raw — slice 400g block into 4–6 slabs, flat bags","No chill needed"],
        [b("5th"), "Juice 50 lemons → ice cube trays → freeze",                    "No chill needed"],
        [b("6th"), "Imli-Khajur chutney — Medjool dates + Tropica tamarind\n→ blend → 24 qt pot → cook 15–20 min → cool → freeze (card 13)", "~96 cubes"],
        [b("7th"), "Aloe gel cubes — drain latex 10–15 min → fillet → scoop → blend → tray","No chill needed"],
    ], [0.5*inch, 4.2*inch, 2.85*inch],
    [("BACKGROUND", (0,1), (-1,3), AMBER)]))

    s.append(Paragraph("Day 2 — Portion & Freeze (~2h)", H2))
    s.append(tbl([
        ["Task",                                         "Portion",       "Into"],
        [b("Chickpeas"),                                  "1.5 cups cooked","Flat freezer bags"],
        [b("Black beans"),                                "1.5 cups cooked","Flat freezer bags"],
        [b("Quinoa"),                                     "½ cup cooked",  "Flat freezer bags"],
        [b("Lentils"),                                    "½ cup cooked",  "Flat freezer bags"],
        [b("Ginger knobs (freeze whole)"),                "~2 kg total",   "One large bag"],
        [b("Garlic (freeze peeled cloves)"),              "~25 heads",     "One bag"],
        [b("Cilantro — blanch 10–15 sec then freeze"),   "15 large bunches","Bags by batch"],
        [b("Mint — blanch 10–15 sec then freeze"),        "8 large bunches","Bags by batch"],
        [b("Chilies — freeze whole"),                     "All varieties", "Labeled bags"],
    ], [3.3*inch, 1.8*inch, 2.45*inch]))

    s.append(Spacer(1, 8))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  RS3 RULE — chickpeas, black beans, quinoa, lentils MUST chill 12–24h in the fridge "
        "before going into the freezer. This is the hard bottleneck. Fridge must be fully cleared "
        "the night before Day 1.", WARN_S))

    s.append(Spacer(1, 8))
    s.append(Paragraph("Spice Jars — Refill on 3-Month Day", H2))
    s.append(Paragraph(
        "Check dry jars: Kashmiri chili (~50g), Turmeric (~150g), Cumin seeds (~200g), "
        "Cumin powder (~100g), Coriander powder (~100g), Black pepper whole (~100g), "
        "Ajwain (~50g), Nigella (~50g), Mustard seeds (~50g), Hing (~10g).", BODY))

    _build(d, s)
    print("✓ 06-batch-session.pdf  (duplex: front=3-week, back=3-month)")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 7 — Tofu Day-Of Prep
# ─────────────────────────────────────────────────────────────────────────────
def card_tofu():
    d = mk_doc("fridge-sheets/07-tofu-prep.pdf")
    s = []
    s.append(Paragraph("Tofu Day-Of Prep", TITLE))
    s.append(Paragraph("Extra-firm only · freeze-thaw → brine → press → sear · 2×/week", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    s.append(Paragraph("Step 1 — Thaw", H2))
    s.append(tbl([
        ["Method",             "Time",      "Notes"],
        [b("Fridge overnight"), "8–12 h",   "Preferred — slow thaw preserves texture best"],
        [b("Cold water fast"),  "30–60 min", "Submerge sealed bag in cold water"],
    ], [2.0*inch, 1.2*inch, 4.35*inch]))

    s.append(Paragraph("Step 2 — Salt Brine", H2))
    s.append(tbl([
        ["Water",    "Salt",   "Boil Level",        "Time"],
        [b("4 cups"), b("1 tsp"), b("Full rolling boil"), b("3–5 min")],
        ["2 cups",   "½ tsp",  "Full rolling boil", "3–5 min"],
        ["8 cups",   "2 tsp",  "Full rolling boil", "3–5 min"],
    ], [1.5*inch, 1.2*inch, 2.5*inch, 1.8*inch],
    [("BACKGROUND", (0,1), (-1,1), MINT)]))
    s.append(Spacer(1, 5))
    s.append(Paragraph(
        "Full boil expels ice-crystal water and opens pores — salt seasons from inside out. "
        "Remove slabs, transfer to clean surface.", NOTE))

    s.append(Paragraph("Step 3 — Press", H2))
    s.append(Paragraph(
        "5 minutes — slabs on a clean towel, heavy pan on top. "
        "Most water exits during the brine; this is the final dry.", BODY))

    s.append(Paragraph("Step 4 — Marinate (Optional — 15–20 min)", H2))
    s.append(tbl([
        ["Option",         "Recipe"],
        [b("Tamari"),       "2 tbsp tamari + 1 ginger cube (melted) + 1 tsp ACV — soak 15 min"],
        [b("Dry rub"),      "Spice mix (turmeric + cumin + coriander + Kashmiri chili) rubbed onto slab — no wait time"],
    ], [1.5*inch, 6.05*inch]))

    s.append(Spacer(1, 14))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))
    s.append(Paragraph("Step 5 — Flash Sear (Allicin Pulse)", H2))
    s.append(tbl([
        ["Clock",     "Action"],
        [b("00:00"),  w("Crush 2–3 garlic cloves — REST 10 MINUTES (allicin formation — non-negotiable)")],
        [b("00:10"),  "COLD START — 2 tbsp avocado oil + methi seeds + chili + rested garlic into COLD pan"],
        [b("00:11"),  "Turn to LOW — bloom 5 min until garlic barely sizzles"],
        [b("00:16"),  "Turn to MEDIUM-HIGH — add tofu slabs — sear 60–90 sec per side until golden crust"],
        [b("00:25"),  "Off heat — tear 5–6 fresh mint (Mentha arvensis) leaves over hot tofu"],
        [b("00:26"),  "Serve immediately with Peppermint Jaljeera"],
    ], [0.75*inch, 6.8*inch],
    [
        ("BACKGROUND", (0,1), (-1,1), AMBER),
        ("BACKGROUND", (0,5), (-1,5), LIGHT),
    ]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  10-minute garlic rest is non-negotiable — alliinase needs time to convert "
        "alliin → allicin before heat destroys it. Crush first, then prep everything else.", WARN_S))

    s.append(Spacer(1, 10))
    s.append(Paragraph("Wet Curry Variant", H2))
    s.append(Paragraph(
        "At 00:25: add 2–3 tbsp coconut milk, stir 30–60 sec into a glaze. "
        "Subtract 1 tbsp oil from the 14:30 salad dressing (Lipid Substitution Rule).", BODY))

    _build(d, s)
    print("✓ 07-tofu-prep.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 8 — Rotations
# ─────────────────────────────────────────────────────────────────────────────
def card_rotations():
    d = mk_doc("fridge-sheets/08-rotations.pdf")
    s = []
    s.append(Paragraph("Protocol Rotations", TITLE))
    s.append(Paragraph("Daily · Weekly · 4-Week cycle", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Daily Rotations", H2))
    s.append(tbl([
        ["What",               "Mon",          "Tue",       "Wed",          "Thu",       "Fri",          "Sat",       "Sun"],
        [b("Morning\n09:15"),  b("Ajwain\n¼ tsp"),b("Jeera\n½ tsp"),b("Ajwain\n¼ tsp"),b("Jeera\n½ tsp"),b("Ajwain\n¼ tsp"),b("Jeera\n½ tsp"),b("Ajwain\n¼ tsp")],
        [b("Seed\n1 tbsp"),    sm("Basil"),    sm("Sesame"),sm("Basil"),    sm("Walnuts"),sm("Basil"),    sm("Pumpkin"),sm("Hemp")],
        [b("Heat\n18:30"),     sm("Epsom"),    sm("Sauna"), sm("Epsom"),    sm("Sauna"), sm("Epsom"),    sm("Sauna"), sm("—")],
        [b("Training\n16:30"), sm("Lift"),     sm("VO2"),   sm("Lift"),     sm("Rest"),  sm("Lift"),     sm("Rest"),  sm("—")],
    ], [1.3*inch] + [0.89*inch]*7,
    [
        ("BACKGROUND", (1,1), (1,1), MINT),
        ("BACKGROUND", (3,1), (3,1), MINT),
        ("BACKGROUND", (5,1), (5,1), MINT),
        ("BACKGROUND", (7,1), (7,1), MINT),
        ("BACKGROUND", (1,3), (1,3), MINT),
        ("BACKGROUND", (3,3), (3,3), MINT),
        ("BACKGROUND", (5,3), (5,3), MINT),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))
    s.append(Spacer(1, 5))
    s.append(Paragraph("Green = workout days.", NOTE))

    s.append(Paragraph("Night Infusion (21:00) — pick by day type", H2))
    s.append(tbl([
        ["Infusion",        "When to use"],
        [b("Ashwagandha"),   "High-cortisol days · tofu-pulse days · VO2 Max (Tue) — mandatory. Do NOT use daily."],
        [b("Tulsi"),         "Lower-stimulation recovery nights · standard rest recovery"],
        [b("Saffron"),       "Parasympathetic emphasis · end-of-day downshift · Week 4 washout"],
    ], [1.5*inch, 6.05*inch]))

    s.append(Paragraph("Weekly Rotations — pick one per category per week", H2))
    s.append(tbl([
        ["Category",                    "Option A",                        "Option B",                          "Option C"],
        [b("Bitter green\n(2 cups)"),    "Arugula\n(high nitrate/NO)",       "Watercress\n(PEITC / dense)",       "Kale*\n(massage 60 sec)"],
        [b("Dry Podi\n(1 tbsp/day)"),   sm("Hormonal Buffer Podi\n(flax + moringa + cumin)"), sm("Vascular Podi\n(sesame + curry leaf + bay leaf + cumin)"), sm("—")],
        [b("Chutney\n(1–2 tbsp)"),       "Coconut\n(MCT + curry leaf)",      "Cilantro/Mint TRP",                "—"],
        [b("Recovery\nextras"),          w("Cacao + vanilla\n(2–3×/week MAX — never daily)"), "Plain bowl\n(rest days)", "—"],
    ], [1.4*inch, 2.1*inch, 2.1*inch, 2.0*inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("* Tofu: 2×/week ceiling — never more. Phytoestrogen accumulation risk.", WARN_S))

    s.append(Paragraph("4-Week Cycle — what shifts each week", H2))
    s.append(tbl([
        ["Week",     "Theme",                     "Morning drink",                       "Special rules"],
        [b("Wk 1"),  b("Baseline &\nAnti-inflam."), "Ajwain / Jeera basic rotation",     "No clove. Establish timing. Follow daily anchors strictly."],
        [b("Wk 2"),  b("Antimicrobial\nPeak"),      "Add Clove 2 mornings\n(replace 2 Jeera days)", "Clove only on Day 9 + Day 12. Sulfur emphasis. Watch gut."],
        [b("Wk 3"),  b("Vascular &\nNitric Peak"),  "Ajwain / Jeera basic rotation",     "Arugula/Watercress priority for NO. Omega-3 week. Monitor logs."],
        [b("Wk 4"),  b("Washout &\nReset"),         "Ajwain / Jeera basic rotation",     "REMOVE all heavy antimicrobials. Tulsi/Saffron at night. Optional: Detox Week (chlorella + double cilantro + extra tamarind)."],
    ], [0.65*inch, 1.3*inch, 1.9*inch, 3.8*inch],
    [
        ("BACKGROUND", (0,2), (-1,2), AMBER),
        ("BACKGROUND", (0,4), (-1,4), LIGHT),
    ]))

    s.append(Spacer(1, 6))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    s.append(Paragraph(
        "⚠  Daily anchors never rotate: Broccoli microgreens · Fresh cilantro · "
        "Turmeric + black pepper · Ginger · Brazil nut (1–2/day).", WARN_S))

    _build(d, s)
    print("✓ 08-rotations.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 9 — Skincare
# ─────────────────────────────────────────────────────────────────────────────
def card_skincare():
    d = mk_doc("fridge-sheets/09-skincare.pdf")
    s = []
    s.append(Paragraph("Skincare & Hair", TITLE))
    s.append(Paragraph("Ayurvedic topical protocols — batch system", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Weekly Schedule", H2))
    s.append(tbl([
        ["Day",           "Hair Mask", "Face Mask", "Body Ubtan", "Leave time"],
        [b("Wednesday"),  b("✓"),      b("✓"),      b("✓"),       "Hair 30–45 min · Face 10–15 min · Body 5–10 min (pre-shower)"],
        [b("Sunday"),     b("✓"),      b("✓"),      "—",          "Hair 30–45 min · Face 10–15 min"],
    ], [0.9*inch, 0.8*inch, 0.8*inch, 0.9*inch, 5.15*inch],
    [("ALIGN", (1,0), (3,2), "CENTER")]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))
    s.append(Paragraph("Per-Application Recipe", H2))
    s.append(tbl([
        ["Protocol",      "Dry mix",              "Wet cubes",                                 "Oil",                      "Extra"],
        [b("Hair Mask"),  b("2 tbsp\nDry Hair"),   "1 fenugreek cube (thawed)\n1 aloe cube (thawed)", "1 tbsp coconut\n(melted)",  "3–5 drops Rosemary EO\nmixed into oil first"],
        [b("Face Mask"),  b("1 tsp\nDry Face"),    "1 aloe cube (thawed)\nor rose water to bind",     sm("Tiny drop coconut\n(dry skin only)"), "Avoid eye area.\n10–15 min."],
        [b("Body Ubtan"), b("2 tbsp\nDry Body"),   "1 aloe cube (thawed)",                      "1 tbsp coconut\nor sesame oil",sm("Apply to damp skin,\ncircular motions.\nScrub off in shower.")],
    ], [1.1*inch, 1.4*inch, 1.9*inch, 1.5*inch, 1.75*inch]))
    s.append(Spacer(1, 5))
    s.append(Paragraph(
        "Hair mask: scalp first, massage 2–3 min, then through lengths. "
        "Rinse while still slightly damp — do NOT let fully dry/harden.", NOTE))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))
    s.append(Paragraph("Dry Mix Jar Recipes", H2))
    s.append(tbl([
        ["Jar",             "Ingredient",                                "Amount"],
        [b("DRY HAIR MIX"), b("Amla powder"),                            "4 tbsp"],
        ["",                "Curry Leaf Powder (air-dried)",              "1 tsp"],
        ["",                "Rotating powder — see 3-month cycle below", "4 tbsp"],
        ["",                sm("Fenugreek powder (backup if no cubes)"),  sm("2 tbsp")],
        [b("DRY FACE MIX"), b("Besan (chickpea flour)"),                 "4 tbsp"],
        ["",                "Amla powder",                               "2 tbsp"],
        ["",                "Turmeric",                                  "1 tsp"],
        ["",                w("Bay Leaf Powder (tejpatta)"),              w("¼ tsp MAX")],
        [b("DRY BODY MIX"), b("Besan (chickpea flour)"),                 "6 tbsp"],
        ["",                "Amla powder",                               "2 tbsp"],
        ["",                "Turmeric",                                  "1.5 tsp"],
        ["",                w("Neem powder (Month 3 only)"),             w("3 tbsp")],
    ], [1.4*inch, 4.0*inch, 1.25*inch],
    [
        ("BACKGROUND", (0,1), (-1,4),  CREAM),
        ("BACKGROUND", (0,5), (-1,8),  LIGHT),
        ("BACKGROUND", (0,9), (-1,12), CREAM),
    ]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))
    s.append(Paragraph("3-Month Hair Powder Cycle (the 4 tbsp rotating slot)", H2))
    s.append(tbl([
        ["Month",    "Powder",                       "What it does"],
        [b("Month 1"), b("Brahmi\n(Bacopa monnieri)"), "Reduces scalp inflammation, strengthens shaft, cortisol-driven hair loss"],
        [b("Month 2"), b("Bhringraj\n(Eclipta alba)"),  "Stimulates follicles, reduces shedding"],
        [b("Month 3"), b("Neem\n(Azadirachta indica)"), "Antifungal, anti-dandruff, clears scalp bacteria\n→ also add 3 tbsp Neem to Dry Body Mix this month"],
    ], [0.9*inch, 1.7*inch, 5.05*inch],
    [("BACKGROUND", (0,3), (-1,3), AMBER)]))

    s.append(Spacer(1, 8))
    s.append(Paragraph("Cube Consumption (per week)", H2))
    s.append(tbl([
        ["Protocol",         "Freq/week",    "Aloe cubes", "Fenugreek cubes"],
        [b("Hair mask"),      "2× (Wed+Sun)", b("2"),       "2"],
        [b("Face mask"),      "2× (Wed+Sun)", b("2"),       "0"],
        [b("Body ubtan"),     "1× (Wed)",     b("1"),       "0"],
        [b("TOTAL / week"),   "",             b("5"),       b("2")],
    ], [1.8*inch, 1.6*inch, 1.6*inch, 2.55*inch],
    [
        ("BACKGROUND", (0,4), (-1,4), LIGHT),
        ("ALIGN", (2,0), (3,4), "CENTER"),
    ]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "3-month supply: ~65 aloe cubes (5 tray batches, 5 leaves) · "
        "~26 fenugreek cubes (4 tbsp seeds every 6 weeks).", NOTE))

    s.append(Spacer(1, 8))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    s.append(Paragraph(
        "⚠  Aloe — drain latex 10–15 min (stand cut-end down) before scooping gel. Aloin irritates skin. "
        "Bay leaf ¼ tsp max — sensitizer at high dose. "
        "Turmeric stains hair yellow — omit or 1/8 tsp max.", WARN_S))

    _build(d, s)
    print("✓ 09-skincare.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 10 — Workout (front=weekly split, back=yoga+thermal)
# ─────────────────────────────────────────────────────────────────────────────
def card_workout():
    d = mk_doc("fridge-sheets/10-workout.pdf")
    s = []

    s.append(Paragraph("Weekly Training Split", TITLE))
    s.append(Paragraph("The Operator Split — Legs / Push / Pull / VO2 / Recovery", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(tbl([
        ["Day",     "06:30 – 09:00",              "16:30 – 18:00",              "21:00 Night",          "Yoga pairing"],
        [b("MON"),  b("Cold Plunge"),              b("HEAVY LEGS"),              "Tulsi",                sm("Half Pigeon\n(hip flexors)")],
        [b("TUE"),  sm("Fasted Cardio\n(Zone 2)"),b("PUSH DAY"),                "Tulsi",                sm("Cobra / Upward Dog\n(chest/shoulders)")],
        [b("WED"),  b("Cold Plunge"),              b("PULL DAY"),                "Saffron",              sm("Thread the Needle\n(thoracic/biceps)")],
        [b("THU"),  b("VO2 Max 4×4"),              "Active Recovery / Walk",     w("Ashwagandha\n(mandatory)"), sm("Legs Up the Wall\n(vagal tone)")],
        [b("FRI"),  b("Cold Plunge"),              b("LIFT ROTATOR\n+ Tofu Pulse"),w("Ashwagandha\n(mandatory)"), sm("Full Body Flush")],
        [b("SAT"),  sm("Active Yoga\n(15–20 min)"),"3-Cycle Contrast Therapy",  "Saffron",              sm("CNS Reset")],
        [b("SUN"),  sm("Batch Meal Prep"),          "Rest / Walk",               "Tulsi",                sm("Gentle Mobility")],
    ], [0.55*inch, 1.5*inch, 1.9*inch, 1.3*inch, 2.35*inch],
    [
        ("BACKGROUND", (0,4), (-1,4), AMBER),
        ("BACKGROUND", (0,7), (-1,7), LIGHT),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    s.append(Spacer(1, 12))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))
    s.append(Paragraph("Diet Adjustments by Day Type", H2))
    s.append(tbl([
        ["Day type",         "12:00 Quinoa",  "17:30",                           "17:50 Casein",                   "14:30 Dressing"],
        [b("Heavy Lift"),    b("½ cup"),       "Whey + creatine\n(strict window)", "1 scoop",                        "4 tbsp"],
        [b("VO2 Max (Thu)"), b("¾ cup\n+50%"),"Whey + creatine",                  "1 scoop",                        "4 tbsp"],
        [b("Rest / Cardio"), b("¼ cup"),       "Whey + creatine",                  w("SKIP\n(no mechanical damage)"), "2–4 tbsp"],
    ], [1.3*inch, 1.1*inch, 2.1*inch, 1.4*inch, 1.65*inch]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    s.append(Paragraph(
        "⚠  COLD PLUNGE RULE — NEVER immediately after heavy lifting. "
        "Blunts mTOR / growth signal. Min 6 hours separation "
        "(cold 06:30 → lift 16:30 is correct). "
        "Morning 'fried'? Swap cold plunge for restorative yoga, skip Matcha.", WARN_S))

    s.append(Spacer(1, 8))
    s.append(Paragraph("VO2 Max 4×4 Progression — do not skip stages", H2))
    s.append(tbl([
        ["Stage",      "Who",                    "Protocol"],
        [b("Stage 1"), b("Novice"),               "Zone 2 fasted walk/jog only — no 4×4s"],
        [b("Stage 2"), b("Intermediate\n(4–8 wk)"),"2×4 intervals (2 reps instead of 4). Monitor HRV."],
        [b("Stage 3"), b("Operator"),             "Full 4×4: 4 min max effort → 3 min active recovery → repeat ×4. Only proceed if resting HR is stable and 21:00 Ashwagandha is maintained."],
    ], [0.75*inch, 1.4*inch, 5.45*inch],
    [("BACKGROUND", (0,3), (-1,3), LIGHT)]))

    s.append(PageBreak())

    s.append(Paragraph("Yoga & Thermal Protocols", TITLE))
    s.append(Paragraph("Autonomic reset sequences + thermal hormesis methods", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Yoga Sequences — which to use when", H2))
    s.append(tbl([
        ["Sequence",                       "When",                                               "Duration",    "Key moves"],
        [b("Active Morning"),               "Replace 06:30 cardio on low-cortisol mornings",      "15–20 min",  sm("Child's Pose → Cat-Cow ×10 → Downward Dog → Ragdoll → Sun Salutation A ×3–5 → Warrior II → Hanuman Dand ×10 → Savasana")],
        [b("Restorative\n(Cortisol Day)"),  "Morning if 'fried' OR 21:00 night infusion window", "15–20 min",  sm("Supported Child's Pose 3–4 min → Supine Spinal Twist 2 min/side → Reclined Bound Angle 3–4 min → LEGS UP WALL 5 min → Savasana")],
        [b("Post-Lift Stretch"),            "Immediately post-workout or active recovery days",   "10–15 min",  sm("Lizard Lunge 2 min/side → Half Pigeon 2 min/side → Thread the Needle 1 min/side → Seated Forward Fold 2 min")],
    ], [1.25*inch, 1.8*inch, 0.9*inch, 3.65*inch],
    [("BACKGROUND", (0,2), (-1,2), AMBER)]))
    s.append(Spacer(1, 5))
    s.append(Paragraph(
        "Restorative breath: inhale 4 sec · exhale 8 sec. "
        "Night yoga: sip Tulsi or Saffron during or immediately after. "
        "Mantra: 'So' on inhale, 'Hum' on exhale — interrupts anxiety loop.", NOTE))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))
    s.append(Paragraph("Thermal Hormesis — three methods", H2))
    s.append(tbl([
        ["Method",                    "When",          "Protocol",                                  "Rule"],
        [b("A — Daily\nMaintenance"), "Daily",          "Cold plunge 06:30\n+ Sauna 18:30 (separate)", sm("Re-warm naturally 10–15 min after cold plunge — activates Brown Adipose Tissue")],
        [b("B — Efficiency\nPump"),   "2–3×/week",     "Sauna 15 min → Cold Plunge 3 min\n(immediate transition)", sm("ALWAYS end on cold. Trains endothelial lining.")],
        [b("C — Weekly\nVascular Flush"), "1×/week (Sat)", "3 continuous cycles:\nSauna → Cold → Sauna → Cold → Sauna → Cold", sm("ALWAYS end on cold. Wait 15 min before warm hydration.")],
    ], [1.1*inch, 1.0*inch, 2.7*inch, 2.85*inch],
    [("BACKGROUND", (0,3), (-1,3), LIGHT)]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))
    s.append(Paragraph("Targeted Yoga Pairings by Lift Day", H2))
    s.append(tbl([
        ["Lift Day",              "Mechanical stress",             "Key pose",              "Why"],
        [b("Mon — HEAVY LEGS"),   "Hip flexors / glute fatigue",   b("Half Pigeon"),        "Unlocks piriformis + glutes — reduces DOMS"],
        [b("Tue — PUSH"),         "Internal shoulder rotation",    b("Cobra / Upward Dog"), "Chest opening counteracts pec shortening"],
        [b("Wed — PULL"),         "Thoracic compression / biceps", b("Thread the Needle"),  "Thoracic rotation + rear delt stretch"],
        [b("Fri — FULL ROTATOR"), "Systemic CNS load",             b("Legs Up the Wall"),   "Vagal nerve stimulation → fastest HRV recovery"],
    ], [1.3*inch, 1.8*inch, 1.3*inch, 3.25*inch]))

    s.append(Spacer(1, 8))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    s.append(Paragraph(
        "⚠  Ice bath > cryo chamber. Water is 25× more thermally conductive than air — "
        "core cooling triggers the sustained dopamine/noradrenaline spike and BAT activation. "
        "Cryo creates an insulating skin boundary layer and cannot replicate this.", WARN_S))

    _build(d, s)
    print("✓ 10-workout.pdf  (duplex: front=weekly split, back=yoga+thermal)")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 11 — Chutney Prep & Blanching
# ─────────────────────────────────────────────────────────────────────────────
def card_chutney():
    d = mk_doc("fridge-sheets/11-chutney-prep.pdf")
    s = []
    s.append(Paragraph("Chutney Prep & Blanching", TITLE))
    s.append(Paragraph("3-week batch · Blanch → Blend → Freeze · done in order below", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("① Blanching — Do First (applies to cilantro AND mint)", H2))
    s.append(tbl([
        ["Step",  "Action",                                             "Time"],
        [b("1"),  "Bring pot of water to a rolling boil",               "—"],
        [b("2"),  w("Submerge cilantro + ALL mint together in boiling water"), w("10–15 sec EXACTLY")],
        [b("3"),  "Transfer immediately to ice bath (≥1:1 ice:water)","30 sec"],
        [b("4"),  "Squeeze out excess water thoroughly",               "—"],
        [b("5"),  "Separate into two piles: cilantro+some mint → chutney / mint only → Jaljeera", "—"],
    ], [0.4*inch, 4.8*inch, 1.5*inch],
    [("BACKGROUND", (0,2), (-1,2), AMBER)]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Why blanch: deactivates polyphenol oxidase (PPO) — the browning enzyme. "
        "10–15 sec deactivates PPO only; chelation compounds and color are preserved.", NOTE))

    s.append(Spacer(1, 8))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("② Curry Leaf Tadka — 1 pan, 5 min · makes ~21 cubes", H2))
    s.append(tbl([
        ["Ingredient",              "Amount",             "Notes"],
        [b("Avocado / coconut oil"), b("7 tbsp (~½ cup)"), "The fat carrier — extracts alkaloids"],
        [b("Mustard seeds"),         b("1 tbsp"),          "Add first — wait for pop (~20 sec)"],
        [b("Fresh curry leaves"),    b("1 cup packed"),    "Rough-chop into ½\" pieces before pan"],
        [b("Dried red chili"),       b("1–1½ tsp flakes"), "Break into flakes — distributes across all 21 cubes"],
        [b("Hing (asafoetida)"),     b("¼ tsp"),           "Add with curry leaves + chili"],
    ], [2.1*inch, 1.6*inch, 3.85*inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Method: heat oil → mustard seeds pop → add curry leaves + chili + hing → "
        "BLOOM 15–20 SEC (use a timer) → off heat → cool 5 min → stir → pour 1 tsp per mini cube cell.", NOTE))
    s.append(Paragraph(
        "⚠  Beyond 30 sec bloom → alkaloids degrade. Do not exceed 20 sec.", WARN_S))

    s.append(Spacer(1, 8))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("③ Cilantro Chutney — 1 Vitamix run · ~17–18 cubes", H2))
    s.append(tbl([
        ["Ingredient",           "Amount",          "Notes"],
        [b("Cilantro (blanched)"), b("4 cups packed"), "From blanching step"],
        [b("Fresh mint (blanched)"),b("2 cups packed"), "Optional — adds brightness"],
        [b("Frozen avocado"),    b("½ cup"),         "Add to blender first with aquafaba"],
        [b("Aquafaba"),          b("1 tbsp"),         "Saponins emulsify avocado fat — add BEFORE herbs"],
        [b("Thai green chilies"), b("4–5"),           ""],
        [b("Garlic (rested 10 min)"), b("4 cloves"), "Crush and rest 10 min for allicin before blending"],
        [b("Fresh ginger"),      b("1 inch knob"),   ""],
        [b("Lemon juice"),       b("4 tbsp"),        "ACID LOCK — critical for color and preservation"],
        [b("Black salt (kala namak)"), b("1 tsp"),   ""],
        [b("Roasted cumin powder"), b("1 tsp"),      ""],
    ], [2.0*inch, 1.4*inch, 4.15*inch],
    [("BACKGROUND", (0,4), (-1,4), AMBER)]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Blend order: aquafaba + frozen avocado 20 sec → add herbs + everything else → "
        "blend 60–90 sec. Pour ~2 tbsp per cube. Freeze immediately.", NOTE))

    s.append(PageBreak())

    s.append(Paragraph("Chutney Prep (continued)", TITLE))
    s.append(Paragraph("Coconut chutney · Jaljeera concentrate", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("④ Coconut Chutney — 2 Vitamix runs · ~48 cubes total", H2))
    s.append(tbl([
        ["Ingredient",            "Per Vitamix run", "× 2 runs total"],
        [b("Fresh grated coconut"), b("4 cups"),       b("8 cups total")],
        [b("Fresh curry leaves"),   b("3–4 tbsp"),     b("6–8 tbsp")],
        [b("Green chili"),          b("4–5"),          b("8–10")],
        [b("Fresh ginger"),         b("2 inch knob"),  b("~180g total")],
        [b("Roasted cumin powder"), b("2 tsp"),        b("4 tsp")],
        [b("Lemon juice"),          b("4 tbsp"),       b("8 tbsp")],
        [b("Water or aquafaba"),    b("½ cup"),        b("1 cup")],
        [b("Salt"),                 b("1 tsp"),        b("2 tsp")],
    ], [2.1*inch, 1.8*inch, 2.65*inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Blend 90 sec per run until smooth. Pour ~2 tbsp per cube. "
        "Rinse blender 10 sec between runs. Yield ~24 cubes per run.", NOTE))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("⑤ Jaljeera Concentrate — 1 Vitamix run · ~21 cubes", H2))
    s.append(tbl([
        ["Ingredient",            "Amount for 21 servings",    "Notes"],
        [b("Mint (blanched)"),     b("~2 cups packed"),         "From blanching step — mint only pile"],
        [b("Thai green chili"),    b("10–12 chilies"),          ""],
        [b("Fresh ginger"),        b("7 tbsp (~200g)"),         ""],
        [b("Lemon juice"),         b("~1¼ cups (~7 cubes)"),    "Or use frozen lemon cubes"],
        [b("ACV (raw)"),           b("~1¼ cups"),               ""],
        [b("Avocado oil"),         b("3½ tbsp"),                "Lipid lock — traps volatile menthol"],
        [b("Hing"),                b("½ tsp"),                  ""],
    ], [2.0*inch, 2.0*inch, 2.55*inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Blend 60 sec. Taste: sharp, minty, spicy, bright. "
        "Pour ~2 tbsp per cube. 21 cubes = 3-week supply at 1/day.", NOTE))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "At serving: add fresh black salt + roasted cumin + ACV + cold/sparkling water. "
        "Never put black salt or cumin in the frozen cube (osmosis bleeds water from paste).", NOTE))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  ACID LOCK IS MANDATORY in cilantro chutney — 4 tbsp lemon juice minimum. "
        "Skipping causes oxidation and grey-green color within 24h even frozen.", WARN_S))

    s.append(Spacer(1, 8))
    s.append(Paragraph("Freeze Stability Reference", H2))
    s.append(tbl([
        ["Item",                  "Shelf life frozen", "Cube size"],
        [b("Tadka cubes"),         "4–6 weeks",         "1 tsp (mini tray)"],
        [b("Jaljeera cubes"),      "3 weeks",           "~2 tbsp (regular tray)"],
        [b("Cilantro chutney"),    "3 weeks",           "~2 tbsp (regular tray)"],
        [b("Coconut chutney"),     "3 weeks",           "~2 tbsp (regular tray)"],
        [b("Mint muddle cubes"),   "4–6 weeks",         "1 tbsp (mini tray)"],
        [b("Fenugreek paste"),     "4–6 weeks",         "1 tbsp (mini tray)"],
    ], [2.0*inch, 1.8*inch, 2.75*inch]))

    _build(d, s)
    print("✓ 11-chutney-prep.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 12 — Ginger & Root Long-Term Storage
# ─────────────────────────────────────────────────────────────────────────────
def card_ginger_storage():
    d = mk_doc("fridge-sheets/12-ginger-storage.pdf")
    s = []
    s.append(Paragraph("Ginger & Root Storage", TITLE))
    s.append(Paragraph("Long-term freeze methods · whole knobs + paste cubes", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Ginger — Two Storage Formats", H2))
    s.append(tbl([
        ["Format",                    "Method",                                            "Shelf life", "When to use"],
        [b("Whole Knobs\n(3-month day)"), sm("Wash. Do NOT peel. Freeze whole in sealed bag."), b("3 months"), sm("Grate directly from frozen — skin grates off naturally.\nSemi-frozen is easiest to peel if needed.\nBuy ~2 kg on 3-month day.")],
        [b("Paste Cubes\n(monthly refresh)"), sm("Pull 2–3 knobs from freezer. Rest 5 min (semi-frozen easiest to peel).\nPeel. Blend with 2–3 tbsp cold water in Vitamix 60 sec.\nPortion ~1 tbsp per mini cube cell.\nFreeze overnight → transfer to labeled bag."), b("3 months"), sm("1 cube = ~1 inch knob equivalent.\nDrop from frozen into warm pan or recipes.")],
    ], [1.4*inch, 3.1*inch, 0.9*inch, 2.2*inch],
    [("BACKGROUND", (0,1), (-1,1), MINT)]))
    s.append(Spacer(1, 5))
    s.append(Paragraph("Label: Ginger — [date] — use by [date +3 months]", NOTE))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("Matcha Hack (morning 09:15 — temperature regulator)", H2))
    s.append(tbl([
        ["Step", "Action"],
        [b("1"),  "Boil water"],
        [b("2"),  "Drop 1 frozen ginger cube into cup — cube pulls temp down toward 170°F (76°C) naturally"],
        [b("3"),  "Pour near-boiling water over cube. Let fully melt, stir to incorporate (~30 sec)"],
        [b("4"),  w("Confirm temp ≤ 170°F — THEN whisk in matcha powder")],
        [b("5"),  "Rationale: 170°F protects L-theanine + EGCG from heat degradation. Ginger cube = flavor + temperature regulator in one step."],
    ], [0.4*inch, 7.15*inch],
    [("BACKGROUND", (0,4), (-1,4), AMBER)]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("Rested Garlic Cubes — monthly · ~14 cubes · shelf life 3 months frozen", H2))
    s.append(tbl([
        ["Step", "Action",                                               "Time"],
        [b("1"),  "Pull ~20 frozen garlic cloves. Thaw 10 min at room temp", "10 min"],
        [b("2"),  "Smash and mince finely",                             "—"],
        [b("3"),  w("REST 10 MINUTES — allicin formation window. Set a timer. Non-negotiable."), w("10 min EXACTLY")],
        [b("4"),  "Add 4–5 drops avocado oil to bind",                  "—"],
        [b("5"),  "Portion into mini cube tray (~1 tsp per cell). Freeze overnight.", "—"],
    ], [0.4*inch, 5.4*inch, 1.8*inch],
    [("BACKGROUND", (0,3), (-1,3), AMBER)]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "⚠  NEVER freeze before the 10-min rest. Ice crystals damage alliinase — "
        "thawed whole garlic cannot form allicin after freezing. Rest must happen before the freeze.", WARN_S))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("Long-Term Freeze: Herbs, Leaves & Coconut", H2))
    s.append(tbl([
        ["Ingredient",             "Blanch?",           "Method",                                              "Shelf life"],
        [b("Cilantro (bunches)"),  b("YES — 10 sec"),   "Wash + dry → blanch 10 sec → ice bath 30 sec → dry → flat bag", "3 months"],
        [b("Mint (bunches)"),      b("YES — 10 sec"),   "Same as cilantro",                                    "3 months"],
        [b("Curry leaves"),        b("NO"),             "Wash + dry → spread on tray → freeze 1 hr → airtight bag\nUse frozen directly for tadka — no thawing needed", "3 months"],
        [b("Fresh coconut (grated)"), b("NO"),          "Spread on tray → freeze 1 hr (prevents clumping) → bag\nMeasure frozen directly into blender for chutney", "3 months"],
        [b("Chilies (whole)"),     b("NO"),             "Freeze whole in labeled bags by variety",             "3–6 months"],
    ], [1.5*inch, 1.0*inch, 3.5*inch, 1.0*inch],
    [
        ("BACKGROUND", (0,1), (-1,2), MINT),
        ("BACKGROUND", (0,3), (-1,3), CREAM),
    ]))

    s.append(Spacer(1, 8))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    s.append(Paragraph(
        "⚠  Blanching cilantro + mint: 10 seconds only — stops browning (PPO deactivation) "
        "without cooking the herb. Longer exposure degrades the chelation compounds.", WARN_S))

    _build(d, s)
    print("✓ 12-ginger-storage.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 13 — Imli-Khajur Chutney (Tamarind-Date)
# ─────────────────────────────────────────────────────────────────────────────
def card_imli_chutney():
    d = mk_doc("fridge-sheets/13-imli-chutney.pdf")
    s = []
    s.append(Paragraph("Imli-Khajur Chutney", TITLE))
    s.append(Paragraph("Tamarind-Date · sweet-sour-spiced · 6-month freeze stability", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Single Batch (~16 cubes — day-of or small top-up)", H2))
    s.append(tbl([
        ["Ingredient",                   "Amount",          "Notes"],
        [b("Medjool dates (pitted)"),     b("10–12"),        "Blend with water until completely smooth"],
        [b("Tropica concentrated tamarind"), b("3 tbsp"),   "3–4× more concentrated than raw block — do not sub 1:1"],
        [b("Water"),                      b("1.5 cups"),     ""],
        [b("Salt"),                       b("1 tsp"),        ""],
        [b("Black salt (kala namak)"),    b("½ tsp"),        ""],
        [b("Roasted cumin powder"),       b("2 tsp"),        ""],
        [b("Ginger — dry powder"),        b("1 tsp"),        "OR: blend 1.5–2 inch fresh knob into dates in step 1"],
        [b("Star anise (ground)"),        b("1/16 tsp"),     "Preferred over fennel — same family, more depth. ~4× potent: do not exceed."],
        [b("Red chili powder"),           b("½ tsp"),        ""],
        [b("Cinnamon"),                   b("¼ tsp"),        "Bridges dates + tamarind"],
        [b("Black pepper"),               b("¼ tsp"),        ""],
        [b("Hing (asafoetida)"),          b("⅛ tsp"),        ""],
    ], [2.2*inch, 1.3*inch, 4.05*inch]))

    s.append(Spacer(1, 8))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("Method (single batch or 24 qt pot batch)", H2))
    s.append(tbl([
        ["Step", "Action"],
        [b("1"),  "Blend pitted dates + water (+ fresh ginger if using) until completely smooth — no chunks"],
        [b("2"),  "Pour date paste into pot. Add Tropica tamarind, stir to dissolve."],
        [b("3"),  "Add all spices + salts. Stir to combine."],
        [b("4"),  "Medium heat — stir frequently — 15–20 min until ribbon consistency (coats back of spoon)"],
        [b("5"),  "Taste: equal sweet-sour-spiced. More tamarind if too sweet; pinch salt if flat."],
        [b("6"),  sm("Optional: push through mesh strainer for silky texture — removes date fiber pulp.")],
        [b("7"),  w("Cool COMPLETELY before portioning. Looks thin hot — thickens as it cools.")],
        [b("8"),  "Pour ~2 tbsp per cube into ice cube trays. Freeze solid (~4 hrs). Bag + label."],
    ], [0.4*inch, 7.15*inch],
    [("BACKGROUND", (0,7), (-1,7), AMBER)]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Freeze stability: 6 months (high acid pH ~2.5 + natural sugar creates hostile environment for microbes). "
        "Thaw: 1 cube at room temp 20 min, or 30 sec microwave.", NOTE))

    s.append(PageBreak())

    s.append(Paragraph("3-Month Batch (24 qt Pot — One Cook)", TITLE))
    s.append(Paragraph("×6 single batch · 2 Vitamix blend runs → combine into 24 qt pot → one cook", SUB))
    s.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    s.append(Paragraph("Step 1 — Blend (2 Vitamix runs)", H2))
    s.append(tbl([
        ["Ingredient",                       "Per Vitamix run (×3 batch)", "× 2 runs = full 3-month batch"],
        [b("Medjool dates (pitted)"),         b("30–36 dates (~600g)"),    b("60–72 dates (~1.2 kg)")],
        [b("Water"),                          b("4.5 cups"),               b("9 cups total")],
        [b("Fresh ginger (blend in step 1)"), b("5 tsp grated\n(~5–6 inch knob)"), b("~200g total")],
    ], [2.2*inch, 2.2*inch, 2.65*inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Blend each run until completely smooth. Pour both into the 24 qt pot.", NOTE))

    s.append(Spacer(1, 10))
    s.append(Paragraph("Step 2 — Cook in 24 qt Pot (once, combined)", H2))
    s.append(tbl([
        ["Ingredient",                       "Amount for full batch",       "Notes"],
        [b("Tropica tamarind"),               b("18 tbsp (~1.1 cups)"),     "Stir into combined date paste until dissolved"],
        [b("Salt"),                           b("2 tbsp"),                  ""],
        [b("Black salt (kala namak)"),        b("1 tbsp"),                  ""],
        [b("Roasted cumin powder"),           b("4 tbsp"),                  ""],
        [b("Star anise (ground)"),            b("⅜ tsp"),                   "Do not exceed — potent"],
        [b("Red chili powder"),               b("1 tbsp"),                  ""],
        [b("Cinnamon"),                       b("¾ tsp"),                   ""],
        [b("Black pepper"),                   b("¾ tsp"),                   ""],
        [b("Hing"),                           b("⅜ tsp"),                   ""],
    ], [2.2*inch, 2.0*inch, 2.45*inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "24 qt pot note: the pre-cook liquid (~10–12 cups) sits shallow in a 24 qt pot — "
        "stir more frequently than normal (every 2–3 min) to prevent hotspots. "
        "Medium heat only. Cook 15–20 min until ribbon consistency.", NOTE))

    s.append(Spacer(1, 8))
    s.append(tbl([
        ["Output",                    "Volume",       "Cubes",     "Supply"],
        [b("Full 3-month batch"),      "~2 liters",    b("~96"),    "~3 months at 1/day"],
    ], [2.0*inch, 1.5*inch, 1.0*inch, 2.0*inch],
    [("BACKGROUND", (0,1), (-1,1), MINT)]))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    s.append(Paragraph("Jaggery Variant (Traditional — thinner)", H2))
    s.append(tbl([
        ["Change",            "Amount (single)", "Amount (×6 batch)"],
        [b("Remove: dates"),   "—",               "—"],
        [b("Add: jaggery"),    b("80–100g"),       b("480–600g")],
        [b("Extra water"),     b("+½ cup"),         b("+3 cups")],
    ], [2.0*inch, 2.0*inch, 2.55*inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph(
        "Jaggery: dissolve directly in water in pot (no blending). "
        "Result: thinner, more pourable, slightly higher GI, trace iron/potassium from molasses.", NOTE))

    s.append(Spacer(1, 10))
    s.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    s.append(Paragraph(
        "⚠  Cool COMPLETELY before portioning — hot chutney in ice trays cracks the tray. "
        "Tropica concentrate is 3–4× more potent than raw block tamarind — never substitute 1:1.", WARN_S))

    _build(d, s)
    print("✓ 13-imli-chutney.pdf  (duplex: single recipe / 24 qt 3-month batch)")

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs("fridge-sheets", exist_ok=True)
    card_produce()
    card_dressing()
    card_salad()
    card_timing()
    card_morning_drink()
    card_batch_flip()
    card_tofu()
    card_rotations()
    card_skincare()
    card_workout()
    card_chutney()
    card_ginger_storage()
    card_imli_chutney()
    print("\nAll 13 fridge cards written to fridge-sheets/")

    # Clean up temp QR file
    try:
        os.unlink(_QR_PATH)
    except OSError:
        pass

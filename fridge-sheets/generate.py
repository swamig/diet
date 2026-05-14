#!/usr/bin/env python3
"""Generate fridge reference cards as PDFs using reportlab."""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

W, H = letter  # 8.5 x 11

# ── Colours ──────────────────────────────────────────────────────────────────
TEAL   = colors.HexColor("#1a6b5a")
CREAM  = colors.HexColor("#fdf8f0")
GOLD   = colors.HexColor("#c9a846")
LIGHT  = colors.HexColor("#e8f4f0")
DARK   = colors.HexColor("#1a2e2a")
WARN   = colors.HexColor("#8b2020")

# ── Styles ────────────────────────────────────────────────────────────────────
ss = getSampleStyleSheet()

def style(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

TITLE  = style("title",  fontSize=32, fontName="Helvetica-Bold",
               textColor=TEAL, alignment=TA_CENTER, spaceAfter=6)
SUB    = style("sub",    fontSize=14, fontName="Helvetica",
               textColor=DARK, alignment=TA_CENTER, spaceAfter=18)
H2     = style("h2",     fontSize=20, fontName="Helvetica-Bold",
               textColor=TEAL, spaceBefore=14, spaceAfter=6)
BODY   = style("body",   fontSize=14, fontName="Helvetica",
               textColor=DARK, leading=22)
WARN_S = style("warn",   fontSize=13, fontName="Helvetica-Bold",
               textColor=WARN, leading=20)
NOTE   = style("note",   fontSize=11, fontName="Helvetica-Oblique",
               textColor=colors.HexColor("#555555"), leading=17)
BIG    = style("big",    fontSize=48, fontName="Helvetica-Bold",
               textColor=TEAL, alignment=TA_CENTER, spaceAfter=4)
MED    = style("med",    fontSize=28, fontName="Helvetica-Bold",
               textColor=DARK, alignment=TA_CENTER, spaceAfter=4)

def tbl(data, col_widths, style_cmds=None):
    base = [
        ("FONTNAME",  (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",  (0,0), (-1,-1), 14),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [CREAM, LIGHT]),
        ("GRID",      (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN",    (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",(0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",(0,0),(-1,-1), 10),
    ]
    if style_cmds:
        base += style_cmds
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(base))
    return t

def header_row_style(n_cols):
    return [
        ("BACKGROUND",  (0,0), (-1,0), TEAL),
        ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0), 14),
    ]

def make_doc(path, margins=0.55):
    m = margins * inch
    return SimpleDocTemplate(path, pagesize=letter,
                             leftMargin=m, rightMargin=m,
                             topMargin=m, bottomMargin=m)

# ─────────────────────────────────────────────────────────────────────────────
# CARD 1 — Produce Cleaning
# ─────────────────────────────────────────────────────────────────────────────
def card_produce():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/01-produce-cleaning.pdf")
    story = []

    story.append(Paragraph("Produce Cleaning", TITLE))
    story.append(Paragraph("Mandatory before every batch — both baths single-use only", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    # Step 1 — baking soda
    story.append(Paragraph("① Alkaline Soak", H2))
    story.append(tbl(
        [
            ["Water",        "Baking Soda",    "Soak Time"],
            ["1 gallon",     "1 tbsp",         "12–15 min"],
            ["1 quart",      "¾ tsp",          "12–15 min"],
            ["1 cup",        "¼ tsp",          "12–15 min"],
        ],
        [2.2*inch, 2.2*inch, 2.2*inch],
        header_row_style(3),
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Use cold water. Fully submerge. Removes up to 96% of surface pesticides.", NOTE))

    # Step 2 — vinegar
    story.append(Paragraph("② Acid Rinse (fresh bowl, fresh water)", H2))
    story.append(tbl(
        [
            ["Water",        "Vinegar",        "Rinse Time"],
            ["1 cup",        "1–2 tbsp",       "2–3 min"],
            ["1 quart",      "4–8 tbsp",       "2–3 min"],
        ],
        [2.2*inch, 2.2*inch, 2.2*inch],
        header_row_style(3),
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "White vinegar or ACV. Kills residual bacteria; neutralises baking soda residue. "
        "Do not shorten to a splash — minimum 2 min at this dilution.", NOTE))

    # Step 3
    story.append(Paragraph("③ Plain Cold Water Rinse", H2))
    story.append(Paragraph("30-second rinse to remove vinegar taste.", BODY))

    # Step 4
    story.append(Paragraph("④ Dry — Mandatory", H2))
    story.append(Paragraph(
        "Spin dry or pat with paper towels. Storing wet causes rapid oxidation and nutrient loss.", BODY))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    story.append(Paragraph(
        "⚠  BOTH BATHS ARE SINGLE-USE — discard after every batch. "
        "Reusing recontaminates the next batch.", WARN_S))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Buy Organic for the Dirty Dozen", H2))
    story.append(Paragraph(
        "Kale · Arugula · Spinach · Blueberries · Strawberries · "
        "Peaches · Pears · Nectarines · Apples · Grapes · Bell Peppers · Cherries", BODY))

    doc.build(story)
    print("✓ 01-produce-cleaning.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 2 — Master Salad Dressing
# ─────────────────────────────────────────────────────────────────────────────
def card_dressing():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/02-salad-dressing.pdf")
    story = []

    story.append(Paragraph("Master Salad Dressing", TITLE))
    story.append(Paragraph("7-day batch — make every Sunday", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=18))

    story.append(Paragraph("Sunday Batch (glass mason jar)", H2))
    story.append(tbl(
        [
            ["Ingredient",          "Amount",    "Notes"],
            ["Olive Oil",           "14 tbsp",   "Or: 7 tbsp Terra Delyssa + 7 tbsp Snake Oil"],
            ["Balsamic Vinegar",    "7 tbsp",    "Just under ½ cup"],
            ["Tomato Puree",        "7 tbsp",    "Just under ½ cup"],
            ["Dijon Mustard",       "7 tsp",     "Sugar-free"],
        ],
        [2.6*inch, 1.4*inch, 3.0*inch],
        header_row_style(3) + [
            ("FONTSIZE", (0,1), (-1,-1), 15),
            ("FONTNAME", (0,1), (1,-1), "Helvetica-Bold"),
        ],
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Whisk or shake vigorously until fully emulsified. "
        "Store in a dark spot in the fridge if using Snake Oil.", NOTE))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=16))

    story.append(Paragraph("Daily Use (at 14:30 — each serving)", H2))
    story.append(tbl(
        [
            ["What",                "Amount",    "How"],
            ["Dressing from jar",   "4 tbsp",    "Pour over assembled greens"],
            ["Turmeric (ground)",   "½ tsp",     "Sprinkle on WET dressing before tossing"],
            ["Black Pepper",        "¼ tsp",     "Grind FRESH — sprinkle on wet dressing"],
        ],
        [2.6*inch, 1.4*inch, 3.0*inch],
        header_row_style(3) + [
            ("FONTSIZE", (0,1), (-1,-1), 15),
            ("FONTNAME", (0,1), (1,-1), "Helvetica-Bold"),
            ("BACKGROUND", (0,3), (-1,3), colors.HexColor("#fff3cd")),
        ],
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Turmeric and pepper go on the wet dressing — never pre-mixed into the jar. "
        "Lipid suspension in the oil is what makes curcumin absorb.", NOTE))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    story.append(Paragraph(
        "⚠  Do NOT add Turmeric or Black Pepper to the master jar — "
        "they go on fresh at eating time only.", WARN_S))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Lipid Lever (Coconut Milk days)", H2))
    story.append(Paragraph(
        "If you add Coconut Milk to your 12:00 Chaas, subtract 1–2 tbsp oil from "
        "the 14:30 dressing to keep total lipid load balanced.", BODY))

    doc.build(story)
    print("✓ 02-salad-dressing.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 3 — Salad Assembly + Seed Rotation
# ─────────────────────────────────────────────────────────────────────────────
def card_salad():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/03-salad-assembly.pdf")
    story = []

    story.append(Paragraph("14:30 Salad Assembly", TITLE))
    story.append(Paragraph("Build in a 56 oz glass container", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    # Assembly layers
    story.append(Paragraph("Assembly Order", H2))
    story.append(tbl(
        [
            ["Layer",              "What",                             "Amount"],
            ["① Bitter Green",    "Arugula / Watercress / Kale*",    "2 cups"],
            ["② Daily Anchors",   "Broccoli Microgreens",             "1 cup"],
            ["",                  "Fresh Cilantro",                   "¼ cup"],
            ["③ Probiotic",       "Sauerkraut or Kimchi (raw/unpast.)","¼ cup"],
            ["④ Seed",            "Day's seed (see table below)",     "1 tbsp"],
            ["⑤ Dressing",        "Master dressing from fridge jar",  "4 tbsp"],
            ["⑥ Activate",        "Turmeric (ground)",                "½ tsp"],
            ["",                  "Black Pepper — grind FRESH",       "¼ tsp"],
        ],
        [1.3*inch, 3.3*inch, 1.8*inch],
        header_row_style(3) + [
            ("FONTSIZE",  (0,1), (-1,-1), 14),
            ("FONTNAME",  (0,1), (1,1),   "Helvetica-Bold"),
            ("FONTNAME",  (0,3), (1,3),   "Helvetica-Bold"),
            ("BACKGROUND",(0,4), (-1,5),  colors.HexColor("#e8f4f0")),
            ("BACKGROUND",(0,6), (-1,7),  colors.HexColor("#fff8e1")),
            ("FONTNAME",  (0,6), (-1,7),  "Helvetica-Bold"),
            ("TEXTCOLOR", (0,6), (-1,7),  WARN),
        ],
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "* Kale must be massaged with lemon + salt for 60 seconds to break cell walls.", NOTE))
    story.append(Paragraph(
        "⑥ Sprinkle turmeric and fresh-ground pepper directly onto the wet dressing "
        "before tossing — do not pre-mix into the dressing jar.", NOTE))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))

    # Seed rotation
    story.append(Paragraph("Weekly Seed Rotation (1 tbsp each)", H2))
    story.append(tbl(
        [
            ["Mon",          "Tue",     "Wed",         "Thu",    "Fri",         "Sat",      "Sun"],
            ["Basil Seeds\n(Sabja)",
             "Sesame",
             "Basil Seeds\n(Sabja)",
             "Walnuts",
             "Basil Seeds\n(Sabja)",
             "Pumpkin\nSeeds",
             "Hemp\nSeeds"],
            ["Iron/\nCooling",
             "Mineral\nDensity",
             "Iron/\nCooling",
             "Omega-3/\nVascular",
             "Iron/\nCooling",
             "Zinc/\nRecovery",
             "Complete\nProtein"],
        ],
        [0.93*inch]*7,
        header_row_style(7) + [
            ("FONTSIZE",     (0,0), (-1,-1), 12),
            ("FONTNAME",     (0,1), (-1,1),  "Helvetica-Bold"),
            ("FONTSIZE",     (0,1), (-1,1),  13),
            ("FONTNAME",     (0,2), (-1,2),  "Helvetica-Oblique"),
            ("FONTSIZE",     (0,2), (-1,2),  11),
            ("TEXTCOLOR",    (0,2), (-1,2),  colors.HexColor("#555555")),
            ("ALIGN",        (0,0), (-1,-1), "CENTER"),
            ("BACKGROUND",   (0,1), (0,1),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (2,1), (2,1),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (4,1), (4,1),   colors.HexColor("#d4edda")),
        ],
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Green = workout days (Mon/Wed/Fri).", NOTE))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    story.append(Paragraph(
        "⚠  Never put seeds in the 17:30 post-workout shake — "
        "mucilage gel slows protein absorption.", WARN_S))

    doc.build(story)
    print("✓ 03-salad-assembly.pdf")

# ─────────────────────────────────────────────────────────────────────────────
# CARD 4 — Daily Timing
# ─────────────────────────────────────────────────────────────────────────────
def card_timing():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/04-daily-timing.pdf")
    story = []

    story.append(Paragraph("Daily Rhythm", TITLE))
    story.append(Paragraph("Protocol at a glance", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    story.append(tbl(
        [
            ["Time",    "Action",               "Key Detail"],
            ["06:30",   "Morning Anchor",        "Cold Plunge — swap Yoga if exhausted"],
            ["09:15",   "Morning Hydration",     "Warm Ajwain / Jeera / Matcha"],
            ["10:00",   "Tannin Deadline",       "Stop all tea & caffeine"],
            ["12:00",   "Main Meal",             "Protein + starch + spice stack + Jaljeera"],
            ["13:00",   "Enzyme Pulse",          "Papaya ½ cup — must follow heavy meal"],
            ["14:30",   "Salad Layer",           "Greens + ferment + seeds + dressing"],
            ["16:30",   "Training",              "Lift (M/W/F) · VO2 Max (Tue) · Rest (Thu/Sat)"],
            ["17:30",   "Post-Workout",          "Whey isolate + creatine"],
            ["17:50",   "Recovery Bowl",         "Yogurt + blueberries + casein"],
            ["18:30",   "Heat Rotation",         "Sauna (Tue/Thu/Sat) · Epsom Bath (M/W/F)"],
            ["21:00",   "Night Infusion",        "Tulsi / Saffron / Ashwagandha"],
        ],
        [0.75*inch, 1.7*inch, 5.1*inch],
        header_row_style(3) + [
            ("FONTSIZE",  (0,0), (-1,-1), 14),
            ("FONTNAME",  (0,1), (1,-1),  "Helvetica-Bold"),
            ("FONTSIZE",  (0,1), (1,-1),  15),
            ("BACKGROUND",(0,5), (-1,5),  colors.HexColor("#d4edda")),
            ("BACKGROUND",(0,1), (-1,1),  colors.HexColor("#e3f2fd")),
        ],
    ))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))

    story.append(Paragraph("Macro Adjustments by Day Type", H2))
    story.append(tbl(
        [
            ["Day Type",       "Quinoa (12:00)", "Casein (17:50)", "Salad Dressing"],
            ["Heavy Lift",     "½ cup",          "1 scoop",        "4 tbsp"],
            ["VO2 Max (Tue)",  "¾ cup",          "1 scoop",        "4 tbsp"],
            ["Rest / Cardio",  "¼ cup",          "SKIP",           "2–4 tbsp"],
        ],
        [2.0*inch, 1.6*inch, 1.6*inch, 2.2*inch],
        header_row_style(4) + [
            ("FONTSIZE",  (0,1), (-1,-1), 14),
            ("FONTNAME",  (0,1), (0,-1),  "Helvetica-Bold"),
            ("TEXTCOLOR", (1,3), (1,3),   WARN),
            ("FONTNAME",  (1,3), (1,3),   "Helvetica-Bold"),
        ],
    ))

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    story.append(Paragraph(
        "⚠  NEVER cold plunge immediately after a heavy lift — "
        "blunts mTOR / growth signal. Keep cold exposure to 06:30 AM only.", WARN_S))

    doc.build(story)
    print("✓ 04-daily-timing.pdf")

# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# CARD 5 — Morning Drink
# ─────────────────────────────────────────────────────────────────────────────
def card_morning_drink():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/05-morning-drink.pdf")
    story = []

    story.append(Paragraph("Morning Drink", TITLE))
    story.append(Paragraph("09:15 — must be warm/hot — finish by 10:00 AM", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=18))

    story.append(tbl(
        [
            ["Day",                     "Base Spice",           "Amount",   "Method"],
            ["Odd days\n(1 · 3 · 5 · 7)",  "Ajwain seeds",     "¼ tsp",    "Boil 1–2 cups water · add seeds · steep 5 min · strain"],
            ["Even days\n(2 · 4 · 6)",     "Whole Jeera\n(cumin seeds)", "½ tsp", "Boil 1–2 cups water · add seeds · steep 5 min"],
        ],
        [1.5*inch, 1.6*inch, 0.9*inch, 3.55*inch],
        header_row_style(4) + [
            ("FONTSIZE",  (0,1), (-1,-1), 14),
            ("FONTNAME",  (0,1), (1,-1),  "Helvetica-Bold"),
            ("FONTSIZE",  (0,1), (1,-1),  15),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [CREAM, LIGHT]),
        ],
    ))

    story.append(Spacer(1, 18))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=14))
    story.append(Paragraph("Optional Upgrades", H2))
    story.append(tbl(
        [
            ["Add-on",                  "Amount",   "When",             "How"],
            ["Matcha powder",           "1 tsp",    "Any day",          "Whisk into warm (not boiling) water separately, stir into drink after steeping"],
            ["Whole Clove",             "1 clove",  "Week 2 only\n(replace a Jeera day)", "Add to water with the seeds, steep together"],
            ["Cardamom pod (crushed)",  "1 pod",    "Any day\n(rotator)", "Crush pod, add to steep"],
            ["Star Anise",              "1 whole",  "Antiviral pulse\n(rotator)", "Add to steep — strong flavour, use sparingly"],
        ],
        [1.8*inch, 0.9*inch, 1.4*inch, 3.45*inch],
        header_row_style(4) + [
            ("FONTSIZE",  (0,1), (-1,-1), 13),
            ("FONTNAME",  (0,1), (0,-1),  "Helvetica-Bold"),
        ],
    ))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    story.append(Paragraph(
        "⚠  TANNIN DEADLINE — 10:00 AM. "
        "Matcha catechins block iron absorption by up to 3×. "
        "All tea/caffeine must be finished 2 hours before the 12:00 main meal.", WARN_S))

    story.append(Spacer(1, 12))
    story.append(Paragraph("The Warm Start Rule", H2))
    story.append(Paragraph(
        "Must be consumed warm to hot — never cold before 10:00. "
        "Warm water vasodilates, stimulates peristalsis, and preps the gut for the 12:00 feeding window. "
        "Do NOT use alkaline water — it neutralises the acids needed for Agni.", BODY))

    story.append(Spacer(1, 14))
    story.append(Paragraph("Sunday Prep Shortcut", H2))
    story.append(Paragraph(
        "Pre-portion 7 small containers on Sunday: each holds the week's base spice. "
        "Alternates automatically — no measuring during the week. "
        "If adding Matcha, include 1 tsp in each pack.", BODY))

    doc.build(story)
    print("✓ 05-morning-drink.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# CARD 6 — Batch Session Flip Card (front = 3-week, back = 3-month)
# ─────────────────────────────────────────────────────────────────────────────
def card_batch_flip():
    # ── PAGE 1: 3-Week Chutney & Cube Session ────────────────────────────────
    from reportlab.platypus import PageBreak

    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/06-batch-session.pdf")
    story = []

    story.append(Paragraph("3-Week Batch Session", TITLE))
    story.append(Paragraph("Run every 3 weeks · ~85 min · one person · no cooking after tadka", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    story.append(Paragraph("Night Before", H2))
    story.append(Paragraph("Soak 4 tbsp fenugreek seeds in water overnight.", BODY))

    story.append(Paragraph("Session Timeline", H2))
    story.append(tbl(
        [
            ["Time",        "Step",                                         "Output"],
            ["T+0:00",      "Setup — ingredients out, start water boiling", "—"],
            ["T+0:05",      "Pre-chop: curry leaves (½\" pieces), break chili to flakes", "—"],
            ["T+0:08",      "Tadka — heat oil, mustard seeds pop → curry leaves + chili + hing\n→ BLOOM 15–20 SEC EXACTLY → remove from heat → cool 5 min", "~21 tadka cubes"],
            ["T+0:15",      "Blanch mint + cilantro together — 10–15 SEC, ice bath, squeeze, separate into two piles", "—"],
            ["T+0:20",      "Pour cooled tadka into mini tray (1 tsp per cell)", "21 cubes"],
            ["T+0:22",      "Blend Jaljeera concentrate → pour into tray", "21 cubes"],
            ["T+0:27",      "Blend cilantro chutney → pour into tray", "17–18 cubes"],
            ["T+0:32",      "Blend coconut chutney — 2 runs × 6 min each", "48 cubes"],
            ["T+0:44",      "Blend mint muddle → pour into mini tray", "21 cubes"],
            ["T+0:54",      "Fenugreek paste — drain seeds, blend immersion, pour into tray", "12–14 cubes"],
            ["T+1:04",      "Aloe topical refresh (only if running low — check freezer first)", "~14–28 cubes"],
            ["T+1:19",      "Label all trays, freeze flat — do NOT stack until frozen", "—"],
            ["T+1:24",      "Cleanup", "Done"],
        ],
        [0.7*inch, 4.3*inch, 1.5*inch],
        header_row_style(3) + [
            ("FONTSIZE",  (0,1), (-1,-1), 12),
            ("FONTNAME",  (0,3), (1,3),   "Helvetica-Bold"),
            ("TEXTCOLOR", (0,3), (1,3),   WARN),
            ("BACKGROUND",(0,3), (-1,3),  colors.HexColor("#fff3cd")),
            ("BACKGROUND",(0,4), (-1,4),  colors.HexColor("#fff3cd")),
        ],
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
    story.append(Paragraph("Key Ratios & Rules", H2))
    story.append(tbl(
        [
            ["Item",                "Critical Number",      "Rule"],
            ["Tadka bloom",         "15–20 sec exactly",    "Beyond 30 sec → alkaloids degrade. Use a timer."],
            ["Blanch time",         "10–15 sec",            "Set timer. Ice bath must be ≥1:1 ice:water."],
            ["Coconut per Vitamix", "4 cups max",           "One run = 4 cups → ~24 cubes. 2 runs = 48 cubes."],
            ["Cube size — mini",    "1 tsp per cell",       "Tadka, mint muddle, fenugreek, ginger cubes."],
            ["Cube size — regular", "~2 tbsp per cell",     "Jaljeera, cilantro chutney, coconut chutney."],
            ["Freeze stability",    "3 weeks",              "Cilantro, coconut, Jaljeera, mint muddle."],
        ],
        [1.6*inch, 1.6*inch, 4.3*inch],
        header_row_style(3) + [
            ("FONTSIZE",  (0,1), (-1,-1), 13),
            ("FONTNAME",  (0,1), (1,-1),  "Helvetica-Bold"),
        ],
    ))

    # ── PAGE 2: 3-Month Big Session (flip side) ───────────────────────────────
    story.append(PageBreak())

    story.append(Paragraph("3-Month Big Session", TITLE))
    story.append(Paragraph("Run every 3 months · ~half day across 2 days · RS3 chill is the bottleneck", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    story.append(Paragraph("Night Before Day 1", H2))
    story.append(Paragraph(
        "Clear chest freezer. Soak chickpeas (5 kg) and black beans (4.5 kg) separately in large pots overnight.", BODY))

    story.append(Paragraph("Day 1 — Cook & Chill (~4h active)", H2))
    story.append(tbl(
        [
            ["Order", "Task",                                         "RS3 Rule"],
            ["1st",   "Cook chickpeas + black beans — pressure cook or boil until just tender", "CHILL in fridge 24h before freezing"],
            ["2nd",   "Cook quinoa — 1 cup dry : 1.75 cups water, simmer 12 min, spread thin in 88oz Pyrex to cool fast", "CHILL in fridge 24h before freezing"],
            ["3rd",   "Cook lentils — simmer 20–25 min, spread thin to cool", "Chill 12–24h"],
            ["4th",   "Freeze tofu slabs raw — slice 400g block into 4–6 slabs, flat in bags", "No chill needed"],
            ["5th",   "Make lemon juice cubes — juice 50 lemons → ice cube trays → freeze", "No chill needed"],
            ["6th",   "Make imli (tamarind) cubes — 1 tray, freeze", "No chill needed"],
            ["7th",   "Make aloe gel cubes — drain latex 10–15 min → fillet → scoop → blend → tray", "No chill needed"],
        ],
        [0.5*inch, 4.0*inch, 3.05*inch],
        header_row_style(3) + [
            ("FONTSIZE",   (0,1), (-1,-1), 12),
            ("FONTNAME",   (2,1), (2,3),   "Helvetica-Bold"),
            ("TEXTCOLOR",  (2,1), (2,3),   WARN),
            ("BACKGROUND", (0,1), (-1,3),  colors.HexColor("#fff3cd")),
        ],
    ))

    story.append(Paragraph("Day 2 — Portion & Freeze (~2h)", H2))
    story.append(tbl(
        [
            ["Task",                                            "Portion size",         "Into"],
            ["Chickpeas — portion into bags",                  "1.5 cups cooked",      "Flat freezer bags"],
            ["Black beans — portion into bags",                "1.5 cups cooked",      "Flat freezer bags"],
            ["Quinoa — portion into bags",                     "½ cup cooked",         "Flat freezer bags"],
            ["Lentils — portion into bags",                    "½ cup cooked",         "Flat freezer bags"],
            ["Freeze whole ginger knobs",                      "~2 kg total",          "One large bag"],
            ["Freeze peeled garlic cloves",                    "~25 heads",            "One bag"],
            ["Blanch + freeze cilantro (15 large bunches)",    "10–15 sec blanch",     "Bags by batch"],
            ["Blanch + freeze mint (8 large bunches)",         "10–15 sec blanch",     "Bags by batch"],
            ["Freeze chilies whole",                           "All varieties",        "Labeled bags"],
        ],
        [3.3*inch, 1.8*inch, 2.45*inch],
        header_row_style(3) + [
            ("FONTSIZE",  (0,1), (-1,-1), 12),
            ("FONTNAME",  (0,1), (0,-1),  "Helvetica-Bold"),
        ],
    ))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    story.append(Paragraph(
        "⚠  RS3 RULE — chickpeas, black beans, quinoa, lentils MUST chill in the fridge 12–24h "
        "before going into the freezer. This is the hard bottleneck. Do not skip. "
        "The fridge needs to be fully cleared on night before Day 1 to fit everything.", WARN_S))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Spice Jars — Refill on 3-Month Day", H2))
    story.append(Paragraph(
        "Check dry jars: Kashmiri chili (~50g), Turmeric (~150g), Cumin seeds (~200g), "
        "Cumin powder (~100g), Coriander powder (~100g), Black pepper whole (~100g), "
        "Ajwain (~50g), Nigella (~50g), Mustard seeds (~50g), Hing (~10g). "
        "Refill any that are below 2-week supply.", BODY))

    doc.build(story)
    print("✓ 06-batch-session.pdf  (page 1 = 3-week front, page 2 = 3-month back — print duplex)")


# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# CARD 7 — Tofu Day-Of Prep
# ─────────────────────────────────────────────────────────────────────────────
def card_tofu():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/07-tofu-prep.pdf")
    story = []

    story.append(Paragraph("Tofu Day-Of Prep", TITLE))
    story.append(Paragraph("Extra-firm only · freeze-thaw → brine → press → sear · 2×/week", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=14))

    story.append(Paragraph("Step 1 — Thaw", H2))
    story.append(tbl(
        [
            ["Method",              "Time",         "Notes"],
            ["Fridge overnight",    "8–12 h",       "Preferred — slow thaw preserves texture best"],
            ["Cold water fast",     "30–60 min",    "Submerge sealed bag in cold water"],
        ],
        [2.0*inch, 1.2*inch, 4.35*inch],
        header_row_style(3),
    ))

    story.append(Paragraph("Step 2 — Salt Brine", H2))
    story.append(tbl(
        [
            ["Water",       "Salt",     "Boil Level",       "Time"],
            ["4 cups",      "1 tsp",    "Full rolling boil", "3–5 min"],
            ["2 cups",      "½ tsp",    "Full rolling boil", "3–5 min"],
            ["8 cups",      "2 tsp",    "Full rolling boil", "3–5 min"],
        ],
        [1.5*inch, 1.2*inch, 2.5*inch, 1.8*inch],
        header_row_style(4) + [
            ("FONTSIZE",  (0,1), (-1,-1), 16),
            ("FONTNAME",  (0,1), (-1,1),  "Helvetica-Bold"),
            ("BACKGROUND",(0,1), (-1,1),  colors.HexColor("#d4edda")),
        ],
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Full boil expels residual ice-crystal water and opens pores — "
        "salt seasons from the inside out. Remove slabs, transfer to clean surface.", NOTE))

    story.append(Paragraph("Step 3 — Press", H2))
    story.append(Paragraph(
        "5 minutes — lay slabs on a clean towel, place a heavy pan on top. "
        "Most water exits during the brine; this is just the final dry.", BODY))

    story.append(Paragraph("Step 4 — Marinate (Optional — 15–20 min)", H2))
    story.append(tbl(
        [
            ["Option",          "Recipe"],
            ["Tamari marinade", "2 tbsp tamari + 1 ginger cube (melted) + 1 tsp ACV — soak 15 min"],
            ["Dry rub",         "Protocol spice mix (turmeric + cumin + coriander + Kashmiri chili) rubbed directly onto slab — no wait time needed"],
        ],
        [1.5*inch, 6.05*inch],
        header_row_style(2) + [("FONTSIZE", (0,1), (-1,-1), 13)],
    ))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    story.append(Paragraph("Step 5 — Flash Sear (Allicin Pulse)", H2))
    story.append(tbl(
        [
            ["Clock",   "Action"],
            ["00:00",   "Crush 2–3 garlic cloves — REST 10 MINUTES (allicin formation — non-negotiable)"],
            ["00:10",   "COLD START — add 2 tbsp avocado oil + methi seeds + chili + rested garlic to COLD pan"],
            ["00:11",   "Turn to LOW — bloom 5 min until garlic barely sizzles (extracts capsaicin + sulfur into fat)"],
            ["00:16",   "Turn to MEDIUM-HIGH — add tofu slabs — sear 60–90 sec per side until golden crust"],
            ["00:25",   "Off heat — tear 5–6 fresh Mentha arvensis (mint) leaves over hot tofu"],
            ["00:26",   "Serve immediately with Peppermint Jaljeera"],
        ],
        [0.75*inch, 6.8*inch],
        header_row_style(2) + [
            ("FONTSIZE",   (0,1), (-1,-1), 14),
            ("FONTNAME",   (0,1), (-1,1),  "Helvetica-Bold"),
            ("TEXTCOLOR",  (0,1), (-1,1),  WARN),
            ("BACKGROUND", (0,1), (-1,1),  colors.HexColor("#fff3cd")),
            ("FONTNAME",   (0,4), (-1,4),  "Helvetica-Bold"),
            ("BACKGROUND", (0,5), (-1,5),  LIGHT),
        ],
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=8))
    story.append(Paragraph(
        "⚠  The 10-minute garlic rest is non-negotiable — "
        "crushing activates alliinase; the enzyme needs time to convert alliin → allicin before heat destroys it. "
        "Crush first, prep everything else, then start the pan.", WARN_S))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Wet Curry Variant", H2))
    story.append(Paragraph(
        "At step 00:25: add 2–3 tbsp coconut milk, stir 30–60 sec into a glaze. "
        "Subtract 1 tbsp oil from the 14:30 salad dressing (Lipid Substitution Rule).", BODY))

    doc.build(story)
    print("✓ 07-tofu-prep.pdf")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    card_produce()
    card_dressing()
    card_salad()
    card_timing()
    card_morning_drink()
    card_batch_flip()
    card_tofu()
    print("\nAll 7 fridge cards written to fridge-sheets/")

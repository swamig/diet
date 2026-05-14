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

# ─────────────────────────────────────────────────────────────────────────────
# CARD 8 — Daily / Weekly / 4-Week Rotations
# ─────────────────────────────────────────────────────────────────────────────
def card_rotations():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/08-rotations.pdf")
    story = []

    story.append(Paragraph("Protocol Rotations", TITLE))
    story.append(Paragraph("Daily · Weekly · 4-Week cycle", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    # ── DAILY ────────────────────────────────────────────────────────────────
    story.append(Paragraph("Daily Rotations", H2))
    story.append(tbl(
        [
            ["What",                "Mon",          "Tue",          "Wed",              "Thu",          "Fri",          "Sat",          "Sun"],
            ["Morning drink\n09:15","Ajwain\n¼ tsp","Jeera\n½ tsp", "Ajwain\n¼ tsp",   "Jeera\n½ tsp", "Ajwain\n¼ tsp","Jeera\n½ tsp", "Ajwain\n¼ tsp"],
            ["Salad seed\n1 tbsp",  "Basil\nseeds", "Sesame",       "Basil\nseeds",     "Walnuts",      "Basil\nseeds", "Pumpkin\nseeds","Hemp\nseeds"],
            ["Heat 18:30",          "Epsom\nbath",  "Sauna",        "Epsom\nbath",      "Sauna",        "Epsom\nbath",  "Sauna",        "—"],
            ["Training\n16:30",     "Lift",         "VO2 Max",      "Lift",             "Rest",         "Lift",         "Rest",         "—"],
        ],
        [1.3*inch] + [0.89*inch]*7,
        header_row_style(8) + [
            ("FONTSIZE",     (0,0), (-1,-1), 11),
            ("FONTNAME",     (0,1), (0,-1),  "Helvetica-Bold"),
            ("BACKGROUND",   (1,1), (1,1),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (3,1), (3,1),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (5,1), (5,1),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (7,1), (7,1),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (1,3), (1,3),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (3,3), (3,3),   colors.HexColor("#d4edda")),
            ("BACKGROUND",   (5,3), (5,3),   colors.HexColor("#d4edda")),
            ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ],
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Green = workout days.", NOTE))

    # ── NIGHT INFUSIONS ───────────────────────────────────────────────────────
    story.append(Paragraph("Night Infusion (21:00) — pick by day type", H2))
    story.append(tbl(
        [
            ["Infusion",        "When to use"],
            ["Ashwagandha",     "High-cortisol days · tofu-pulse days · VO2 Max (Tue) — mandatory. Do NOT use daily."],
            ["Tulsi",           "Lower-stimulation recovery nights · standard rest recovery"],
            ["Saffron",         "Parasympathetic emphasis · end-of-day downshift · Week 4 washout"],
        ],
        [1.5*inch, 6.05*inch],
        header_row_style(2) + [("FONTSIZE", (0,1), (-1,-1), 13), ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold")],
    ))

    # ── WEEKLY ────────────────────────────────────────────────────────────────
    story.append(Paragraph("Weekly Rotations — pick one per category per week", H2))
    story.append(tbl(
        [
            ["Category",            "Option A",                     "Option B",                     "Option C"],
            ["Bitter green\n(2 cups)","Arugula\n(high nitrate/NO)", "Watercress\n(PEITC / dense)",  "Kale*\n(massage 60 sec)"],
            ["Dry Podi\n(1 tbsp/day)","Hormonal Buffer Podi\n(flax + moringa + cumin)", "Vascular Podi\n(sesame + curry leaf + bay leaf + cumin)", "—"],
            ["Chutney\n(1–2 tbsp/meal)","Coconut chutney\n(MCT + curry leaf)","Cilantro/Mint TRP\n(4 cups cilantro + mint)","—"],
            ["Recovery bowl\nextras","Cacao nibs + vanilla\n(2–3×/week MAX — never daily)","Plain bowl\n(rest days)", "—"],
        ],
        [1.4*inch, 2.1*inch, 2.1*inch, 2.0*inch],
        header_row_style(4) + [
            ("FONTSIZE",   (0,1), (-1,-1), 11),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("TEXTCOLOR",  (1,4), (2,4),   WARN),
        ],
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph("* Tofu: 2×/week ceiling — never more. Phytoestrogen accumulation risk.", WARN_S))

    # ── 4-WEEK ────────────────────────────────────────────────────────────────
    story.append(Paragraph("4-Week Cycle — what shifts each week", H2))
    story.append(tbl(
        [
            ["Week",    "Theme",                    "Morning drink",                    "Special rules"],
            ["Week 1",  "Baseline &\nAnti-inflammatory","Ajwain / Jeera basic rotation", "No clove. Establish timing. Follow daily anchors strictly."],
            ["Week 2",  "Antimicrobial\nPeak",      "Add Clove 2 mornings\n(replace 2 Jeera days)", "Clove only on Day 9 + Day 12. Sulfur emphasis. Watch gut."],
            ["Week 3",  "Vascular &\nNitric Peak",  "Ajwain / Jeera basic rotation","Arugula/Watercress priority for NO. Omega-3 week. Monitor logs."],
            ["Week 4",  "Washout &\nReset",         "Ajwain / Jeera basic rotation","REMOVE all heavy antimicrobials (no clove, no star anise). "
                                                                                    "Low stimulation — Tulsi/Saffron at night, skip Ashwagandha unless high-cortisol. "
                                                                                    "Optional: run Detox Week (chlorella + double cilantro + extra tamarind)."],
        ],
        [0.65*inch, 1.3*inch, 1.9*inch, 3.8*inch],
        header_row_style(4) + [
            ("FONTSIZE",   (0,1), (-1,-1), 11),
            ("FONTNAME",   (0,1), (1,-1),  "Helvetica-Bold"),
            ("BACKGROUND", (0,2), (-1,2),  colors.HexColor("#fff3cd")),
            ("BACKGROUND", (0,4), (-1,4),  colors.HexColor("#e8f4f0")),
        ],
    ))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    story.append(Paragraph(
        "⚠  Daily anchors never rotate: Broccoli microgreens · Fresh cilantro · Turmeric + black pepper · Ginger · Brazil nut (1–2/day).", WARN_S))

    doc.build(story)
    print("✓ 08-rotations.pdf")


# ─────────────────────────────────────────────────────────────────────────────
# CARD 9 — Skincare (Topical Protocols)
# ─────────────────────────────────────────────────────────────────────────────
def card_skincare():
    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/09-skincare.pdf")
    story = []

    story.append(Paragraph("Skincare & Hair", TITLE))
    story.append(Paragraph("Ayurvedic topical protocols — batch system", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    # Weekly schedule
    story.append(Paragraph("Weekly Schedule", H2))
    story.append(tbl(
        [
            ["Day",         "Hair Mask",    "Face Mask",    "Body Ubtan",   "Leave time"],
            ["Wednesday",   "✓",            "✓",            "✓",            "Hair 30–45 min · Face 10–15 min · Body 5–10 min (pre-shower)"],
            ["Sunday",      "✓",            "✓",            "—",            "Hair 30–45 min · Face 10–15 min"],
        ],
        [0.9*inch, 0.8*inch, 0.8*inch, 0.9*inch, 5.15*inch],
        header_row_style(5) + [
            ("FONTSIZE",   (0,1), (-1,-1), 13),
            ("FONTNAME",   (1,1), (3,2),   "Helvetica-Bold"),
            ("TEXTCOLOR",  (3,2), (3,2),   colors.HexColor("#888888")),
            ("ALIGN",      (1,0), (3,2),   "CENTER"),
        ],
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    # Per-application recipes
    story.append(Paragraph("Per-Application Recipe", H2))
    story.append(tbl(
        [
            ["Protocol",        "Dry mix",          "Wet cubes",                    "Oil",              "Extra"],
            ["Hair Mask",       "2 tbsp Dry Hair Mix","1 fenugreek cube (thawed)\n1 aloe cube (thawed)","1 tbsp coconut oil\n(melted)", "3–5 drops Rosemary EO\nmixed into oil first"],
            ["Face Mask",       "1 tsp Dry Face Mix","1 aloe cube (thawed)\n— or rose water to bind","Tiny drop coconut oil\n(dry skin only)", "Avoid eye area.\nLeave 10–15 min."],
            ["Body Ubtan",      "2 tbsp Dry Body Mix","1 aloe cube (thawed)",        "1 tbsp coconut\nor sesame oil", "Apply to damp skin,\ncircular motions.\nScrub off in shower."],
        ],
        [1.1*inch, 1.5*inch, 1.8*inch, 1.5*inch, 1.75*inch],
        header_row_style(5) + [
            ("FONTSIZE",   (0,1), (-1,-1), 11),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("BACKGROUND", (4,1), (4,1),   colors.HexColor("#e8f4f0")),
        ],
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Hair mask: apply to scalp first, massage 2–3 min, then work through lengths. "
        "Do NOT let mask fully dry and harden — rinse while still slightly damp.", NOTE))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    # Dry mix jar recipes
    story.append(Paragraph("Dry Mix Jar Recipes (make once, top up monthly)", H2))
    story.append(tbl(
        [
            ["Jar",             "Ingredient",                       "Amount"],
            # Hair
            ["DRY HAIR MIX",   "Amla powder",                      "4 tbsp"],
            ["",               "Curry Leaf Powder (air-dried)",     "1 tsp"],
            ["",               "Rotating powder — see 3-month cycle below", "4 tbsp"],
            ["",               "Fenugreek powder (backup if no cubes)", "2 tbsp"],
            # Face
            ["DRY FACE MIX",   "Besan (chickpea flour)",            "4 tbsp"],
            ["",               "Amla powder",                       "2 tbsp"],
            ["",               "Turmeric",                          "1 tsp"],
            ["",               "Bay Leaf Powder (tejpatta)",         "¼ tsp MAX"],
            # Body
            ["DRY BODY MIX",   "Besan (chickpea flour)",            "6 tbsp"],
            ["",               "Amla powder",                       "2 tbsp"],
            ["",               "Turmeric",                          "1.5 tsp"],
            ["",               "Neem powder (Month 3 only)",        "3 tbsp"],
        ],
        [1.4*inch, 4.0*inch, 1.25*inch],
        header_row_style(3) + [
            ("FONTSIZE",     (0,0), (-1,-1), 12),
            ("FONTNAME",     (0,1), (0,4),   "Helvetica-Bold"),
            ("BACKGROUND",   (0,1), (-1,4),  CREAM),
            ("FONTNAME",     (0,5), (0,8),   "Helvetica-Bold"),
            ("BACKGROUND",   (0,5), (-1,8),  LIGHT),
            ("FONTNAME",     (0,9), (0,12),  "Helvetica-Bold"),
            ("BACKGROUND",   (0,9), (-1,12), CREAM),
            ("TEXTCOLOR",    (1,4), (2,4),   WARN),
            ("TEXTCOLOR",    (1,8), (2,8),   WARN),
            ("TEXTCOLOR",    (1,12),(2,12),  WARN),
            ("FONTNAME",     (1,4), (2,4),   "Helvetica-Bold"),
            ("FONTNAME",     (1,8), (2,8),   "Helvetica-Bold"),
            ("FONTNAME",     (1,12),(2,12),  "Helvetica-Bold"),
        ],
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    # 3-month rotating powder
    story.append(Paragraph("3-Month Hair Powder Cycle (rotating 4 tbsp in Dry Hair Mix)", H2))
    story.append(tbl(
        [
            ["Month",   "Powder",       "What it does"],
            ["Month 1", "Brahmi\n(Bacopa monnieri)", "Reduces scalp inflammation, strengthens shaft, cortisol-driven hair loss"],
            ["Month 2", "Bhringraj\n(Eclipta alba)",  "Stimulates follicles, reduces shedding"],
            ["Month 3", "Neem\n(Azadirachta indica)", "Antifungal, anti-dandruff, clears scalp bacteria\n→ also add 3 tbsp Neem to Dry Body Mix this month"],
        ],
        [0.9*inch, 1.7*inch, 5.05*inch],
        header_row_style(3) + [
            ("FONTSIZE",   (0,1), (-1,-1), 13),
            ("FONTNAME",   (0,1), (1,-1),  "Helvetica-Bold"),
            ("BACKGROUND", (0,3), (-1,3),  colors.HexColor("#fff3cd")),
            ("FONTNAME",   (0,3), (-1,3),  "Helvetica-Bold"),
        ],
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Cube Consumption (per week)", H2))
    story.append(tbl(
        [
            ["Protocol",    "Freq/week",    "Aloe cubes",   "Fenugreek cubes"],
            ["Hair mask",   "2× (Wed+Sun)", "2",            "2"],
            ["Face mask",   "2× (Wed+Sun)", "2",            "0"],
            ["Body ubtan",  "1× (Wed)",     "1",            "0"],
            ["TOTAL/week",  "",             "5",            "2"],
        ],
        [1.8*inch, 1.6*inch, 1.6*inch, 2.55*inch],
        header_row_style(4) + [
            ("FONTSIZE",   (0,1), (-1,-1), 13),
            ("FONTNAME",   (0,4), (-1,4),  "Helvetica-Bold"),
            ("BACKGROUND", (0,4), (-1,4),  LIGHT),
            ("ALIGN",      (2,0), (3,4),   "CENTER"),
        ],
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "3-month supply: ~65 aloe cubes (5 tray batches from 5 leaves) · "
        "~26 fenugreek cubes (1 batch from 4 tbsp seeds every 6 weeks).", NOTE))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    story.append(Paragraph(
        "⚠  Aloe — drain latex 10–15 min (stand cut-end down) before scooping gel. "
        "Aloin irritates skin. "
        "Bay leaf max ¼ tsp in face mix — sensitizer at high dose. "
        "Turmeric stains hair yellow — omit or use 1/8 tsp max in hair mask.", WARN_S))

    doc.build(story)
    print("✓ 09-skincare.pdf")


# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# CARD 10 — Workout & Yoga (front = weekly split, back = yoga + thermal)
# ─────────────────────────────────────────────────────────────────────────────
def card_workout():
    from reportlab.platypus import PageBreak

    doc = make_doc("/home/user/bluevedaprotocol/fridge-sheets/10-workout.pdf")
    story = []

    # ── PAGE 1: Weekly Training Split ─────────────────────────────────────────
    story.append(Paragraph("Weekly Training Split", TITLE))
    story.append(Paragraph("The Operator Split — Legs / Push / Pull / VO2 / Recovery", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    story.append(tbl(
        [
            ["Day",         "06:30 – 09:00",            "16:30 – 18:00",                "21:00 Night",  "Yoga pairing"],
            ["MON",         "Cold Plunge",               "HEAVY LEGS",                   "Tulsi",        "Half Pigeon\n(hip flexors)"],
            ["TUE",         "Fasted Cardio\n(Zone 2)",   "PUSH DAY",                     "Tulsi",        "Cobra / Upward Dog\n(chest/shoulders)"],
            ["WED",         "Cold Plunge",               "PULL DAY",                     "Saffron",      "Thread the Needle\n(thoracic/biceps)"],
            ["THU",         "VO2 Max 4×4\n(full intervals)",  "Active Recovery / Walk",  "Ashwagandha\n(mandatory)",  "Legs Up the Wall\n(vagal tone)"],
            ["FRI",         "Cold Plunge",               "LIFT ROTATOR\n+ Tofu Pulse",   "Ashwagandha\n(mandatory)",  "Full Body Flush\n(Legs Up the Wall)"],
            ["SAT",         "Active Yoga\n(15–20 min)",  "3-Cycle Contrast Therapy",     "Saffron",      "CNS Reset"],
            ["SUN",         "Batch Meal Prep",           "Rest / Walk",                  "Tulsi",        "Gentle Mobility"],
        ],
        [0.55*inch, 1.5*inch, 1.9*inch, 1.3*inch, 2.35*inch],
        header_row_style(5) + [
            ("FONTSIZE",   (0,1), (-1,-1), 12),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("FONTNAME",   (1,1), (2,1),   "Helvetica-Bold"),  # Mon
            ("FONTNAME",   (2,2), (2,2),   "Helvetica-Bold"),  # Tue push
            ("FONTNAME",   (2,3), (2,3),   "Helvetica-Bold"),  # Wed pull
            ("FONTNAME",   (1,4), (2,4),   "Helvetica-Bold"),  # Thu VO2
            ("FONTNAME",   (2,5), (2,5),   "Helvetica-Bold"),  # Fri
            ("BACKGROUND", (0,4), (-1,4),  colors.HexColor("#fff3cd")),  # Thu highlight
            ("TEXTCOLOR",  (3,4), (3,5),   WARN),  # Ashwagandha mandatory
            ("FONTNAME",   (3,4), (3,5),   "Helvetica-Bold"),
            ("BACKGROUND", (0,7), (-1,7),  LIGHT),  # Sunday
            ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ],
    ))

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    story.append(Paragraph("Diet Adjustments by Day Type", H2))
    story.append(tbl(
        [
            ["Day type",        "12:00 Quinoa",     "17:30",                "17:50 Casein", "14:30 Dressing"],
            ["Heavy Lift",      "½ cup",            "Whey + creatine\n(mandatory — strict window)", "1 scoop",   "4 tbsp"],
            ["VO2 Max (Thu)",   "¾ cup\n(+50%)",    "Whey + creatine",      "1 scoop",      "4 tbsp"],
            ["Rest / Cardio",   "¼ cup",            "Whey + creatine",      "SKIP\n(no mechanical damage)", "2–4 tbsp"],
        ],
        [1.3*inch, 1.1*inch, 2.1*inch, 1.4*inch, 1.65*inch],
        header_row_style(5) + [
            ("FONTSIZE",   (0,1), (-1,-1), 12),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("FONTNAME",   (1,2), (1,2),   "Helvetica-Bold"),
            ("TEXTCOLOR",  (3,3), (3,3),   WARN),
            ("FONTNAME",   (3,3), (3,3),   "Helvetica-Bold"),
        ],
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    story.append(Paragraph(
        "⚠  COLD PLUNGE RULE — NEVER immediately after heavy lifting. "
        "Blunts mTOR / muscle growth signal. "
        "Minimum 6 hours between cold plunge and lift (cold at 06:30 → lift at 16:30 is correct). "
        "If you feel 'fried' in the morning — swap cold plunge for restorative yoga, skip Matcha.", WARN_S))

    story.append(Spacer(1, 8))
    story.append(Paragraph("VO2 Max 4×4 Progression — do not skip stages", H2))
    story.append(tbl(
        [
            ["Stage",       "Who",                  "Protocol"],
            ["Stage 1",     "Novice",               "Zone 2 fasted walk/jog only — no 4×4s"],
            ["Stage 2",     "Intermediate\n(4–8 wk)","2×4 intervals (2 reps instead of 4). Monitor HRV."],
            ["Stage 3",     "Operator",             "Full 4×4: 4 min max effort → 3 min active recovery → repeat ×4. Proceed only if morning resting HR is stable and 21:00 Ashwagandha is maintained."],
        ],
        [0.75*inch, 1.4*inch, 5.45*inch],
        header_row_style(3) + [
            ("FONTSIZE",   (0,1), (-1,-1), 12),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("BACKGROUND", (0,3), (-1,3),  LIGHT),
        ],
    ))

    # ── PAGE 2: Yoga + Thermal ────────────────────────────────────────────────
    story.append(PageBreak())

    story.append(Paragraph("Yoga & Thermal Protocols", TITLE))
    story.append(Paragraph("Autonomic reset sequences + thermal hormesis methods", SUB))
    story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=10))

    story.append(Paragraph("Yoga Sequences — which to use when", H2))
    story.append(tbl(
        [
            ["Sequence",                "When",             "Duration",     "Key moves"],
            ["Active Morning",          "Replace 06:30 cardio on low-cortisol mornings",
             "15–20 min", "Child's Pose → Cat-Cow × 10 → Downward Dog → Ragdoll → Sun Salutation A ×3–5 → Warrior II → Hanuman Dand ×10 → Savasana"],
            ["Restorative\n(Cortisol Day)", "Morning if 'fried' OR 21:00 night infusion window",
             "15–20 min", "Supported Child's Pose 3–4 min → Supine Spinal Twist 2 min/side → Reclined Bound Angle 3–4 min → LEGS UP THE WALL 5 min → Savasana"],
            ["Post-Lift Stretch",       "Immediately post-workout or active recovery days",
             "10–15 min", "Lizard Lunge 2 min/side → Half Pigeon 2 min/side → Thread the Needle 1 min/side → Seated Forward Fold 2 min"],
        ],
        [1.25*inch, 1.8*inch, 0.9*inch, 3.65*inch],
        header_row_style(4) + [
            ("FONTSIZE",   (0,1), (-1,-1), 11),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("BACKGROUND", (0,2), (-1,2),  colors.HexColor("#fff3cd")),
        ],
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Restorative breath: inhale 4 sec · exhale 8 sec. Night yoga: sip Tulsi or Saffron during or immediately after. "
        "Mantra option: 'So' on inhale, 'Hum' on exhale — interrupts anxiety loop in Default Mode Network.", NOTE))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    story.append(Paragraph("Thermal Hormesis — three methods", H2))
    story.append(tbl(
        [
            ["Method",              "When",             "Protocol",                         "Rule"],
            ["A — Daily Maintenance","Daily",           "Cold plunge 06:30 + Sauna 18:30 (separate, isolated)",
             "Re-warm naturally 10–15 min after cold plunge — activates Brown Adipose Tissue"],
            ["B — Efficiency Pump", "2–3×/week",       "Sauna 15 min → Cold Plunge 3 min\n(immediate transition)",
             "ALWAYS end on cold. Trains endothelial lining."],
            ["C — Weekly Vascular Flush","1×/week (Sat)","3 continuous cycles:\nSauna → Cold → Sauna → Cold → Sauna → Cold",
             "ALWAYS end on cold. Wait 15 min before drinking warm hydration. Clears deep-tissue inflammation."],
        ],
        [1.1*inch, 1.0*inch, 2.7*inch, 2.85*inch],
        header_row_style(4) + [
            ("FONTSIZE",   (0,1), (-1,-1), 11),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("BACKGROUND", (0,3), (-1,3),  LIGHT),
        ],
    ))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=10))

    story.append(Paragraph("Targeted Yoga Pairings by Lift Day", H2))
    story.append(tbl(
        [
            ["Lift Day",            "Mechanical stress",            "Key pose",             "Why"],
            ["Mon — HEAVY LEGS",    "Hip flexors / glute fatigue",  "Half Pigeon",          "Unlocks piriformis + glutes — reduces DOMS and postural tilt"],
            ["Tue — PUSH",          "Internal shoulder rotation",   "Cobra / Upward Dog",   "Heart/chest opening counteracts pec shortening from pressing"],
            ["Wed — PULL",          "Thoracic compression / biceps","Thread the Needle",    "Thoracic rotation + rear delt stretch — prevents rounding"],
            ["Fri — FULL ROTATOR",  "Systemic CNS load",            "Legs Up the Wall",     "Vagal nerve stimulation → fastest HRV recovery tool available"],
        ],
        [1.3*inch, 1.8*inch, 1.3*inch, 3.25*inch],
        header_row_style(4) + [
            ("FONTSIZE",   (0,1), (-1,-1), 12),
            ("FONTNAME",   (0,1), (0,-1),  "Helvetica-Bold"),
            ("FONTNAME",   (2,1), (2,-1),  "Helvetica-Bold"),
        ],
    ))

    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=WARN, spaceAfter=6))
    story.append(Paragraph(
        "⚠  Ice bath > cryo chamber. Water is 25× more thermally conductive than air — "
        "core cooling triggers the sustained dopamine/noradrenaline spike and BAT activation. "
        "Cryo creates an insulating skin boundary layer and cannot replicate this.", WARN_S))

    doc.build(story)
    print("✓ 10-workout.pdf  (page 1 = weekly split, page 2 = yoga + thermal — print duplex)")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
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
    print("\nAll 10 fridge cards written to fridge-sheets/")

import re

path = '05-practical/functional-samosas.md'
with open(path, 'r') as f:
    content = f.read()

summary_section = """
## The 3-Option Architecture (Quick Jump)
To maintain gut resilience and balance your amino acid profile, you must rotate your crusts based on your daily training load:
*   [**Option 1: The Seitan Hybrid Skin**](#option-1-the-seitan-hybrid-skin-high-protein) — The **"Protein Bomb."** 90% VWG. Used on M/W/F (Heavy Lift days) for maximal muscle recovery (~50g protein for two).
*   [**Option 2: The "Daily Bread" Hybrid**](#option-2-the-daily-bread-hybrid-atta--vwg) — The **"Standard Balance."** 50% Atta / 50% VWG. Excellent texture, hits your 40g target without fortification.
*   [**Option 3: The 'Green Crystal' GF Skin**](#option-3-the-green-crystal-gf-skin-rice-tapioca--moringa) — The **"Fiber Sweep."** Tapioca/Rice/Moringa base. Used on T/Th/S (Rest/Cardio days) for GI motility. Requires Pea/Rice fortification to hit the 40g target.

---
"""

if "## The 3-Option Architecture (Quick Jump)" not in content:
    content = content.replace('---', summary_section, 1) # Replace the first hr line after Objectives

with open(path, 'w') as f:
    f.write(content)

print("Updated functional-samosas.md with Quick Jump Summary")

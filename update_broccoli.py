import os, glob, re

# 1. Update Execution Files
for filepath in glob.glob("03-execution/week-*/*.md"):
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = re.sub(r'\*.*150g broccoli.*\n', '', content)
    content = re.sub(r'\d+\.\s*Sauté broccoli.*\n', '', content)
    content = re.sub(r'\d+\.\s*Sauté rested broccoli.*\n', '', content)
    content = re.sub(r'\*.*\d+/\d+ cup microgreens.*\n', '*   **1 cup Broccoli Microgreens** (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)\n', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

# 2. Update sunday-prep.md
with open("05-practical/sunday-prep.md", "r") as f:
    prep = f.read()
prep = re.sub(r'Chop \*\*7 portions of broccoli\*\* \(~150g each\)\.', 'Portion **7 cups of Broccoli Microgreens** for the daily salads.', prep)
prep = re.sub(r'Let rest for 30 minutes \(non-negotiable for sulforaphane\)\.', 'Keep dry in the original container with a paper towel.', prep)
prep = re.sub(r'Chop fresh broccoli, refresh paper towels', 'Refresh paper towels in microgreen and leafy green containers', prep)
prep = re.sub(r'\*   \*\*The Workflow:\*\* Broccoli is chopped and allowed to \*\*rest for 30 minutes\*\* before being stored or cooked\.\n\*   \*\*The Benefit:\*\* Chopping breaks the plant cell walls, allowing the enzyme \*myrosinase\* to interact with \*glucoraphanin\* to create \*\*Sulforaphane\*\*\. Resting ensures the reaction is complete before heat is applied, as heat destroys the myrosinase enzyme\.', '*   **The Workflow:** Mature broccoli is replaced with **Broccoli Microgreens**.\n*   **The Benefit:** Microgreens contain up to 50x the glucoraphanin of mature broccoli. Because they are eaten raw in the salad, the myrosinase enzyme remains 100% intact, requiring no chopping, resting, or heat management.', prep)
with open("05-practical/sunday-prep.md", "w") as f:
    f.write(prep)

# 3. Update protocol-broccoli.md
new_broccoli = """---
title: 'The Protocol Broccoli (Microgreen Sulforaphane Engine)'
section: 'practical'
type: 'procedure'
priority: 'high'
---

# The Protocol Broccoli (Microgreen Sulforaphane Engine)

Broccoli is not treated as a side dish in this protocol; it is the primary pharmacological vector for **Nrf2 activation** (Phase II liver detoxification and DNA protection). 

Historically, the protocol required chopping 150g of mature broccoli, resting it for 30 minutes to form sulforaphane, and strictly managing cooking temperatures. **This has been upgraded.** The protocol now exclusively uses **Broccoli Microgreens** to achieve a 50x magnitude increase in signaling efficiency while eliminating cooking friction.

## Ingredients (Daily Portion)

*   **1 Cup Fresh Broccoli Microgreens** (Must be specifically Broccoli or Radish, not a generic "mild mix").
*   **1/2 tsp Mustard Seed Powder** (Optional Exogenous Enzyme Booster).

## The 50x Multiplier (Why Microgreens?)
Sulforaphane does not exist intact in the plant. It is formed when the precursor (*glucoraphanin*) mixes with the enzyme (*myrosinase*). 
1.  **Density:** 3-day-old broccoli microgreens contain 10 to 100 times higher levels of glucoraphanin than mature broccoli florets.
2.  **Enzyme Preservation:** Because you consume microgreens completely raw in your 14:30 Salad Layer, the *myrosinase* enzyme is 100% intact. There is no risk of a "Thermal Ceiling" destroying the enzyme during cooking.

## Execution (The Salad Drop)
*   **Timing:** 14:30 Salad Window.
*   **Action:** Simply place 1 full cup of raw Broccoli Microgreens on top of your daily greens.
*   **The Mustard Hack (Optional):** If you want to absolutely maximize conversion in the gut, you can sprinkle 1/2 tsp of Mustard Seed powder directly into your wet salad dressing before tossing. Mustard seeds contain highly resilient myrosinase that acts as an exogenous "insurance policy" [[4]](../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control).

## Related Pages
- [Inflammatory Signaling Control](../01-foundations/02-inflammatory-control.md)
- [Liver Load Spacing and Detox Pathways](../04-advanced-control/liver-load.md)
- [Master Citations (Sulforaphane)](../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)
"""
with open("05-practical/protocol-broccoli.md", "w") as f:
    f.write(new_broccoli)

# 4. Remove microgreens.md from indexes
def remove_line(filepath, pattern):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        lines = f.readlines()
    with open(filepath, 'w') as f:
        for line in lines:
            if pattern not in line:
                f.write(line)
                
remove_line("README.md", "02-ingredients/microgreens.md")
remove_line("02-ingredients/README.md", "(microgreens.md)")
remove_line("02-ingredients/cilantro.md", "microgreens.md")

# Update daily-salad-layer.md
with open("05-practical/daily-salad-layer.md", "r") as f:
    salad = f.read()
salad = re.sub(r'\*   \*\*Microgreens \(1/2 cup\):\*\* Concentrated sulforaphane and enzyme potential.*', '*   **Broccoli Microgreens (1 cup):** Concentrated sulforaphane and enzyme potential (The Sulforaphane Engine) [[13]](../07-appendices/master-citations.md#13-metabolic-oncology--chemoprevention).', salad)
with open("05-practical/daily-salad-layer.md", "w") as f:
    f.write(salad)

# 5. Delete microgreens.md
if os.path.exists("02-ingredients/microgreens.md"):
    os.remove("02-ingredients/microgreens.md")

# 6. Update liver-load.md
with open("04-advanced-control/liver-load.md", "r") as f:
    ll = f.read()
ll = re.sub(r'\*   \*\*The "Chop & Rest" Rule:\*\* Broccoli must be chopped and left at \*\*room temperature for 30 minutes\*\* before cooking.*', '*   **The Raw Microgreen Rule:** The protocol uses 1 cup of raw Broccoli Microgreens in the 14:30 salad. Because they are eaten raw, the myrosinase enzyme is preserved 100%, and no chopping/resting is required [[4]](../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control).', ll)
with open("04-advanced-control/liver-load.md", "w") as f:
    f.write(ll)

# 7. Update inflammatory-control.md
with open("01-foundations/02-inflammatory-control.md", "r") as f:
    ic = f.read()
ic = re.sub(r'2\.  \*\*Broccoli must be chopped and rested for 30 minutes\.\*\*', '2.  **Broccoli Microgreens are used exclusively (raw) to preserve myrosinase.**', ic)
ic = re.sub(r'3\.  \*\*Cooking must be brief \(under 4 minutes\)\.\*\*', '3.  **Cooking is eliminated to prevent the thermal destruction of myrosinase.**', ic)
ic = re.sub(r'- Cooking broccoli immediately after chopping works against the sulforaphane workflow described here\.', '- Cooking mature broccoli destroys myrosinase; microgreens bypass this entirely.', ic)
with open("01-foundations/02-inflammatory-control.md", "w") as f:
    f.write(ic)

# 8. Update ingredient-conflict-matrix.md
with open("07-appendices/ingredient-conflict-matrix.md", "r") as f:
    icm = f.read()
icm = icm.replace(
    "| **Broccoli cooked immediately after chopping** | Heat can erase the sulforaphane workflow if the myrosinase reaction has not finished. | Chop first, rest 30 minutes, then cook briefly and add mustard powder off heat. |",
    "| **Cooking Broccoli Microgreens** | Heat will erase the myrosinase enzyme and the sulforaphane workflow. | Eat the 1 cup of Broccoli Microgreens completely raw in the 14:30 Salad Layer. |"
)
with open("07-appendices/ingredient-conflict-matrix.md", "w") as f:
    f.write(icm)

# 9. Update weekly-prep-mis-en-place.md
with open("05-practical/weekly-prep-mis-en-place.md", "r") as f:
    mep = f.read()
mep = re.sub(r'2-3 large heads Broccoli', '4-5 boxes Broccoli Microgreens', mep)
mep = re.sub(r'\| \*\*Main Meal\*\* \| Broccoli \| 150g daily \| \*\*Chopped and rested 30 mins\*\* before storage\. \|', '| **Salad Layer** | Broccoli Microgreens | 1 cup daily | **Raw**. Keep in original container with paper towel. |', mep)
with open("05-practical/weekly-prep-mis-en-place.md", "w") as f:
    f.write(mep)

print("Update complete.")

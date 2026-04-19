import re

# Jaljeera
path1 = '05-practical/peppermint-jaljeera.md'
with open(path1, 'r') as f:
    content1 = f.read()

macro_box1 = """
## Macro Profile (Per Serving)
*   **Calories:** ~5 kcal | **Fat:** 0g | **Protein:** 0g | **Net Carbs:** ~1g | **Complex Carbs:** 0g
*   *Note:* This drink is utilized entirely for mineral replenishment, enzymatic signaling, and hydration, not macronutrient delivery.
"""
if "## Macro Profile" not in content1:
    content1 = content1.replace('## Core Ingredients', macro_box1 + '\n## Core Ingredients')
with open(path1, 'w') as f:
    f.write(content1)

# Garlic Chili Oil
path2 = '05-practical/garlic-chili-oil.md'
with open(path2, 'r') as f:
    content2 = f.read()

macro_box2 = """
## Macro Profile (Per 1 Tbsp Serving)
*   **Calories:** ~120 kcal
*   **Fat:** ~14g (Primarily Monounsaturated from Avocado Oil)
*   **Protein:** 0g
*   **Net Carbs:** 0g
*   **Complex Carbs:** 0g
*   *Note:* The garlic and chili particulate provide trace fiber and dense phytochemicals (Allicin/Capsaicin), but negligible caloric impact.
"""
if "## Macro Profile" not in content2:
    content2 = content2.replace('## Required Inputs', macro_box2 + '\n## Required Inputs')
with open(path2, 'w') as f:
    f.write(content2)

# Lauki
path3 = '05-practical/lauki-reset.md'
with open(path3, 'r') as f:
    content3 = f.read()

macro_box3 = """
## Macro Profile (Per 1 Cup Cooked)
*   **Calories:** ~16 kcal
*   **Total Protein:** ~0.5g
*   **Total Carbs:** ~4g
*   **Dietary Fiber:** ~1.5g *(Insoluble sweep)*
*   **Complex Carbs:** ~2g
*   **Net Carbs:** ~2.5g
*   **Fat:** 0g
"""
if "## Macro Profile" not in content3:
    content3 = content3.replace('## Preparation Rules', macro_box3 + '\n## Preparation Rules')
with open(path3, 'w') as f:
    f.write(content3)

print("Updated remaining recipes with macros")

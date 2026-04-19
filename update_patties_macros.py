import re

path = '05-practical/vegan-protein-patties.md'
with open(path, 'r') as f:
    content = f.read()

macro_box = """
## Macro Profile (Per Serving: 2 Patties)
*   **Calories:** ~305 kcal
*   **Total Protein:** ~27g *(Complete EAA profile from Pea/VWG/Chickpeas)*
*   **Total Carbs:** ~25g
*   **Dietary Fiber:** ~6g
*   **Complex Carbs (RS3/Starches):** ~15g *(Sustained energy)*
*   **Net Carbs:** ~19g
*   **Fat:** ~8.5g (Olive Oil + Natural lipids)
"""

if "## Macro Profile" not in content:
    content = content.replace('## Inputs', macro_box + '\n## Inputs')

with open(path, 'w') as f:
    f.write(content)

print("Updated vegan-protein-patties.md with inline macros")

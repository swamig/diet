import re

path = '05-practical/protocol-chickpeas.md'
with open(path, 'r') as f:
    content = f.read()

macro_box = """
## Macro Profile (Per 1 Cup Cooked/Chilled)
*   **Calories:** ~270 kcal
*   **Total Protein:** ~15g
*   **Total Carbs:** ~45g
*   **Dietary Fiber:** ~12g *(Dense Prebiotic load)*
*   **Complex Carbs (RS3/Starches):** ~28g *(Slow-release energy)*
*   **Net Carbs:** ~33g
*   **Fat:** ~4g
"""

if "## Macro Profile" not in content:
    content = content.replace('## Ingredients (Weekly Batch)', macro_box + '\n## Ingredients (Weekly Batch)')

with open(path, 'w') as f:
    f.write(content)

print("Updated protocol-chickpeas.md with inline macros")

import re

path = '05-practical/performance-refried-beans.md'
with open(path, 'r') as f:
    content = f.read()

macro_box = """
## Macro Profile (Per Serving: 1 Cup)
*   **Calories:** ~310 kcal
*   **Total Protein:** ~15g
*   **Total Carbs:** ~45g
*   **Dietary Fiber:** ~12g *(Dense Prebiotic load)*
*   **Complex Carbs (RS3/Starches):** ~28g *(Slow-release energy)*
*   **Net Carbs:** ~33g
*   **Fat:** ~8.5g (Garlic Chili Oil)
"""

if "## Macro Profile" not in content:
    content = content.replace('## The Components', macro_box + '\n## The Components')

with open(path, 'w') as f:
    f.write(content)

print("Updated performance-refried-beans.md with inline macros")

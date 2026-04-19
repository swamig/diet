import re

path = '05-practical/protocol-quinoa.md'
with open(path, 'r') as f:
    content = f.read()

macro_box = """
## Macro Profile (By Portion Size)
*   **Standard Day (1/2 Cup Cooked):** ~111 kcal | **Protein:** 4g | **Total Carbs:** 20g | **Fiber:** 2.5g | **Complex Carbs (RS3):** ~15g | **Net Carbs:** ~17.5g
*   **Rest/Cardio Day (1/4 Cup Cooked):** ~55 kcal | **Protein:** 2g | **Total Carbs:** 10g | **Fiber:** 1.3g | **Complex Carbs (RS3):** ~7.5g | **Net Carbs:** ~8.7g
*   **VO2 Max 4x4 Day (3/4 Cup Cooked):** ~166 kcal | **Protein:** 6g | **Total Carbs:** 30g | **Fiber:** 3.8g | **Complex Carbs (RS3):** ~22.5g | **Net Carbs:** ~26.2g
"""

if "## Macro Profile" not in content:
    content = content.replace('## Protocol Dosing & Timing', macro_box + '\n## Protocol Dosing & Timing')

with open(path, 'w') as f:
    f.write(content)

print("Updated protocol-quinoa.md with inline macros")

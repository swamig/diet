import re

path = '05-practical/functional-samosas.md'
with open(path, 'r') as f:
    content = f.read()

# Replace Option 1
old_opt1 = """### Macro Profile (For 2 Samosas)
*   **Total Protein:** ~50g
*   **Total Carbs:** ~32g
*   **Dietary Fiber:** ~10g
*   **Complex Carbs (RS3/Starches):** ~20g *(Sustained energy, flat insulin curve)*
*   **Net Carbs:** ~22g
*   **Fat:** ~12g (Avocado Oil)"""

new_opt1 = """### Macro Profile (For 2 Samosas)
*   **Protocol Window:** **Heavy Lift (M/W/F)**
*   **Total Protein:** ~50g
*   **Total Carbs:** ~32g
*   **Dietary Fiber:** ~10g
*   **Complex Carbs (RS3/Starches):** ~20g *(Sustained energy, flat insulin curve)*
*   **Net Carbs:** ~22g
*   **Fat:** ~12g (Avocado Oil)"""
content = content.replace(old_opt1, new_opt1)

# Replace Option 2
old_opt2 = """### Macro Profile (For 2 Samosas)
*   **Total Protein:** ~40g
*   **Total Carbs:** ~42g
*   **Dietary Fiber:** ~14g
*   **Complex Carbs (RS3/Starches):** ~26g *(Moderate glycemic load)*
*   **Net Carbs:** ~28g
*   **Fat:** ~12g (Avocado Oil)"""

new_opt2 = """### Macro Profile (For 2 Samosas)
*   **Protocol Window:** **Standard (Any)**
*   **Total Protein:** ~40g
*   **Total Carbs:** ~42g
*   **Dietary Fiber:** ~14g
*   **Complex Carbs (RS3/Starches):** ~26g *(Moderate glycemic load)*
*   **Net Carbs:** ~28g
*   **Fat:** ~12g (Avocado Oil)"""
content = content.replace(old_opt2, new_opt2)

# Replace Option 3
old_opt3 = """### Macro Profile (For 2 Samosas + 1 Scoop Pea/Rice Protein)
*   **Total Protein:** ~42g
*   **Total Carbs:** ~48g
*   **Dietary Fiber:** ~16g (Massive Psyllium Sweep)
*   **Complex Carbs (RS3/Starches):** ~30g *(Tapioca/Rice delayed by fiber gel)*
*   **Net Carbs:** ~32g
*   **Fat:** ~12g (Avocado Oil)"""

new_opt3 = """### Macro Profile (For 2 Samosas + 1 Scoop Pea/Rice Protein)
*   **Protocol Window:** **Rest/Recovery (T/Th/S)**
*   **Total Protein:** ~42g
*   **Total Carbs:** ~48g
*   **Dietary Fiber:** ~16g (Massive Psyllium Sweep)
*   **Complex Carbs (RS3/Starches):** ~30g *(Tapioca/Rice delayed by fiber gel)*
*   **Net Carbs:** ~32g
*   **Fat:** ~12g (Avocado Oil)"""
content = content.replace(old_opt3, new_opt3)

# Remove the redundant Macro Summary table at the bottom to avoid confusion
content = re.sub(r'## Macro Summary \(For 2 Samosas\)\n\n\| Metric.*?\n\n', '', content, flags=re.DOTALL)

with open(path, 'w') as f:
    f.write(content)

print("Updated functional-samosas.md inline macros and removed duplicate table")

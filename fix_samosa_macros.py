import re

path = '05-practical/functional-samosas.md'
with open(path, 'r') as f:
    content = f.read()

# Add Macro box to Option 1
macro_opt1 = """
### Macro Profile (For 2 Samosas)
*   **Total Protein:** ~50g
*   **Total Carbs:** ~32g
*   **Dietary Fiber:** ~10g
*   **Complex Carbs (RS3/Starches):** ~20g *(Sustained energy, flat insulin curve)*
*   **Net Carbs:** ~22g
*   **Fat:** ~12g (Avocado Oil)
"""
# Find Option 1 Execution section and append the macro box
content = re.sub(r'(Air Fry at \*\*400°F \(200°C\) for 7-8 minutes\*\*\.)', r'\1\n' + macro_opt1, content)

# Add Macro box to Option 2
macro_opt2 = """
### Macro Profile (For 2 Samosas)
*   **Total Protein:** ~40g
*   **Total Carbs:** ~42g
*   **Dietary Fiber:** ~14g
*   **Complex Carbs (RS3/Starches):** ~26g *(Moderate glycemic load)*
*   **Net Carbs:** ~28g
*   **Fat:** ~12g (Avocado Oil)
"""
# Find Option 2 Execution section and append the macro box
content = re.sub(r'(Air Fry at \*\*390°F \(195°C\) for 8-10 minutes\*\*\.)', r'\1\n' + macro_opt2, content)

# Add Macro box to Option 3
macro_opt3 = """
### Macro Profile (For 2 Samosas + 1 Scoop Pea/Rice Protein)
*   **Total Protein:** ~42g
*   **Total Carbs:** ~48g
*   **Dietary Fiber:** ~16g (Massive Psyllium Sweep)
*   **Complex Carbs (RS3/Starches):** ~30g *(Tapioca/Rice delayed by fiber gel)*
*   **Net Carbs:** ~32g
*   **Fat:** ~12g (Avocado Oil)
"""
# Find Option 3 Execution section and append the macro box
content = re.sub(r'(Air Fry at \*\*380°F \(190°C\) for 10-12 minutes\*\*\.)', r'\1\n' + macro_opt3, content)

with open(path, 'w') as f:
    f.write(content)

print("Updated functional-samosas.md with inline macros")

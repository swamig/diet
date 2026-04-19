import re

path = '05-practical/functional-samosas.md'
with open(path, 'r') as f:
    content = f.read()

# The script seems to have appended the macros multiple times because I ran it twice. Let's clean it up.
# First, remove ALL occurrences of the macro profile blocks
content = re.sub(r'### Macro Profile.*?Fat:.*?\(Avocado Oil\)\n', '', content, flags=re.DOTALL)

# Now, add them back ONCE after the cook instruction.
macro_opt1 = """
### Macro Profile (For 2 Samosas)
*   **Total Protein:** ~50g
*   **Total Carbs:** ~32g
*   **Dietary Fiber:** ~10g
*   **Complex Carbs (RS3/Starches):** ~20g *(Sustained energy, flat insulin curve)*
*   **Net Carbs:** ~22g
*   **Fat:** ~12g (Avocado Oil)
"""
content = re.sub(r'(Air Fry at \*\*400°F \(200°C\) for 7-8 minutes\*\*\.)', r'\1\n' + macro_opt1, content)

macro_opt2 = """
### Macro Profile (For 2 Samosas)
*   **Total Protein:** ~40g
*   **Total Carbs:** ~42g
*   **Dietary Fiber:** ~14g
*   **Complex Carbs (RS3/Starches):** ~26g *(Moderate glycemic load)*
*   **Net Carbs:** ~28g
*   **Fat:** ~12g (Avocado Oil)
"""
content = re.sub(r'(Air Fry at \*\*390°F \(195°C\) for 8-10 minutes\*\*\.)', r'\1\n' + macro_opt2, content)

macro_opt3 = """
### Macro Profile (For 2 Samosas + 1 Scoop Pea/Rice Protein)
*   **Total Protein:** ~42g
*   **Total Carbs:** ~48g
*   **Dietary Fiber:** ~16g (Massive Psyllium Sweep)
*   **Complex Carbs (RS3/Starches):** ~30g *(Tapioca/Rice delayed by fiber gel)*
*   **Net Carbs:** ~32g
*   **Fat:** ~12g (Avocado Oil)
"""
content = re.sub(r'(Air Fry at \*\*380°F \(190°C\) for 10-12 minutes\*\*\.)', r'\1\n' + macro_opt3, content)

# There is a duplicate summary table at the bottom of the file (from a previous edit). I will remove the inline macros from the script above that were duplicating it.
# Actually, the user wants the macros INLINE under each section, AND they want complex carbs explicitly stated.

with open(path, 'w') as f:
    f.write(content)

print("Fixed duplicate macros in functional-samosas.md")

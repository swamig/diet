import re

path = '05-practical/functional-indian-formats.md'
with open(path, 'r') as f:
    content = f.read()

macro_box = """
## High-Signaling Format Macros (Per Standard 2 Tbsp Serving)
*   **MCT Coconut Chutney:** ~35 kcal | **Fat:** ~3.5g (MCT) | **Net Carbs:** ~1g | **Complex Carbs:** 0g
*   **Imlee (Tamarind) Chutney (Sugar-Free):** ~15 kcal | **Fat:** 0g | **Net Carbs:** ~3g | **Complex Carbs:** ~1g (Pectin)
*   **TRP Mint/Cilantro Chutney:** ~5 kcal | **Fat:** 0g | **Net Carbs:** ~1g | **Complex Carbs:** 0g
*   **Raw Toum (Garlic Paste):** ~85 kcal | **Fat:** ~9g (Avocado Oil) | **Net Carbs:** ~1g | **Complex Carbs:** 0g
*   **Vascular Podi (Gunpowder):** ~45 kcal | **Fat:** ~3.5g | **Protein:** ~2g | **Fiber:** ~1.5g
"""

if "## High-Signaling Format Macros" not in content:
    content = content.replace('## 1. High-Signaling Chutneys', macro_box + '\n## 1. High-Signaling Chutneys')

with open(path, 'w') as f:
    f.write(content)

print("Updated functional-indian-formats.md with inline macros")

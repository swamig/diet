import re

path = '05-practical/functional-samosas.md'
with open(path, 'r') as f:
    content = f.read()

spicy_variant_text = """
*   **The High-Signaling (Spicy) Variant (Optional):** Add **1/2 tsp Kashmiri Chili Powder**, **1/2 tsp Amchur (Dried Mango Powder)**, and **1-2 finely chopped Green Chilies**. *Reasoning:* This increases the capsaicin load, which synergizes with the Ajwain in the crust to further accelerate gastric emptying.
"""

if "High-Signaling (Spicy) Variant" not in content:
    # Find the end of the Ingredients list under Master Filling
    insert_pos = content.find("### Instructions:")
    if insert_pos != -1:
        content = content[:insert_pos] + spicy_variant_text + "\n" + content[insert_pos:]
        with open(path, 'w') as f:
            f.write(content)
        print("Added Spicy Variant to Samosas")

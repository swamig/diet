import re

path = '05-practical/garlic-chili-oil.md'
with open(path, 'r') as f:
    content = f.read()

wet_curry_text = """
## The "Wet Curry" Variant (Optional)
To convert this into a creamy "Wet Kadhi" without violating the Dairy Blockade:
1.  At **00:25** (after tearing the mint), add **2-3 tbsp of full-fat coconut milk** directly to the hot pan. 
2.  Stir vigorously for 30-60 seconds until the coconut milk reduces into a thick, spiced glaze coating the tofu.
3.  **CRITICAL (The Lipid Substitution Rule):** Coconut milk is high in MCTs. If you use this variant, you **MUST** reduce your 14:30 Salad Dressing oil by 1 tbsp to maintain the protocol's caloric ceiling.
"""

if '## The "Wet Curry" Variant' not in content:
    content = content.replace("## Benefits of the Fresh Method", wet_curry_text + "\n## Benefits of the Fresh Method")
    with open(path, 'w') as f:
        f.write(content)
    print("Updated garlic-chili-oil.md")
else:
    print("Already updated garlic-chili-oil.md")

import re

path = '05-practical/sunday-prep.md'
with open(path, 'r') as f:
    content = f.read()

# I will add it under Block 4: Salad Infrastructure
lauki_text = """
**Optional Veggie Upgrades (Lauki for Tofu Days):**
1.  **Peel & Taste:** Peel 1-2 cups of Lauki. Cut a tiny slice and taste it raw. (If it is bitter, THROW IT AWAY—it is toxic).
2.  **Grate:** If it tastes neutral/sweet, grate the flesh.
3.  **Storage (CRITICAL):** Store the *raw, unsalted* shreds in an airtight glass container lined with a dry paper towel. **Do NOT salt it on Sunday** (salt will cause it to turn into a mushy puddle by Wednesday). Salt it right before pressing/cooking on the day of.
"""

if "Optional Veggie Upgrades" not in content:
    content = content.replace("## Block 5: Spice Mix", lauki_text + "\n## Block 5: Spice Mix")
    with open(path, 'w') as f:
        f.write(content)
    print("Added Lauki prep to sunday-prep.md")


import re

# 1. Update the Practical Guide
path = '05-practical/vegan-protein-patties.md'
with open(path, 'r') as f:
    content = f.read()

new_sear_inst = """10. **The Final Sear (The "Flash Allicin Crust"):** When you are ready to eat them at 12:00, you must protect the RS3 while restoring the Allicin signal lost during Sunday prep.
    *   **The Allicin Prep:** Crush 1-2 cloves fresh garlic (rest 10 min).
    *   **The Bloom:** Heat a pan with a tiny drizzle of avocado oil on medium-low. Add the rested garlic and the **Daily Spice Jar** powders to the oil.
    *   **The Sear:** Quickly sear the patty for 60-90 seconds per side, allowing the garlic and spices to "crust" the exterior.
    *   **The Iron Anchor:** Remove from heat and **squeeze 1/2 fresh lemon** directly over the hot patties immediately before serving. This restores the Vitamin C anchor for 100% iron bioavailability."""

# Find the old section 10 and replace it
pattern = r"10\.\s+\*\*The Final Sear.*?Flash-roast.*?(?=\n\n|\n---)" # Adjusting to match the file's section 10
# Actually let's just use a more direct string replacement since I have the file content
old_sear_start = '10. **The Final Sear (The "Flash Bloom")**'
# The search showed: 10. **The Final Sear (The "Flash Bloom"):**
old_sear_start_v2 = '10. **The Final Sear (The "Flash Bloom"):**'

if old_sear_start_v2 in content:
    # Find the end of that section
    section_end = content.find("---", content.find(old_sear_start_v2))
    if section_end == -1: section_end = len(content)
    
    content = content.replace(content[content.find(old_sear_start_v2):section_end], new_sear_inst + "\n\n")

with open(path, 'w') as f:
    f.write(content)
print("Updated vegan-protein-patties.md")

# 2. Update all daily execution files that use patties
import glob
days = glob.glob("03-execution/week-*/day-*.md")
for d in days:
    with open(d, 'r') as f:
        c = f.read()
    
    # We only update if it's a Patty day (not Tofu)
    if "## Main Meal: Tofu" not in c and "Sear patties" in c:
        # Replace the simple sear with the Allicin Crust version
        old_inst = """**Instructions:**
1.  Sear patties.
2.  Sear 3-4 min/side."""
        
        new_inst = """**Instructions:**
1.  **Allicin Prep:** Crush 1-2 cloves garlic (rest 10 min).
2.  **The Bloom:** Heat oil in pan; add rested garlic and Daily Spice Jar.
3.  **The Sear:** Sear patties 2-3 min/side to create a "Garlic Crust."
4.  **The Iron Anchor:** Squeeze 1/2 fresh lemon over patties before serving."""
        
        if old_inst in c:
            c = c.replace(old_inst, new_inst)
            with open(d, 'w') as f:
                f.write(c)
            print(f"Updated {d}")


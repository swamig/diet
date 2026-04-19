import re
import glob

days = glob.glob("03-execution/week-*/day-*.md")
new_inst = """**Instructions:**
1.  **Allicin Prep:** Crush 1-2 cloves garlic (rest 10 min).
2.  **The Bloom:** Heat oil in pan; add rested garlic and Daily Spice Jar.
3.  **The Sear:** Sear patties 2-3 min/side to create a "Garlic Crust."
4.  **The Iron Anchor:** Squeeze 1/2 fresh lemon over patties before serving."""

for d in days:
    with open(d, 'r') as f:
        c = f.read()
    
    if "## Main Meal: Tofu" not in c:
        # Match anything starting with **Instructions:** and ending before the next heading or end of file
        # Specifically targeting the patty sear instructions
        pattern = r"\*\*Instructions:\*\*.*?(?=\n\n##|\Z)"
        if "**Instructions:**" in c and "Sear patties" in c:
            c = re.sub(pattern, new_inst, c, flags=re.DOTALL)
            with open(d, 'w') as f:
                f.write(c)
            print(f"Updated {d}")

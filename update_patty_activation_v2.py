import re
import glob

days = glob.glob("03-execution/week-*/day-*.md")
for d in days:
    with open(d, 'r') as f:
        c = f.read()
    
    if "## Main Meal: Tofu" not in c and "**Instructions:**" in c:
        # Check for various forms of patty instructions
        patterns = [
            r"\*\*Instructions:\*\*\n1\.\s+Sear patties\.\n2\.\s+Sear 3-4 min/side\.",
            r"\*\*Instructions:\*\*\n1\.\s+Sear patties with spice mix/nigella\.\n2\.\s+Sear 5-6 min/side \(165°F\)\."
        ]
        
        new_inst = """**Instructions:**
1.  **Allicin Prep:** Crush 1-2 cloves garlic (rest 10 min).
2.  **The Bloom:** Heat oil in pan; add rested garlic and Daily Spice Jar.
3.  **The Sear:** Sear patties 2-3 min/side to create a "Garlic Crust."
4.  **The Iron Anchor:** Squeeze 1/2 fresh lemon over patties before serving."""
        
        updated = False
        for p in patterns:
            if re.search(p, c):
                c = re.sub(p, new_inst, c)
                updated = True
        
        if updated:
            with open(d, 'w') as f:
                f.write(c)
            print(f"Updated {d}")

import re

tofu_days = [
    "03-execution/week-01/day-05.md",
    "03-execution/week-02/day-12.md",
    "03-execution/week-03/day-19.md",
    "03-execution/week-04/day-26.md"
]

for path in tofu_days:
    with open(path, 'r') as f:
        content = f.read()

    # Add Lauki to Ingredients
    lauki_ing = """*   **Optional Volume Upgrade (Lauki Pakoda):** 1/2 cup grated Lauki + 2-3 tbsp Besan + 1/4 tsp Ajwain + 1/4 tsp Kala Namak + 1/2 tsp Grated Ginger."""
    if "Lauki Pakoda" not in content:
        content = content.replace("## Main Meal: Tofu", "## Main Meal: Tofu\n" + lauki_ing)

    # Update Instructions with the Strainer Hack
    new_instructions = """**Instructions:**
1.  **Smash & Rest:** Crush garlic cloves; set aside for 10 min to activate allicin.
2.  **Lauki Prep (Optional):** Grate Lauki and toss with Kala Namak. Let sit for 2 min. Press hard through a **fine mesh strainer** using a spoon to extract all juice (drink the juice!). 
3.  **The Pakoda Bind:** Mix the dry lauki shreds with Besan, Ajwain, and Ginger until a thick dough forms.
4.  **Rub:** Coat pressed tofu cubes with the dry spice mix.
5.  **The Bloom:** Place oil, methi, chilies, and garlic in a COLD pan. Turn heat to low; let bloom for 5 min until methi is golden.
6.  **The Sear:** Increase heat to med-high. Add tofu **and small flat discs of Lauki dough** to the pan. Sear both for 3-4 min/side.
7.  **The Wet Kadhi:** Tear mint leaves over pan. Add 2-3 tbsp coconut milk; stir for 30s until it forms a thick glaze coating both tofu and pakodas."""

    # Replace the previous instructions block
    # We look for the start of the instruction block we just made in the last turn
    start_mark = "**Instructions:**"
    end_mark = "## Salad"
    
    start_idx = content.find(start_mark)
    end_idx = content.find(end_mark)
    
    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + new_instructions + "\n\n" + content[end_idx:]

    with open(path, 'w') as f:
        f.write(content)
    print(f"Added Lauki Upgrade to {path}")


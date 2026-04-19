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

    # Identify the ingredient block
    # We want to insert Methi, Garlic, Chili, Mint
    ingredients_start = content.find("**Ingredients:**")
    instructions_start = content.find("**Instructions:**")
    
    if ingredients_start != -1 and instructions_start != -1:
        # Extract existing ingredients to preserve them (like Quinoa amounts which vary)
        ing_block = content[ingredients_start:instructions_start]
        
        # Add the "Fresh Pulse" anchors to ingredients
        new_ing_block = ing_block.strip()
        if "Methi" not in new_ing_block:
            new_ing_block += "\n*   **1/4 tsp Whole Methi Seeds** (Glycemic Anchor)\n*   **2-3 Cloves Garlic** (Crushed)\n*   **1-2 Thai Bird’s Eye Chilies**\n*   **Fresh Peppermint Leaves** (Mentha arvensis)"
        
        # New Integrated Instructions
        new_instructions = """**Instructions:**
1.  **Smash & Rest:** Crush garlic cloves; set aside for 10 min to activate allicin.
2.  **Rub:** Coat pressed tofu cubes with the dry spice mix.
3.  **The Bloom:** Place oil, methi, chilies, and garlic in a COLD pan. Turn heat to low; let bloom for 5 min until methi is golden.
4.  **The Sear:** Increase heat to med-high. Sear tofu 3-4 min/side.
5.  **The Wet Kadhi:** Tear mint leaves over tofu. Add 2-3 tbsp coconut milk; stir for 30s until it forms a thick glaze. (If used, reduce 14:30 Salad oil by 1 tbsp)."""

        # Replace the old blocks
        content = content[:ingredients_start] + new_ing_block + "\n\n" + new_instructions + content[content.find("## Salad"):]
        
        with open(path, 'w') as f:
            f.write(content)
        print(f"Fully integrated recipe into {path}")


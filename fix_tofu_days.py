import os
import glob

tofu_instruction_replacement = """**Instructions:**
1.  Rub tofu with spice mix.
2.  Sear 3-4 min/side.
3.  *(Optional Wet Curry)*: Add 2-3 tbsp coconut milk to the pan for the final 60 seconds to create a thick glaze. (If used, reduce 14:30 Salad oil by 1 tbsp)."""

# First, fix days 5 and 12
for day_file in ["03-execution/week-01/day-05.md", "03-execution/week-02/day-12.md"]:
    with open(day_file, 'r') as f:
        content = f.read()
    
    old_inst = "**Instructions:**\n1.  Rub tofu with spice mix.\n2.  Sear 3-4 min/side."
    if old_inst in content:
        content = content.replace(old_inst, tofu_instruction_replacement)
        with open(day_file, 'w') as f:
            f.write(content)
        print(f"Updated instructions in {day_file}")

# Next, fix days 19 and 26 which have the Patty copy-paste bug under the Tofu heading
for day_file in ["03-execution/week-03/day-19.md", "03-execution/week-04/day-26.md"]:
    with open(day_file, 'r') as f:
        content = f.read()
    
    # Check if the Patty bug exists under Tofu heading
    if "## Main Meal: Tofu" in content and "*   2 Vegan Protein Patties" in content:
        print(f"Found patty bug in {day_file}, fixing ingredients and instructions...")
        
        # Replace ingredients
        content = content.replace("*   2 Vegan Protein Patties + 1/2 cup Chickpeas", "*   200g firm tofu (pressed 15 min)")
        content = content.replace("*   1/2 cup quinoa", "*   1/2 cup cooked quinoa")  # Normalize
        content = content.replace("*   1/2 cup cooked quinoa\n*   5g olive oil", "*   1/2 cup cooked quinoa\n*   1 tsp olive oil") # match day 12 format somewhat or leave it. Just fix patties.
        
        # Replace instructions
        old_inst = "**Instructions:**\n1.  Sear patties with spice mix/nigella.\n2.  Sear 5-6 min/side (165°F)."
        if old_inst in content:
            content = content.replace(old_inst, tofu_instruction_replacement)
        
        with open(day_file, 'w') as f:
            f.write(content)
        print(f"Fixed bug and updated {day_file}")


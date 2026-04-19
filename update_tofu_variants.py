import glob

tofu_days = [
    "03-execution/week-01/day-05.md",
    "03-execution/week-02/day-12.md",
    "03-execution/week-03/day-19.md",
    "03-execution/week-04/day-26.md"
]

for path in tofu_days:
    with open(path, 'r') as f:
        content = f.read()

    # Update Quinoa to include Purple Sweet Potato Chaat swap
    if "*   90g cooked quinoa" in content:
        content = content.replace(
            "*   90g cooked quinoa",
            "*   90g cooked quinoa **(OR 90g 24h-chilled Purple Sweet Potato tossed with 1/4 tsp Chaat Masala)**"
        )
    elif "*   1/2 cup quinoa" in content:
        content = content.replace(
            "*   1/2 cup quinoa",
            "*   1/2 cup quinoa **(OR 90g 24h-chilled Purple Sweet Potato tossed with 1/4 tsp Chaat Masala)**"
        )

    # Add Teriyaki Variant note to the instructions
    teriyaki_note = """
**Flavor Variant (The "Teriyaki Pulse"):** 
To mimic a sweet/savory teriyaki without the sugar spike:
1. Add **1 tbsp diced onion & 1 tbsp diced red bell pepper** to the cold pan during "The Bloom".
2. Instead of plain coconut milk for the glaze, whisk **2 tbsp Coconut Milk, 1-2 tsp Soy Sauce (Tamari), 1 tsp ACV, 1/8 tsp Cinnamon, and 1/4 tsp Vanilla Extract**. Add this at the very end and stir for 30s until glossy.
"""
    if "The \"Teriyaki Pulse\"" not in content and "## Salad: Nitric Layer" in content:
        content = content.replace("## Salad: Nitric Layer", teriyaki_note + "\n## Salad: Nitric Layer")

    with open(path, 'w') as f:
        f.write(content)

print("Updated Tofu days with Teriyaki variant and Purple Sweet Potato Chaat swap.")

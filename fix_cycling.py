import os, glob

# Fix Clove (Only allow in Week 2, remove from W1, W3, W4)
for w in ["week-01", "week-03", "week-04"]:
    files = glob.glob(f"03-execution/{w}/day-*.md")
    for filepath in files:
        with open(filepath, 'r') as f: content = f.read()
        content = content.replace("Morning: Clove Infusion", "Morning: Jeera Water")
        content = content.replace("*   1 whole clove\n*   Simmer 2 min, steep 8 min. Remove clove.", "*   1/2 tsp cumin seeds\n*   1 cup water\n*   Boil 5 min, strain.")
        with open(filepath, 'w') as f: f.write(content)

# Fix Cacao (Week 3 is currently 4 days: Day 15, 17, 19, 20. We will remove it from Day 20 to hit the 3x cap)
filepath = "03-execution/week-03/day-20.md"
if os.path.exists(filepath):
    with open(filepath, 'r') as f: content = f.read()
    content = content.replace("## Recovery Bowl: Cacao Day", "## Recovery Bowl (Baseline)")
    content = content.replace("*   **1 tbsp cacao nibs**", "*   **No cacao (spacing oxalate).**")
    with open(filepath, 'w') as f: f.write(content)

# Fix Ajwain/Jeera (Enforce alternating days rather than "Ajwain/Jeera" options)
# We will do Ajwain on Days 1,3,5 (W1), 8,10,12 (W2), etc., Jeera on evens.
def set_morning_water(filepath, is_ajwain):
    with open(filepath, 'r') as f: content = f.read()
    if is_ajwain:
        content = content.replace("Morning Hydration (Warm Ajwain/Jeera/Matcha", "Morning Hydration (Warm Ajwain + Matcha")
        content = content.replace("Morning: Jeera Water", "Morning: Ajwain Water")
        content = content.replace("*   1/2 tsp cumin seeds\n*   1 cup water\n*   Boil 5 min, strain.", "*   1/4 tsp ajwain seeds\n*   1 cup water\n*   Simmer 2 min, steep 10 min. Drink warm.")
    else:
        content = content.replace("Morning Hydration (Warm Ajwain/Jeera/Matcha", "Morning Hydration (Warm Jeera + Matcha")
        content = content.replace("Morning: Ajwain Water", "Morning: Jeera Water")
        content = content.replace("*   1/4 tsp ajwain seeds\n*   1 cup water\n*   Simmer 2 min, steep 10 min. Drink warm.", "*   1/2 tsp cumin seeds\n*   1 cup water\n*   Boil 5 min, strain.")
    with open(filepath, 'w') as f: f.write(content)

for week_num, w in enumerate(["week-01", "week-02", "week-03", "week-04"]):
    files = sorted(glob.glob(f"03-execution/{w}/day-*.md"))
    for i, filepath in enumerate(files):
        # Even index (Day 1, 3, 5) -> Ajwain
        # Odd index (Day 2, 4, 6) -> Jeera
        # Wait, Day 4 is Clove in week 2? Let's not overwrite Clove in Week 2.
        with open(filepath, 'r') as f: current = f.read()
        if "Morning: Clove Infusion" in current:
            continue # Leave Clove alone
        
        set_morning_water(filepath, is_ajwain=(i % 2 == 0))

print("Cycling fixed.")

import glob, re

weeks = ["week-01", "week-02", "week-03", "week-04"]
ingredients = ["clove", "ajwain", "jeera", "nigella", "cacao", "saffron", "ashwagandha", "tulsi", "tofu"]

for week in weeks:
    print(f"\n--- {week.upper()} ---")
    counts = {ing: 0 for ing in ingredients}
    files = glob.glob(f"03-execution/{week}/day-*.md")
    for f in files:
        with open(f, 'r') as file:
            content = file.read().lower()
            for ing in ingredients:
                if ing in content:
                    counts[ing] += 1
    
    for ing, count in counts.items():
        print(f"{ing.capitalize()}: {count} days")

import glob, re

weeks = ["week-01", "week-02", "week-03", "week-04"]

def check_active(content, pattern, anti_pattern=None):
    if anti_pattern and re.search(anti_pattern, content, re.IGNORECASE):
        return False
    return bool(re.search(pattern, content, re.IGNORECASE))

for week in weeks:
    print(f"\n--- {week.upper()} ---")
    counts = {
        "Clove": 0,
        "Ajwain": 0,
        "Jeera": 0,
        "Nigella": 0,
        "Cacao": 0,
        "Saffron": 0,
        "Ashwagandha": 0,
        "Tulsi": 0,
        "Tofu": 0
    }
    
    files = glob.glob(f"03-execution/{week}/day-*.md")
    for f in files:
        with open(f, 'r') as file:
            c = file.read()
            
            if check_active(c, r'1\s*whole clove|clove infusion'): counts["Clove"] += 1
            if check_active(c, r'ajwain', r'no ajwain|jeera water'): counts["Ajwain"] += 1
            if check_active(c, r'jeera', r'no jeera|ajwain water'): counts["Jeera"] += 1
            if check_active(c, r'nigella|black jeera', r'no nigella'): counts["Nigella"] += 1
            if check_active(c, r'cacao nibs', r'no cacao|reduced cacao'): counts["Cacao"] += 1
            if check_active(c, r'saffron', r'no saffron'): counts["Saffron"] += 1
            if check_active(c, r'ashwagandha', r'no ashwagandha'): counts["Ashwagandha"] += 1
            if check_active(c, r'tulsi', r'no tulsi'): counts["Tulsi"] += 1
            if check_active(c, r'tofu', r'no tofu'): counts["Tofu"] += 1
            
    for ing, count in counts.items():
        print(f"{ing}: {count} days")

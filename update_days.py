import glob
import re

files = glob.glob('03-execution/week-*/day-*.md')

chaas_old = "(Chaas Hack: Add 2 tbsp Coconut + ACV to Jaljeera for creaminess)"
chaas_new = "(Chaas Hack: Add 1-2 tbsp Coconut Milk + ACV for creaminess. If used, subtract 1-2 tbsp Oil from 14:30 Salad Dressing)"

iron_bullet = "*   **Iron-Reduction Anchor:** Consume with lemon juice (Vitamin C) to multiply iron absorption from legumes by **2x-3x** [[6]](../../07-appendices/master-citations.md#6-iron-absorption--tannin-blockades-the-matcha-rule)."

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    content = content.replace(chaas_old, chaas_new)
    
    pattern = re.compile(r'(## Main Meal[^\n]*\n)\*\*Ingredients:\*\*')
    
    def repl(match):
        return f"{match.group(1)}{iron_bullet}\n\n**Ingredients:**"
        
    new_content, count = pattern.subn(repl, content)
    
    if count != 1:
        print(f"Warning: Count was {count} for {file_path}")
        
    with open(file_path, 'w') as f:
        f.write(new_content)

print(f"Done updating {len(files)} files.")

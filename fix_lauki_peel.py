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

    # Update Instructions to include Peel & Taste
    old_line = "2.  **Lauki Prep (Optional):** Grate Lauki and toss with Kala Namak."
    new_line = "2.  **Lauki Prep (Optional):** Peel Lauki and **taste a raw slice** (if bitter, discard the whole gourd!). Grate and toss with Kala Namak."
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Updated {path} with Peel & Taste check.")


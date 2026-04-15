import glob
import os

target_files = glob.glob('03-execution/week-*/day-*.md')
replacement_text = """*   **Alternative:** Blend into a **[Savory Recovery Chaas](../../05-practical/functional-indian-formats.md)** (Yogurt + Water + Cumin + Black Salt + Unflavored Protein). **Must not be spicy.**

## Clinical Rationale"""

for file_path in target_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We replace the exact string "\n\n## Clinical Rationale"
    # This assumes there's an empty line before "## Clinical Rationale" which we saw in the grep
    
    if "## Clinical Rationale" in content:
        # Avoid double-adding
        if "Savory Recovery Chaas" not in content:
            updated_content = content.replace('\n## Clinical Rationale', '\n' + replacement_text)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated {file_path}")
        else:
            print(f"Skipped {file_path} - already contains alternative")
    else:
        print(f"Warning: '## Clinical Rationale' not found in {file_path}")

print("Done")

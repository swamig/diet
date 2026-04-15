import glob

target_files = glob.glob('03-execution/week-*/day-*.md')

for file_path in target_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace "\n\n*   **Alternative:**" with "\n*   **Alternative:**"
    updated_content = content.replace('\n\n*   **Alternative:**', '\n*   **Alternative:**')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

print("Done fixing formatting")

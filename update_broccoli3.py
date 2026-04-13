import glob
import re
import os

files = glob.glob('03-execution/week-*/day-*.md')

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()

    # Determine Day Type
    if 'Day Type:** **Heavy Lift**' in content or 'Day Type:** **VO2 Max 4x4**' in content:
        day_type = 'heavy'
        salad_replacement = "'1/2 cup Broccoli Microgreens (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'"
        macro_insertion = '    *   **Broccoli Microgreens (14:30):** 1/2 cup (Performance Nrf2 dose).\n    *   **Dressing'
    elif 'Day Type:** **Cardio-Only Rest**' in content:
        day_type = 'cardio'
        salad_replacement = "'1/4 cup Broccoli Microgreens (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'"
        macro_insertion = '    *   **Broccoli Microgreens (14:30):** 1/4 cup (Clinical baseline Nrf2 dose).\n    *   **Dressing'
    else:
        print(f"Skipping {file_path}: Unknown Day Type")
        continue

    # Note: I am stripping the bold tags and replacing with exactly what the user asked.
    # We will search for any variation of the broccoli line and replace it exactly.
    # Let's use a regex to find the line that starts with "*   " and contains "Broccoli Microgreens"
    
    if day_type == 'heavy':
        new_line = '*   1/2 cup Broccoli Microgreens (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'
    else:
        new_line = '*   1/4 cup Broccoli Microgreens (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'

    new_content = re.sub(r'\*\s+\*\*?(?:1/4 to 1/2 cup|1 cup).*?Broccoli Microgreens.*?\n', new_line + '\n', content)

    if content == new_content:
       # Fallback: maybe it's not bolded?
       new_content = re.sub(r'\*\s+.*?Broccoli Microgreens.*?\n', new_line + '\n', content)

    if content != new_content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes needed for {file_path}")

print("Done.")

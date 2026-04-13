import glob
import re

files = glob.glob('03-execution/week-*/day-*.md')

for file_path in files:
    with open(file_path, 'r') as f:
        content = f.read()

    # Determine Day Type
    if 'Day Type:** **Heavy Lift**' in content or 'Day Type:** **VO2 Max 4x4**' in content:
        day_type = 'heavy'
        salad_search = '*   **1/4 to 1/2 cup Broccoli Microgreens** (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'
        salad_replacement = '*   1/2 cup Broccoli Microgreens (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'
        macro_insertion = '    *   **Broccoli Microgreens (14:30):** 1/2 cup (Performance Nrf2 dose).\n    *   **Dressing'
    elif 'Day Type:** **Cardio-Only Rest**' in content:
        day_type = 'cardio'
        salad_search = '*   **1/4 to 1/2 cup Broccoli Microgreens** (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'
        salad_replacement = '*   1/4 cup Broccoli Microgreens (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'
        macro_insertion = '    *   **Broccoli Microgreens (14:30):** 1/4 cup (Clinical baseline Nrf2 dose).\n    *   **Dressing'
    else:
        print(f"Skipping {file_path}: Unknown Day Type")
        continue

    # Update Salad Section
    new_content = content.replace(salad_search, salad_replacement)

    # Update Macro Execution Section
    # Find "    *   **Dressing" and replace it. Ensure no extra newlines.
    # The \n is placed exactly before the spaces of Dressing.
    new_content = re.sub(r'(\n\s*)\*\s*\*\*Dressing', r'\1*   **Broccoli Microgreens (14:30):** ' + ('1/2 cup (Performance Nrf2 dose).' if day_type == 'heavy' else '1/4 cup (Clinical baseline Nrf2 dose).') + r'\1*   **Dressing', new_content)

    if content != new_content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes needed for {file_path}")

print("Done.")

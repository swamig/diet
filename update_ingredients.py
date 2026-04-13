import os
import glob
import re

files = glob.glob('03-execution/week-*/day-*.md')

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Determine Day Type
    if 'Day Type:** **VO2 Max 4x4**' in content:
        day_type = 'vo2'
    elif 'Day Type:** **Cardio-Only Rest**' in content:
        day_type = 'cardio'
    elif 'Day Type:** **Heavy Lift**' in content:
        day_type = 'heavy'
    else:
        print(f"Unknown day type in {filepath}")
        continue

    if day_type == 'heavy':
        continue # No changes for Heavy Lift

    # Split into sections to only modify the ingredient lists
    # We'll use simple regex replacements

    new_content = content
    
    if day_type == 'vo2':
        # Replace quinoa in Main Meal
        # Look for the exact variations we found
        new_content = re.sub(r'\*   90g cooked quinoa(?!\s*\(12:00\))', '*   135g cooked quinoa (3/4 cup)', new_content)
        new_content = re.sub(r'\*   1/2 cup cooked quinoa(?!\s*\(12:00\))', '*   135g cooked quinoa (3/4 cup)', new_content)
        new_content = re.sub(r'\*   1/2 cup quinoa(?!\s*\(12:00\))', '*   135g cooked quinoa (3/4 cup)', new_content)
        
    elif day_type == 'cardio':
        # Replace quinoa in Main Meal
        new_content = re.sub(r'\*   90g cooked quinoa(?!\s*\(12:00\))', '*   45g cooked quinoa (1/4 cup)', new_content)
        new_content = re.sub(r'\*   1/2 cup cooked quinoa(?!\s*\(12:00\))', '*   45g cooked quinoa (1/4 cup)', new_content)
        new_content = re.sub(r'\*   1/2 cup quinoa(?!\s*\(12:00\))', '*   45g cooked quinoa (1/4 cup)', new_content)
        
        # Replace dressing
        new_content = new_content.replace(
            '*   Dressing: Olive oil + Balsamic + 1 tbsp Tomato Puree + 1 tsp Dijon Mustard + Pinch Turmeric + Pinch Black Pepper',
            '*   Dressing (2 tbsp): Olive oil + Balsamic + 1 tbsp Tomato Puree + 1 tsp Dijon Mustard + Pinch Turmeric + Pinch Black Pepper'
        )
        
        # Replace casein
        new_content = new_content.replace(
            '*   Standard yogurt + casein + blueberries',
            '*   Standard yogurt + blueberries'
        )
        new_content = re.sub(r'\*   Casein\n', '', new_content)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"No changes needed for {filepath} despite being {day_type}")


import os
import re

base_dir = '/Users/saumya.garg/Documents/GitHub/diet/03-execution'

personal_admin_text = """### Personal Admin
*   Hypertrophy Blockade: No Cold Plunge for 6 hours after lifting.
*   Fatigue Check: If 'fried', swap morning cold for Yoga and skip Matcha.
*   Mineral Reload: Drink Jaljeera after 18:30 Heat.

"""

ashwagandha_hydration_text = """**Night: Ashwagandha (Tasty Net 8)**
*   1/2 tsp Ashwagandha root powder
*   1/4 tsp Ceylon Cinnamon + pinch Cardamom
*   1 cup warm Alkaline Water (pH 8+) + splash almond milk."""

for week in range(1, 5):
    for day in range(1, 8):
        absolute_day = (week - 1) * 7 + day
        file_path = os.path.join(base_dir, f'week-0{week}', f'day-{absolute_day:02d}.md')
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r') as f:
            content = f.read()

        # 1. Insert "Next Morning Feedback & Adjustments"
        if "## Next Morning Feedback & Adjustments" not in content:
            feedback_section = "## Next Morning Feedback & Adjustments\n"
            if absolute_day == 1:
                feedback_section += "*   **Feedback:** Baseline/Prep state (Did you complete Sunday Prep? If not, use the \"When to Simplify\" rule in [Troubleshooting](../../05-practical/troubleshooting-guide.md)).\n"
                feedback_section += "*   **General Rule:** Yoga is the daily \"Autonomic Switch\" and should be used at 21:00 or as a morning substitute if the \"Target Feel\" isn't met.\n"
            elif absolute_day in [2, 9, 16, 23]:
                feedback_section += "*   **Target:** Productively sore, mentally sharp.\n"
                feedback_section += "*   **If \"Crushed\" (Lethargic/Foggy):** Swap morning cardio for Restorative Yoga; skip Matcha; add 1/4 tsp extra salt to Jaljeera.\n"
                feedback_section += "*   **General Rule:** Yoga is the daily \"Autonomic Switch\" and should be used at 21:00 or as a morning substitute if the \"Target Feel\" isn't met.\n"
            elif absolute_day in [3, 10, 17, 24]:
                feedback_section += "*   **Target:** High energy, stable mood.\n"
                feedback_section += "*   **If \"Fried\" (Jittery/Anxious/Poor Sleep):** Mandatory Yoga morning; double the Tulsi at night; ensure Quinoa was +50% yesterday.\n"
                feedback_section += "*   **General Rule:** Yoga is the daily \"Autonomic Switch\" and should be used at 21:00 or as a morning substitute if the \"Target Feel\" isn't met.\n"
            else:
                feedback_section += "*   **General Rule:** Yoga is the daily \"Autonomic Switch\" and should be used at 21:00 or as a morning substitute if the \"Target Feel\" isn't met.\n"

            # Insert below ## Objective and its content
            obj_match = re.search(r'(## Objective\n.*?)(?=\n## |\Z)', content, re.DOTALL)
            if obj_match:
                content = content.replace(obj_match.group(1), obj_match.group(1) + "\n\n" + feedback_section.strip() + "\n")

        # 2. Add Personal Admin if missing
        if "### Personal Admin" not in content:
            content = content.replace("## Monitoring Focus", personal_admin_text + "## Monitoring Focus")

        # 3. Fix 18:30 Heat Rotation
        content = re.sub(r'\*\s*\*\*18:30\*\*\s*–\s*Sauna', '*   **18:30** – 18:30 Heat Rotation (Sauna)', content)
        content = re.sub(r'\*\s*\*\*18:30\*\*\s*–\s*Epsom Bath', '*   **18:30** – 18:30 Heat Rotation (Epsom Bath)', content)
        content = re.sub(r'\*\s*18:30\s*–\s*Sauna', '*   18:30 – 18:30 Heat Rotation (Sauna)', content)
        content = re.sub(r'\*\s*18:30\s*–\s*Epsom Bath', '*   18:30 – 18:30 Heat Rotation (Epsom Bath)', content)
        
        # 4. Fix Tuesday Quinoa/Ashwagandha (Days 2, 9, 16, 23)
        if absolute_day in [2, 9, 16, 23]:
            # Replace Cinnamon Water with Ashwagandha if Cinnamon Water is there instead
            if "**Night: Cinnamon Water**" in content:
                content = re.sub(r'\*\*Night: Cinnamon Water\*\*.*?(?=\n## |\Z)', ashwagandha_hydration_text + '\n', content, flags=re.DOTALL)
            
            if "Night hydration (Ashwagandha" not in content and "21:00" in content:
                content = re.sub(r'\*\s*\*\*21:00\*\*\s*–\s*Night hydration.*?(\n|$)', '*   **21:00** – Night hydration (Ashwagandha [5](../../07-appendices/master-citations.md#5-adaptogens--parasympathetic-alignment-ashwagandha) \'Net 8\')\n', content)

            if "3/4 cup cooked" not in content:
                content = re.sub(r'\*\*Quinoa \(12:00\):\*\*.*?(\n|$)', '**Quinoa (12:00):** 3/4 cup cooked (+50% starch pulse).\n', content)

        # Cleanup multiple newlines
        content = re.sub(r'\n{3,}', '\n\n', content)

        with open(file_path, 'w') as f:
            f.write(content)

print("Done updating files.")

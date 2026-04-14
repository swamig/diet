import os, glob

# Update daily execution files
for filepath in glob.glob("03-execution/week-*/*.md"):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add pure vanilla extract to standard recovery bowl components
    content = content.replace(
        '*   Greek yogurt + 1 scoop Casein + blueberries + unflavored whey.',
        '*   Greek yogurt + 1 scoop Casein + blueberries + unflavored whey + 1/4 tsp Pure Vanilla Extract (Anti-Angiogenic).'
    )
    content = content.replace(
        '*   Greek yogurt + blueberries + unflavored whey.',
        '*   Greek yogurt + blueberries + unflavored whey + 1/4 tsp Pure Vanilla Extract (Anti-Angiogenic).'
    )
    content = content.replace(
        '*   Standard yogurt + casein + blueberries',
        '*   Standard yogurt + casein + blueberries + 1/4 tsp Pure Vanilla Extract'
    )
    content = content.replace(
        '*   Standard yogurt + blueberries',
        '*   Standard yogurt + blueberries + 1/4 tsp Pure Vanilla Extract'
    )
    
    # Specific day replacements where format differs slightly
    content = content.replace(
        '*   Blueberries\n*   **1 tbsp cacao nibs**',
        '*   Blueberries + 1/4 tsp Pure Vanilla Extract\n*   **1 tbsp cacao nibs**'
    )
    content = content.replace(
        '*   Blueberries\n*   **2 tsp cacao nibs**',
        '*   Blueberries + 1/4 tsp Pure Vanilla Extract\n*   **2 tsp cacao nibs**'
    )
    content = content.replace(
        '*   Blueberries\n*   **No cacao',
        '*   Blueberries + 1/4 tsp Pure Vanilla Extract\n*   **No cacao'
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Vanilla Extract added to daily recovery bowls.")


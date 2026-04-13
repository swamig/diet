import os, glob

# Dictionary mapping ingredient filenames to a markdown string of recipes they are used in.
links = {
    "turmeric.md": "- [Vegan Protein Patties (Spice Sear)](../05-practical/vegan-protein-patties.md)\n- [Master Dressing (Sunday Prep)](../05-practical/sunday-prep.md#block-6-dressing-master-batch-5-min)\n- [Protocol Quinoa (Sofrito Base)](../05-practical/protocol-quinoa.md)",
    "black-pepper.md": "- [Vegan Protein Patties (Spice Sear)](../05-practical/vegan-protein-patties.md)\n- [Master Dressing (Sunday Prep)](../05-practical/sunday-prep.md#block-6-dressing-master-batch-5-min)",
    "ginger.md": "- [Peppermint Jaljeera (The Muddle)](../05-practical/peppermint-jaljeera.md)\n- [Vegan Protein Patties (Dough Base)](../05-practical/vegan-protein-patties.md)\n- [Coconut Chutney (MCT Matrix)](../05-practical/sunday-prep.md#2-mct-matrix-scaled-3-day-coconut-chutney)",
    "garlic.md": "- [Vegan Protein Patties (Dough Base)](../05-practical/vegan-protein-patties.md)\n- [Protocol Chickpeas (RS3 Matrix)](../05-practical/protocol-chickpeas.md)\n- [Toum (Raw Garlic Emulsion)](../05-practical/functional-indian-formats.md#2-high-signaling-emulsions-toum--garlic-paste)",
    "cumin.md": "- [Protocol Quinoa (Sofrito Base)](../05-practical/protocol-quinoa.md)\n- [Vegan Protein Patties (Spice Sear)](../05-practical/vegan-protein-patties.md)\n- [Imlee (Tamarind) Chutney](../05-practical/sunday-prep.md#1-7-day-imlee-tamarind-paste-concentrate-version)",
    "peppermint-chili.md": "- [Peppermint Jaljeera (The Muddle)](../05-practical/peppermint-jaljeera.md)\n- [Coconut Chutney (MCT Matrix)](../05-practical/sunday-prep.md#2-mct-matrix-scaled-3-day-coconut-chutney)",
    "cilantro.md": "- [14:30 Salad Layer (Chelation Anchor)](../05-practical/daily-salad-layer.md)\n- [Performance Refried Beans](../05-practical/performance-refried-beans.md)",
    "cacao.md": "- [17:50 Recovery Bowl](../03-execution/week-01/day-01.md#recovery-bowl)",
    "chia.md": "- [14:30 Salad Layer (Seed Rotation)](../05-practical/daily-salad-layer.md#explicit-weekly-rotation-table)",
    "sesame.md": "- [14:30 Salad Layer (Seed Rotation)](../05-practical/daily-salad-layer.md#explicit-weekly-rotation-table)\n- [The Vascular Podi (Gunpowder)](../05-practical/functional-indian-formats.md#3-therapeutic-podis--gunpowders-dry-matrix)",
    "pumpkin-seeds.md": "- [14:30 Salad Layer (Seed Rotation)](../05-practical/daily-salad-layer.md#explicit-weekly-rotation-table)",
    "walnuts.md": "- [14:30 Salad Layer (Seed Rotation)](../05-practical/daily-salad-layer.md#explicit-weekly-rotation-table)",
    "ferments.md": "- [14:30 Salad Layer (Microbiome Anchor)](../05-practical/daily-salad-layer.md)",
    "achiote.md": "- [Protocol Quinoa (RS3 Anchor)](../05-practical/protocol-quinoa.md)",
    "nigella.md": "- [Vegan Protein Patties (Spice Sear Variant)](../05-practical/vegan-protein-patties.md)",
    "lauki.md": "- [The Lauki Gut-Reset Protocol](../05-practical/lauki-reset.md)",
    "papaya.md": "- [Daily Timing Cheat Sheet (13:00 Enzyme Pulse)](../07-appendices/daily-timing-cheat-sheet.md)"
}

for filename, recipe_links in links.items():
    filepath = os.path.join("02-ingredients", filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        if "## Culinary Integration (Recipes)" not in content:
            new_section = f"\n## Culinary Integration (Recipes)\nThis ingredient is functionally integrated into the following protocol meals:\n{recipe_links}\n"
            
            # Insert before ## Related Pages or ## Evidence Status if they exist, otherwise at the end
            if "## Related Pages" in content:
                content = content.replace("## Related Pages", new_section + "\n## Related Pages")
            elif "## Evidence Status" in content:
                content = content.replace("## Evidence Status", new_section + "\n## Evidence Status")
            else:
                content += new_section
                
            with open(filepath, 'w') as f:
                f.write(content)

print("Linked ingredients to recipes.")

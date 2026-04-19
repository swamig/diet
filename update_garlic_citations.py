import re

# 1. Update 07-appendices/master-citations.md
citations_path = '07-appendices/master-citations.md'
with open(citations_path, 'r') as f:
    citations_content = f.read()

ajoene_citation = """
*   **The Allicin vs. Ajoene Partition (Bloom vs. Fresh):** Block, E., 1985, *Scientific American*. "The Chemistry of Garlic and Onions." Establishes that while raw crushing creates Allicin (acute antimicrobial), heating Allicin in a lipid medium (Blooming) converts it into stable organosulfur compounds like **Ajoene** and **Vinyldithiins**. These secondary compounds are significantly more potent at inhibiting platelet aggregation and improving vascular blood flow (nitric oxide synergy) than raw Allicin itself, while being gentler on the gastric mucosa.
"""

if "Allicin vs. Ajoene Partition" not in citations_content:
    # Insert after the existing Allicin citation (Section 3)
    citations_content = citations_content.replace("making the allicin relatively heat-stable for brief cooking.", 
                                                 "making the allicin relatively heat-stable for brief cooking.\n" + ajoene_citation)
    with open(citations_path, 'w') as f:
        f.write(citations_content)
    print("Updated master-citations.md with Ajoene logic.")

# 2. Update 02-ingredients/garlic.md
garlic_path = '02-ingredients/garlic.md'
with open(garlic_path, 'r') as f:
    garlic_content = f.read()

garlic_considerations = """
## Clinical Considerations: The Allicin-Ajoene Partition
The protocol utilizes two different preparation methods to target specific physiological outcomes:

1.  **The Fresh Pulse (Raw/Flash Sear):** Targeting **Allicin**. Used for acute immune support and antimicrobial action. High intensity, high gastric bite.
2.  **The Lipid Bloom (Low Heat Sauté):** Targeting **Ajoenes**. By slowly warming rested garlic in oil, Allicin converts into stable ajoenes. These are superior for vascular health, blood flow, and platelet management, with a significantly reduced "garlic breath" and gastric irritation profile.
"""

if "Clinical Considerations: The Allicin-Ajoene Partition" not in garlic_content:
    # Insert before Related Pages
    garlic_content = garlic_content.replace("## Related Pages", garlic_considerations + "\n## Related Pages")
    with open(garlic_path, 'w') as f:
        f.write(garlic_content)
    print("Updated garlic.md with Allicin-Ajoene partition.")


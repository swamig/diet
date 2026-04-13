import os, glob

for filepath in glob.glob("03-execution/week-*/*.md"):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Update Macro Execution Header
    content = content.replace(
        '*   **Broccoli Microgreens (14:30):** 1/2 cup (Performance Nrf2 dose).',
        '*   **Broccoli Microgreens/Sprouts (14:30):** 1/2 cup Microgreens OR 1/4 cup Sprouts (Performance Nrf2 dose).'
    )
    content = content.replace(
        '*   **Broccoli Microgreens (14:30):** 1/4 cup (Clinical baseline Nrf2 dose).',
        '*   **Broccoli Microgreens/Sprouts (14:30):** 1/4 cup Microgreens OR 2 tbsp Sprouts (Clinical baseline Nrf2 dose).'
    )
    
    # Update Salad Ingredients List
    content = content.replace(
        '*   **1/2 cup Broccoli Microgreens** (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)',
        '*   **1/2 cup Broccoli Microgreens OR 1/4 cup Frozen/Thawed Sprouts** ([Sulforaphane Engine](../../05-practical/protocol-broccoli.md#the-sprout-freezing-hack-3x-potency)) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'
    )
    content = content.replace(
        '*   **1/4 cup Broccoli Microgreens** (Sulforaphane Engine) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)',
        '*   **1/4 cup Broccoli Microgreens OR 2 tbsp Frozen/Thawed Sprouts** ([Sulforaphane Engine](../../05-practical/protocol-broccoli.md#the-sprout-freezing-hack-3x-potency)) [4](../../07-appendices/master-citations.md#4-sulforaphane--inflammatory-control)'
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Daily files updated with Sprout alternatives.")

with open('05-practical/functional-samosas.md', 'r') as f:
    content = f.read()

if "### Macro Profile (For 2 Samosas + 1 Scoop Pea/Rice Protein)" in content:
    print("Option 3 macros are present.")
else:
    print("Option 3 macros are NOT present.")

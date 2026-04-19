import os

files = ['05-practical/peppermint-jaljeera.md', '05-practical/garlic-chili-oil.md', '05-practical/lauki-reset.md']

for path in files:
    if os.path.exists(path):
        print(f"File: {path} exists")

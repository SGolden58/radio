name: Update Radio EPG

on:
  workflow_dispatch:  # Allows manual triggering

permissions:
  contents: write  # Allows write access to the repository contents

jobs:
  update_epg:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'  # Specify the Python version

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4

      - name: Generate EPG XML
        run: python generate_epg.py

      - name: Commit and push changes
        run: |
          git config --local user.name "github-actions"
          git config --local user.email "github-actions@github.com"
          git add epg.xml
          git commit -m "Update EPG XML" || echo "No changes to commit"
          git push

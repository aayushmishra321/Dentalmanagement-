#!/bin/bash

echo "=========================================="
echo "GitHub Repository Cleanup Script"
echo "=========================================="
echo ""

# Remove .env from git if committed
echo "Removing .env from git tracking..."
git rm --cached .env 2>/dev/null || echo "  .env not in git (good!)"

# Remove database from git if committed
echo "Removing db.sqlite3 from git tracking..."
git rm --cached db.sqlite3 2>/dev/null || echo "  db.sqlite3 not in git (good!)"

# Remove log files from git if committed
echo "Removing log files from git tracking..."
git rm --cached logs/*.log 2>/dev/null || echo "  No log files in git (good!)"

# Remove staticfiles from git if committed
echo "Removing staticfiles/ from git tracking..."
git rm -r --cached staticfiles/ 2>/dev/null || echo "  staticfiles/ not in git (good!)"

# Remove media files from git (keep .gitkeep)
echo "Removing media files from git tracking..."
git rm -r --cached media/ 2>/dev/null || echo "  media/ not in git"
git add media/.gitkeep 2>/dev/null || echo "  media/.gitkeep added"

# Add logs/.gitkeep
git add logs/.gitkeep 2>/dev/null || echo "  logs/.gitkeep added"

# Remove __pycache__ directories
echo "Removing __pycache__ directories from git..."
find . -type d -name __pycache__ -exec git rm -r --cached {} + 2>/dev/null || echo "  No __pycache__ in git (good!)"

# Clean local files
echo ""
echo "Cleaning local files..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "  Python cache cleaned"

# Show status
echo ""
echo "=========================================="
echo "Git Status:"
echo "=========================================="
git status

echo ""
echo "=========================================="
echo "Cleanup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review the git status above"
echo "2. Run: git add ."
echo "3. Run: git commit -m 'Clean repository for deployment'"
echo "4. Run: git push origin main"
echo ""

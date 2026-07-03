#!/bin/bash
echo "========================================="
echo "NOTEBOOK EXECUTION PROGRESS"
echo "========================================="
echo ""

cd /workshop/rag_pattern_notebooks

# Count total notebooks
total=14

# Count completed (those with outputs)
completed=0
for nb in aws_notebooks/{10..23}_*.ipynb; do
  if [ -f "$nb" ]; then
    # Check if notebook has execution outputs
    if python3 -c "
import json
import sys
try:
    with open('$nb', 'r') as f:
        nb = json.load(f)
    has_output = any(
        cell.get('cell_type') == 'code' and 
        cell.get('outputs') and 
        len(cell.get('outputs', [])) > 0
        for cell in nb.get('cells', [])
    )
    sys.exit(0 if has_output else 1)
except:
    sys.exit(1)
" 2>/dev/null; then
      ((completed++))
      echo "✅ $(basename $nb)"
    else
      echo "⏳ $(basename $nb)"
    fi
  fi
done

echo ""
echo "Progress: $completed/$total notebooks"
echo "Remaining: $((total - completed))"
echo ""

# Show currently running
if pgrep -f "jupyter nbconvert" > /dev/null; then
  echo "🔄 Execution in progress..."
  ps aux | grep "jupyter nbconvert" | grep -v grep | awk '{print "  PID:", $2, "-", $(NF)}'
else
  echo "⏸️  No execution currently running"
fi

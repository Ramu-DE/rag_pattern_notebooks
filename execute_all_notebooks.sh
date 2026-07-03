#!/bin/bash
cd /workshop/rag_pattern_notebooks
source venv/bin/activate

notebooks=(
  "aws_notebooks/20_Iterative_RAG_AWS.ipynb"
  "aws_notebooks/21_Few_Shot_RAG_AWS.ipynb"
  "aws_notebooks/22_Hierarchical_RAG_AWS.ipynb"
  "aws_notebooks/23_Parent_Child_RAG_AWS.ipynb"
  "aws_notebooks/16_Chain_of_Thought_RAG_AWS.ipynb"
  "aws_notebooks/12_Agentic_RAG_AWS.ipynb"
  "aws_notebooks/17_ReAct_RAG_AWS.ipynb"
  "aws_notebooks/13_Corrective_RAG_AWS.ipynb"
  "aws_notebooks/14_Self_RAG_AWS.ipynb"
  "aws_notebooks/10_Recursive_RAG_AWS.ipynb"
  "aws_notebooks/15_Tree_of_Thoughts_RAG_AWS.ipynb"
  "aws_notebooks/19_Ensemble_RAG_AWS.ipynb"
  "aws_notebooks/18_Memory_Augmented_RAG_AWS.ipynb"
  "aws_notebooks/11_Multimodal_RAG_AWS.ipynb"
)

total=${#notebooks[@]}
success=0
failed=0

echo "================================"
echo "Executing $total notebooks"
echo "================================"

for i in "${!notebooks[@]}"; do
  nb="${notebooks[$i]}"
  num=$((i + 1))
  name=$(basename "$nb")
  
  echo ""
  echo "[$num/$total] Executing: $name"
  echo "----------------------------------------"
  
  jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=600 \
    --ExecutePreprocessor.kernel_name=python3 \
    "$nb" 2>&1 | tee "execution_$(basename $nb .ipynb).log"
  
  if [ $? -eq 0 ]; then
    echo "✅ SUCCESS: $name"
    ((success++))
  else
    echo "❌ FAILED: $name"
    ((failed++))
  fi
done

echo ""
echo "================================"
echo "EXECUTION SUMMARY"
echo "================================"
echo "Total:   $total"
echo "Success: $success"
echo "Failed:  $failed"

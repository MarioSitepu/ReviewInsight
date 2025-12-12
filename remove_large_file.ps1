# Script to remove backend.rar from git history
# Run this script to clean git history

Write-Host "Removing backend.rar from git history..." -ForegroundColor Yellow

# Method 1: Use git filter-branch
$env:FILTER_BRANCH_SQUELCH_WARNING = "1"

# Remove from all branches
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend.rar" --prune-empty --tag-name-filter cat -- --all

if ($LASTEXITCODE -eq 0) {
    Write-Host "File removed from history. Cleaning up..." -ForegroundColor Green
    
    # Clean up refs
    git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive
    
    Write-Host "Done! Now you can push with: git push origin --force --all" -ForegroundColor Green
} else {
    Write-Host "Error removing file. Trying alternative method..." -ForegroundColor Red
    
    # Alternative: Reset last commit and recommit without the file
    Write-Host "Alternative: You can manually reset and recommit" -ForegroundColor Yellow
}


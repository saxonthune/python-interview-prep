#!/usr/bin/env bash
# Interactive minor version bump. Tags a commit (default: HEAD) with the
# next vMAJOR.(MINOR+1).0 after the latest existing tag.
# Usage: scripts/bump-version.sh [commit-ish]
set -euo pipefail

commit="${1:-HEAD}"
last="$(git tag --sort=-v:refname | head -1)"
last="${last:-v0.0.0}"

IFS=. read -r major minor _ <<< "${last#v}"
next="v${major}.$((minor + 1)).0"

echo "Last tag:      ${last}"
echo "Next tag:      ${next}"
echo "Target commit: $(git rev-parse --short "$commit") $(git log -1 --format=%s "$commit")"
read -rp "Create and push ${next}? [y/N] " ans
[[ "${ans,,}" == y* ]] || { echo "aborted"; exit 1; }

git tag -a "$next" "$commit" -m "$next"
git push origin "$next"
echo "pushed ${next} (deploy workflow triggered)"

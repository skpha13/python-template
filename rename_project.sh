#!/bin/bash
set -e

OLD_DIR="src"
OLD_PROJECT="python-template"

# read input package name
if [ -z "$1" ]; then
    read -rp "Enter new package name (replaces '$OLD_DIR'): " NEW
else
    NEW="$1"
fi

# input validation
if [ -z "$NEW" ]; then
    echo "Error: package name cannot be empty."
    exit 1
fi

if [ "$NEW" = "$OLD_DIR" ]; then
    echo "Error: new name is the same as the current name ('$OLD_DIR')."
    exit 1
fi

if ! [[ "$NEW" =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]]; then
    echo "Error: '$NEW' is not a valid Python package name."
    echo "       Must start with a letter or underscore and contain only letters, digits, or underscores."
    exit 1
fi

if [ ! -d "$OLD_DIR" ]; then
    echo "Error: directory '$OLD_DIR' does not exist. Already renamed?"
    exit 1
fi

if [ -e "$NEW" ]; then
    echo "Error: '$NEW' already exists. Aborting to avoid overwriting."
    exit 1
fi

# convert underscores to hyphens for the project-level name (e.g. my_package -> my-package)
NEW_PROJECT=$(echo "$NEW" | tr '_' '-')

echo ""
echo "Renaming '$OLD_DIR' -> '$NEW' ..."
echo "Project name: '$OLD_PROJECT' -> '$NEW_PROJECT'"
echo ""

# rename dir
mv "$OLD_DIR" "$NEW"
echo "  [ok] Renamed directory: $OLD_DIR/ -> $NEW/"

# update python imports
for f in "$NEW"/*.py; do
    [ -f "$f" ] || continue
    if grep -q "from $OLD_DIR\." "$f" 2>/dev/null || grep -q "import $OLD_DIR\." "$f" 2>/dev/null; then
        sed -i '' "s/from $OLD_DIR\./from $NEW./g; s/import $OLD_DIR\./import $NEW./g" "$f"
        echo "  [ok] Updated imports in: $f"
    fi
done

# update template strings
for f in "$NEW"/*.py; do
    [ -f "$f" ] || continue
    if grep -q "$OLD_PROJECT" "$f" 2>/dev/null; then
        sed -i '' "s/$OLD_PROJECT/$NEW_PROJECT/g" "$f"
        echo "  [ok] Updated project name strings in: $f"
    fi
done

# update pyproject.toml
if [ -f "pyproject.toml" ]; then
    sed -i '' \
        -e "s/name = \"$OLD_PROJECT\"/name = \"$NEW_PROJECT\"/" \
        -e "s/\"$OLD_DIR\"/\"$NEW\"/g" \
        -e "s/\"$OLD_DIR\.\*\"/\"$NEW.*\"/g" \
        -e "s/\"$OLD_DIR\.egg-info\"/\"$NEW.egg-info\"/g" \
        pyproject.toml
    echo "  [ok] Updated pyproject.toml"
fi

# update helper script
if [ -f "d" ]; then
    sed -i '' "s| $OLD_DIR| $NEW|g" d
    echo "  [ok] Updated d script"
fi

echo ""
echo "Done! Package renamed from '$OLD_DIR' to '$NEW'."
echo ""
echo "Summary of changes:"
echo "  - Directory:      $OLD_DIR/ -> $NEW/"
echo "  - Project name:   $OLD_PROJECT -> $NEW_PROJECT"
echo "  - Imports:        'from $OLD_DIR.' -> 'from $NEW.'"
echo "  - String literals: '$OLD_PROJECT' -> '$NEW_PROJECT' (in .py files)"
echo "  - pyproject.toml:  package name + references updated"
echo "  - d script:        tool targets updated"

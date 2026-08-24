#!/bin/sh
# ANF boundary checker — enforces ADR-001 KILL list.
# Usage:
#   tools/check_boundaries.sh --staged     # check git-staged changes
#   tools/check_boundaries.sh --all        # check whole working tree (default)
#   tools/check_boundaries.sh PATH...      # check specific paths
# Exit 0 = clean, exit 1 = violation(s).
set -u

VIOLATIONS=0
TMPDIR_ANF="${TMPDIR:-/tmp}"

# Legacy files pending ADR-001 migration: exempt from import-scan only.
LEGACY_ALLOWLIST=" scripts/skill_audit.py scripts/skill_consolidation_checker.py scripts/crystallization_scheduler.py scripts/capability_assessment.py "

in_allowlist() {
  case " $LEGACY_ALLOWLIST " in
    *" $1 "*) return 0 ;;
    *) return 1 ;;
  esac
}

fail() {
  echo "BOUNDARY VIOLATION: $1" >&2
  VIOLATIONS=$((VIOLATIONS + 1))
}

collect_files() {
  if [ "$MODE" = "--staged" ]; then
    git diff --cached --name-only --diff-filter=ACMR
  else
    find . -type f ! -path "./.git/*" ! -name "*.pyc" ! -path "./node_modules/*" | sed 's|^\./||'
  fi
}

check_narrative() {
  f="$1"
  hits="$TMPDIR_ANF/anf_hits.$$"
  grep -niE 'autonomous self-evolving agent platform|enterprise memory os|agent capability operating system|universal skill marketplace|all-in-one organizational intelligence platform|agi memory layer|general agent runtime' "$f" > "$hits" 2>/dev/null
  if [ -s "$hits" ]; then
    while IFS= read -r line; do
      case "$line" in
        *"NO "*|*"NOT "*|*"not a "*|*"orbidden"*) ;;  # prohibition contexts allowed
        *) fail "product-narrative phrase: $f:$line" ;;
      esac
    done < "$hits"
  fi
  rm -f "$hits"
}

check_file() {
  f="$1"
  [ -f "$f" ] || return 0

  # 1) Forbidden infrastructure paths/filenames (no runtime reintroduction)
  case "$f" in
    *policy_promotion*|*policy_auto*|*mcp_server*|"web/"*|"dashboard/"*|"ui/"*)
      fail "$f matches forbidden path pattern (ADR-001 KILL list)"
      return 0 ;;
  esac

  # 2) Forbidden imports in Python outside legacy allowlist
  case "$f" in
    *.py)
      if ! in_allowlist "$f"; then
        if grep -nEq '^[[:space:]]*(import|from)[[:space:]]+(flask|fastapi|sqlalchemy|psycopg2?|sqlite3|chromadb|qdrant_client|pymilvus|weaviate|pinecone|lancedb)([[:space:]]|$|\.)' "$f"; then
          fail "$f imports forbidden backend/framework module"
        fi
      fi
      ;;
    *.md) check_narrative "$f" ;;
  esac
}

MODE="${1:---all}"
shift 1 2>/dev/null || true

LIST="$TMPDIR_ANF/anf_files.$$"
if [ "$MODE" = "--staged" ] || [ "$MODE" = "--all" ]; then
  collect_files > "$LIST"
else
  printf '%s\n' "$MODE" "$@" > "$LIST"
  MODE="paths"
fi

while IFS= read -r f; do
  [ -n "$f" ] && check_file "$f"
done < "$LIST"
rm -f "$LIST"

if [ "$VIOLATIONS" -gt 0 ]; then
  echo "check_boundaries: $VIOLATIONS violation(s)." >&2
  exit 1
fi
echo "check_boundaries: clean."
exit 0

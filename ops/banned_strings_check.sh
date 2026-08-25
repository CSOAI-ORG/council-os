#!/bin/sh
# Fails if any banned internal/brand string appears in a public surface file.
BAD='sovereign\|ceasai\|byzantine\|fault-tolerance\|cibola\|dorado'
HITS=$(grep -ril "$BAD" --exclude-dir=.git --exclude=banned_strings_check.sh . || true)
[ -z "$HITS" ] && echo "banned-strings: clean" || { echo "BANNED STRINGS in:"; echo "$HITS"; exit 1; }

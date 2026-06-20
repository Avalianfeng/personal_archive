# Known issues · collect phase

> Auto-generated. Fix in cleanup phase unless blocking ingest.

## Subcategory naming

Inconsistent education subcategory labels:

- `real:教育与求学` (31 questions)
- `real:education` (1 questions)

## ID gaps (normal)

Skipped/rejected numbering — not errors:

- DEC: missing [1]
- EMO: missing [1, 4, 5, 6, 7, 8, 9, 10, 14, 15, 45]
- SELF: missing [6, 9]
- VAL: missing [4, 21]

## Cleanup phase backlog

- Scale near-duplicate clusters: no `similar` relations yet
- Run `manage sync --with-duplicate-scan` after collection completes


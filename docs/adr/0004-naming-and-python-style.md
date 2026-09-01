# ADR-0004: Naming and Python style

**Status:** accepted, 2026-09-01

## Context

The repository mixes Python tooling, documents, static web files and 3D assets.
Case-sensitive filesystems make inconsistent case a reliability problem. The
Python scripts need a clear, lightweight quality baseline without forcing a
large refactor of unrelated legacy modules.

## Decision

- Python modules, packages, functions, variables, tests and machine-oriented
  metadata use lowercase snake_case. Classes use PascalCase; constants use
  UPPER_CASE.
- Markdown documentation, general asset folders and static web assets use
  lowercase kebab-case.
- Canonical repository names, tool-mandated files and React component filenames
  retain their required conventions.
- Every new or modified Python module follows PEP 8 and PEP 257. Public modules,
  classes and functions receive concise English docstrings. New code favours the
  smallest direct solution consistent with KISS.

## Consequences

New files are named predictably and links remain portable across case-sensitive
systems. Existing names are migrated only together with all references and only
when the change has a concrete maintenance benefit. PEP compliance is applied to
new and touched code first; broad legacy cleanup remains separate work, not a
reason to block unrelated avatar work.

# ADR-0005: MkDocs documentation and local Avatar Studio

Status: Accepted

## Context

The React viewer mixed public presentation with project-stage guidance and was becoming a second application. The production workflow also requires local access to private files and workstation tools that must not be exposed through GitHub Pages.

## Decision

GitHub Pages will publish a static MkDocs Material documentation portal only. Interactive workflow guidance, project state, artefact inspection and local tool execution will be implemented in a separate Python 3.11 / PySide6 desktop application named Avatar Studio. Project state will be stored locally in SQLite; portable validation reports may be exported as JSON. Windows distribution will use PyInstaller `.exe`; Linux will use a native PyInstaller build.

## Consequences

The old web viewer/backend are retired. Documentation becomes versioned and reviewable Markdown. The desktop application may reuse Python validators and invoke local DCC/tool adapters without moving private biometric data to a web service.

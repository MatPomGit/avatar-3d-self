\# AGENTS.md - System Instructions \& Guidelines for AI Autonomous Agents



This file establishes execution rules, architectural context, and safety constraints for AI coding agents (e.g., Cursor, Claude Code, Devin, GitHub Copilot) operating within the `avatar-3d-self` repository.



\---



\## 1. Project Overview \& Architecture



`avatar-3d-self` is an automated 3D avatar generation pipeline that converts photogrammetry scans into MetaHuman-compatible blendshapes and exports Unreal Engine ready assets (`.fbx`).



\* \*\*Primary Stack:\*\* Python 3.10+, Open3D, Trimesh, SciPy, Unreal Engine Python API, COLMAP CLI, pygltflib, ufbx, assimp, pyscript, Three.js.
Optional: Pygbag + Ursina Engine.

\* \*\*Target Workflows:\*\* GitHub Actions (`.github/workflows/`), Python automation (`scripts/`).

\* \*\*Storage Rules:\*\* Heavy 3D assets (`.fbx`, `.obj`, raw scans) \*\*MUST\*\* use Git LFS. Never commit large binary files directly to standard Git tracking.



\---



\## 2. Agent Responsibilities \& Workflows



| Agent Focus | Allowed Operations | Restricted Operations |

| :--- | :--- | :--- |

| \*\*Mesh \& Geometry Agent\*\* | Modifying `scripts/blendshape\_generator.py`, processing `.obj`/`.ply` meshes, running `pytest tests/test\_blendshapes.py`. | Overwriting `source/metahuman/metahuman\_base.fbx` directly without validation. |

| \*\*Unreal Engine Agent\*\* | Editing `scripts/ue\_export\_fbx.py`, configuring `unreal\_project/` settings, running headless UE python jobs. | Modifying core C++ plugins without updating build targets. |

| \*\*CI/CD Pipeline Agent\*\* | Updating `.github/workflows/\*.yml`, managing `pyproject.toml` dependencies. | Pushing directly to `main` branch without PR check triggers. |



\---



\## 3. Code Conventions \& Standards



\* \*\*Python Constraints:\*\*

&#x20; \* Enforce strict type hints (`typing` module) across all script interfaces.

&#x20; \* Use standard logging (`logging` library) instead of bare `print()` statements in production scripts.

&#x20; \* Format all code using `black` and adhere to PEP 8 standards (`flake8`).

\* \*\*Geometry Processing:\*\*

&#x20; \* Coordinate System standard: \*\*Z-Up, Right-Handed\*\* for raw scans; convert to \*\*Z-Up, Left-Handed\*\* for Unreal Engine exports.

&#x20; \* Mesh units must be in \*\*centimeters (cm)\*\* upon export.



\---



\## 4. Common Commands for Agents



\* \*\*Environment Setup:\*\*

&#x20; ```bash

&#x20; python -m venv venv

&#x20; source venv/bin/activate  # Or venv\\Scripts\\activate on Windows

&#x20; pip install -e .\[dev]


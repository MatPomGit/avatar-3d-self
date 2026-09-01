from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "check_mkdocs_coverage.py"
spec = spec_from_file_location("check_mkdocs_coverage", MODULE_PATH)
assert spec and spec.loader
coverage = module_from_spec(spec)
spec.loader.exec_module(coverage)


def test_every_markdown_document_is_in_navigation():
    missing, nonexistent = coverage.validate()
    assert missing == set(), f"Documents missing from MkDocs nav: {sorted(missing)}"
    assert nonexistent == set(), f"MkDocs nav points to missing files: {sorted(nonexistent)}"

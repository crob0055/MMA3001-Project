"""Generate the test report and standard-library HTML API documentation."""
import importlib
import json
from pathlib import Path
import pydoc
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
out = ROOT / "docs" / "html"
out.mkdir(parents=True, exist_ok=True)
for name in ("data", "model", "metrics"):
    module = importlib.import_module("appletree." + name)
    (out / f"appletree.{name}.html").write_text(pydoc.HTMLDoc().docmodule(module), encoding="utf-8")
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT / "tests")))
report = dict(tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
              successful=result.wasSuccessful(), details=[str(x) for x in result.failures + result.errors])
(ROOT / "docs" / "test_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
sys.exit(0 if result.wasSuccessful() else 1)

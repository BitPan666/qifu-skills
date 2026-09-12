#!/usr/bin/env python3
"""Exercise the standalone drawer release builder in an isolated directory."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "sync_drawer_release.py"


def main() -> int:
    spec = importlib.util.spec_from_file_location("sync_drawer_release", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load sync_drawer_release.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    with tempfile.TemporaryDirectory(prefix="qifu-drawer-release-test-") as temp:
        stage = Path(temp) / "release"
        module.build_release(stage, "0" * 40)
        module.validate_stage(stage)

        assert (stage / "skills/qifu-drawer-form/SKILL.md").is_file()
        assert (stage / "skills/qifu-shared/SKILL.md").is_file()
        assert not (stage / "skills/qifu-drawer-form/references/component-map.md").exists()

        result = subprocess.run(
            [sys.executable, str(stage / "scripts/validate_release.py")],
            cwd=stage,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode:
            print(result.stdout, end="")
            return result.returncode

    print("PASS: standalone drawer release build and validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_skill_contract.py"


class SkillContractTest(unittest.TestCase):
    def test_published_skill_contract_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(SKILL_ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS qifu-business-flow", result.stdout)


if __name__ == "__main__":
    unittest.main()

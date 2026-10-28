from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SHARED = ROOT / 'skills' / 'qifu-shared'
RESOLVER = ROOT / 'skills/qifu-drawer-form/scripts/resolve_platform.py'
VALIDATOR = SHARED / 'scripts/validate_platform_assets.py'
REGISTRY = SHARED / 'references/platform-registry.json'
THEMES = SHARED / 'theme/theme-registry.json'
spec = importlib.util.spec_from_file_location('foundation_resolver', RESOLVER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def arguments(**overrides):
    data = dict(platform_key=None, name=None, figma_node_name=[],
                figma_variable_mode=[], template_node_id=[])
    data.update(overrides)
    return argparse.Namespace(**data)


class FivePlatformFoundationTest(unittest.TestCase):
    def resolve(self, **kwargs):
        return module.resolve(module.load_platforms(REGISTRY), arguments(**kwargs))

    def test_resolves_missing_platform_names_without_borrowing_another_adapter(self):
        for name, key, theme in [('金毓盟', 'jinyumeng', 'jinyumeng-blue'),
                                 ('电销', 'dianxiao', 'dianxiao-green')]:
            with self.subTest(name=name):
                value, code = self.resolve(name=name)
                self.assertEqual(code, 0)
                self.assertEqual(value['platformKey'], key)
                self.assertEqual(value['defaultTheme'], theme)
                self.assertEqual(value['capabilities']['drawer'], 'pending-adapter')

    def test_resolves_smartops_shell_as_frame_without_upgrading_page_readiness(self):
        value, code = self.resolve(template_node_id=['6155:1851'])
        self.assertEqual(code, 0)
        self.assertEqual(value['platformKey'], 'zhineng-yunying')
        self.assertEqual(value['shell']['nodeType'], 'FRAME')
        self.assertEqual(value['shell']['method'], 'clone-frame')
        self.assertEqual(value['shell']['content']['nodeType'], 'RECTANGLE')
        self.assertEqual(value['shellReadiness'], 'source-verified')
        self.assertNotEqual(value['capabilities']['list'], 'ready')

    def test_legacy_zhikexing_source_is_identified_but_blocks_generation(self):
        value, code = self.resolve(template_node_id=['4892:34812'])
        self.assertEqual(code, 4)
        self.assertEqual(value['status'], 'BLOCKED_SOURCE')
        self.assertEqual(value['platformKey'], 'zhikexing')
        self.assertEqual(value['reason'], 'BLOCKED_PLATFORM_COMPONENT_INTEGRITY')

    def test_new_zhikexing_candidate_does_not_become_validated(self):
        value, code = self.resolve(template_node_id=['5468:3233'])
        self.assertEqual(code, 0)
        self.assertEqual(value['shellReadiness'], 'candidate')
        self.assertEqual(value['shell']['header']['nodeId'], '5517:2109')

    def test_explicit_platform_conflicts_with_other_platform_shell(self):
        value, code = self.resolve(platform_key='dianxiao', template_node_id=['6155:1851'])
        self.assertEqual(code, 3)
        self.assertEqual(value['status'], 'CONFLICT')

    def run_validator(self, registry=None, themes=None):
        with tempfile.TemporaryDirectory() as tmp:
            command = [sys.executable, str(VALIDATOR)]
            for flag, data in [('--registry', registry), ('--themes', themes)]:
                if data is not None:
                    path = Path(tmp) / (flag[2:] + '.json')
                    path.write_text(json.dumps(data), encoding='utf-8')
                    command.extend([flag, str(path)])
            return subprocess.run(command, text=True, capture_output=True)

    def test_published_registry_passes_asset_validation(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validator_rejects_smartops_menu_replaced_with_electric_master(self):
        data = json.loads(REGISTRY.read_text())
        data['platforms']['zhineng-yunying'].setdefault('shell', {})['menu'] = {
            'nodeId': '5763:1753', 'nodeType': 'COMPONENT_SET'}
        result = self.run_validator(registry=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('CROSS_PLATFORM_MENU', result.stdout)

    def test_validator_rejects_candidate_promoted_without_acceptance(self):
        data = json.loads(REGISTRY.read_text())
        data['platforms']['zhikexing']['shellReadiness'] = 'validated-template'
        result = self.run_validator(registry=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('UNVERIFIED_PROMOTION', result.stdout)

    def test_validator_rejects_stale_smartops_brand_verification(self):
        data = json.loads(THEMES.read_text())
        data['themes']['smartops-blue']['primary'] = '#1677FF'
        result = self.run_validator(themes=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('THEME_VALUE_DRIFT', result.stdout)

    def test_validator_rejects_blank_rectangle_declared_as_native_slot(self):
        data = json.loads(REGISTRY.read_text())
        data['platforms']['zhineng-yunying'].setdefault('shell', {})['content'] = {
            'nodeId': '6148:34365', 'nodeType': 'SLOT', 'method': 'replace-slot'}
        result = self.run_validator(registry=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('INVALID_CONTENT_ASSEMBLY', result.stdout)

    def test_validator_rejects_foreign_header_on_current_zhikexing_candidate(self):
        data = json.loads(REGISTRY.read_text())
        data['platforms']['zhikexing']['shell']['header']['nodeId'] = '3639:1529'
        result = self.run_validator(registry=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('OBSERVED_ASSET_DRIFT', result.stdout)

    def test_validator_rejects_a_platform_mode_from_another_platform(self):
        data = json.loads(THEMES.read_text())
        data['themes']['smartops-blue']['figmaModeId'] = '5722:0'
        result = self.run_validator(themes=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('THEME_MODE_MISSING', result.stdout)

    def test_validator_rejects_coordinated_foreign_theme_substitution(self):
        data = json.loads(THEMES.read_text())
        data['themes']['smartops-blue'] = copy.deepcopy(data['themes']['dianxiao-green'])
        result = self.run_validator(themes=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('THEME_PLATFORM_OWNERSHIP', result.stdout)

    def test_validator_rejects_platform_default_pointing_to_another_theme(self):
        data = json.loads(REGISTRY.read_text())
        data['platforms']['zhineng-yunying']['defaultTheme'] = 'dianxiao-green'
        result = self.run_validator(registry=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('THEME_PLATFORM_OWNERSHIP', result.stdout)

    def test_validator_rejects_unimplemented_drawer_promoted_to_preflight(self):
        data = json.loads(REGISTRY.read_text())
        data['platforms']['dianxiao']['capabilities']['drawer'] = 'preflight-required'
        result = self.run_validator(registry=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('CAPABILITY_EVIDENCE_MISSING', result.stdout)

    def test_validator_rejects_coordinated_candidate_promotion(self):
        data = json.loads(REGISTRY.read_text())
        data['platforms']['zhikexing']['shellReadiness'] = 'validated-template'
        data['platforms']['zhikexing']['shell']['sourceStatus'] = 'source-verified'
        result = self.run_validator(registry=data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('UNVERIFIED_PROMOTION', result.stdout)


if __name__ == '__main__':
    unittest.main()

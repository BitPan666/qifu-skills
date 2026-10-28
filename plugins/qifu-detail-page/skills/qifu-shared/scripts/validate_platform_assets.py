#!/usr/bin/env python3
"""Validate recorded platform sources and live theme bindings without editing Figma."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SHARED = Path(__file__).resolve().parents[1]
PLATFORMS = {'yushu', 'jinyumeng', 'dianxiao', 'zhikexing', 'zhineng-yunying'}


def validate(registry: dict, themes: dict, snapshot: dict, asset_snapshot: dict) -> list[str]:
    errors = []
    platforms = registry.get('platforms', {})
    if not isinstance(platforms, dict) or not PLATFORMS.issubset(platforms):
        return ['PLATFORM_MISSING: all five named platforms must be registered']
    for key in sorted(PLATFORMS):
        platform = platforms[key]
        shell = platform.get('shell', {})
        if not shell or not shell.get('method'):
            errors.append(f'SOURCE_MISSING: {key}')
        observed = asset_snapshot.get('platforms', {}).get(key, {})
        for part in ('shell', 'header', 'menu'):
            actual = shell if part == 'shell' else shell.get(part, {})
            for field, value in observed.get(part, {}).items():
                if field == 'scope':
                    continue
                if actual.get(field) != value:
                    errors.append(f'OBSERVED_ASSET_DRIFT: {key}.{part}.{field}')
        if not observed:
            errors.append(f'ASSET_EVIDENCE_MISSING: {key}')
        policy = asset_snapshot.get('releasePolicy', {}).get('platforms', {}).get(key, {})
        if not policy:
            errors.append(f'RELEASE_POLICY_MISSING: {key}')
        else:
            theme_key = policy.get('defaultTheme')
            theme = themes.get('themes', {}).get(theme_key, {})
            if platform.get('defaultTheme') != theme_key or not theme or theme.get('figmaModeId') != policy.get('figmaModeId'):
                errors.append(f'THEME_PLATFORM_OWNERSHIP: {key}')
            if platform.get('capabilities') != policy.get('capabilities'):
                errors.append(f'CAPABILITY_EVIDENCE_MISSING: {key}')
            if platform.get('shellReadiness') != policy.get('shellReadiness') or shell.get('sourceStatus') != policy.get('sourceStatus'):
                errors.append(f'UNVERIFIED_PROMOTION: {key} source readiness')
        if not observed.get('generationValidated') and any(value == 'ready' for value in platform.get('capabilities', {}).values()):
            errors.append(f'UNVERIFIED_PROMOTION: {key} page capability')
        if shell.get('sourceStatus') == 'candidate' and platform.get('shellReadiness') != 'candidate':
            errors.append(f'UNVERIFIED_PROMOTION: {key}')
        if not isinstance(platform.get('capabilities'), dict):
            errors.append(f'CAPABILITY_STATUS_MISSING: {key}')
        blocked = {item.get('nodeId') for item in platform.get('blockedSources', [])}
        if shell.get('nodeId') in blocked:
            errors.append(f'BLOCKED_DEFAULT_SOURCE: {key}')
        adapter = SHARED / platform.get('adapter', '')
        if not adapter.is_file():
            errors.append(f'ADAPTER_MISSING: {key}')

    smart = platforms['zhineng-yunying'].get('shell', {})
    electric = platforms['dianxiao'].get('shell', {})
    if smart.get('menu', {}).get('nodeId') == electric.get('menu', {}).get('nodeId'):
        errors.append('CROSS_PLATFORM_MENU: SmartOps and Dianxiao masters must be independent')
    if smart.get('nodeType') != 'FRAME' or smart.get('method') != 'clone-frame':
        errors.append('INVALID_SHELL_ASSEMBLY: SmartOps source is an editable frame')
    content = smart.get('content', {})
    if content.get('nodeType') != 'RECTANGLE' or content.get('method') != 'create-container-on-copy':
        errors.append('INVALID_CONTENT_ASSEMBLY: preserve blank source; create content container on copy')

    collection = snapshot.get('collection', {})
    modes = {item['name']: item['modeId'] for item in collection.get('modes', [])}
    variables = {item['path']: item for item in snapshot.get('semanticVariables', [])}
    for key, theme in themes.get('themes', {}).items():
        if key == 'custom':
            continue
        if theme.get('figmaCollectionId') != collection.get('id') or theme.get('figmaCollection') != collection.get('name'):
            errors.append(f'THEME_COLLECTION_MISSING: {key}')
        for path in theme.get('semanticBindings', {}).values():
            if path not in variables:
                errors.append(f'THEME_VARIABLE_MISSING: {key}: {path}')
        mode = theme.get('figmaMode')
        if mode is None:
            if theme.get('bindingStrategy') != 'inherit-template-then-semantic-variable' or theme.get('primary') is not None:
                errors.append(f'UNVERIFIED_TEMPLATE_COLOR: {key}')
            continue
        mode_id = modes.get(mode)
        if mode_id is None or theme.get('figmaModeId') != mode_id:
            errors.append(f'THEME_MODE_MISSING: {key}')
            continue
        brand = variables.get('基础颜色拓展/brand/default', {})
        observed = brand.get('resolvedByMode', {}).get(mode_id, {}).get('hex')
        if not observed or theme.get('primary') != observed:
            errors.append(f'THEME_VALUE_DRIFT: {key}: observed {observed}')
        chain = brand.get('resolvedByMode', {}).get(mode_id, {}).get('aliasChain', [])
        if not any(item['path'].startswith(theme.get('colorVariableGroup', '') + '/') for item in chain):
            errors.append(f'THEME_COLOR_GROUP_MISSING: {key}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', type=Path, default=SHARED / 'references/platform-registry.json')
    parser.add_argument('--themes', type=Path, default=SHARED / 'theme/theme-registry.json')
    parser.add_argument('--bindings', type=Path, default=SHARED / 'theme/live-platform-bindings.json')
    parser.add_argument('--assets', type=Path, default=SHARED / 'references/platform-asset-snapshot.json')
    args = parser.parse_args()
    try:
        data = [json.loads(p.read_text(encoding='utf-8')) for p in (args.registry, args.themes, args.bindings, args.assets)]
        if not all(isinstance(item, dict) for item in data):
            raise ValueError('all input roots must be objects')
        errors = validate(*data)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(f'INVALID_ASSET_CONTRACT: {exc}')
        return 1
    if errors:
        print('\n'.join(errors))
        return 1
    print('PASS: five platform sources and live theme bindings (source verification only)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

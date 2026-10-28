import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/plan_platform_drawer.py'

class PlatformDrawerPlanTests(unittest.TestCase):
    def spec(self,platform='jinyumeng'):
        return {'platformKey':platform,'drawerTitle':'新增运营任务','targetPageId':'3497:651','operation':'create','sections':[{'sectionTitle':'基础信息','fields':[{'fieldKey':'name','label':'任务名称','control':'Input','required':True}]}]}

    def call(self,spec,registry=None):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'spec.json';path.write_text(json.dumps(spec))
            args=[sys.executable,str(SCRIPT),'--spec',str(path)]
            if registry is not None:
                reg=Path(d)/'registry.json';reg.write_text(json.dumps(registry));args+=['--registry',str(reg)]
            r=subprocess.run(args,capture_output=True,text=True)
        self.assertTrue(r.stdout.strip(),r.stderr)
        return r.returncode,json.loads(r.stdout)

    def blocked(self,spec,error):
        code,out=self.call(spec);self.assertNotEqual(code,0);self.assertEqual(out['error'],error)

    def test_jinyumeng_plan_uses_own_background_theme_and_top_labels(self):
        code,out=self.call(self.spec());self.assertEqual(code,0)
        self.assertEqual(out['status'],'PREFLIGHT_REQUIRED');self.assertFalse(out['generationValidated'])
        self.assertEqual(out['headerHeight'],56);self.assertEqual(out['sidebarWidth'],208)
        self.assertEqual(out['modeId'],'4717:0');self.assertEqual(out['labelLayout'],'top')
        self.assertEqual(out['menuOwnerId'],'4746:46261');self.assertEqual(out['footerHeight'],64)
        self.assertEqual(out['controlSources']['Input'],'5010:19')

    def test_dianxiao_plan_has_no_action_slot_or_smartops_menu(self):
        code,out=self.call(self.spec('dianxiao'));self.assertEqual(code,0)
        self.assertEqual(out['sidebarWidth'],200);self.assertEqual(out['modeId'],'5722:0')
        self.assertEqual(out['menuOwnerId'],'5763:1753');self.assertEqual(out['footerHeight'],52)
        self.assertEqual(out['labelLayout'],'left');self.assertNotIn('actionSlot',out['backgroundSlots'])

    def test_edit_keeps_initial_values_and_footer_save(self):
        spec=self.spec('dianxiao');spec['operation']='edit';spec['sections'][0]['fields'][0]['defaultValue']='回访任务'
        code,out=self.call(spec);self.assertEqual(code,0);self.assertEqual(out['footer']['okText'],'保存')
        self.assertEqual(out['drawerSpec']['sections'][0]['fields'][0]['defaultValue'],'回访任务')

    def test_foreign_mode_rejected_even_with_correct_platform_name(self):
        spec=self.spec();spec['modeId']='5722:0';self.blocked(spec,'THEME_PLATFORM_CONFLICT')

    def test_foreign_theme_key_rejected(self):
        spec=self.spec();spec['themeKey']='smartops-blue';self.blocked(spec,'THEME_PLATFORM_CONFLICT')

    def test_unknown_control_does_not_fallback_to_input(self):
        spec=self.spec();spec['sections'][0]['fields'][0]['control']='TreeSelect';self.blocked(spec,'COMPONENT_MISSING')

    def test_duplicate_keys_fail_before_writes(self):
        spec=self.spec();spec['sections'][0]['fields']*=2;self.blocked(spec,'INVALID_FIELDS')

    def test_unvalidated_archetype_is_rejected(self):
        spec=self.spec();spec['compositionName']='Qifu Drawer Form / Data Detail with Table';self.blocked(spec,'UNSUPPORTED_ARCHETYPE')

    def test_unknown_width_does_not_resize_unvalidated_source(self):
        spec=self.spec();spec['widthTier']=840;self.blocked(spec,'UNSUPPORTED_WIDTH')

    def test_jinyumeng_1024_source_is_not_silently_used_as_open_scene(self):
        spec=self.spec();spec['viewport']={'width':1366,'height':1024};self.blocked(spec,'UNSUPPORTED_VIEWPORT')

    def test_legacy_or_foreign_background_is_rejected(self):
        for source in ['4892:34812','6034:4860']:
            spec=self.spec();spec['background']={'sourceNode':source};self.blocked(spec,'BLOCKED_SOURCE')

    def test_missing_target_is_rejected(self):
        spec=self.spec();del spec['targetPageId'];self.blocked(spec,'TARGET_REQUIRED')

    def test_label_layout_requires_its_own_acceptance(self):
        spec=self.spec();spec['labelLayout']='right';self.blocked(spec,'UNSUPPORTED_LABEL_LAYOUT')

    def test_unimplemented_platform_is_not_replaced_with_generic(self):
        self.blocked(self.spec('yushu'),'UNSUPPORTED_PLATFORM')

    def test_simple_create_rejects_grouped_or_too_many_fields(self):
        spec=self.spec();spec['compositionName']='Qifu Drawer Form / Simple Create'
        spec['sections'].append({'sectionTitle':'规则','fields':[{'fieldKey':'other','label':'其他','control':'Input'}]})
        self.blocked(spec,'UNSUPPORTED_ARCHETYPE')

    def test_edit_operation_cannot_use_create_composition(self):
        spec=self.spec();spec['operation']='edit';spec['compositionName']='Qifu Drawer Form / Simple Create'
        self.blocked(spec,'UNSUPPORTED_ARCHETYPE')

    def test_custom_footer_text_is_preserved(self):
        spec=self.spec();spec['footer']={'okText':'发布','cancelText':'返回'}
        code,out=self.call(spec);self.assertEqual(code,0);self.assertEqual(out['footer']['okText'],'发布');self.assertEqual(out['footer']['cancelText'],'返回')

    def test_registry_can_disable_adapter_before_generation(self):
        registry=json.loads((SCRIPT.parents[2]/'qifu-shared/references/platform-registry.json').read_text())
        registry['platforms']['jinyumeng']['capabilities']['drawer']='unsupported'
        code,out=self.call(self.spec(),registry)
        self.assertNotEqual(code,0);self.assertEqual(out['error'],'BLOCKED_PLATFORM_ADAPTER')

    def test_registry_control_scope_is_enforced(self):
        registry=json.loads((SCRIPT.parents[2]/'qifu-shared/references/platform-registry.json').read_text())
        p=registry['platforms']['jinyumeng'];p['capabilities']['drawer']='preflight-required'
        p['drawerAdapter']['supportedControls']=[]
        code,out=self.call(self.spec(),registry)
        self.assertNotEqual(code,0);self.assertEqual(out['error'],'COMPONENT_MISSING')

    def test_registry_operation_scope_is_enforced(self):
        registry=json.loads((SCRIPT.parents[2]/'qifu-shared/references/platform-registry.json').read_text())
        registry['platforms']['jinyumeng']['drawerAdapter']['supportedOperations']=['create']
        spec=self.spec();spec['operation']='edit'
        code,out=self.call(spec,registry);self.assertNotEqual(code,0);self.assertEqual(out['error'],'UNSUPPORTED_ARCHETYPE')

    def test_registry_readiness_and_geometry_scope_are_enforced(self):
        for field,value,error in [('readiness','unsupported','BLOCKED_PLATFORM_ADAPTER'),('widthTiers',[],'UNSUPPORTED_WIDTH'),('labelLayouts',[],'UNSUPPORTED_LABEL_LAYOUT'),('viewport',{'width':1366,'height':1024},'UNSUPPORTED_VIEWPORT')]:
            with self.subTest(field=field):
                registry=json.loads((SCRIPT.parents[2]/'qifu-shared/references/platform-registry.json').read_text())
                registry['platforms']['jinyumeng']['drawerAdapter'][field]=value
                code,out=self.call(self.spec(),registry)
                self.assertNotEqual(code,0);self.assertEqual(out['error'],error)

    def test_explicit_existing_background_requires_validated_node(self):
        spec=self.spec();spec['background']={'source':'EXISTING_LIST_PAGE'}
        self.blocked(spec,'BACKGROUND_SOURCE_REQUIRED')

    def test_unimplemented_background_modes_are_rejected(self):
        for mode in ['STRUCTURE_PREVIEW','TEMPLATE','UNKNOWN']:
            spec=self.spec();spec['background']={'source':mode}
            self.blocked(spec,'UNSUPPORTED_BACKGROUND_MODE')

    def test_explicit_validated_scene_is_preserved_in_plan(self):
        spec=self.spec();spec['background']={'source':'EXISTING_LIST_PAGE','sourceNode':'6197:8368'}
        code,out=self.call(spec);self.assertEqual(code,0)
        self.assertEqual(out['background'],spec['background'])

    def test_auto_background_is_normalized_to_real_platform_source(self):
        code,out=self.call(self.spec('dianxiao'));self.assertEqual(code,0)
        self.assertEqual(out['background'],{'source':'AUTO','sourceNode':'6034:4860'})

if __name__=='__main__':unittest.main()

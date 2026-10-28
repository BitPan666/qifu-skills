#!/usr/bin/env python3
"""Read-only preflight plans for the bounded Jinyumeng and Dianxiao drawer adapters."""
import argparse
import json
from pathlib import Path

FACTS={
'jinyumeng':{'themeKey':'jinyumeng-blue','modeId':'4717:0','headerOwnerId':'4993:1440','headerHeight':56,'sidebarWidth':208,'menuOwnerId':'4746:46261','shellNodeId':'5022:16','backgroundSourceNodeId':'6017:2723','sceneSourceNodeId':'6197:8368','labelLayout':'top','footerHeight':64,'backgroundSlots':['tabsSlot','filterSlot','actionSlot','tableSlot'],'controlSources':{'Input':'5010:19','Select':'5010:7028','DateRange':'5010:7055','Textarea':'2936:3834'}},
'dianxiao':{'themeKey':'dianxiao-green','modeId':'5722:0','headerOwnerId':'5824:4491','headerHeight':56,'sidebarWidth':200,'menuOwnerId':'5763:1753','shellNodeId':'5829:31','backgroundSourceNodeId':'6034:4860','sceneSourceNodeId':'6205:11709','labelLayout':'left','footerHeight':52,'backgroundSlots':['tabsSlot','filterSlot','tableSlot'],'controlSources':{'Input':'3406:853','Select':'2859:2820','DateRange':'2967:30327','Textarea':'2936:3834'}}}
REGISTRY=Path(__file__).resolve().parents[2]/'qifu-shared/references/platform-registry.json'
ALLOWED_COMPOSITIONS={'Qifu Drawer Form / Simple Create','Qifu Drawer Form / Sectioned Create','Qifu Drawer Form / Edit'}

class PlanError(ValueError): pass

def plan_drawer(spec,registry=None):
    if not isinstance(spec,dict):raise PlanError('INVALID_SPEC')
    key=spec.get('platformKey')
    if key not in FACTS:raise PlanError('UNSUPPORTED_PLATFORM')
    fact=FACTS[key]
    registry=registry if registry is not None else json.loads(REGISTRY.read_text())
    platform=registry.get('platforms',{}).get(key,{})
    if platform.get('capabilities',{}).get('drawer')!='preflight-required':raise PlanError('BLOCKED_PLATFORM_ADAPTER')
    adapter=platform.get('drawerAdapter',{})
    if adapter.get('readiness')!='preflight-required':raise PlanError('BLOCKED_PLATFORM_ADAPTER')
    if spec.get('operation','create') not in adapter.get('supportedOperations',[]):raise PlanError('UNSUPPORTED_ARCHETYPE')
    if spec.get('modeId',fact['modeId'])!=fact['modeId'] or spec.get('themeKey',fact['themeKey'])!=fact['themeKey']:raise PlanError('THEME_PLATFORM_CONFLICT')
    if not isinstance(spec.get('targetPageId'),str) or not spec['targetPageId'].strip():raise PlanError('TARGET_REQUIRED')
    if not isinstance(spec.get('drawerTitle'),str) or not spec['drawerTitle'].strip():raise PlanError('TITLE_REQUIRED')
    if spec.get('widthTier',640)!=640 or 640 not in adapter.get('widthTiers',[]):raise PlanError('UNSUPPORTED_WIDTH')
    viewport=spec.get('viewport',{'width':1366,'height':768})
    if viewport!={'width':1366,'height':768} or viewport!=adapter.get('viewport'):raise PlanError('UNSUPPORTED_VIEWPORT')
    if spec.get('labelLayout',fact['labelLayout'])!=fact['labelLayout'] or fact['labelLayout'] not in adapter.get('labelLayouts',[]):raise PlanError('UNSUPPORTED_LABEL_LAYOUT')
    if spec.get('operation','create') not in ('create','edit') or spec.get('embeddedTable'):raise PlanError('UNSUPPORTED_ARCHETYPE')
    sections=spec.get('sections')
    if not isinstance(sections,list) or not 1<=len(sections)<=3:raise PlanError('INVALID_FIELDS')
    fields=[]
    for section in sections:
        if not isinstance(section,dict) or not isinstance(section.get('fields'),list) or not section['fields']:raise PlanError('INVALID_FIELDS')
        fields.extend(section['fields'])
    if not 1<=len(fields)<=15:raise PlanError('UNSUPPORTED_ARCHETYPE')
    keys=[]
    for f in fields:
        if not isinstance(f,dict) or not isinstance(f.get('fieldKey'),str) or not f['fieldKey'].strip() or not isinstance(f.get('label'),str) or not f['label'].strip():raise PlanError('INVALID_FIELDS')
        if f.get('control') not in adapter.get('supportedControls',[]) or f.get('control') not in fact['controlSources']:raise PlanError('COMPONENT_MISSING')
        keys.append(f['fieldKey'])
    if len(set(keys))!=len(keys):raise PlanError('INVALID_FIELDS')
    composition=spec.get('compositionName') or ('Qifu Drawer Form / Edit' if spec.get('operation')=='edit' else ('Qifu Drawer Form / Sectioned Create' if len(sections)>1 else 'Qifu Drawer Form / Simple Create'))
    if composition not in adapter.get('supportedCompositions',[]) or composition not in ALLOWED_COMPOSITIONS:raise PlanError('UNSUPPORTED_ARCHETYPE')
    if (spec.get('operation')=='edit') != (composition=='Qifu Drawer Form / Edit'):raise PlanError('UNSUPPORTED_ARCHETYPE')
    if composition=='Qifu Drawer Form / Simple Create' and (len(fields)>6 or len(sections)!=1):raise PlanError('UNSUPPORTED_ARCHETYPE')
    if composition=='Qifu Drawer Form / Sectioned Create' and not 2<=len(sections)<=3:raise PlanError('UNSUPPORTED_ARCHETYPE')
    background=spec.get('background',{})
    if not isinstance(background,dict):raise PlanError('INVALID_SPEC')
    background_mode=background.get('source','AUTO')
    if background_mode not in ('AUTO','EXISTING_LIST_PAGE'):raise PlanError('UNSUPPORTED_BACKGROUND_MODE')
    if background_mode=='EXISTING_LIST_PAGE' and not background.get('sourceNode'):raise PlanError('BACKGROUND_SOURCE_REQUIRED')
    if background.get('sourceNode',fact['backgroundSourceNodeId']) not in (fact['backgroundSourceNodeId'],fact['sceneSourceNodeId']):raise PlanError('BLOCKED_SOURCE')
    background={**background,'source':background_mode,'sourceNode':background.get('sourceNode',fact['backgroundSourceNodeId'])}
    footer={'showCancel':True,'cancelText':'取消','okText':'保存' if spec.get('operation')=='edit' else '确定'}
    supplied=spec.get('footer',{})
    if not isinstance(supplied,dict) or set(supplied)-set(footer):raise PlanError('UNSUPPORTED_FOOTER')
    footer.update(supplied)
    if not all(isinstance(footer[k],str) and footer[k].strip() for k in ('okText','cancelText')) or not isinstance(footer['showCancel'],bool):raise PlanError('INVALID_FOOTER')
    return {**fact,'status':'PREFLIGHT_REQUIRED','generationValidated':False,'platformKey':key,'compositionName':composition,'drawerSpec':spec,'background':background,'widthTier':640,'viewport':viewport,'footer':footer,'requiredChecks':['editable-backup','background-platform-geometry','component-properties','semantic-bindings','text-styles','body-scroll-footer-pinned','screenshot']}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--spec',required=True,type=Path);parser.add_argument('--registry',type=Path,default=REGISTRY);args=parser.parse_args()
    try:result=plan_drawer(json.loads(args.spec.read_text(encoding='utf-8')),json.loads(args.registry.read_text(encoding='utf-8')))
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps({'status':'BLOCKED','error':str(exc) if isinstance(exc,PlanError) else 'INVALID_SPEC'},ensure_ascii=False));return 2
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0

if __name__=='__main__':raise SystemExit(main())

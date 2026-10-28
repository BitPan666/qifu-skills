// Fixed Create/Edit regression fixture, not a generic generator.
// Uses existing editable platform-specific backgrounds and controls.
// First call clones and commits; repeat the same fixture to apply to fully loaded nested instances.
const PLATFORM='jinyumeng';
const OPERATION='create';
const page=await figma.getNodeByIdAsync('3497:651');await figma.setCurrentPageAsync(page);
const sourceId=PLATFORM==='jinyumeng'?'6197:8368':'6205:11709';
const mode=PLATFORM==='jinyumeng'?'4717:0':'5722:0';
const label=PLATFORM==='jinyumeng'?'金毓盟':'电销';
const title=OPERATION==='create'?'新增运营任务':'编辑运营任务';
const name='Trial / 20261028-233328 / '+label+' / '+title;
const exists=page.children.find(n=>n.name===name);
const source=await figma.getNodeByIdAsync(sourceId);
const fonts=new Map();for(const t of source.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))fonts.set(JSON.stringify(seg.fontName),seg.fontName);
await Promise.all([...fonts.values()].map(f=>figma.loadFontAsync(f)));
const root=exists||source.clone();
if(!exists){page.appendChild(root);root.name=name;root.x=Math.max(0,...page.children.filter(n=>n.id!==root.id).map(n=>n.x+n.width))+120;root.y=200;return {status:'CREATED_NEEDS_APPLY',createdNodeIds:[root.id],nodeId:root.id,sourceId};}
const collection=await figma.variables.getVariableCollectionByIdAsync('VariableCollectionId:9:8');root.setExplicitVariableModeForCollection(collection,mode);
const drawer=root.children.find(n=>n.name.startsWith('Drawer /'));
drawer.name='Drawer / '+label+' / '+title;
const header=drawer.children.find(n=>n.name==='Drawer / Header');
const body=drawer.children.find(n=>n.name==='Drawer / Body');
const footer=drawer.children.find(n=>n.name==='Drawer / Footer');
header.children.find(n=>n.type==='TEXT').characters=title;
const fieldLabels={'策略名称':'任务名称','有效期':'执行时间','策略类型':'任务类型','备注':'说明','策略配置':'任务配置'};
for(const t of body.findAllWithCriteria({types:['TEXT']})){if(!t.id.startsWith('I')&&fieldLabels[t.characters])t.characters=fieldLabels[t.characters];}
function prop(i,prefix,value){const keys=Object.keys(i.componentProperties).filter(k=>k.startsWith(prefix));if(keys.length!==1)throw new Error('PROPERTY_MISSING:'+prefix);i.setProperties({[keys[0]]:value});if(i.componentProperties[keys[0]].value!==value)throw new Error('PROPERTY_READBACK:'+prefix);}
const changed=[root.id,drawer.id,header.id];
const controls=[];
for(const i of body.findAllWithCriteria({types:['INSTANCE']})){const m=await i.getMainComponentAsync();controls.push({i,owner:m?.parent?.type==='COMPONENT_SET'?m.parent.id:m?.id});}
for(const {i,owner} of controls){
 if(owner==='3406:853'){prop(i,'value 文本',OPERATION==='create'?'请输入任务名称':'客户回访任务');prop(i,'content 内容',OPERATION==='create'?'Placeholder 占位':'Value 已填');changed.push(i.id);}
 if(owner==='2859:2820'){prop(i,'value 文本',OPERATION==='create'?'请选择任务类型':'客户回访');if(OPERATION==='edit'){const primary=await figma.variables.getVariableByIdAsync('VariableID:9:112');for(const t of i.findAllWithCriteria({types:['TEXT']})){if(t.characters==='客户回访'){await figma.loadFontAsync(t.fontName);t.fills=t.fills.map(p=>p.type==='SOLID'?figma.variables.setBoundVariableForPaint(p,'color',primary):p);}}}changed.push(i.id);}
 if(owner==='2967:30327'){prop(i,'placeholder 提示','开始日期 至 结束日期');prop(i,'filled 填充',OPERATION==='create'?'false':'true');prop(i,'value 文本','2026-10-29 至 2026-11-05');changed.push(i.id);}
 if(owner==='2936:3834'){prop(i,'value 文本',OPERATION==='create'?'请输入说明':'联系近期未回访客户');prop(i,'content 内容',OPERATION==='create'?'Placeholder 占位':'Value 已填');changed.push(i.id);}
}
for(const i of footer.findAllWithCriteria({types:['INSTANCE']})){const key=Object.keys(i.componentProperties).find(k=>k.startsWith('text 文案'));if(key&&i.componentProperties[key].value==='确定'){prop(i,'text 文案',OPERATION==='create'?'确定':'保存');changed.push(i.id);}}
const visible=t=>{let p=t;while(p&&p.id!==root.id){if(p.visible===false)return false;p=p.parent;}return true;};
const missing=root.findAllWithCriteria({types:['TEXT']}).filter(t=>visible(t)&&(!t.textStyleId||t.textStyleId===figma.mixed));
return {nodeId:root.id,createdNodeIds:[],mutatedNodeIds:changed,sourceId,platform:PLATFORM,operation:OPERATION,mode:root.explicitVariableModes,scene:{width:root.width,height:root.height},drawer:{x:drawer.x,y:drawer.y,width:drawer.width,height:drawer.height},footer:{y:footer.y,height:footer.height},missingTextStyleCount:missing.length,missingTextStyles:missing.slice(0,12).map(t=>({id:t.id,text:t.characters,parentType:t.parent.type}))};

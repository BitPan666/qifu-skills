// Maintenance fixture, not an automatic generation fallback.
// Requires figma-use + figma-generate-library and the recorded editable backup page.
// Replace only TARGET_ID with the explicitly selected regression frame.
const TARGET_ID = '6185:7863';
const target = await figma.getNodeByIdAsync(TARGET_ID);
let page=target;while(page.type!=='PAGE')page=page.parent;
await figma.setCurrentPageAsync(page);
const backupPage=await figma.getNodeByIdAsync('6183:2');
const texts=target.findAllWithCriteria({types:['TEXT']});
const missing=texts.filter(t=>!t.textStyleId||t.textStyleId===figma.mixed);
const styles=await figma.getLocalTextStylesAsync();
const restored=[],createdStyleIds=[],componentBackups=[],skipped=[];
const done=new Set();
for(const visible of missing){
  let node=visible;
  if(visible.id.startsWith('I')){
    node=await figma.getNodeByIdAsync(visible.id.split(';').pop());
    if(!node||node.type!=='TEXT'){skipped.push({id:visible.id,reason:'SOURCE_TEXT_UNRESOLVED'});continue;}
    let component=node.parent;while(component&&component.type!=='COMPONENT')component=component.parent;
    if(!component){skipped.push({id:visible.id,reason:'SOURCE_COMPONENT_UNRESOLVED'});continue;}
    const backupName='Backup / Typography / 20261028-233328 / '+component.id;
    let copy=backupPage.children.find(n=>n.name===backupName);
    if(!copy){
      const fonts=new Map();for(const t of component.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))fonts.set(JSON.stringify(seg.fontName),seg.fontName);
      await Promise.all([...fonts.values()].map(f=>figma.loadFontAsync(f)));
      copy=component.clone();backupPage.appendChild(copy);copy.name=backupName;
      copy.x=backupPage.children.length*260;copy.y=1300;
    }
    if(!componentBackups.some(x=>x.sourceId===component.id))componentBackups.push({sourceId:component.id,backupId:copy.id});
  }
  if(done.has(node.id)||node.textStyleId)continue;
  done.add(node.id);
  if(node.fontName===figma.mixed||node.fontSize===figma.mixed||node.lineHeight===figma.mixed||node.letterSpacing===figma.mixed){skipped.push({id:node.id,reason:'MIXED_TYPOGRAPHY'});continue;}
  const before={id:node.id,textStyleId:node.textStyleId,fontName:node.fontName,fontSize:node.fontSize,lineHeight:node.lineHeight,letterSpacing:node.letterSpacing,textCase:node.textCase,textDecoration:node.textDecoration};
  await figma.loadFontAsync(node.fontName);
  const name='Platform Typography / '+node.fontName.family+' / '+node.fontName.style+' / '+node.fontSize+' / '+(node.lineHeight.unit==='PIXELS'?node.lineHeight.value:node.lineHeight.unit);
  let style=styles.find(s=>s.name===name);
  if(!style){style=figma.createTextStyle();style.name=name;style.fontName=node.fontName;style.fontSize=node.fontSize;style.lineHeight=node.lineHeight;style.letterSpacing=node.letterSpacing;style.textCase=node.textCase;style.textDecoration=node.textDecoration;styles.push(style);createdStyleIds.push(style.id);}
  await node.setTextStyleIdAsync(style.id);
  restored.push({...before,appliedStyleId:style.id});
}
return {targetId:target.id,createdNodeIds:componentBackups.map(x=>x.backupId),createdStyleIds,mutatedNodeIds:restored.map(x=>x.id),componentBackups,restoreTypography:restored,skipped};

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
const available=await figma.listAvailableFontsAsync();
const supported=f=>available.some(x=>x.fontName.family===f.family&&x.fontName.style===f.style);
const restored=[],createdStyleIds=[],componentBackups=[],skipped=[];
const done=new Set();
const specialBackups={'4968:8898':'6202:10164'};
for(const visible of missing){
  if(restored.length>=10)break;
  let node=visible;
  if(visible.id.startsWith('I')){
    node=await figma.getNodeByIdAsync(visible.id.split(';').pop());
    if(!node||node.type!=='TEXT'){
      const indices=[];let child=visible,ancestor=visible.parent;
      while(ancestor&&ancestor.type!=='INSTANCE'){indices.unshift(ancestor.children.findIndex(n=>n.id===child.id));child=ancestor;ancestor=ancestor.parent;}
      if(ancestor){indices.unshift(ancestor.children.findIndex(n=>n.id===child.id));let mapped=await ancestor.getMainComponentAsync();for(const index of indices)mapped=mapped&&'children'in mapped?mapped.children[index]:null;if(mapped?.type==='TEXT')node=mapped;}
    }
    if(!node||node.type!=='TEXT'){skipped.push({id:visible.id,reason:'SOURCE_TEXT_UNRESOLVED'});continue;}
    let component=node.parent;while(component&&component.type!=='COMPONENT')component=component.parent;
    if(!component){skipped.push({id:visible.id,reason:'SOURCE_COMPONENT_UNRESOLVED'});continue;}
    const backupName='Backup / Typography / 20261028-233328 / '+component.id;
    let copy=specialBackups[component.id]?await figma.getNodeByIdAsync(specialBackups[component.id]):backupPage.children.find(n=>n.name===backupName);
    if(!copy){
      const fonts=new Map();for(const t of component.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))fonts.set(JSON.stringify(seg.fontName),seg.fontName);
      await Promise.all([...fonts.values()].filter(supported).map(f=>figma.loadFontAsync(f)));
      // A missing legacy font is copied as an editable backup before normalization; no text is edited in the backup.
      copy=component.clone();
      if([...fonts.values()].every(supported))backupPage.appendChild(copy);
      copy.name=backupName;
      copy.x=copy.parent.type==='PAGE'?Math.max(0,...copy.parent.children.filter(n=>n.id!==copy.id).map(n=>n.x+n.width))+120:backupPage.children.length*260;copy.y=1300;
    }
    if(!componentBackups.some(x=>x.sourceId===component.id))componentBackups.push({sourceId:component.id,backupId:copy.id});
  }
  if(done.has(node.id)||node.textStyleId)continue;
  done.add(node.id);
  if(node.fontName===figma.mixed||node.fontSize===figma.mixed||node.lineHeight===figma.mixed||node.letterSpacing===figma.mixed){skipped.push({id:node.id,reason:'MIXED_TYPOGRAPHY'});continue;}
  const before={id:node.id,textStyleId:node.textStyleId,fontName:node.fontName,fontSize:node.fontSize,lineHeight:node.lineHeight,letterSpacing:node.letterSpacing,textCase:node.textCase,textDecoration:node.textDecoration,boundVariables:node.boundVariables};
  // Explicit maintenance normalization: the legacy PingFang SC Semibold label resolves to Bold in verified existing instances; keep the semantic weight binding.
  const resolvedFont=supported(visible.fontName)?visible.fontName:(node.fontName.family==='PingFang SC'&&node.fontName.style==='Semibold'?{family:'PingFang SC',style:'Bold'}:null);
  const effectiveFont=supported(node.fontName)?node.fontName:resolvedFont;
  if(!effectiveFont||!supported(effectiveFont)||effectiveFont.family!==node.fontName.family){skipped.push({id:node.id,reason:'NO_VERIFIED_EFFECTIVE_FONT'});continue;}
  await figma.loadFontAsync(effectiveFont);
  const bindingSignature=JSON.stringify(Object.fromEntries(Object.entries(before.boundVariables).filter(([k])=>['fontFamily','fontStyle','fontWeight','fontSize','lineHeight','letterSpacing','paragraphSpacing','paragraphIndent'].includes(k))));
  let signatureHash=2166136261;for(let i=0;i<bindingSignature.length;i++)signatureHash=Math.imul(signatureHash^bindingSignature.charCodeAt(i),16777619)>>>0;
  const name='Platform Typography / '+effectiveFont.family+' / '+effectiveFont.style+' / '+node.fontSize+' / '+(node.lineHeight.unit==='PIXELS'?node.lineHeight.value:node.lineHeight.unit)+' / b'+signatureHash.toString(16);
  let style=styles.find(s=>s.name===name);
  if(!style){style=figma.createTextStyle();style.name=name;style.fontName=effectiveFont;style.fontSize=node.fontSize;style.lineHeight=node.lineHeight;style.letterSpacing=node.letterSpacing;style.textCase=node.textCase;style.textDecoration=node.textDecoration;styles.push(style);createdStyleIds.push(style.id);}
  for(const field of ['fontFamily','fontStyle','fontWeight','fontSize','lineHeight','letterSpacing','paragraphSpacing','paragraphIndent']){
    const aliases=before.boundVariables[field];
    if(Array.isArray(aliases)&&aliases.length===1){
      const variable=await figma.variables.getVariableByIdAsync(aliases[0].id);
      if(field==='fontFamily'){
        const families=Object.values(variable.valuesByMode).filter(v=>typeof v==='string');
        await Promise.all(available.filter(f=>families.includes(f.fontName.family)).map(f=>figma.loadFontAsync(f.fontName)));
      }
      style.setBoundVariable(field,variable);
    }
  }
  await node.setTextStyleIdAsync(style.id);
  if(JSON.stringify(node.fontName)!==JSON.stringify(effectiveFont)||node.fontSize!==before.fontSize||JSON.stringify(node.lineHeight)!==JSON.stringify(before.lineHeight))throw new Error("TYPOGRAPHY_CHANGED:"+node.id);
  restored.push({...before,appliedStyleId:style.id,effectiveFont,normalizedMissingFont:JSON.stringify(before.fontName)!==JSON.stringify(effectiveFont),bindingsAfter:node.boundVariables,styleBindings:style.boundVariables,backupScope:visible.id.startsWith('I')?'component-backup':'new-trial-node'});
}
return {targetId:target.id,createdNodeIds:componentBackups.map(x=>x.backupId),createdStyleIds,mutatedNodeIds:restored.map(x=>x.id),componentBackups,restoreTypography:restored,skipped};

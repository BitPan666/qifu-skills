await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('3497:651'));
const repaired=[],skipped=[];
for(const id of ['6205:11709','6205:14118']){
 const root=await figma.getNodeByIdAsync(id);
 const missing=root.findAllWithCriteria({types:['TEXT']}).filter(t=>!t.textStyleId||t.textStyleId===figma.mixed);
 for(const t of missing){
  const source=await figma.getNodeByIdAsync(t.id.split(';').pop());
  if(!source||source.type!=='TEXT'||!source.textStyleId){skipped.push(t.id);continue;}
  const before={fontName:t.fontName,fontSize:t.fontSize,lineHeight:t.lineHeight};
  if(JSON.stringify(before)!==JSON.stringify({fontName:source.fontName,fontSize:source.fontSize,lineHeight:source.lineHeight})){skipped.push(t.id);continue;}
  await figma.loadFontAsync(t.fontName);
  await t.setTextStyleIdAsync(source.textStyleId);
  if(JSON.stringify(before)!==JSON.stringify({fontName:t.fontName,fontSize:t.fontSize,lineHeight:t.lineHeight}))throw new Error('TYPOGRAPHY_CHANGED:'+t.id);
  repaired.push({id:t.id,sourceId:source.id,approvedStyleId:source.textStyleId,before});
 }
}
return {mutatedNodeIds:repaired.map(x=>x.id),restoredStyleAssociations:repaired,skipped};

import{s as u,Q as c,a as m,v as a,j as s,e as f}from"./index-176b79a9.js";import{L as g}from"./context-4c50fddd.js";import x from"./ModelLineage-d6235abf.js";import"./_commonjs-dynamic-modules-302442b1.js";import"./Input-a01139a4.js";import"./editor-d35a2632.js";import"./file-d5b08b04.js";import"./project-e6dc9a02.js";import"./help-68063aae.js";import"./SourceList-a47c6829.js";import"./index-ae36976e.js";import"./transition-19ed7834.js";import"./ListboxShow-71b4cfa2.js";import"./SearchList-a958facb.js";function Q(){const l=u(),{modelName:t}=c(),i=m(e=>e.models),o=m(e=>e.lastSelectedModel),r=a(t)||t===(o==null?void 0:o.name)?o:i.get(encodeURI(t));function d(e){const n=i.get(e);a(n)||l(f.LineageModels+"/"+n.name)}function p(e){console.log(e==null?void 0:e.message)}return s.jsx("div",{className:"flex overflow-hidden w-full h-full",children:s.jsx(g,{showColumns:!0,handleClickModel:d,handleError:p,children:s.jsx(x,{model:r})})})}export{Q as default};

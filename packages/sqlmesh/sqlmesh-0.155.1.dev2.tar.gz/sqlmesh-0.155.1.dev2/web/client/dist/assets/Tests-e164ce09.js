import{x as u,j as s,e as t,H as f,B as c,m as x,l as p,O as j}from"./index-176b79a9.js";import{P as d}from"./Page-fac9d8c9.js";import{u as h}from"./project-e6dc9a02.js";import{S as v}from"./SourceList-a47c6829.js";import{S}from"./SourceListItem-1c90281a.js";import"./SplitPane-94158256.js";import"./file-d5b08b04.js";import"./Input-a01139a4.js";import"./index-ae36976e.js";function T(){const{pathname:a}=u(),i=h(e=>e.files),r=Array.from(i.values()).filter(e=>e.path.endsWith("tests"));return s.jsx(d,{sidebar:s.jsxs("div",{className:"flex flex-col w-full h-full",children:[s.jsx(v,{keyId:"basename",keyName:"basename",to:t.Tests,items:r,isActive:e=>`${t.Tests}/${e}`===a,listItem:({to:e,name:o,description:m,text:l,disabled:n=!1})=>s.jsx(S,{to:e,name:o,text:l,description:m,disabled:n})}),s.jsx(f,{}),s.jsx("div",{className:"py-1 px-1 flex justify-end",children:s.jsx(c,{size:x.sm,variant:p.Neutral,children:"Run All"})})]}),content:s.jsx(j,{})})}export{T as default};

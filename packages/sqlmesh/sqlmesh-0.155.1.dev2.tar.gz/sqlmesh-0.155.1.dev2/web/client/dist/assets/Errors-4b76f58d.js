import{x as j,s as v,d as y,r as l,D as N,e as i,v as g,j as r,l as m,H as h,B as D,m as k,O as S,i as A}from"./index-176b79a9.js";import{P as z}from"./Page-fac9d8c9.js";import{S as C}from"./SourceList-a47c6829.js";import{S as I}from"./SourceListItem-1c90281a.js";import"./SplitPane-94158256.js";import"./Input-a01139a4.js";import"./index-ae36976e.js";function $(){const{pathname:c}=j(),a=v(),{errors:o,removeError:u,clearErrors:f}=y(),t=l.useMemo(()=>Array.from(o).reverse(),[o]);l.useEffect(()=>{var e;if(N(t))setTimeout(()=>a(i.Home));else{const s=(e=t[0])==null?void 0:e.id;g(s)?a(i.Errors,{replace:!0}):a(i.Errors+"/"+s,{replace:!0})}},[t]);function d(e){const s=t.find(n=>n.id===e);A(s)&&u(s)}return r.jsx(z,{sidebar:r.jsxs("div",{className:"flex flex-col h-full w-full",children:[r.jsx(C,{keyId:"id",keyName:"key",keyDescription:"message",to:i.Errors,items:t,isActive:e=>`${i.Errors}/${e}`===c,types:t.reduce((e,s)=>Object.assign(e,{[s.id]:s.status}),{}),listItem:({id:e,to:s,name:n,description:p,text:x,disabled:E=!1})=>r.jsx(I,{to:s,name:n,text:x,description:p,variant:m.Danger,disabled:E,handleDelete:()=>d(e)})}),r.jsx(h,{}),o.size>0&&r.jsx("div",{className:"flex justify-end",children:r.jsx(D,{size:k.sm,variant:m.Neutral,onClick:()=>f(),children:"Clear All"})})]}),content:r.jsx(S,{})})}export{$ as default};

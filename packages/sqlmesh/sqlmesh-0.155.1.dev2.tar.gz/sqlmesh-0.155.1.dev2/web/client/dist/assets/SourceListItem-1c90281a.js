import{j as t,N as c,c as u,i as l,l as i}from"./index-176b79a9.js";function f({name:o,description:a,to:p,text:n,variant:s,disabled:x=!1,handleDelete:r}){function d(e){(e.key==="Delete"||e.key==="Backspace")&&(e.preventDefault(),e.stopPropagation(),r==null||r())}return t.jsxs(c,{onKeyUp:d,to:p,className:({isActive:e})=>u("block overflow-hidden px-2 py-1.5 rounded-md w-full font-semibold",x&&"opacity-50 pointer-events-none",e?s===i.Primary?"text-primary-500 bg-primary-10":s===i.Danger?"text-danger-500 bg-danger-5":"text-neutral-600 dark:text-neutral-100 bg-neutral-10":"hover:bg-neutral-5 text-neutral-500 dark:text-neutral-400"),children:[t.jsxs("div",{className:"flex items-center",children:[t.jsx("span",{className:"whitespace-nowrap overflow-ellipsis overflow-hidden min-w-10",children:o}),l(n)&&t.jsx("span",{className:" ml-2 px-2 rounded-md leading-0 text-[0.5rem] bg-neutral-10 text-neutral-700 dark:text-neutral-200",children:n})]}),l(a)&&t.jsx("p",{className:"text-xs overflow-hidden whitespace-nowrap overflow-ellipsis text-neutral-300 dark:text-neutral-500",children:a})]})}export{f as S};

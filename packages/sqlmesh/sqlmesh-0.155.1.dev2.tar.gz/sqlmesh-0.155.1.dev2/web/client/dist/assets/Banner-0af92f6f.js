import{j as s,c as i,m as a,l as n,H as p}from"./index-176b79a9.js";function l({variant:t=n.Neutral,size:e=a.md,isFull:r=!1,isCenter:u=!1,hasBackground:x=!0,hasBackgroundOnHover:f=!1,hasBorder:c=!1,children:m,className:b}){return s.jsx("div",{className:i("w-full text-sm px-4 overflow-hidden rounded-lg",e===a.sm&&"py-2",e===a.md&&"py-4",e===a.lg&&"py-6",r&&"h-full",u&&"justify-center items-center",c&&"border-2",w(t,x,f),b),children:m})}function g({className:t}){return s.jsx(p,{className:i("mx-4 w-full",t)})}function d({children:t,className:e}){return s.jsx("h4",{className:i("font-bold text-sm whitespace-nowrap text-left",e),children:t})}function o({children:t,className:e}){return s.jsx("p",{className:i("text-neutral-600",e),children:t})}l.Label=d;l.Description=o;l.Divider=g;function w(t,e=!0,r=!1){switch(t){case n.Primary:return[r?"hover:bg-primary-5":"",e?"bg-primary-5":"","text-primary-600 dark:text-primary-400"];case n.Success:return[r?"hover:bg-success-5":"",e?"bg-success-5":"","text-success-600 dark:text-success-400"];case n.Warning:return[r?"hover:bg-warning-5":"",e?"bg-warning-5":"","text-warning-600 dark:text-warning-400"];case n.Danger:return[r?"hover:bg-danger-5":"",e?"bg-danger-5":"","text-danger-600 dark:text-danger-400"];case n.Info:return[r?"hover:bg-info-5":"",e?"bg-info-5":"","text-info-600 dark:text-info-400"];case n.Neutral:return[r?"hover:bg-neutral-5":"",e?"bg-neutral-5":"","text-neutral-600 dark:text-neutral-400"];default:return["bg-transparent","text-neutral-600 dark:text-neutral-400"]}}export{l as B};

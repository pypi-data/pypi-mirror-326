import{R as x,r as s,a3 as U,a2 as F}from"./index-176b79a9.js";import{S as L,D as k,y as E,L as H,o as C,B as A,u as S,i as R,X as I,I as M,z as K,C as N,A as V,r as P,v as W}from"./transition-19ed7834.js";import{c as G}from"./_commonjs-dynamic-modules-302442b1.js";var O;let Q=(O=x.startTransition)!=null?O:function(e){e()};var X=(e=>(e[e.Open=0]="Open",e[e.Closed=1]="Closed",e))(X||{}),Y=(e=>(e[e.ToggleDisclosure=0]="ToggleDisclosure",e[e.CloseDisclosure=1]="CloseDisclosure",e[e.SetButtonId=2]="SetButtonId",e[e.SetPanelId=3]="SetPanelId",e[e.LinkPanel=4]="LinkPanel",e[e.UnlinkPanel=5]="UnlinkPanel",e))(Y||{});let Z={0:e=>({...e,disclosureState:S(e.disclosureState,{0:1,1:0})}),1:e=>e.disclosureState===1?e:{...e,disclosureState:1},4(e){return e.linkedPanel===!0?e:{...e,linkedPanel:!0}},5(e){return e.linkedPanel===!1?e:{...e,linkedPanel:!1}},2(e,n){return e.buttonId===n.buttonId?e:{...e,buttonId:n.buttonId}},3(e,n){return e.panelId===n.panelId?e:{...e,panelId:n.panelId}}},D=s.createContext(null);D.displayName="DisclosureContext";function z(e){let n=s.useContext(D);if(n===null){let l=new Error(`<${e} /> is missing a parent <Disclosure /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(l,z),l}return n}let T=s.createContext(null);T.displayName="DisclosureAPIContext";function B(e){let n=s.useContext(T);if(n===null){let l=new Error(`<${e} /> is missing a parent <Disclosure /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(l,B),l}return n}let j=s.createContext(null);j.displayName="DisclosurePanelContext";function J(){return s.useContext(j)}function _(e,n){return S(n.type,Z,e,n)}let ee=s.Fragment;function te(e,n){let{defaultOpen:l=!1,...c}=e,v=s.useRef(null),i=E(n,H(r=>{v.current=r},e.as===void 0||e.as===s.Fragment)),p=s.useRef(null),$=s.useRef(null),d=s.useReducer(_,{disclosureState:l?0:1,linkedPanel:!1,buttonRef:$,panelRef:p,buttonId:null,panelId:null}),[{disclosureState:m,buttonId:g},b]=d,h=C(r=>{b({type:1});let a=V(v);if(!a||!g)return;let o=(()=>r?r instanceof HTMLElement?r:r.current instanceof HTMLElement?r.current:a.getElementById(g):a.getElementById(g))();o==null||o.focus()}),y=s.useMemo(()=>({close:h}),[h]),u=s.useMemo(()=>({open:m===0,close:h}),[m,h]),t={ref:i};return x.createElement(D.Provider,{value:d},x.createElement(T.Provider,{value:y},x.createElement(A,{value:S(m,{0:R.Open,1:R.Closed})},I({ourProps:t,theirProps:c,slot:u,defaultTag:ee,name:"Disclosure"}))))}let re="button";function ae(e,n){let l=M(),{id:c=`headlessui-disclosure-button-${l}`,...v}=e,[i,p]=z("Disclosure.Button"),$=J(),d=$===null?!1:$===i.panelId,m=s.useRef(null),g=E(m,n,d?null:i.buttonRef);s.useEffect(()=>{if(!d)return p({type:2,buttonId:c}),()=>{p({type:2,buttonId:null})}},[c,p,d]);let b=C(a=>{var o;if(d){if(i.disclosureState===1)return;switch(a.key){case P.Space:case P.Enter:a.preventDefault(),a.stopPropagation(),p({type:0}),(o=i.buttonRef.current)==null||o.focus();break}}else switch(a.key){case P.Space:case P.Enter:a.preventDefault(),a.stopPropagation(),p({type:0});break}}),h=C(a=>{switch(a.key){case P.Space:a.preventDefault();break}}),y=C(a=>{var o;W(a.currentTarget)||e.disabled||(d?(p({type:0}),(o=i.buttonRef.current)==null||o.focus()):p({type:0}))}),u=s.useMemo(()=>({open:i.disclosureState===0}),[i]),t=K(e,m),r=d?{ref:g,type:t,onKeyDown:b,onClick:y}:{ref:g,id:c,type:t,"aria-expanded":i.disclosureState===0,"aria-controls":i.linkedPanel?i.panelId:void 0,onKeyDown:b,onKeyUp:h,onClick:y};return I({ourProps:r,theirProps:v,slot:u,defaultTag:re,name:"Disclosure.Button"})}let ne="div",se=L.RenderStrategy|L.Static;function ie(e,n){let l=M(),{id:c=`headlessui-disclosure-panel-${l}`,...v}=e,[i,p]=z("Disclosure.Panel"),{close:$}=B("Disclosure.Panel"),d=E(n,i.panelRef,y=>{Q(()=>p({type:y?4:5}))});s.useEffect(()=>(p({type:3,panelId:c}),()=>{p({type:3,panelId:null})}),[c,p]);let m=N(),g=(()=>m!==null?(m&R.Open)===R.Open:i.disclosureState===0)(),b=s.useMemo(()=>({open:i.disclosureState===0,close:$}),[i,$]),h={ref:d,id:c};return x.createElement(j.Provider,{value:i.panelId},I({ourProps:h,theirProps:v,slot:b,defaultTag:ne,features:se,visible:g,name:"Disclosure.Panel"}))}let oe=k(te),le=k(ae),ue=k(ie),ve=Object.assign(oe,{Button:le,Panel:ue});var q={exports:{}};(function(e,n){(function(l,c){typeof G=="function"?e.exports=c():l.pluralize=c()})(F,function(){var l=[],c=[],v={},i={},p={};function $(t){return typeof t=="string"?new RegExp("^"+t+"$","i"):t}function d(t,r){return t===r?r:t===t.toLowerCase()?r.toLowerCase():t===t.toUpperCase()?r.toUpperCase():t[0]===t[0].toUpperCase()?r.charAt(0).toUpperCase()+r.substr(1).toLowerCase():r.toLowerCase()}function m(t,r){return t.replace(/\$(\d{1,2})/g,function(a,o){return r[o]||""})}function g(t,r){return t.replace(r[0],function(a,o){var f=m(r[1],arguments);return d(a===""?t[o-1]:a,f)})}function b(t,r,a){if(!t.length||v.hasOwnProperty(t))return r;for(var o=a.length;o--;){var f=a[o];if(f[0].test(r))return g(r,f)}return r}function h(t,r,a){return function(o){var f=o.toLowerCase();return r.hasOwnProperty(f)?d(o,f):t.hasOwnProperty(f)?d(o,t[f]):b(f,o,a)}}function y(t,r,a,o){return function(f){var w=f.toLowerCase();return r.hasOwnProperty(w)?!0:t.hasOwnProperty(w)?!1:b(w,w,a)===w}}function u(t,r,a){var o=r===1?u.singular(t):u.plural(t);return(a?r+" ":"")+o}return u.plural=h(p,i,l),u.isPlural=y(p,i,l),u.singular=h(i,p,c),u.isSingular=y(i,p,c),u.addPluralRule=function(t,r){l.push([$(t),r])},u.addSingularRule=function(t,r){c.push([$(t),r])},u.addUncountableRule=function(t){if(typeof t=="string"){v[t.toLowerCase()]=!0;return}u.addPluralRule(t,"$0"),u.addSingularRule(t,"$0")},u.addIrregularRule=function(t,r){r=r.toLowerCase(),t=t.toLowerCase(),p[t]=r,i[r]=t},[["I","we"],["me","us"],["he","they"],["she","they"],["them","them"],["myself","ourselves"],["yourself","yourselves"],["itself","themselves"],["herself","themselves"],["himself","themselves"],["themself","themselves"],["is","are"],["was","were"],["has","have"],["this","these"],["that","those"],["echo","echoes"],["dingo","dingoes"],["volcano","volcanoes"],["tornado","tornadoes"],["torpedo","torpedoes"],["genus","genera"],["viscus","viscera"],["stigma","stigmata"],["stoma","stomata"],["dogma","dogmata"],["lemma","lemmata"],["schema","schemata"],["anathema","anathemata"],["ox","oxen"],["axe","axes"],["die","dice"],["yes","yeses"],["foot","feet"],["eave","eaves"],["goose","geese"],["tooth","teeth"],["quiz","quizzes"],["human","humans"],["proof","proofs"],["carve","carves"],["valve","valves"],["looey","looies"],["thief","thieves"],["groove","grooves"],["pickaxe","pickaxes"],["passerby","passersby"]].forEach(function(t){return u.addIrregularRule(t[0],t[1])}),[[/s?$/i,"s"],[/[^\u0000-\u007F]$/i,"$0"],[/([^aeiou]ese)$/i,"$1"],[/(ax|test)is$/i,"$1es"],[/(alias|[^aou]us|t[lm]as|gas|ris)$/i,"$1es"],[/(e[mn]u)s?$/i,"$1s"],[/([^l]ias|[aeiou]las|[ejzr]as|[iu]am)$/i,"$1"],[/(alumn|syllab|vir|radi|nucle|fung|cact|stimul|termin|bacill|foc|uter|loc|strat)(?:us|i)$/i,"$1i"],[/(alumn|alg|vertebr)(?:a|ae)$/i,"$1ae"],[/(seraph|cherub)(?:im)?$/i,"$1im"],[/(her|at|gr)o$/i,"$1oes"],[/(agend|addend|millenni|dat|extrem|bacteri|desiderat|strat|candelabr|errat|ov|symposi|curricul|automat|quor)(?:a|um)$/i,"$1a"],[/(apheli|hyperbat|periheli|asyndet|noumen|phenomen|criteri|organ|prolegomen|hedr|automat)(?:a|on)$/i,"$1a"],[/sis$/i,"ses"],[/(?:(kni|wi|li)fe|(ar|l|ea|eo|oa|hoo)f)$/i,"$1$2ves"],[/([^aeiouy]|qu)y$/i,"$1ies"],[/([^ch][ieo][ln])ey$/i,"$1ies"],[/(x|ch|ss|sh|zz)$/i,"$1es"],[/(matr|cod|mur|sil|vert|ind|append)(?:ix|ex)$/i,"$1ices"],[/\b((?:tit)?m|l)(?:ice|ouse)$/i,"$1ice"],[/(pe)(?:rson|ople)$/i,"$1ople"],[/(child)(?:ren)?$/i,"$1ren"],[/eaux$/i,"$0"],[/m[ae]n$/i,"men"],["thou","you"]].forEach(function(t){return u.addPluralRule(t[0],t[1])}),[[/s$/i,""],[/(ss)$/i,"$1"],[/(wi|kni|(?:after|half|high|low|mid|non|night|[^\w]|^)li)ves$/i,"$1fe"],[/(ar|(?:wo|[ae])l|[eo][ao])ves$/i,"$1f"],[/ies$/i,"y"],[/\b([pl]|zomb|(?:neck|cross)?t|coll|faer|food|gen|goon|group|lass|talk|goal|cut)ies$/i,"$1ie"],[/\b(mon|smil)ies$/i,"$1ey"],[/\b((?:tit)?m|l)ice$/i,"$1ouse"],[/(seraph|cherub)im$/i,"$1"],[/(x|ch|ss|sh|zz|tto|go|cho|alias|[^aou]us|t[lm]as|gas|(?:her|at|gr)o|[aeiou]ris)(?:es)?$/i,"$1"],[/(analy|diagno|parenthe|progno|synop|the|empha|cri|ne)(?:sis|ses)$/i,"$1sis"],[/(movie|twelve|abuse|e[mn]u)s$/i,"$1"],[/(test)(?:is|es)$/i,"$1is"],[/(alumn|syllab|vir|radi|nucle|fung|cact|stimul|termin|bacill|foc|uter|loc|strat)(?:us|i)$/i,"$1us"],[/(agend|addend|millenni|dat|extrem|bacteri|desiderat|strat|candelabr|errat|ov|symposi|curricul|quor)a$/i,"$1um"],[/(apheli|hyperbat|periheli|asyndet|noumen|phenomen|criteri|organ|prolegomen|hedr|automat)a$/i,"$1on"],[/(alumn|alg|vertebr)ae$/i,"$1a"],[/(cod|mur|sil|vert|ind)ices$/i,"$1ex"],[/(matr|append)ices$/i,"$1ix"],[/(pe)(rson|ople)$/i,"$1rson"],[/(child)ren$/i,"$1"],[/(eau)x?$/i,"$1"],[/men$/i,"man"]].forEach(function(t){return u.addSingularRule(t[0],t[1])}),["adulthood","advice","agenda","aid","aircraft","alcohol","ammo","analytics","anime","athletics","audio","bison","blood","bream","buffalo","butter","carp","cash","chassis","chess","clothing","cod","commerce","cooperation","corps","debris","diabetes","digestion","elk","energy","equipment","excretion","expertise","firmware","flounder","fun","gallows","garbage","graffiti","hardware","headquarters","health","herpes","highjinks","homework","housework","information","jeans","justice","kudos","labour","literature","machinery","mackerel","mail","media","mews","moose","music","mud","manga","news","only","personnel","pike","plankton","pliers","police","pollution","premises","rain","research","rice","salmon","scissors","series","sewage","shambles","shrimp","software","species","staff","swine","tennis","traffic","transportation","trout","tuna","wealth","welfare","whiting","wildebeest","wildlife","you",/pok[eé]mon$/i,/[^aeiou]ese$/i,/deer$/i,/fish$/i,/measles$/i,/o[iu]s$/i,/pox$/i,/sheep$/i].forEach(u.addUncountableRule),u})})(q);var ce=q.exports;const be=U(ce);function pe({title:e,titleId:n,...l},c){return s.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor","aria-hidden":"true",ref:c,"aria-labelledby":n},l),e?s.createElement("title",{id:n},e):null,s.createElement("path",{fillRule:"evenodd",d:"M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm3 10.5a.75.75 0 000-1.5H9a.75.75 0 000 1.5h6z",clipRule:"evenodd"}))}const de=s.forwardRef(pe),ye=de;function fe({title:e,titleId:n,...l},c){return s.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor","aria-hidden":"true",ref:c,"aria-labelledby":n},l),e?s.createElement("title",{id:n},e):null,s.createElement("path",{fillRule:"evenodd",d:"M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 9a.75.75 0 00-1.5 0v2.25H9a.75.75 0 000 1.5h2.25V15a.75.75 0 001.5 0v-2.25H15a.75.75 0 000-1.5h-2.25V9z",clipRule:"evenodd"}))}const me=s.forwardRef(fe),we=me;export{ye as M,we as P,be as p,ve as v};

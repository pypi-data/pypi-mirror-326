(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[4319],{23374:(e,n,t)=>{"use strict";t.d(n,{A:()=>i});var c=t(40991),o=t(53350),a=t(71347),r=t(90055),l=function(e,n){return o.createElement(r.A,(0,c.A)({},e,{ref:n,icon:a.A}))};const i=o.forwardRef(l)},57849:(e,n,t)=>{"use strict";t.d(n,{A:()=>i});var c=t(40991),o=t(53350),a=t(5578),r=t(90055),l=function(e,n){return o.createElement(r.A,(0,c.A)({},e,{ref:n,icon:a.A}))};const i=o.forwardRef(l)},42175:(e,n,t)=>{"use strict";t.d(n,{A:()=>p});var c=t(92509),o=t(48977),a=t.n(o),r=t(53350),l=t(48512),i=t(66625),s=t(66413),u=t(51146);const p=function(e,n){var t;u.A&&((0,s.Tn)(e)||console.error("useThrottleFn expected parameter is a function, got ".concat(typeof e)));var o=(0,l.A)(e),p=null!==(t=null===n||void 0===n?void 0:n.wait)&&void 0!==t?t:1e3,d=(0,r.useMemo)((function(){return a()((function(){for(var e=[],n=0;n<arguments.length;n++)e[n]=arguments[n];return o.current.apply(o,(0,c.fX)([],(0,c.zs)(e),!1))}),p,n)}),[]);return(0,i.A)((function(){d.cancel()})),{run:d,cancel:d.cancel,flush:d.flush}}},24034:(e,n,t)=>{"use strict";t.d(n,{A:()=>P});var c=t(53350),o=t(33310),a=t(62097),r=t.n(a),l=t(5596),i=t(79876),s=t(22028),u=t(12510),p=t(79442),d=t(52110),f=t(52335),v=t(59036),g=t(10582),m=t(43),y=t(45762),h=t(14275);const b=(0,h.OF)("Popconfirm",(e=>(e=>{const{componentCls:n,iconCls:t,antCls:c,zIndexPopup:o,colorText:a,colorWarning:r,marginXXS:l,marginXS:i,fontSize:s,fontWeightStrong:u,colorTextHeading:p}=e;return{[n]:{zIndex:o,[`&${c}-popover`]:{fontSize:s},[`${n}-message`]:{marginBottom:i,display:"flex",flexWrap:"nowrap",alignItems:"start",[`> ${n}-message-icon ${t}`]:{color:r,fontSize:s,lineHeight:1,marginInlineEnd:i},[`${n}-title`]:{fontWeight:u,color:p,"&:only-child":{fontWeight:"normal"}},[`${n}-description`]:{marginTop:l,color:a}},[`${n}-buttons`]:{textAlign:"end",whiteSpace:"nowrap",button:{marginInlineStart:i}}}}})(e)),(e=>{const{zIndexPopupBase:n}=e;return{zIndexPopup:n+60}}),{resetStyle:!1});var O=function(e,n){var t={};for(var c in e)Object.prototype.hasOwnProperty.call(e,c)&&n.indexOf(c)<0&&(t[c]=e[c]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var o=0;for(c=Object.getOwnPropertySymbols(e);o<c.length;o++)n.indexOf(c[o])<0&&Object.prototype.propertyIsEnumerable.call(e,c[o])&&(t[c[o]]=e[c[o]])}return t};const N=e=>{const{prefixCls:n,okButtonProps:t,cancelButtonProps:a,title:r,description:l,cancelText:i,okText:u,okType:y="primary",icon:h=c.createElement(o.A,null),showCancel:b=!0,close:O,onConfirm:N,onCancel:j,onPopupClick:w}=e,{getPrefixCls:x}=c.useContext(s.QO),[S]=(0,g.A)("Popconfirm",m.A.Popconfirm),P=(0,d.b)(r),C=(0,d.b)(l);return c.createElement("div",{className:`${n}-inner-content`,onClick:w},c.createElement("div",{className:`${n}-message`},h&&c.createElement("span",{className:`${n}-message-icon`},h),c.createElement("div",{className:`${n}-message-text`},P&&c.createElement("div",{className:`${n}-title`},P),C&&c.createElement("div",{className:`${n}-description`},C))),c.createElement("div",{className:`${n}-buttons`},b&&c.createElement(f.Ay,Object.assign({onClick:j,size:"small"},a),i||(null===S||void 0===S?void 0:S.cancelText)),c.createElement(p.A,{buttonProps:Object.assign(Object.assign({size:"small"},(0,v.DU)(y)),t),actionFn:N,close:O,prefixCls:x("btn"),quitOnNullishReturnValue:!0,emitEvent:!0},u||(null===S||void 0===S?void 0:S.okText))))},j=e=>{const{prefixCls:n,placement:t,className:o,style:a}=e,l=O(e,["prefixCls","placement","className","style"]),{getPrefixCls:i}=c.useContext(s.QO),u=i("popconfirm",n),[p]=b(u);return p(c.createElement(y.Ay,{placement:t,className:r()(u,o),style:a,content:c.createElement(N,Object.assign({prefixCls:u},l))}))};var w=function(e,n){var t={};for(var c in e)Object.prototype.hasOwnProperty.call(e,c)&&n.indexOf(c)<0&&(t[c]=e[c]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var o=0;for(c=Object.getOwnPropertySymbols(e);o<c.length;o++)n.indexOf(c[o])<0&&Object.prototype.propertyIsEnumerable.call(e,c[o])&&(t[c[o]]=e[c[o]])}return t};const x=c.forwardRef(((e,n)=>{var t,a,p,d,f,v;const{prefixCls:g,placement:m="top",trigger:y="click",okType:h="primary",icon:O=c.createElement(o.A,null),children:j,overlayClassName:x,onOpenChange:S,onVisibleChange:P,overlayStyle:C,styles:E,classNames:A}=e,k=w(e,["prefixCls","placement","trigger","okType","icon","children","overlayClassName","onOpenChange","onVisibleChange","overlayStyle","styles","classNames"]),{getPrefixCls:L,popconfirm:I}=c.useContext(s.QO),[T,$]=(0,l.A)(!1,{value:null!==(t=e.open)&&void 0!==t?t:e.visible,defaultValue:null!==(a=e.defaultOpen)&&void 0!==a?a:e.defaultVisible}),z=(e,n)=>{$(e,!0),null===P||void 0===P||P(e),null===S||void 0===S||S(e,n)},D=L("popconfirm",g),W=r()(D,x,null===(p=null===I||void 0===I?void 0:I.classNames)||void 0===p?void 0:p.root,null===A||void 0===A?void 0:A.root),V=r()(null===(d=null===I||void 0===I?void 0:I.classNames)||void 0===d?void 0:d.body,null===A||void 0===A?void 0:A.body),[_]=b(D);return _(c.createElement(u.A,Object.assign({},(0,i.A)(k,["title"]),{trigger:y,placement:m,onOpenChange:(n,t)=>{const{disabled:c=!1}=e;c||z(n,t)},open:T,ref:n,classNames:{root:W,body:V},styles:{root:Object.assign(Object.assign(Object.assign(Object.assign({},null===(f=null===I||void 0===I?void 0:I.styles)||void 0===f?void 0:f.root),null===I||void 0===I?void 0:I.style),C),null===E||void 0===E?void 0:E.root),body:Object.assign(Object.assign({},null===(v=null===I||void 0===I?void 0:I.styles)||void 0===v?void 0:v.body),null===E||void 0===E?void 0:E.body)},content:c.createElement(N,Object.assign({okType:h,icon:O},e,{prefixCls:D,close:e=>{z(!1,e)},onConfirm:n=>{var t;return null===(t=e.onConfirm)||void 0===t?void 0:t.call(void 0,n)},onCancel:n=>{var t;z(!1,n),null===(t=e.onCancel)||void 0===t||t.call(void 0,n)}})),"data-popover-inject":!0}),j))})),S=x;S._InternalPanelDoNotUseOrYouWillBeFired=j;const P=S},48977:(e,n,t)=>{var c=t(2174),o=t(42366);e.exports=function(e,n,t){var a=!0,r=!0;if("function"!=typeof e)throw new TypeError("Expected a function");return o(t)&&(a="leading"in t?!!t.leading:a,r="trailing"in t?!!t.trailing:r),c(e,n,{leading:a,maxWait:n,trailing:r})}},61245:(e,n,t)=>{"use strict";t.d(n,{A:()=>C});var c=t(44743),o=t(94835),a=t(57362),r=t(53350),l=t(40991);function i(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var c=Object.getOwnPropertySymbols(e);n&&(c=c.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,c)}return t}function s(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?i(Object(t),!0).forEach((function(n){(0,a.A)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):i(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var u={};function p(e){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},t=arguments.length>2?arguments[2]:void 0;return function(e){if(0===e.length||1===e.length)return e;var n=e.join(".");return u[n]||(u[n]=function(e){var n=e.length;return 0===n||1===n?e:2===n?[e[0],e[1],"".concat(e[0],".").concat(e[1]),"".concat(e[1],".").concat(e[0])]:3===n?[e[0],e[1],e[2],"".concat(e[0],".").concat(e[1]),"".concat(e[0],".").concat(e[2]),"".concat(e[1],".").concat(e[0]),"".concat(e[1],".").concat(e[2]),"".concat(e[2],".").concat(e[0]),"".concat(e[2],".").concat(e[1]),"".concat(e[0],".").concat(e[1],".").concat(e[2]),"".concat(e[0],".").concat(e[2],".").concat(e[1]),"".concat(e[1],".").concat(e[0],".").concat(e[2]),"".concat(e[1],".").concat(e[2],".").concat(e[0]),"".concat(e[2],".").concat(e[0],".").concat(e[1]),"".concat(e[2],".").concat(e[1],".").concat(e[0])]:n>=4?[e[0],e[1],e[2],e[3],"".concat(e[0],".").concat(e[1]),"".concat(e[0],".").concat(e[2]),"".concat(e[0],".").concat(e[3]),"".concat(e[1],".").concat(e[0]),"".concat(e[1],".").concat(e[2]),"".concat(e[1],".").concat(e[3]),"".concat(e[2],".").concat(e[0]),"".concat(e[2],".").concat(e[1]),"".concat(e[2],".").concat(e[3]),"".concat(e[3],".").concat(e[0]),"".concat(e[3],".").concat(e[1]),"".concat(e[3],".").concat(e[2]),"".concat(e[0],".").concat(e[1],".").concat(e[2]),"".concat(e[0],".").concat(e[1],".").concat(e[3]),"".concat(e[0],".").concat(e[2],".").concat(e[1]),"".concat(e[0],".").concat(e[2],".").concat(e[3]),"".concat(e[0],".").concat(e[3],".").concat(e[1]),"".concat(e[0],".").concat(e[3],".").concat(e[2]),"".concat(e[1],".").concat(e[0],".").concat(e[2]),"".concat(e[1],".").concat(e[0],".").concat(e[3]),"".concat(e[1],".").concat(e[2],".").concat(e[0]),"".concat(e[1],".").concat(e[2],".").concat(e[3]),"".concat(e[1],".").concat(e[3],".").concat(e[0]),"".concat(e[1],".").concat(e[3],".").concat(e[2]),"".concat(e[2],".").concat(e[0],".").concat(e[1]),"".concat(e[2],".").concat(e[0],".").concat(e[3]),"".concat(e[2],".").concat(e[1],".").concat(e[0]),"".concat(e[2],".").concat(e[1],".").concat(e[3]),"".concat(e[2],".").concat(e[3],".").concat(e[0]),"".concat(e[2],".").concat(e[3],".").concat(e[1]),"".concat(e[3],".").concat(e[0],".").concat(e[1]),"".concat(e[3],".").concat(e[0],".").concat(e[2]),"".concat(e[3],".").concat(e[1],".").concat(e[0]),"".concat(e[3],".").concat(e[1],".").concat(e[2]),"".concat(e[3],".").concat(e[2],".").concat(e[0]),"".concat(e[3],".").concat(e[2],".").concat(e[1]),"".concat(e[0],".").concat(e[1],".").concat(e[2],".").concat(e[3]),"".concat(e[0],".").concat(e[1],".").concat(e[3],".").concat(e[2]),"".concat(e[0],".").concat(e[2],".").concat(e[1],".").concat(e[3]),"".concat(e[0],".").concat(e[2],".").concat(e[3],".").concat(e[1]),"".concat(e[0],".").concat(e[3],".").concat(e[1],".").concat(e[2]),"".concat(e[0],".").concat(e[3],".").concat(e[2],".").concat(e[1]),"".concat(e[1],".").concat(e[0],".").concat(e[2],".").concat(e[3]),"".concat(e[1],".").concat(e[0],".").concat(e[3],".").concat(e[2]),"".concat(e[1],".").concat(e[2],".").concat(e[0],".").concat(e[3]),"".concat(e[1],".").concat(e[2],".").concat(e[3],".").concat(e[0]),"".concat(e[1],".").concat(e[3],".").concat(e[0],".").concat(e[2]),"".concat(e[1],".").concat(e[3],".").concat(e[2],".").concat(e[0]),"".concat(e[2],".").concat(e[0],".").concat(e[1],".").concat(e[3]),"".concat(e[2],".").concat(e[0],".").concat(e[3],".").concat(e[1]),"".concat(e[2],".").concat(e[1],".").concat(e[0],".").concat(e[3]),"".concat(e[2],".").concat(e[1],".").concat(e[3],".").concat(e[0]),"".concat(e[2],".").concat(e[3],".").concat(e[0],".").concat(e[1]),"".concat(e[2],".").concat(e[3],".").concat(e[1],".").concat(e[0]),"".concat(e[3],".").concat(e[0],".").concat(e[1],".").concat(e[2]),"".concat(e[3],".").concat(e[0],".").concat(e[2],".").concat(e[1]),"".concat(e[3],".").concat(e[1],".").concat(e[0],".").concat(e[2]),"".concat(e[3],".").concat(e[1],".").concat(e[2],".").concat(e[0]),"".concat(e[3],".").concat(e[2],".").concat(e[0],".").concat(e[1]),"".concat(e[3],".").concat(e[2],".").concat(e[1],".").concat(e[0])]:void 0}(e)),u[n]}(e.filter((function(e){return"token"!==e}))).reduce((function(e,n){return s(s({},e),t[n])}),n)}function d(e){return e.join(" ")}function f(e){var n=e.node,t=e.stylesheet,c=e.style,o=void 0===c?{}:c,a=e.useInlineStyles,i=e.key,u=n.properties,v=n.type,g=n.tagName,m=n.value;if("text"===v)return m;if(g){var y,h=function(e,n){var t=0;return function(c){return t+=1,c.map((function(c,o){return f({node:c,stylesheet:e,useInlineStyles:n,key:"code-segment-".concat(t,"-").concat(o)})}))}}(t,a);if(a){var b=Object.keys(t).reduce((function(e,n){return n.split(".").forEach((function(n){e.includes(n)||e.push(n)})),e}),[]),O=u.className&&u.className.includes("token")?["token"]:[],N=u.className&&O.concat(u.className.filter((function(e){return!b.includes(e)})));y=s(s({},u),{},{className:d(N)||void 0,style:p(u.className,Object.assign({},u.style,o),t)})}else y=s(s({},u),{},{className:d(u.className)});var j=h(n.children);return r.createElement(g,(0,l.A)({key:i},y),j)}}const v=function(e,n){return-1!==e.listLanguages().indexOf(n)};var g=["language","children","style","customStyle","codeTagProps","useInlineStyles","showLineNumbers","showInlineLineNumbers","startingLineNumber","lineNumberContainerStyle","lineNumberStyle","wrapLines","wrapLongLines","lineProps","renderer","PreTag","CodeTag","code","astGenerator"];function m(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var c=Object.getOwnPropertySymbols(e);n&&(c=c.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,c)}return t}function y(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?m(Object(t),!0).forEach((function(n){(0,a.A)(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):m(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}var h=/\n/g;function b(e){var n=e.codeString,t=e.codeStyle,c=e.containerStyle,o=void 0===c?{float:"left",paddingRight:"10px"}:c,a=e.numberStyle,l=void 0===a?{}:a,i=e.startingLineNumber;return r.createElement("code",{style:Object.assign({},t,o)},function(e){var n=e.lines,t=e.startingLineNumber,c=e.style;return n.map((function(e,n){var o=n+t;return r.createElement("span",{key:"line-".concat(n),className:"react-syntax-highlighter-line-number",style:"function"===typeof c?c(o):c},"".concat(o,"\n"))}))}({lines:n.replace(/\n$/,"").split("\n"),style:l,startingLineNumber:i}))}function O(e,n){return{type:"element",tagName:"span",properties:{key:"line-number--".concat(e),className:["comment","linenumber","react-syntax-highlighter-line-number"],style:n},children:[{type:"text",value:e}]}}function N(e,n,t){var c,o={display:"inline-block",minWidth:(c=t,"".concat(c.toString().length,".25em")),paddingRight:"1em",textAlign:"right",userSelect:"none"},a="function"===typeof e?e(n):e;return y(y({},o),a)}function j(e){var n=e.children,t=e.lineNumber,c=e.lineNumberStyle,a=e.largestLineNumber,r=e.showInlineLineNumbers,l=e.lineProps,i=void 0===l?{}:l,s=e.className,u=void 0===s?[]:s,p=e.showLineNumbers,d=e.wrapLongLines,f=e.wrapLines,v=void 0!==f&&f?y({},"function"===typeof i?i(t):i):{};if(v.className=v.className?[].concat((0,o.A)(v.className.trim().split(/\s+/)),(0,o.A)(u)):u,t&&r){var g=N(c,t,a);n.unshift(O(t,g))}return d&p&&(v.style=y({display:"flex"},v.style)),{type:"element",tagName:"span",properties:v,children:n}}function w(e){for(var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[],t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],c=0;c<e.length;c++){var a=e[c];if("text"===a.type)t.push(j({children:[a],className:(0,o.A)(new Set(n))}));else if(a.children){var r=n.concat(a.properties.className);w(a.children,r).forEach((function(e){return t.push(e)}))}}return t}function x(e,n,t,c,o,a,r,l,i){var s,u=w(e.value),p=[],d=-1,f=0;function v(e,a){var s=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[];return n||s.length>0?function(e,a){return j({children:e,lineNumber:a,lineNumberStyle:l,largestLineNumber:r,showInlineLineNumbers:o,lineProps:t,className:arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],showLineNumbers:c,wrapLongLines:i,wrapLines:n})}(e,a,s):function(e,n){if(c&&n&&o){var t=N(l,n,r);e.unshift(O(n,t))}return e}(e,a)}for(var g=function(){var e=u[f],n=e.children[0].value;if(n.match(h)){var t=n.split("\n");t.forEach((function(n,o){var r=c&&p.length+a,l={type:"text",value:"".concat(n,"\n")};if(0===o){var i=v(u.slice(d+1,f).concat(j({children:[l],className:e.properties.className})),r);p.push(i)}else if(o===t.length-1){var s=u[f+1]&&u[f+1].children&&u[f+1].children[0],g={type:"text",value:"".concat(n)};if(s){var m=j({children:[g],className:e.properties.className});u.splice(f+1,0,m)}else{var y=v([g],r,e.properties.className);p.push(y)}}else{var h=v([l],r,e.properties.className);p.push(h)}})),d=f}f++};f<u.length;)g();if(d!==u.length-1){var m=u.slice(d+1,u.length);if(m&&m.length){var y=v(m,c&&p.length+a);p.push(y)}}return n?p:(s=[]).concat.apply(s,p)}function S(e){var n=e.rows,t=e.stylesheet,c=e.useInlineStyles;return n.map((function(e,n){return f({node:e,stylesheet:t,useInlineStyles:c,key:"code-segement".concat(n)})}))}function P(e){return e&&"undefined"!==typeof e.highlightAuto}function C(e,n){return function(t){var o=t.language,a=t.children,l=t.style,i=void 0===l?n:l,s=t.customStyle,u=void 0===s?{}:s,p=t.codeTagProps,d=void 0===p?{className:o?"language-".concat(o):void 0,style:y(y({},i['code[class*="language-"]']),i['code[class*="language-'.concat(o,'"]')])}:p,f=t.useInlineStyles,m=void 0===f||f,h=t.showLineNumbers,O=void 0!==h&&h,N=t.showInlineLineNumbers,j=void 0===N||N,w=t.startingLineNumber,C=void 0===w?1:w,E=t.lineNumberContainerStyle,A=t.lineNumberStyle,k=void 0===A?{}:A,L=t.wrapLines,I=t.wrapLongLines,T=void 0!==I&&I,$=t.lineProps,z=void 0===$?{}:$,D=t.renderer,W=t.PreTag,V=void 0===W?"pre":W,_=t.CodeTag,R=void 0===_?"code":_,B=t.code,F=void 0===B?(Array.isArray(a)?a[0]:a)||"":B,G=t.astGenerator,X=(0,c.A)(t,g);G=G||e;var Q=O?r.createElement(b,{containerStyle:E,codeStyle:d.style||{},numberStyle:k,startingLineNumber:C,codeString:F}):null,H=i.hljs||i['pre[class*="language-"]']||{backgroundColor:"#fff"},U=P(G)?"hljs":"prismjs",q=m?Object.assign({},X,{style:Object.assign({},H,u)}):Object.assign({},X,{className:X.className?"".concat(U," ").concat(X.className):U,style:Object.assign({},u)});if(d.style=y(T?{whiteSpace:"pre-wrap"}:{whiteSpace:"pre"},d.style),!G)return r.createElement(V,q,Q,r.createElement(R,d,F));(void 0===L&&D||T)&&(L=!0),D=D||S;var M=[{type:"text",value:F}],Y=function(e){var n=e.astGenerator,t=e.language,c=e.code,o=e.defaultCodeValue;if(P(n)){var a=v(n,t);return"text"===t?{value:o,language:"text"}:a?n.highlight(t,c):n.highlightAuto(c)}try{return t&&"text"!==t?{value:n.highlight(c,t)}:{value:o}}catch(r){return{value:o}}}({astGenerator:G,language:o,code:F,defaultCodeValue:M});null===Y.language&&(Y.value=M);var J=Y.value.length;1===J&&"text"===Y.value[0].type&&(J=Y.value[0].value.split("\n").length);var K=x(Y,L,z,O,j,C,J+C,k,T);return r.createElement(V,q,r.createElement(R,d,!j&&Q,D({rows:K,stylesheet:i,useInlineStyles:m})))}}}}]);
//# sourceMappingURL=4319.ccb43a21.chunk.js.map
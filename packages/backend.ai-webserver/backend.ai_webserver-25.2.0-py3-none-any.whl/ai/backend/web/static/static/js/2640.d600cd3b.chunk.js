/*! For license information please see 2640.d600cd3b.chunk.js.LICENSE.txt */
"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[2640],{95762:(e,t,n)=>{n.d(t,{A:()=>u});var l=n(72338),r=n(9571),i=n(50128),a=n(46976),o=n.n(a),s=(n(53350),n(60598));const u=e=>{let{title:t,valueLabel:n,percent:a,width:u,strokeColor:d,labelStyle:c,progressStyle:p,size:m="small"}=e;const{token:y}=r.A.useToken(),g="small"===m?y.fontSizeSM:"middle"===m?y.fontSize:y.fontSizeLG;return(0,s.jsxs)(l.A,{style:{padding:1,border:`1px solid ${y.colorBorder}`,borderRadius:3,backgroundColor:y.colorBgContainerDisabled,...o().isNumber(u)||o().isString(u)?{width:u}:{flex:1},...p},direction:"column",align:"stretch",children:[(0,s.jsx)(l.A,{style:{height:"100%",width:`${!a||o().isNaN(a)?0:o().min([a,100])}%`,position:"absolute",left:0,top:0,backgroundColor:null!==d&&void 0!==d?d:y.colorSuccess,opacity:.7,zIndex:0,overflow:"hidden"}}),(0,s.jsxs)(l.A,{direction:"row",justify:"between",children:[(0,s.jsx)(i.A.Text,{style:{fontSize:g,...c},children:t}),(0,s.jsx)(i.A.Text,{style:{fontSize:g,color:o().isNaN(a)||o().isUndefined(a)?y.colorTextDisabled:void 0,...c},children:n})]})]})}},8570:(e,t,n)=>{n.d(t,{Ay:()=>k,r2:()=>j});var l=n(72375),r=n(72338),i=n(71515),a=n(51847),o=n(9571),s=n(65196),u=n(1581),d=n(82919),c=n(78186),p=n(83978),m=n(24798),y=n(52335),g=n(46976),v=n.n(g),h=n(53350),f=n(91788),x=n(60598);const b={string:"ilike",boolean:"=="},S={boolean:[{label:"True",value:"true"},{label:"False",value:"false"}],string:void 0},A={boolean:!0};function j(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"&";const n=v().join(v().map((0,l.LY)(e),(e=>`(${e})`)),t);return n||void 0}const k=e=>{var t;let{filterProperties:n,value:l,onChange:g,defaultValue:j,loading:k,...w}=e;const[C,z]=(0,h.useState)(),T=(0,h.useRef)(null),[_,L]=(0,h.useState)(!1),[N,O]=(0,a.A)({value:l,defaultValue:j,onChange:g}),I=(0,h.useMemo)((()=>{if(void 0===N||""===N)return[];return N.split("&").map((e=>e.trim())).map(((e,t)=>{var l,r;const{property:i,operator:a,value:o}=function(e){const[t,...n]=e.split(/\s+(?=(?:(?:[^"]*"){2})*[^"]*$)/),[l,...r]=n.join(" ").split(/\s+(?=(?:(?:[^"]*"){2})*[^"]*$)/);return{property:t,operator:l,value:r.join(" ").replace(/^"|"$/g,"")}}(e);return{key:t+o,property:i,operator:a,value:o,propertyLabel:(null===(l=v().find(n,(e=>e.key===i)))||void 0===l?void 0:l.propertyLabel)||i,type:(null===(r=v().find(n,(e=>e.key===i)))||void 0===r?void 0:r.type)||"string"}}))}),[N,n]),{t:$}=(0,f.Bd)(),F=v().map(n,(e=>({label:e.propertyLabel,value:e.key,filter:e}))),[E,M]=(0,h.useState)(F[0].filter),{token:V}=o.A.useToken(),[K,P]=(0,h.useState)(!0),[R,D]=(0,h.useState)(!1),B=e=>{if(0===e.length)O(void 0);else{const t=v().map(e,(e=>{const t="string"===e.type?`"${e.value}"`:e.value;return`${e.property} ${e.operator} ${t}`}));O(function(e,t){return e.join(` ${t} `)}(t,"&"))}},X=e=>{var t,n,l;if(v().isEmpty(e))return;if(E.strictSelection||A[E.type]){if(!v().find(E.options||S[E.type],(t=>t.value===e)))return}const r=!(null!==(t=E.rule)&&void 0!==t&&t.validate)||E.rule.validate(e);if(P(r),!r)return;z("");const i=E.defaultOperator||b[E.type],a="ilike"===i||"like"===i?`%${e}%`:`${e}`;var o;o={property:E.key,propertyLabel:E.propertyLabel,operator:i,value:a,label:null===(n=E.options)||void 0===n||null===(l=n.find((t=>t.value===e)))||void 0===l?void 0:l.label,type:E.type},B([...I,o])};return(0,x.jsxs)(r.A,{direction:"column",gap:"xs",style:{flex:1},align:"start",children:[(0,x.jsxs)(s.A.Compact,{children:[(0,x.jsx)(u.A,{popupMatchSelectWidth:!1,options:F,value:E.key,onChange:(e,t)=>{M(v().castArray(t)[0].filter)},onSelect:()=>{var e;null===(e=T.current)||void 0===e||e.focus(),L(!0),P(!0)},showSearch:!0,optionFilterProp:"label"}),(0,x.jsx)(d.A,{title:K||!R?"":null===(t=E.rule)||void 0===t?void 0:t.message,open:!K&&R,color:V.colorError,children:(0,x.jsx)(c.A,{ref:T,value:C,open:_,onDropdownVisibleChange:L,onSelect:X,onChange:e=>{P(!0),z(e)},style:{minWidth:200},options:v().filter(E.options||S[E.type],(e=>{var t;return!C||(null===(t=e.label)||void 0===t?void 0:t.toString().includes(C))})),placeholder:$("propertyFilter.PlaceHolder"),onBlur:()=>{D(!1)},onFocus:()=>{D(!0)},children:(0,x.jsx)(p.A.Search,{onSearch:X,allowClear:!0,status:!K&&R?"error":void 0})})})]}),I.length>0&&(0,x.jsxs)(r.A,{direction:"row",gap:"xs",wrap:"wrap",style:{alignSelf:"stretch"},children:[v().map(I,(e=>{return(0,x.jsxs)(m.A,{closable:!0,onClose:()=>(e=>{const t=I.filter((t=>t.key!==e));B(t)})(e.key),style:{margin:0},children:[e.propertyLabel,": ",(t=e.value,t.replace(/^%|%$/g,""))]},e.key);var t})),I.length>1&&(0,x.jsx)(d.A,{title:$("propertyFilter.ResetFilter"),children:(0,x.jsx)(y.Ay,{size:"small",icon:(0,x.jsx)(i.A,{style:{color:V.colorTextSecondary}}),type:"text",onClick:()=>{B([])}})})]})]})}},42388:(e,t,n)=>{n.d(t,{A:()=>f,s:()=>h});var l=n(72375),r=n(7971),i=n(81530),a=n(72338),o=n(9571),s=n(50128),u=n(82919),d=n(46976),c=n.n(d),p=n(64054),m=n(53350),y=n(60598);const g=e=>{var t,n;let{type:u,value:d,extra:p,opts:m,hideTooltip:g=!1,max:v}=e;const{token:f}=o.A.useToken(),x=(0,i.Nw)(),{mergedResourceSlots:b}=(0,r.Hv)(x||void 0),S=e=>{var t,n,r;return null!==b&&void 0!==b&&null!==(t=b[u])&&void 0!==t&&t.number_format.binary?Number(null===(n=(0,l.Is)(e,"g",3,!0))||void 0===n?void 0:n.numberFixed).toString():((null===b||void 0===b||null===(r=b[u])||void 0===r?void 0:r.number_format.round_length)||0)>0?parseFloat(e).toFixed(2):e};return(0,y.jsxs)(a.A,{direction:"row",gap:"xxs",children:[null!==b&&void 0!==b&&b[u]?(0,y.jsx)(h,{type:u,showTooltip:!g}):u,(0,y.jsxs)(s.A.Text,{children:[S(d),c().isUndefined(v)?null:"Infinity"===v?"~\u221e":`~${S(v)}`]}),(0,y.jsx)(s.A.Text,{type:"secondary",children:(null===b||void 0===b||null===(t=b[u])||void 0===t?void 0:t.display_unit)||""}),"mem"===u&&null!==m&&void 0!==m&&m.shmem&&(null===m||void 0===m?void 0:m.shmem)>0?(0,y.jsxs)(s.A.Text,{type:"secondary",style:{fontSize:f.fontSizeSM},children:["(SHM:"," ",null===(n=(0,l.Is)(m.shmem+"b","g",2,!0))||void 0===n?void 0:n.numberFixed,"GiB)"]}):null,p]})},v=e=>{let{size:t=16,children:n}=e;return(0,y.jsx)("mwc-icon",{style:{"--mdc-icon-size":`${t+2}px`,width:t,height:t},children:n})},h=e=>{var t,n;let{type:l,size:i=16,showIcon:o=!0,showUnit:s=!0,showTooltip:d=!0,...c}=e;const m={cpu:(0,y.jsx)(v,{size:i,children:"developer_board"}),mem:(0,y.jsx)(v,{size:i,children:"memory"}),"cuda.device":"/resources/icons/file_type_cuda.svg","cuda.shares":"/resources/icons/file_type_cuda.svg","rocm.device":"/resources/icons/rocm.svg","tpu.device":(0,y.jsx)(v,{size:i,children:"view_module"}),"ipu.device":(0,y.jsx)(v,{size:i,children:"view_module"}),"atom.device":"/resources/icons/rebel.svg","atom-plus.device":"/resources/icons/rebel.svg","gaudi2.device":"/resources/icons/gaudi.svg","warboy.device":"/resources/icons/furiosa.svg","rngd.device":"/resources/icons/furiosa.svg","hyperaccel-lpu.device":"/resources/icons/npu_generic.svg"},g=null!==(t=m[l])&&void 0!==t?t:(0,y.jsx)(p.A,{}),{mergedResourceSlots:h}=(0,r.Hv)(),f="string"===typeof g?(0,y.jsx)("img",{...c,style:{height:i,alignSelf:"center",...c.style||{}},src:m[l]||"",alt:l}):(0,y.jsx)(a.A,{style:{width:16,height:16},children:g||l});return d?(0,y.jsx)(u.A,{title:(null===(n=h[l])||void 0===n?void 0:n.description)||l,children:f}):(0,y.jsx)(a.A,{style:{pointerEvents:"none"},children:f})},f=m.memo(g)},74325:(e,t,n)=>{n.d(t,{A:()=>y});var l=n(9189),r=n(28567),i=n(9571),a=n(13170),o=n(83978),s=n(92280),u=n(46976),d=n.n(u),c=n(53350),p=n(91788),m=n(60598);const y=e=>{var t;let{open:n,onRequestClose:u,columns:y,hiddenColumnKeys:g,...v}=e;const h=(0,c.useRef)(null),{t:f}=(0,p.Bd)(),{token:x}=i.A.useToken(),b=d().map(y,(e=>{return"string"===typeof e.title?{label:e.title,value:d().toString(e.key)}:"object"===typeof e.title&&"props"in e.title?{label:(t=e.title,c.Children.map(t.props.children,(e=>{if("string"===typeof e)return e}))),value:d().toString(e.key)}:{label:void 0,value:d().toString(e.key)};var t}));return(0,m.jsx)(l.A,{title:f("table.SettingTable"),open:n,destroyOnClose:!0,centered:!0,onOk:()=>{var e;null===(e=h.current)||void 0===e||e.validateFields().then((e=>{u(e)})).catch((()=>{}))},onCancel:()=>{u()},...v,children:(0,m.jsxs)(a.A,{ref:h,preserve:!1,initialValues:{selectedColumnKeys:null===(t=d().map(b,"value"))||void 0===t?void 0:t.filter((e=>!d().includes(g,e)))},layout:"vertical",children:[(0,m.jsx)(a.A.Item,{name:"searchInput",label:f("table.SelectColumnToDisplay"),style:{marginBottom:0},children:(0,m.jsx)(o.A,{prefix:(0,m.jsx)(r.A,{}),style:{marginBottom:x.marginSM},placeholder:f("table.SearchTableColumn")})}),(0,m.jsx)(a.A.Item,{noStyle:!0,shouldUpdate:(e,t)=>e.searchInput!==t.searchInput,children:e=>{let{getFieldValue:t}=e;const n=t("searchInput")?d().toLower(t("searchInput")):void 0,l=d().map(b,(e=>d().toLower(d().toString(e.label)).includes(n||"")?e:{...e,style:{display:"none"}}));return(0,m.jsx)(a.A.Item,{name:"selectedColumnKeys",style:{height:220,overflowY:"auto"},children:(0,m.jsx)(s.A.Group,{options:l,style:{flexDirection:"column"}})})}})]})})}},25669:(e,t,n)=>{n.r(t),n.d(t,{default:()=>r});const l=function(){var e={defaultValue:null,kind:"LocalArgument",name:"filter"},t={defaultValue:null,kind:"LocalArgument",name:"limit"},n={defaultValue:null,kind:"LocalArgument",name:"offset"},l={defaultValue:null,kind:"LocalArgument",name:"order"},r={defaultValue:null,kind:"LocalArgument",name:"status"},i=[{alias:null,args:[{kind:"Variable",name:"filter",variableName:"filter"},{kind:"Variable",name:"limit",variableName:"limit"},{kind:"Variable",name:"offset",variableName:"offset"},{kind:"Variable",name:"order",variableName:"order"},{kind:"Variable",name:"status",variableName:"status"}],concreteType:"AgentSummaryList",kind:"LinkedField",name:"agent_summary_list",plural:!1,selections:[{alias:null,args:null,concreteType:"AgentSummary",kind:"LinkedField",name:"items",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"status",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"architecture",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"available_slots",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"occupied_slots",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"scaling_group",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"schedulable",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"total_count",storageKey:null}],storageKey:null}];return{fragment:{argumentDefinitions:[e,t,n,l,r],kind:"Fragment",metadata:null,name:"AgentSummaryListQuery",selections:i,type:"Queries",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[t,n,e,r,l],kind:"Operation",name:"AgentSummaryListQuery",selections:i},params:{cacheID:"caaf8909248bac69bce5c748e6d28032",id:null,metadata:{},name:"AgentSummaryListQuery",operationKind:"query",text:"query AgentSummaryListQuery(\n  $limit: Int!\n  $offset: Int!\n  $filter: String\n  $status: String\n  $order: String\n) {\n  agent_summary_list(limit: $limit, offset: $offset, filter: $filter, status: $status, order: $order) {\n    items {\n      id\n      status\n      architecture\n      available_slots\n      occupied_slots\n      scaling_group\n      schedulable\n    }\n    total_count\n  }\n}\n"}}}();l.hash="dab7ef4f1205af54a6f80ce0d28098c7";const r=l},54690:(e,t,n)=>{n.d(t,{w4:()=>a});var l=n(46976),r=n.n(l),i=n(53350);n(22018),n(32043);const a=e=>{const[t,n]=(0,i.useState)(e);return{baiPaginationOption:{limit:t.pageSize,first:t.pageSize,offset:t.current>1?(t.current-1)*t.pageSize:0},tablePaginationOption:{pageSize:t.pageSize,current:t.current},setTablePaginationOption:e=>{r().isEqual(e,t)||n((t=>({...t,...e})))}}}},76148:(e,t,n)=>{n.d(t,{a:()=>r});var l=n(39768);const r=e=>{const[t,n]=(0,l.q)(`hiddenColumnKeys.${e}`);return[t,n]}},42640:(e,t,n)=>{n.r(t),n.d(t,{default:()=>V});var l,r=n(72375),i=n(23441),a=n(7971),o=n(54690),s=n(81530),u=n(76148),d=n(95762),c=n(8570),p=n(72338),m=n(42388),y=n(74325),g=n(94495),v=n(67483),h=n(43622),f=n(2667),x=n(53651),b=n(40915),S=n(9571),A=n(50128),j=n(27099),k=n(82919),w=n(52335),C=n(37826),z=n(46976),T=n.n(z),_=n(53350),L=n(91788),N=n(22018),O=n(60598);const I=e=>{let{containerStyle:t,tableProps:z}=e;const{t:I}=(0,L.Bd)(),{token:$}=S.A.useToken(),{mergedResourceSlots:F}=(0,a.Hv)(),[E,{toggle:M}]=(0,b.A)(),[V,K]=(0,_.useTransition)(),[P,R]=(0,_.useTransition)(),[D,B]=(0,_.useTransition)(),[X,q]=(0,_.useState)("ALIVE"),[Q,G]=(0,_.useState)(X),[W,Z]=(0,_.useTransition)(),[H,U]=(0,_.useState)(),{baiPaginationOption:Y,tablePaginationOption:J,setTablePaginationOption:ee}=(0,o.w4)({current:1,pageSize:20}),[te,ne]=(0,_.useState)(),[le,re]=(0,i.Tw)("first"),[ie]=(0,_.useState)("network-only"),{allSftpScalingGroups:ae}=(0,s.Bk)(),{agent_summary_list:oe}=(0,N.useLazyLoadQuery)(void 0!==l?l:l=n(25669),{limit:Y.limit,offset:Y.offset,filter:H,order:te,status:X},{fetchKey:le,fetchPolicy:ie}),se=T().filter(null===oe||void 0===oe?void 0:oe.items,(e=>!T().includes(ae,null===e||void 0===e?void 0:e.scaling_group))),ue=[{title:"#",fixed:"left",render:(e,t,n)=>n+1+(J.current-1)*J.pageSize,showSorterTooltip:!1,rowScope:"row"},{title:(0,O.jsx)(O.Fragment,{children:"ID"}),key:"id",dataIndex:"id",fixed:"left",render:(e,t)=>(0,O.jsx)(p.A,{direction:"column",align:"start",children:(0,O.jsx)(A.A.Text,{children:e})}),sorter:!0},{title:I("agent.Architecture"),key:"architecture",dataIndex:"architecture"},{title:I("agent.Allocation"),key:"allocation",render:(e,t)=>{const n=JSON.parse((null===t||void 0===t?void 0:t.occupied_slots)||"{}"),l=JSON.parse((null===t||void 0===t?void 0:t.available_slots)||"{}");return(0,O.jsx)(p.A,{direction:"column",gap:"xxs",children:T().map(l,((e,t)=>{if("cpu"===t){var i;const e=T().toFinite(T().toNumber(n.cpu)/T().toNumber(l.cpu)*100);return(0,O.jsxs)(p.A,{justify:"between",style:{minWidth:220},children:[(0,O.jsxs)(p.A,{gap:"xxs",children:[(0,O.jsx)(m.s,{type:t},t),(0,O.jsxs)(A.A.Text,{children:[(0,r.Z1)(n.cpu||0,0),"/",(0,r.Z1)(l.cpu||0,0)]}),(0,O.jsx)(A.A.Text,{type:"secondary",style:{fontSize:$.sizeXS},children:null===F||void 0===F||null===(i=F.cpu)||void 0===i?void 0:i.display_unit})]}),(0,O.jsx)(d.A,{percent:e,strokeColor:e>80?$.colorError:$.colorSuccess,width:120,valueLabel:(0,r.Z1)(e,1)+" %"})]},t)}if("mem"===t){var a,o,s,u;const e=T().toFinite(T().toNumber(n.mem)/T().toNumber(l.mem)*100);return(0,O.jsxs)(p.A,{justify:"between",style:{minWidth:220},children:[(0,O.jsxs)(p.A,{gap:"xxs",children:[(0,O.jsx)(m.s,{type:"mem"}),(0,O.jsxs)(A.A.Text,{children:[null!==(a=null===(o=(0,r.Is)(n.mem,"g",0))||void 0===o?void 0:o.numberFixed)&&void 0!==a?a:0,"/",null!==(s=null===(u=(0,r.Is)(l.mem,"g",0))||void 0===u?void 0:u.numberFixed)&&void 0!==s?s:0]}),(0,O.jsx)(A.A.Text,{type:"secondary",style:{fontSize:$.sizeXS},children:"GiB"})]}),(0,O.jsx)(d.A,{percent:e,strokeColor:e>80?$.colorError:$.colorSuccess,width:120,valueLabel:(0,r.Z1)(e,1)+" %"})]},"mem")}if(l[t]){var c;const e=T().toFinite(T().toNumber(n[t])/T().toNumber(l[t])*100);return(0,O.jsxs)(p.A,{justify:"between",style:{minWidth:220},gap:"xxs",children:[(0,O.jsxs)(p.A,{gap:"xxs",children:[(0,O.jsx)(m.s,{type:t},t),(0,O.jsxs)(A.A.Text,{children:[(0,r.Z1)(n[t]||0,2),"/",(0,r.Z1)(l[t],2)]}),(0,O.jsx)(A.A.Text,{type:"secondary",style:{fontSize:$.sizeXS},children:null===F||void 0===F||null===(c=F[t])||void 0===c?void 0:c.display_unit})]}),(0,O.jsx)(d.A,{percent:e,strokeColor:e>80?$.colorError:$.colorSuccess,width:120,valueLabel:(0,r.Z1)(e,1)+" %"})]},t)}}))})}},{title:I("agent.Schedulable"),key:"schedulable",dataIndex:"schedulable",render:e=>(0,O.jsx)(p.A,{justify:"center",children:!0===e?(0,O.jsx)(g.A,{style:{color:$.colorSuccess,fontSize:$.fontSizeXL}}):(0,O.jsx)(v.A,{style:{color:$.colorTextDisabled,fontSize:$.fontSizeXL}})}),sorter:!0}],[de,ce]=(0,u.a)("AgentSummaryList");return(0,O.jsxs)(p.A,{direction:"column",align:"stretch",style:t,children:[(0,O.jsxs)(p.A,{justify:"between",align:"start",gap:"xs",style:{padding:$.paddingXS},wrap:"wrap",children:[(0,O.jsxs)(p.A,{direction:"row",gap:"sm",align:"start",style:{flex:1},wrap:"wrap",children:[(0,O.jsx)(j.A,{options:[{label:I("agent.Connected"),value:"ALIVE"},{label:I("agent.Terminated"),value:"TERMINATED"}],value:V?Q:X,onChange:e=>{G(e),K((()=>{q(e)}))}}),(0,O.jsx)(c.Ay,{filterProperties:[{key:"id",propertyLabel:"ID",type:"string"},{key:"schedulable",propertyLabel:I("agent.Schedulable"),type:"boolean",options:[{label:I("general.Enabled"),value:"true"},{label:I("general.Disabled"),value:"false"}]}],value:H,onChange:e=>{Z((()=>{U(e)}))}})]}),(0,O.jsx)(p.A,{gap:"xs",children:(0,O.jsx)(k.A,{title:I("button.Refresh"),children:(0,O.jsx)(w.Ay,{loading:P,onClick:()=>R((()=>{re()})),icon:(0,O.jsx)(h.A,{})})})})]}),(0,O.jsx)(C.A,{bordered:!0,scroll:{x:"max-content"},rowKey:"id",dataSource:(0,r.tS)(se),showSorterTooltip:!1,columns:T().filter(ue,(e=>!T().includes(de,T().toString(null===e||void 0===e?void 0:e.key)))),pagination:{pageSize:J.pageSize,showSizeChanger:!0,total:null===oe||void 0===oe?void 0:oe.total_count,current:J.current,showTotal:(e,t)=>`${t[0]}-${t[1]} of ${e} items`,pageSizeOptions:["10","20","50"],style:{marginRight:$.marginXS}},onChange:(e,t,n)=>{let{pageSize:l,current:i}=e;B((()=>{T().isNumber(i)&&T().isNumber(l)&&ee({current:i,pageSize:l}),ne((0,r.Wh)(n))}))},loading:{spinning:D||V||W,indicator:(0,O.jsx)(f.A,{})},...z}),(0,O.jsx)(p.A,{justify:"end",style:{padding:$.paddingXXS},children:(0,O.jsx)(w.Ay,{type:"text",icon:(0,O.jsx)(x.A,{}),onClick:()=>{M()}})}),(0,O.jsx)(y.A,{open:E,onRequestClose:e=>{(null===e||void 0===e?void 0:e.selectedColumnKeys)&&ce(T().difference(ue.map((e=>T().toString(e.key))),null===e||void 0===e?void 0:e.selectedColumnKeys)),M()},columns:ue,hiddenColumnKeys:de})]})};var $=n(20418),F=n(91867),E=n(32043);const M=(0,E.withDefault)(E.StringParam,"agent-summary"),V=e=>{const{t:t}=(0,L.Bd)(),[n,l]=(0,E.useQueryParam)("tab",M,{updateType:"replace"}),{token:r}=S.A.useToken();return(0,O.jsx)($.A,{activeTabKey:n,onTabChange:e=>l(e),tabList:[{key:"agent-summary",tab:t("webui.menu.AgentSummary")}],styles:{body:{padding:0,paddingTop:1,overflow:"hidden"}},children:"agent-summary"===n?(0,O.jsx)(_.Suspense,{fallback:(0,O.jsx)(F.A,{active:!0,style:{padding:r.paddingContentVerticalLG}}),children:(0,O.jsx)(I,{containerStyle:{marginLeft:-1,marginRight:-1}})}):null})}},20940:(e,t,n)=>{n.d(t,{A:()=>l});const l={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M696 480H328c-4.4 0-8 3.6-8 8v48c0 4.4 3.6 8 8 8h368c4.4 0 8-3.6 8-8v-48c0-4.4-3.6-8-8-8z"}},{tag:"path",attrs:{d:"M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z"}}]},name:"minus-circle",theme:"outlined"}},67483:(e,t,n)=>{n.d(t,{A:()=>s});var l=n(40991),r=n(53350),i=n(20940),a=n(90055),o=function(e,t){return r.createElement(a.A,(0,l.A)({},e,{ref:t,icon:i.A}))};const s=r.forwardRef(o)},28567:(e,t,n)=>{n.d(t,{A:()=>s});var l=n(40991),r=n(53350),i=n(14334),a=n(90055),o=function(e,t){return r.createElement(a.A,(0,l.A)({},e,{ref:t,icon:i.A}))};const s=r.forwardRef(o)},51847:(e,t,n)=>{n.d(t,{A:()=>s});var l=n(92509),r=n(53350),i=n(66413),a=n(7447);const o=function(){var e=(0,l.zs)((0,r.useState)({}),2)[1];return(0,r.useCallback)((function(){return e({})}),[])};const s=function(e,t){void 0===e&&(e={}),void 0===t&&(t={});var n=t.defaultValue,s=t.defaultValuePropName,u=void 0===s?"defaultValue":s,d=t.valuePropName,c=void 0===d?"value":d,p=t.trigger,m=void 0===p?"onChange":p,y=e[c],g=Object.prototype.hasOwnProperty.call(e,c),v=(0,r.useMemo)((function(){return g?y:Object.prototype.hasOwnProperty.call(e,u)?e[u]:n}),[]),h=(0,r.useRef)(v);g&&(h.current=y);var f=o();return[h.current,(0,a.A)((function(t){for(var n=[],r=1;r<arguments.length;r++)n[r-1]=arguments[r];var a=(0,i.Tn)(t)?t(h.current):t;g||(h.current=a,f()),e[m]&&e[m].apply(e,(0,l.fX)([a],(0,l.zs)(n),!1))}))]}},78186:(e,t,n)=>{n.d(t,{A:()=>h});var l=n(53350),r=n(62097),i=n.n(r),a=n(83531),o=n(79876),s=n(44432),u=n(91970),d=n(22028),c=n(1581);const{Option:p}=c.A;function m(e){return(null===e||void 0===e?void 0:e.type)&&(e.type.isSelectOption||e.type.isSelectOptGroup)}const y=(e,t)=>{var n;const{prefixCls:r,className:u,popupClassName:y,dropdownClassName:g,children:v,dataSource:h}=e,f=(0,a.A)(v);let x;1===f.length&&l.isValidElement(f[0])&&!m(f[0])&&([x]=f);const b=x?()=>x:void 0;let S;S=f.length&&m(f[0])?v:h?h.map((e=>{if(l.isValidElement(e))return e;switch(typeof e){case"string":return l.createElement(p,{key:e,value:e},e);case"object":{const{value:t}=e;return l.createElement(p,{key:t,value:t},e.text)}default:return}})):[];const{getPrefixCls:A}=l.useContext(d.QO),j=A("select",r),[k]=(0,s.YK)("SelectLike",null===(n=e.dropdownStyle)||void 0===n?void 0:n.zIndex);return l.createElement(c.A,Object.assign({ref:t,suffixIcon:null},(0,o.A)(e,["dataSource","dropdownClassName"]),{prefixCls:j,popupClassName:y||g,dropdownStyle:Object.assign(Object.assign({},e.dropdownStyle),{zIndex:k}),className:i()(`${j}-auto-complete`,u),mode:c.A.SECRET_COMBOBOX_MODE_DO_NOT_USE,getInputElement:b}),S)},g=l.forwardRef(y),v=(0,u.A)(g,"dropdownAlign",(e=>(0,o.A)(e,["visible"])));g.Option=p,g._InternalPanelDoNotUseOrYouWillBeFired=v;const h=g},64054:(e,t,n)=>{n.d(t,{A:()=>l});const l=(0,n(60521).A)("Microchip",[["path",{d:"M18 12h2",key:"quuxs7"}],["path",{d:"M18 16h2",key:"zsn3lv"}],["path",{d:"M18 20h2",key:"9x5y9y"}],["path",{d:"M18 4h2",key:"1luxfb"}],["path",{d:"M18 8h2",key:"nxqzg"}],["path",{d:"M4 12h2",key:"1ltxp0"}],["path",{d:"M4 16h2",key:"8a5zha"}],["path",{d:"M4 20h2",key:"27dk57"}],["path",{d:"M4 4h2",key:"10groj"}],["path",{d:"M4 8h2",key:"18vq6w"}],["path",{d:"M8 2a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2h-1.5c-.276 0-.494.227-.562.495a2 2 0 0 1-3.876 0C9.994 2.227 9.776 2 9.5 2z",key:"1681fp"}]])}}]);
//# sourceMappingURL=2640.d600cd3b.chunk.js.map
"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[4244],{91238:(e,i,n)=>{n.d(i,{A:()=>d});var t=n(72338),s=n(96141),l=n(24798),r=n(46976),o=n.n(r),a=n(53350),c=n(60598);const d=e=>{let i,{values:n=[],highlightKeyword:r}=e;return 0===n.length?null:(i=n[0]&&("string"===typeof n[0]||a.isValidElement(n[0]))?n.map((e=>({label:e,color:"blue"}))):n,(0,c.jsx)(t.A,{direction:"row",children:o().map(i,((e,n)=>o().isEmpty(e.label)?null:(0,c.jsx)(l.A,{style:o().last(i)===e?void 0:{margin:0,marginRight:-1},color:e.color,children:o().isUndefined(r)?e.label:(0,c.jsx)(s.A,{keyword:r,children:e.label})},n)))}))}},14244:(e,i,n)=>{n.r(i),n.d(i,{default:()=>y});var t=n(72375),s=n(23441),l=n(73e3),r=n(72338),o=n(50128),a=(n(53350),n(60598));const c=e=>{let{title:i,subtitle:n}=e;return(0,a.jsxs)(r.A,{direction:"column",align:"start",children:[(0,a.jsx)(o.A.Text,{strong:!0,children:i}),n&&(0,a.jsx)(o.A.Text,{type:"secondary",children:n})]})};var d=n(91238),m=n(93143),x=n(31291),A=n(9571),h=n(92351),j=n(56625),f=n(20418),u=n(8227),b=n(24798),g=n(49978),p=n(91788);const y=()=>{const{t:e}=(0,p.Bd)(),{token:i}=A.A.useToken(),n=(0,s.CX)();let{data:o,isLoading:y}=(0,l.nN)({queryKey:["licenseInfo"],queryFn:()=>n.enterprise.getLicense()});o||(o={valid:!1,type:e("information.CannotRead"),licensee:e("information.CannotRead"),key:e("information.CannotRead"),expiration:e("information.CannotRead")});const I={xxl:4,xl:4,lg:2,md:1,sm:1,xs:1};return(0,a.jsxs)(r.A,{direction:"column",align:"stretch",style:{gap:i.margin},children:[(0,a.jsxs)(h.A,{gutter:[i.margin,i.margin],children:[(0,a.jsx)(j.A,{xs:24,xxl:12,children:(0,a.jsx)(f.A,{style:{height:"100%"},children:(0,a.jsxs)(u.A,{title:e("information.Core"),bordered:!0,column:I,children:[(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.ManagerVersion")}),children:(0,a.jsxs)(r.A,{direction:"column",style:{gap:i.marginXXS},align:"start",children:["Backend.AI ",n.managerVersion,(0,a.jsx)(d.A,{values:[e("information.Installation"),n.managerVersion]})]})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.APIVersion")}),children:n.apiVersion})]})})}),(0,a.jsx)(j.A,{xs:24,xxl:12,children:(0,a.jsx)(f.A,{children:(0,a.jsxs)(u.A,{title:e("information.Security"),bordered:!0,column:I,children:[(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.DefaultAdministratorAccountChanged"),subtitle:e("information.DescDefaultAdministratorAccountChanged")}),children:(0,a.jsx)(m.A,{title:"Yes"})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.UsesSSL"),subtitle:e("information.DescUsesSSL")}),children:null!==n&&void 0!==n&&n._config.endpoint.startsWith("https:")?(0,a.jsx)(m.A,{title:"Yes"}):(0,a.jsx)(x.A,{style:{color:i.colorWarning},title:"No"})})]})})})]}),(0,a.jsx)(f.A,{children:(0,a.jsxs)(u.A,{title:e("information.Component"),bordered:!0,column:{xxl:4,xl:2,lg:2,md:1,sm:1,xs:1},children:[(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.DockerVersion"),subtitle:e("information.DescDockerVersion")}),children:(0,a.jsx)(b.A,{children:e("information.Compatible")})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.PostgreSQLVersion"),subtitle:e("information.DescPostgreSQLVersion")}),children:(0,a.jsx)(b.A,{children:e("information.Compatible")})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.ETCDVersion"),subtitle:e("information.DescETCDVersion")}),children:(0,a.jsx)(b.A,{children:e("information.Compatible")})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.RedisVersion"),subtitle:(0,t.y1)(e("information.DescRedisVersion"))}),children:(0,a.jsx)(b.A,{children:e("information.Compatible")})})]})}),(0,a.jsx)(f.A,{children:(0,a.jsx)(g.A,{spinning:y,children:(0,a.jsxs)(u.A,{title:e("information.License"),bordered:!0,column:{xxl:2,xl:2,lg:2,md:1,sm:1,xs:1},children:[(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.IsLicenseValid"),subtitle:e("information.DescIsLicenseValid")}),children:o.valid?(0,a.jsx)(m.A,{}):(0,a.jsx)(x.A,{style:{color:i.colorWarning}})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.LicenseType"),subtitle:(0,t.y1)(e("information.DescLicenseType"))}),children:(0,a.jsx)(b.A,{children:"fixed"===o.type?e("information.FixedLicense"):e("information.DynamicLicense")})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.Licensee"),subtitle:e("information.DescLicensee")}),children:(0,a.jsx)(b.A,{children:o.licensee})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.LicenseKey"),subtitle:e("information.DescLicenseKey")}),children:(0,a.jsx)(b.A,{children:o.key})}),(0,a.jsx)(u.A.Item,{label:(0,a.jsx)(c,{title:e("information.Expiration"),subtitle:e("information.DescExpiration")}),children:(0,a.jsx)(b.A,{children:o.expiration})})]})})})]})}},49412:(e,i,n)=>{n.d(i,{A:()=>t});const t={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M464 720a48 48 0 1096 0 48 48 0 10-96 0zm16-304v184c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V416c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8zm475.7 440l-416-720c-6.2-10.7-16.9-16-27.7-16s-21.6 5.3-27.7 16l-416 720C56 877.4 71.4 904 96 904h832c24.6 0 40-26.6 27.7-48zm-783.5-27.9L512 239.9l339.8 588.2H172.2z"}}]},name:"warning",theme:"outlined"}},31291:(e,i,n)=>{n.d(i,{A:()=>a});var t=n(40991),s=n(53350),l=n(49412),r=n(90055),o=function(e,i){return s.createElement(r.A,(0,t.A)({},e,{ref:i,icon:l.A}))};const a=s.forwardRef(o)},56625:(e,i,n)=>{n.d(i,{A:()=>t});const t=n(14967).A},92351:(e,i,n)=>{n.d(i,{A:()=>t});const t=n(26297).A}}]);
//# sourceMappingURL=4244.3e4d20a4.chunk.js.map
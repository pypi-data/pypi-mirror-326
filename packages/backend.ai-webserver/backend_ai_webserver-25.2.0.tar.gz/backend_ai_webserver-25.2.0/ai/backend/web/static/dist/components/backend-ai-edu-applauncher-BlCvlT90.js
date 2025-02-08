import{_ as i,n as e,e as t,t as n,B as s,b as o,I as a,a as c,F as r,c as l,i as p,ax as h,ay as d,g as u,d as g,k as f}from"./backend-ai-webui-CPozzKCP.js";let b=class extends s{constructor(){super(...arguments),this.webUIShell=Object(),this.clientConfig=Object(),this.client=Object(),this.notification=Object(),this.resources=Object(),this._eduAppNamePrefix=""}static get styles(){return[o,a,c,r,l,p``]}firstUpdated(){this.notification=globalThis.lablupNotification}detectIE(){try{return!!!!document.documentMode||(navigator.userAgent.indexOf("MSIE")>0||navigator.userAgent.indexOf("WOW")>0||navigator.userAgent.indexOf(".NET")>0)}catch(i){const e=i.toString();return console.log(e),!1}}async prepareProjectInformation(){const i=`query { user{ ${["email","groups {name, id}"].join(" ")} } }`,e=await globalThis.backendaiclient.query(i,{});globalThis.backendaiclient.groups=e.user.groups.map((i=>i.name)).sort(),globalThis.backendaiclient.groupIds=e.user.groups.reduce(((i,e)=>(i[e.name]=e.id,i)),{});const t=globalThis.backendaiutils._readRecentProjectGroup();globalThis.backendaiclient.current_group=t||globalThis.backendaiclient.groups[0],globalThis.backendaiclient.current_group_id=()=>globalThis.backendaiclient.groupIds[globalThis.backendaiclient.current_group],console.log("current project:",t)}async launch(i){await this._initClient(i);const e=new URLSearchParams(window.location.search);this.resources={cpu:e.get("cpu"),mem:e.get("mem"),shmem:e.get("shmem"),"cuda.shares":e.get("cuda-shares"),"cuda.device":e.get("cuda-device")};if(await this._token_login()){await this.prepareProjectInformation();const i=window.location.search,e=new URLSearchParams(i),t=e.get("session_id")||null;if(t){const i=e.get("app")||"jupyter";this._openServiceApp(t,i)}else await this._createEduSession()}}async _initClient(i){this.notification=globalThis.lablupNotification;const e=document.querySelector("#webui-shell");if(""===i){const e=localStorage.getItem("backendaiwebui.api_endpoint");null!=e&&(i=e.replace(/^"+|"+$/g,""))}i=i.trim(),this.clientConfig=new h("","",i,"SESSION"),globalThis.backendaiclient=new d(this.clientConfig,"Backend.AI Web UI.");await e._parseConfig("../../config.toml"),globalThis.backendaiclient._config._proxyURL=e.config.wsproxy.proxyURL,await globalThis.backendaiclient.get_manager_version(),globalThis.backendaiclient.ready=!0}async _token_login(){const i=window.location.search,e=new URLSearchParams(i),t=e.get("sToken")||e.get("stoken")||null;null!==t&&(document.cookie=`sToken=${t}; expires=Session; path=/`);const n={};for(const[i,t]of e.entries())"sToken"!==i&&"stoken"!==i&&(n[i]=t);try{if(await globalThis.backendaiclient.check_login())console.log("already logged-in session");else{console.log("logging with (cookie) token...");if(!await globalThis.backendaiclient.token_login(t,n))return this.notification.text=u("eduapi.CannotAuthorizeSessionByToken"),this.notification.show(!0),!1}return!0}catch(i){return this.notification.text=u("eduapi.CannotAuthorizeSessionByToken"),this.notification.show(!0,i),!1}}generateSessionId(){let i="";const e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";for(let t=0;t<8;t++)i+=e.charAt(Math.floor(62*Math.random()));return i+"-session"}async _createEduSession(){this.appLauncher.indicator=await globalThis.lablupIndicator.start(),this._eduAppNamePrefix=globalThis.backendaiclient._config.eduAppNamePrefix;const i=["session_id","name","access_key","status","status_info","service_ports","mounts"];let e;e=globalThis.backendaiclient.supports("avoid-hol-blocking")?["RUNNING","RESTARTING","TERMINATING","PENDING","SCHEDULED",globalThis.backendaiclient.supports("prepared-session-status")?"PREPARED":void 0,globalThis.backendaiclient.supports("creating-session-status")?"CREATING":void 0,"PREPARING","PULLING"].filter((i=>!!i)).join(","):["RUNNING","RESTARTING","TERMINATING","PENDING",globalThis.backendaiclient.supports("prepared-session-status")?"PREPARED":void 0,globalThis.backendaiclient.supports("creating-session-status")?"CREATING":void 0,"PREPARING","PULLING"].filter((i=>!!i)).join(",");const t=globalThis.backendaiclient._config.accessKey;let n;try{this.appLauncher.indicator.set(20,u("eduapi.QueryingExistingComputeSession")),n=await globalThis.backendaiclient.computeSession.list(i,e,t,30,0)}catch(i){return this.appLauncher.indicator.end(),console.error(i),void(i&&i.message?(i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i)))}const s=window.location.search,o=new URLSearchParams(s),a=o.get("app")||"jupyter";let c=a;const r=o.get("session_template")||o.get("sessionTemplate")||a;""!==this._eduAppNamePrefix&&a.startsWith(this._eduAppNamePrefix)&&(c=a.slice(this._eduAppNamePrefix.length));let l,p=!0;try{l=await globalThis.backendaiclient.sessionTemplate.list(!1),l=l.filter((i=>i.name===r))}catch(i){return this.appLauncher.indicator.end(),console.error(i),void(i&&i.message?(i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i)))}if(l.length<1)return this.appLauncher.indicator.end(),this.notification.text=u("eduapi.NoSessionTemplate"),void this.notification.show(!0);const h=l[0];let d;if(n.compute_session_list.total_count>0){console.log("Reusing an existing session ...");let i=null;for(let e=0;e<n.compute_session_list.items.length;e++){const t=n.compute_session_list.items[e],s=t.image,o=JSON.parse(t.service_ports||"{}"),a=Object.keys(o).map((i=>o[i].name))||[],r=t.status;if(s!=h.template.spec.kernel.image){this.appLauncher.indicator.end();const i="Cannot create a session with an image different from any running session.";return this.notification.text=g.relieve(i),void this.notification.show(!0,i)}if("RUNNING"!==r)return this.appLauncher.indicator.end(),this.notification.text=u("eduapi.SessionStatusIs")+` ${r}. `+u("eduapi.PleaseReload"),void this.notification.show(!0);if(a.includes(c)){i=t;break}}i?(p=!1,d="session_id"in i?i.session_id:null,this.appLauncher.indicator.set(50,u("eduapi.FoundExistingComputeSession"))):p=!0,d=null!==i&&"session_id"in i?i.session_id:null}if(p){console.log("Creating a new session ..."),this.appLauncher.indicator.set(40,u("eduapi.FindingSessionTemplate"));const i=h.id;try{const e=await globalThis.backendaiclient.eduApp.get_mount_folders(),t=await globalThis.backendaiclient.eduApp.get_user_projects();if(!t)return this.notification.text=u("eduapi.EmptyProject"),void this.notification.show();const n=o.get("sToken")||o.get("stoken"),s=n?(await globalThis.backendaiclient.eduApp.get_user_credential(n)).script:void 0,a={...this.resources,group_name:t[0].name,...e&&Object.keys(e).length>0?{mounts:e}:{},...s?{bootstrap_script:s}:{}};let c;try{this.appLauncher.indicator.set(60,u("eduapi.CreatingComputeSession")),c=await globalThis.backendaiclient.createSessionFromTemplate(i,null,null,a,2e4)}catch(i){return this.appLauncher.indicator.end(),console.error(i),void(i&&i.message?(i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i)))}d=c.sessionId}catch(i){this.appLauncher.indicator.end(),console.error(i),i&&i.message?("statusCode"in i&&408===i.statusCode?this.notification.text=u("eduapi.SessionStillPreparing"):i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i))}}this.appLauncher.indicator.set(100,u("eduapi.ComputeSessionPrepared")),d&&this._openServiceApp(d,c)}async _openServiceApp(i,e){this.appLauncher.indicator=await globalThis.lablupIndicator.start(),console.log(`launching ${e} from session ${i} ...`),this.appLauncher._open_wsproxy(i,e,null,null).then((async i=>{if(i.url){const e=await this.appLauncher._connectToProxyWorker(i.url,""),t=String(null==e?void 0:e.appConnectUrl)||i.url;if(!t)return this.appLauncher.indicator.end(),this.notification.text=u("session.appLauncher.ConnectUrlIsNotValid"),void this.notification.show(!0);this.appLauncher.indicator.set(100,u("session.appLauncher.Prepared")),setTimeout((()=>{globalThis.open(t,"_self")}))}}))}render(){return f`
      <backend-ai-app-launcher id="app-launcher"></backend-ai-app-launcher>
    `}};i([e({type:Object})],b.prototype,"webUIShell",void 0),i([e({type:Object})],b.prototype,"clientConfig",void 0),i([e({type:Object})],b.prototype,"client",void 0),i([e({type:Object})],b.prototype,"notification",void 0),i([e({type:String})],b.prototype,"resources",void 0),i([e({type:String})],b.prototype,"_eduAppNamePrefix",void 0),i([t("#app-launcher")],b.prototype,"appLauncher",void 0),b=i([n("backend-ai-edu-applauncher")],b);

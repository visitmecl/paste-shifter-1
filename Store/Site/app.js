const clipButtons=[...document.querySelectorAll('[data-clip]')];
clipButtons.forEach((button,index)=>button.addEventListener('click',()=>{
  clipButtons.forEach(item=>{const active=item===button;item.setAttribute('aria-pressed',String(active));document.querySelector(`#demo-${item.dataset.clip}`).hidden=!active;});
  document.querySelector('#demo-counter').textContent=`${index+1} / 3`;
}));
const sendButton=document.querySelector('#orbital-demo-send');
sendButton.addEventListener('click',()=>{
 const result=document.querySelector('#orbital-demo-result');
 const sent=sendButton.dataset.sent==='true';
 if(sent){
  result.replaceChildren(Object.assign(document.createElement('span'),{className:'message-placeholder',textContent:'Tu texto de ejemplo aparecerá aquí.'}));
  document.querySelector('#orbital-demo-status').textContent='Ejemplo interactivo';
  sendButton.textContent='Probar envío de ejemplo ↗';
  sendButton.dataset.sent='false';
 }else{
  result.textContent=document.querySelector('#example-text').textContent;
  document.querySelector('#orbital-demo-status').textContent='Ejemplo recibido · listo para continuar';
  sendButton.textContent='Volver a probar ↺';
  sendButton.dataset.sent='true';
 }
});

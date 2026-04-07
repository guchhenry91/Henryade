const ws = require('ws');
const PAGE_ID = 'F26F9B80A7736EF69D09D73A800E6319';
const socket = new ws.WebSocket(`ws://localhost:9222/devtools/page/${PAGE_ID}`);

const text = process.argv[2] || 'Hello world';

socket.on('open', () => {
  const jsCode = `
    (function() {
      // Try textarea first
      const ta = document.querySelector('textarea');
      if (ta) {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, ${JSON.stringify(text)});
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        ta.focus();
        return 'pasted via textarea: ' + ${JSON.stringify(text)}.length + ' chars';
      }

      // Try contenteditable
      const ce = document.querySelector('[contenteditable=true]');
      if (ce) {
        ce.focus();
        ce.innerHTML = '';
        ce.textContent = ${JSON.stringify(text)};
        ce.dispatchEvent(new Event('input', { bubbles: true }));
        ce.dispatchEvent(new Event('change', { bubbles: true }));
        return 'pasted via contenteditable: ' + ${JSON.stringify(text)}.length + ' chars';
      }

      return 'no text input found';
    })()
  `;
  socket.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: { expression: jsCode }
  }));
});

socket.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.id === 1) {
    console.log(msg.result?.result?.value || JSON.stringify(msg.result));
    socket.close();
  }
});

setTimeout(() => process.exit(), 5000);

const ws = require('ws');
const PAGE_ID = 'F26F9B80A7736EF69D09D73A800E6319';
const socket = new ws.WebSocket(`ws://localhost:9222/devtools/page/${PAGE_ID}`);

const textToType = process.argv[2] || 'George';
let msgId = 0;

function send(method, params = {}) {
  msgId++;
  socket.send(JSON.stringify({ id: msgId, method, params }));
  return msgId;
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

socket.on('open', async () => {
  // First focus the search input
  send('Runtime.evaluate', {
    expression: `
      (function() {
        const inputs = document.querySelectorAll('input');
        for (const inp of inputs) {
          if (inp.placeholder && inp.placeholder.includes('Start typing')) {
            inp.focus();
            inp.value = '';
            inp.dispatchEvent(new Event('input', { bubbles: true }));
            return 'focused';
          }
        }
        return 'not found';
      })()
    `
  });

  await sleep(500);

  // Use CDP to type each character as real keyboard events
  for (const char of textToType) {
    send('Input.dispatchKeyEvent', {
      type: 'keyDown',
      text: char,
      key: char,
      code: 'Key' + char.toUpperCase(),
    });
    await sleep(50);
    send('Input.dispatchKeyEvent', {
      type: 'char',
      text: char,
      key: char,
      code: 'Key' + char.toUpperCase(),
    });
    await sleep(50);
    send('Input.dispatchKeyEvent', {
      type: 'keyUp',
      text: char,
      key: char,
      code: 'Key' + char.toUpperCase(),
    });
    await sleep(100);
  }

  await sleep(1500);

  // Check what's visible
  send('Runtime.evaluate', {
    expression: `
      (function() {
        const body = document.body.innerText;
        const idx = body.indexOf('Select a voice');
        if (idx > -1) return body.substring(idx, idx + 800);
        return body.substring(0, 800);
      })()
    `
  });
});

socket.on('message', (data) => {
  const msg = JSON.parse(data);
  // Only log the last evaluation result
  if (msg.result?.result?.type === 'string' && msg.result.result.value.length > 20) {
    console.log(msg.result.result.value);
  }
});

setTimeout(() => {
  socket.close();
  process.exit();
}, 10000);

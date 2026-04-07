const ws = require('ws');
const PAGE_ID = 'E73C5338AFD0F581F3F617028768026F';
const socket = new ws.WebSocket(`ws://localhost:9222/devtools/page/${PAGE_ID}`);
const searchTerm = process.argv[2] || 'George';

function evaluate(expr) {
  return new Promise((resolve) => {
    const id = Math.floor(Math.random() * 100000);
    const handler = (data) => {
      const msg = JSON.parse(data);
      if (msg.id === id) {
        socket.removeListener('message', handler);
        resolve(msg.result?.result?.value);
      }
    };
    socket.on('message', handler);
    socket.send(JSON.stringify({ id, method: 'Runtime.evaluate', params: { expression: expr } }));
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

socket.on('open', async () => {
  // Search via React onChange
  const searchResult = await evaluate(`
    (function() {
      const inputs = document.querySelectorAll('input');
      let searchInput = null;
      for (const inp of inputs) {
        if (inp.placeholder && inp.placeholder.includes('Start typing')) {
          searchInput = inp;
          break;
        }
      }
      if (!searchInput) return 'no search input';
      const propsKey = Object.keys(searchInput).find(k => k.startsWith('__reactProps'));
      const props = searchInput[propsKey];
      if (props && props.onChange) {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(searchInput, '${searchTerm}');
        searchInput.dispatchEvent(new Event('input', { bubbles: true }));
        props.onChange({ target: { value: '${searchTerm}' }, currentTarget: { value: '${searchTerm}' } });
        return 'searched ${searchTerm}';
      }
      return 'no onChange';
    })()
  `);
  console.log(searchResult);

  await sleep(2000);

  // Check results
  const results = await evaluate(`
    (function() {
      const body = document.body.innerText;
      const idx = body.indexOf('Select a voice');
      if (idx > -1) return body.substring(idx, idx + 1500);
      return body.substring(0, 1500);
    })()
  `);
  console.log(results);

  socket.close();
});

setTimeout(() => process.exit(), 10000);

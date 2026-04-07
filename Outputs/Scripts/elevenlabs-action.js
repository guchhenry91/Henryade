const ws = require('ws');
const PAGE_ID = 'F26F9B80A7736EF69D09D73A800E6319';
const socket = new ws.WebSocket(`ws://localhost:9222/devtools/page/${PAGE_ID}`);

const action = process.argv[2] || 'check';

socket.on('open', () => {
  socket.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: { expression: action, awaitPromise: true }
  }));
});

socket.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.id === 1) {
    if (msg.result?.result?.value !== undefined) {
      console.log(msg.result.result.value);
    } else if (msg.result?.exceptionDetails) {
      console.log('ERROR:', msg.result.exceptionDetails.text);
    } else {
      console.log(JSON.stringify(msg.result));
    }
    socket.close();
  }
});

setTimeout(() => process.exit(), 8000);

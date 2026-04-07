const ws = require('ws');
const PAGE_ID = 'E73C5338AFD0F581F3F617028768026F';
const socket = new ws.WebSocket(`ws://localhost:9222/devtools/page/${PAGE_ID}`);
const voiceName = process.argv[2] || 'George - Natural, Full and Confident';

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
  // Click the LI element containing the voice name
  const result = await evaluate(`
    (function() {
      const allLis = [...document.querySelectorAll('li')];
      const voiceLi = allLis.find(e => e.textContent.includes('${voiceName}'));
      if (voiceLi) { voiceLi.click(); return 'clicked LI: ${voiceName}'; }

      // Try div with cursor pointer
      const allEls = [...document.querySelectorAll('*')];
      const voiceEl = allEls.find(e => {
        const t = e.textContent.trim();
        return t.startsWith('${voiceName}') && t.length < 200 && getComputedStyle(e).cursor === 'pointer' && e.tagName === 'LI';
      });
      if (voiceEl) { voiceEl.click(); return 'clicked element'; }

      return 'not found';
    })()
  `);
  console.log(result);

  await sleep(2000);

  // Verify selection
  const check = await evaluate(`
    (function() {
      const body = document.body.innerText;
      if (body.includes('George') && body.includes('Generate')) return 'George selected! Ready to generate.';
      if (body.includes('George') && body.includes('Select a voice')) return 'George visible but panel still open';
      const voiceIdx = body.indexOf('Voice\\n');
      if (voiceIdx > -1) return 'Voice: ' + body.substring(voiceIdx, voiceIdx + 100);
      return body.substring(0, 300);
    })()
  `);
  console.log(check);

  socket.close();
});

setTimeout(() => process.exit(), 10000);

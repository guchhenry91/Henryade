const ws = require('ws');
const PAGE_ID = 'F26F9B80A7736EF69D09D73A800E6319';

const scenes = [
  // Scene 18
  `Four episodes into Genesis and the pattern is unmistakable. The Garden, they ate the fruit. Cain, it led to murder. The flood, total destruction. Babel, confusion and scattering. The sin is always the same. Pride. Independence from God. And the result is always brokenness. But after Babel, God does something unexpected. He calls one man. And through that one man, He begins to rebuild everything.`,

  // Scene 19
  `Genesis 12. God speaks to Abram. "Go from your country to the land I will show you. I will make you into a great nation and I will make your name great." At Babel, humanity tried to make a name for themselves and got confusion. With Abraham, God says, I will make your name great. Babel was built on pride. Abraham walked in faith. And from that one man came Israel, the prophets, the law, the Messiah. Everything the tower could never achieve, faith accomplished in a single step.`,

  // Scene 20
  `And here is the final irony. At Babel, humanity tried to build a city that reached up to God. In Revelation, God builds a city that comes down to us. The New Jerusalem, not brick and tar, but gold and light. God does not ask us to climb to Him. He comes to us. He always has. He walked with Adam. He sealed Noah in the ark. He called Abraham. He sent His Son. And one day He will bring His city down to earth. Babel reversed. Forever.`,

  // Scene 21
  `If this video spoke to you, share it with someone who needs to hear it. Watch our full Genesis series, links in the description. Subscribe to Quiet Revelations. Next time, we follow Abraham into the unknown. God bless you. And remember, you don't need to build a tower to reach God. He already came down for you.`
];

function connect() {
  return new Promise((resolve) => {
    const socket = new ws.WebSocket(`ws://localhost:9222/devtools/page/${PAGE_ID}`);
    socket.on('open', () => resolve(socket));
  });
}

function evaluate(socket, expr) {
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

async function main() {
  const socket = await connect();
  console.log(`Connected. Generating ${scenes.length} missing scenes...`);

  for (let i = 0; i < scenes.length; i++) {
    const sceneNum = i + 18;
    const text = scenes[i];
    console.log(`\n--- Scene ${sceneNum} (${text.length} chars) ---`);

    const pasteResult = await evaluate(socket, `
      (function() {
        const ta = document.querySelector('textarea');
        if (ta) {
          const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
          setter.call(ta, ${JSON.stringify(text)});
          ta.dispatchEvent(new Event('input', { bubbles: true }));
          return 'pasted via textarea';
        }
        const ce = document.querySelector('[contenteditable=true]');
        if (ce) {
          ce.focus();
          ce.innerHTML = '';
          ce.textContent = ${JSON.stringify(text)};
          ce.dispatchEvent(new Event('input', { bubbles: true }));
          return 'pasted via contenteditable';
        }
        return 'no input found';
      })()
    `);
    console.log('Paste: ' + pasteResult);
    await sleep(1000);

    const genResult = await evaluate(socket, `
      (function() {
        const allBtns = [...document.querySelectorAll('button')];
        const genBtn = allBtns.find(b => b.textContent.trim().includes('Generate'));
        if (genBtn && !genBtn.disabled) { genBtn.click(); return 'generating'; }
        if (genBtn && genBtn.disabled) return 'button disabled';
        return 'no generate button';
      })()
    `);
    console.log('Generate: ' + genResult);

    if (genResult !== 'generating') {
      console.log('SKIPPING');
      continue;
    }

    let done = false;
    for (let w = 0; w < 10; w++) {
      await sleep(3000);
      const status = await evaluate(socket, `
        (function() {
          const genBtn = [...document.querySelectorAll('button')].find(b => b.textContent.trim().includes('Generate'));
          const body = document.body.innerText;
          const credits = (body.match(/(\\d[\\d,]+)\\s*credits/) || ['','?'])[1];
          return 'credits: ' + credits + ', btn_disabled: ' + (genBtn ? genBtn.disabled : 'none');
        })()
      `);
      console.log('  ' + status);
      if (status.includes('btn_disabled: false')) { done = true; break; }
    }
    console.log(done ? `Scene ${sceneNum} DONE` : `Scene ${sceneNum} TIMEOUT`);
    await sleep(2000);
  }

  const finalCredits = await evaluate(socket, `
    (function() {
      const body = document.body.innerText;
      const match = body.match(/(\\d[\\d,]+)\\s*credits remaining/);
      return match ? match[1] + ' credits remaining' : 'unknown';
    })()
  `);
  console.log('\n=== DONE === ' + finalCredits);
  socket.close();
}

main().catch(err => { console.error(err); process.exit(1); });

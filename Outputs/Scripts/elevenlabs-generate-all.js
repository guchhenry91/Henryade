const ws = require('ws');
const PAGE_ID = 'F26F9B80A7736EF69D09D73A800E6319';

const scenes = [
  // Scene 03 (Scene 01 already done)
  `Welcome back to Quiet Revelations. In our first three episodes, we watched sin enter the world through Adam and Eve, grow into murder with Cain, and consume the earth until God sent the flood. Humanity had a fresh start. But did they learn? Genesis chapter 11 gives us the answer. This is episode four. The Tower of Babel.`,

  // Scene 04
  `After the flood, Noah's descendants multiplied. Genesis 11:1 tells us, "Now the whole world had one language and a common speech." No barriers. No misunderstanding. Complete unity. This was a gift from God. They could have used it to worship. To build something for His glory. Instead, they used it to build something for their own.`,

  // Scene 05
  `As the population grew, they migrated eastward and found a plain in Shinar, modern-day Iraq. Instead of spreading across the earth as God commanded, "Be fruitful and multiply and fill the earth," they stopped. They settled. God told them to fill the earth. They refused. They chose comfort over obedience. And that decision planted the seed for what came next.`,

  // Scene 06
  `Genesis 11:3 says, "They said to each other, Come, let us make bricks and bake them thoroughly. They used brick instead of stone, and tar for mortar." There was no natural stone, so they engineered a solution. This was advanced. This was human innovation at its finest. And there is nothing wrong with innovation, unless you look at what your hands have made and forget whose hands made you.`,

  // Scene 07
  `Then came the declaration that changed everything. Genesis 11:4. "Come, let us build ourselves a city, with a tower that reaches to the heavens, so that we may make a name for ourselves; otherwise we will be scattered." Three things to notice. First, they wanted to reach God's domain on their own terms. Not through worship. Through brick and tar. Second, "let us make a name for ourselves." Not for God. For themselves. Third, they knew God's command to spread out. And they openly refused. This was defiance.`,

  // Scene 08
  `And so they built. Brick upon brick. Layer upon layer. A massive ziggurat spiraling upward toward the sky. Around it, a city grew. This was a civilization declaring its independence from God. The higher the tower grew, the more their confidence swelled. We don't need God. We are enough. The oldest lie in history. The same lie the serpent whispered in Eden. "You will be like God."`,

  // Scene 09
  `What was the real sin of Babel? God is not threatened by architecture. The sin was the heart behind it. Self-worship disguised as progress. Unity without God at the center. This is the pattern since Genesis chapter 3. Adam and Eve wanted to be like God. Cain wanted worship on his own terms. The pre-flood world abandoned God entirely. And now the post-flood world was repeating the same sin.`,

  // Scene 10
  `Higher and higher it rose. Into the clouds. Their pride grew with every brick. They believed they were unstoppable. Their unity made them powerful. Their ambition made them relentless. But they had forgotten one thing. The One who gave them their language and their ability to build, was watching.`,

  // Scene 11
  `Then comes one of the most brilliantly ironic verses in the Bible. Genesis 11:5. "But the Lord came down to see the city and the tower the people were building." They thought their tower reached the heavens. God had to come down just to see it. From God's perspective, it was so small He had to descend to even look at it. All their ambition. All their pride. From heaven's viewpoint, barely a speck on the ground. What looks colossal from earth looks like nothing from eternity.`,

  // Scene 12
  `God said, "If as one people speaking the same language they have begun to do this, then nothing they plan to do will be impossible for them." God is not threatened by a brick tower. He recognized that unified humanity without God at the center would destroy itself. Every time humanity gains great power without moral grounding, the result is the same. Oppression. War. Self-destruction. God was protecting them from what their pride would inevitably produce.`,

  // Scene 13
  `"Come, let us go down and confuse their language so they will not understand each other." The same God who spoke creation into existence now spoke confusion into their language. In an instant, everything changed. Workers could not understand each other. The foreman shouted orders and heard gibberish. The unity that made them powerful shattered like glass. The greatest construction project in human history stopped. Not because of war. Because they could no longer say, "Pass me a brick."`,

  // Scene 14
  `"So the Lord scattered them over all the earth, and they stopped building the city." The very thing they feared, being scattered, became their reality. The very thing they built the tower to prevent was the exact consequence of building it. They wanted to stay together, God spread them apart. They wanted to make a name, God gave them names they couldn't even pronounce to each other. Groups formed around shared language and walked away. North. South. East. West. Exactly as God had originally commanded.`,

  // Scene 15
  `The tower stood alone. Unfinished. Abandoned. Genesis 11:9 says, "That is why it was called Babel, because there the Lord confused the language of the whole world." The city they built to glorify their name became synonymous with chaos. Every empire built on pride ends the same way. The bricks crack. The mortar fails. And what remains is a name that means "confusion."`,

  // Scene 16
  `But the scattering was not just judgment, it was fulfillment. God told Noah to fill the earth. Humanity refused. So God did it for them. From that scattering came every nation, every culture, every language on earth. What began as judgment became the foundation for human civilization. God took their rebellion and wove it into His plan. He always does.`,

  // Scene 17
  `Babel is not the end. Thousands of years later, at Pentecost, the Holy Spirit fell on the disciples. They spoke in other tongues, and people from every nation heard them in their own language. At Babel, God divided languages to scatter prideful humanity. At Pentecost, God united languages to gather humble believers. Babel was the curse. Pentecost was the cure. What pride broke apart, the Holy Spirit put back together. The division that began with a tower was healed by a cross.`,

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
  console.log(`Connected. Processing ${scenes.length} scenes...`);

  for (let i = 0; i < scenes.length; i++) {
    const sceneNum = i === 0 ? 3 : i + 3; // Scene 01 already done, start from 03
    const text = scenes[i];
    console.log(`\n--- Scene ${String(sceneNum).padStart(2,'0')} (${text.length} chars) ---`);

    // Paste text
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

    // Click Generate
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
      console.log('SKIPPING - could not generate');
      continue;
    }

    // Wait for generation (check credits every 3 seconds, up to 30s)
    let done = false;
    for (let w = 0; w < 10; w++) {
      await sleep(3000);
      const credits = await evaluate(socket, `
        (function() {
          const body = document.body.innerText;
          const match = body.match(/(\\d[\\d,]+)\\s*credits remaining/);
          return match ? match[1] : 'unknown';
        })()
      `);
      const hasPlay = await evaluate(socket, `
        (function() {
          // Check if audio player appeared or generation complete
          const body = document.body.innerText;
          const genBtn = [...document.querySelectorAll('button')].find(b => b.textContent.trim().includes('Generate'));
          const isDisabled = genBtn ? genBtn.disabled : false;
          return 'credits: ' + (body.match(/(\\d[\\d,]+)\\s*credits/) || ['','?'])[1] + ', btn_disabled: ' + isDisabled;
        })()
      `);
      console.log('  Waiting... ' + hasPlay);
      // If button is no longer disabled, generation is done
      if (hasPlay.includes('btn_disabled: false')) {
        done = true;
        break;
      }
    }

    if (done) {
      console.log('Scene ' + sceneNum + ' DONE');
    } else {
      console.log('Scene ' + sceneNum + ' - timeout, moving on');
    }

    await sleep(2000);
  }

  console.log('\n=== ALL SCENES COMPLETE ===');
  const finalCredits = await evaluate(socket, `
    (function() {
      const body = document.body.innerText;
      const match = body.match(/(\\d[\\d,]+)\\s*credits remaining/);
      return match ? match[1] + ' credits remaining' : 'unknown';
    })()
  `);
  console.log(finalCredits);
  socket.close();
}

main().catch(err => { console.error(err); process.exit(1); });

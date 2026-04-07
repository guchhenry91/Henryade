const ws = require('ws');
const PAGE_ID = 'E73C5338AFD0F581F3F617028768026F'; // New account with George

// FULL SCRIPT (not trimmed)
const scenes = [
  // Scene 01 — Cold Open
  `They spoke one language. They shared one ambition. And they decided, together, that they no longer needed God. So they built. Not a temple. Not an altar. A tower. A monument to themselves, rising from the plains of Shinar into the heavens. And God came down, not in anger at first, but to look. And what He saw changed the course of human history forever. This is not just a story about a building. This is the story of the day humanity declared war on heaven. And lost.`,

  // Scene 03 — Channel Intro
  `Welcome back to Quiet Revelations. In our first three episodes, we watched sin enter the world through Adam and Eve, grow into murder with Cain, and consume the entire earth until God sent the flood. Noah and his family survived. God made a covenant, a rainbow promise. Humanity had a fresh start. A clean slate. But here's the question, did they learn? Genesis chapter 11 gives us the answer. And it's not the one we'd hope for. This is episode four. The Tower of Babel.`,

  // Scene 04 — One Language, One People
  `After the flood, Noah's descendants multiplied. They spread out, but not far. Genesis 11:1 tells us, "Now the whole world had one language and a common speech." One language. No barriers. No misunderstanding. Every person on earth could speak to every other person perfectly. Think about the power of that. No translation needed. No cultural divide. Complete unity. This was a gift. God had given humanity the ability to collaborate without limits. They could have used that gift to worship. To build something for God's glory. Instead, they used it to build something for their own.`,

  // Scene 05 — The Plain of Shinar
  `As the population grew, people migrated eastward and found a plain in Shinar, the region we know today as Mesopotamia, modern-day Iraq. And instead of spreading across the earth as God had commanded Noah, "Be fruitful and multiply and fill the earth," they stopped. They settled. They looked at this flat, fertile land and said, "This is where we stay." This was the first act of rebellion. God had explicitly told Noah's descendants to fill the earth. To spread out. To go everywhere. But they chose comfort over obedience. They chose each other over God's command. And that decision planted the seed for what came next.`,

  // Scene 06 — The Invention of Bricks
  `Genesis 11:3 includes a detail that's easy to miss but deeply important. "They said to each other, 'Come, let us make bricks and bake them thoroughly.' They used brick instead of stone, and tar for mortar." Why does this matter? Because in that region, there was no natural stone. So they invented an alternative. They engineered a solution. They fired clay into bricks and used bitumen as cement. This was not primitive. This was advanced. This was human innovation at its finest. And there is nothing wrong with innovation, unless it becomes the foundation for pride. Unless you look at what your hands have made and forget whose hands made you.`,

  // Scene 07 — The Declaration
  `And then came the declaration that changed everything. Genesis 11:4. "Come, let us build ourselves a city, with a tower that reaches to the heavens, so that we may make a name for ourselves; otherwise we will be scattered over the face of the whole earth." Three things to notice. First, "a tower that reaches to the heavens." This was not about architecture. This was about access. They wanted to reach God's domain on their own terms. Not through worship. Not through faith. Through brick and tar. Second, "let us make a name for ourselves." Not for God. For themselves. This was glory for humanity, by humanity. Third, "otherwise we will be scattered." They knew God's command was to spread out. And they openly refused. This was not ignorance. This was defiance.`,

  // Scene 08 — Construction Begins
  `And so they built. Thousands of hands working in perfect coordination. Brick upon brick. Layer upon layer. The tower rose from the plain of Shinar like nothing the world had ever seen. A massive ziggurat, wide at the base, narrowing as it climbed, spiraling upward toward the sky. Around it, a city grew. Markets. Homes. Walls. This was not a village project. This was a civilization declaring its independence from God. And the higher the tower grew, the more their confidence swelled. They looked at what they were building and thought, we can do anything. We don't need God. We are enough. It is the oldest lie in history. The same lie the serpent whispered in Eden. "You will be like God."`,

  // Scene 09 — The Sin Beneath the Bricks
  `But what was the real sin of Babel? It wasn't building a tall structure. God is not threatened by architecture. The sin was the heart behind it. It was self-worship disguised as progress. It was unity without God at the center. It was humanity saying, we will define our own purpose, our own meaning, our own destiny. We will reach heaven on our own terms. This is the pattern we've seen since Genesis chapter 3. Adam and Eve wanted to be like God. Cain wanted to worship God on his own terms. The pre-flood world abandoned God entirely. And now, the post-flood world, the world that had been given a second chance, was repeating the same sin. Building a monument not to God's greatness, but to their own.`,

  // Scene 10 — The Tower Rises
  `Higher and higher it rose. Through the haze. Into the clouds. The people below could barely see the top. And with every new layer of brick, their pride grew. They believed they were unstoppable. They believed that together, with one language and one purpose, nothing could stand in their way. And in a sense, they were right. Their unity made them powerful. Their shared language made them efficient. Their ambition made them relentless. But they had forgotten one thing. The One who gave them their language, their intelligence, and their ability to build, was watching.`,

  // Scene 11 — The Lord Came Down
  `And then comes one of the most brilliantly ironic verses in the entire Bible. Genesis 11:5. "But the Lord came down to see the city and the tower the people were building." They thought their tower reached the heavens. God had to come down just to see it. The tower that humanity believed pierced the sky, from God's perspective, was so small He had to descend to even look at it. This is divine irony at its finest. All their ambition. All their engineering. All their pride. And from heaven's viewpoint, it was barely a speck on the ground. Every empire that has ever tried to make itself God has discovered the same truth. What looks colossal from earth looks like nothing from eternity.`,

  // Scene 12 — God's Assessment
  `God looked at what they were doing and said something remarkable. "If as one people speaking the same language they have begun to do this, then nothing they plan to do will be impossible for them." This is not God being afraid. God is not threatened by a brick tower. This is God recognizing something dangerous, that unified humanity, without God at the center, would destroy itself. Think about it. Every time humanity gains great power without moral grounding, the result is the same. Oppression. War. Self-destruction. God was not punishing their ability. He was protecting them from what their ability, combined with their pride, would inevitably produce. The flood had already shown what unchecked evil leads to. God would not let it happen again.`,

  // Scene 13 — The Confusion of Languages
  `"Come, let us go down and confuse their language so they will not understand each other." Notice the words, "let us." The same plural language used in Genesis 1:26 when God said, "Let us make mankind in our image." The same God who spoke creation into existence now spoke confusion into humanity's language. And in an instant, everything changed. The worker who handed bricks to his partner suddenly could not understand him. The foreman who shouted orders heard gibberish in return. Families could no longer speak to their neighbors. The unity that had made them powerful shattered like glass. One moment, one language. The next, dozens. Maybe hundreds. The greatest construction project in human history ground to a halt. Not because of war. Not because of famine. Because they could no longer say, "Pass me a brick."`,

  // Scene 14 — The Scattering
  `"So the Lord scattered them from there over all the earth, and they stopped building the city." The very thing they feared, being scattered, became their reality. The very thing they built the tower to prevent was the exact consequence of building it. This is the pattern of sin throughout Scripture. You run from God's plan, and you run straight into the thing you were trying to avoid. They wanted to stay together, God spread them apart. They wanted to make a name for themselves, God gave them names they couldn't even pronounce to each other. They wanted to reach heaven, they couldn't even reach their neighbor anymore. Groups formed around shared language. Families clustered with those they could still understand. And they walked away. North. South. East. West. Into every corner of the earth, exactly as God had originally commanded.`,

  // Scene 15 — The Abandoned Tower
  `And the tower stood alone. Unfinished. Abandoned. A monument to nothing. Genesis 11:9 says, "That is why it was called Babel, because there the Lord confused the language of the whole world." The word "Babel" sounds like the Hebrew word for "confused." The city they built to glorify their name became synonymous with chaos. The tower they raised to reach heaven became a ruin on an empty plain. Every empire built on pride ends the same way. Babylon. Rome. Every kingdom that puts itself in God's place eventually crumbles. The bricks crack. The mortar fails. And what remains is a name that means "confusion."`,

  // Scene 16 — Nations of the Earth
  `But here is what we must not miss. The scattering was not just judgment, it was also fulfillment. God had told Noah to fill the earth. Humanity refused. So God did it for them. And from that scattering came every nation, every culture, every language, every people group on earth. The diversity of humanity, the thousands of languages, the countless traditions, the beautiful differences between peoples, all of it traces back to this moment. What began as judgment became the foundation for the rich tapestry of human civilization. God took humanity's rebellion and wove it into His plan. He always does.`,

  // Scene 17 — Babel and Pentecost
  `And this is where the story gets extraordinary. Because Babel is not the end. Thousands of years later, on the day of Pentecost, something happened that reversed everything. Acts chapter 2 tells us that the Holy Spirit fell on the disciples in Jerusalem. And they began to speak in other tongues, and people from every nation under heaven heard them, each in their own language. At Babel, God divided the languages to scatter prideful humanity. At Pentecost, God united the languages to gather humble believers. Babel was the curse. Pentecost was the cure. What pride broke apart, the Holy Spirit put back together. The division that began with a tower was healed by a cross. And the unity that humanity tried to manufacture through brick and tar, God freely gave through grace and fire.`,

  // Scene 18 — The Pattern of Pride
  `Four episodes into Genesis, and the pattern is unmistakable. In the Garden, humanity wanted to be like God, they ate the fruit. With Cain, humanity wanted to worship on their own terms, it led to murder. Before the flood, humanity abandoned God completely, it led to total destruction. And at Babel, humanity tried to reach God's domain without God, it led to confusion and scattering. The sin is always the same. Pride. Independence from God. The belief that we are enough on our own. And the result is always the same. Brokenness. But woven through every story of failure is a thread of hope. Because after Babel, after the scattering, God does something no one expected. He calls one man. And through that one man, He begins to rebuild everything.`,

  // Scene 19 — The Call of Abraham
  `Genesis 12 opens with God speaking to a man named Abram. "Go from your country, your people and your father's household to the land I will show you. I will make you into a great nation, and I will bless you; I will make your name great." Did you catch that? At Babel, humanity tried to make a name for themselves, and got confusion. With Abraham, God says, I will make your name great. The difference? Babel was built on pride. Abraham walked in faith. Babel tried to reach God through a tower. Abraham simply trusted God's voice and walked. And from that one man, one act of obedience, came Israel, came the prophets, came the law, came the Messiah. Everything the tower could never achieve, faith accomplished in a single step.`,

  // Scene 20 — The City God Builds
  `And here is the final beautiful irony. At Babel, humanity tried to build a city that reached up to God. In Revelation, God builds a city that comes down to us. The New Jerusalem, not made of brick and tar, but of gold and light, descends from heaven to earth. God does not ask us to climb to Him. He comes to us. He always has. He walked with Adam in the garden. He sealed Noah in the ark. He called Abraham by name. He sent His Son to be born in a stable. And one day, He will bring His city, His eternal home, down to earth. What Babel tried to achieve through pride, God will accomplish through love. And in that city, Revelation tells us, every nation and every language will worship together, not in confusion, but in perfect unity. Babel reversed. Forever.`,

  // Scene 21 — Closing & Call to Action
  `If this video spoke to you, share it with someone who needs to hear it. Watch our full Genesis series, the Garden of Eden, Cain and Abel, and Noah's Ark, links are in the description. Subscribe to Quiet Revelations and turn on notifications so you don't miss what's coming next. Because next time, we follow Abraham into the unknown. God bless you. And remember, you don't need to build a tower to reach God. He already came down for you.`
];

const sceneNums = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21];

function connect() {
  return new Promise((resolve, reject) => {
    const socket = new ws.WebSocket(`ws://localhost:9222/devtools/page/${PAGE_ID}`);
    socket.on('open', () => resolve(socket));
    socket.on('error', reject);
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
  let totalChars = scenes.reduce((s, t) => s + t.length, 0);

  // VERIFY ROGER IS SELECTED FIRST
  const voiceCheck = await evaluate(socket, `
    (function() {
      const body = document.body.innerText;
      if (body.includes('George')) return 'GEORGE';
      return 'NOT_GEORGE';
    })()
  `);
  console.log('Voice check: ' + voiceCheck);
  if (voiceCheck !== 'GEORGE') {
    console.log('ERROR: George is NOT selected! Aborting to avoid wasting credits.');
    socket.close();
    process.exit(1);
  }

  const creditCheck = await evaluate(socket, `
    (function() {
      const body = document.body.innerText;
      const match = body.match(/(\\d[\\d,]+)\\s*credits remaining/);
      return match ? match[1] : 'unknown';
    })()
  `);
  console.log('Credits: ' + creditCheck);
  console.log('Total chars to generate: ' + totalChars);
  console.log('Scenes: ' + scenes.length + '\\n');

  for (let i = 0; i < scenes.length; i++) {
    const sceneNum = sceneNums[i];
    const text = scenes[i];
    console.log(`--- Scene ${String(sceneNum).padStart(2,'0')} (${text.length} chars) ---`);

    // VERIFY ROGER BEFORE EACH GENERATION
    const preCheck = await evaluate(socket, `
      (function() {
        const body = document.body.innerText;
        if (body.includes('George')) return 'GEORGE';
        return 'NOT_GEORGE';
      })()
    `);
    if (preCheck !== 'GEORGE') {
      console.log('  WARNING: Voice changed! Stopping.');
      break;
    }

    // Paste text
    const pasteResult = await evaluate(socket, `
      (function() {
        const ta = document.querySelector('textarea');
        if (ta) {
          const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
          setter.call(ta, ${JSON.stringify(text)});
          ta.dispatchEvent(new Event('input', { bubbles: true }));
          return 'textarea';
        }
        const ce = document.querySelector('[contenteditable=true]');
        if (ce) {
          ce.focus();
          ce.innerHTML = '';
          ce.textContent = ${JSON.stringify(text)};
          ce.dispatchEvent(new Event('input', { bubbles: true }));
          return 'contenteditable';
        }
        return 'none';
      })()
    `);
    await sleep(1000);

    // Click Generate
    const genResult = await evaluate(socket, `
      (function() {
        const allBtns = [...document.querySelectorAll('button')];
        const genBtn = allBtns.find(b => {
          const t = b.textContent.trim();
          return t === 'Generate speech' || t === 'Regenerate speech';
        });
        if (genBtn && !genBtn.disabled) { genBtn.click(); return 'generating'; }
        if (genBtn && genBtn.disabled) return 'disabled';
        return 'not found';
      })()
    `);
    console.log('  ' + pasteResult + ' -> ' + genResult);

    if (genResult !== 'generating') {
      console.log('  SKIPPED');
      continue;
    }

    // Wait for completion (up to 60 seconds)
    let done = false;
    for (let w = 0; w < 20; w++) {
      await sleep(3000);
      const status = await evaluate(socket, `
        (function() {
          const genBtn = [...document.querySelectorAll('button')].find(b => {
            const t = b.textContent.trim();
            return t.includes('Generate');
          });
          const body = document.body.innerText;
          const credits = (body.match(/(\\d[\\d,]+)\\s*credits/) || ['','?'])[1];
          return credits + '|' + (genBtn ? genBtn.disabled : 'none');
        })()
      `);
      const [credits, disabled] = status.split('|');
      if (disabled === 'false') {
        console.log('  Done! Credits: ' + credits);
        done = true;
        break;
      }
    }
    if (!done) console.log('  TIMEOUT (may still have generated)');
    await sleep(1500);
  }

  const finalCredits = await evaluate(socket, `
    (function() {
      const body = document.body.innerText;
      const match = body.match(/(\\d[\\d,]+)\\s*credits remaining/);
      return match ? match[1] : 'unknown';
    })()
  `);
  console.log('\\n=== ALL DONE === Credits remaining: ' + finalCredits);
  socket.close();
}

main().catch(err => { console.error(err); process.exit(1); });

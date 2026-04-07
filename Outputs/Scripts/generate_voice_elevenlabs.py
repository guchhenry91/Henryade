"""
ElevenLabs Voice Generator via Browser-Use
Generates voiceover audio using ElevenLabs through browser automation.
No API key required — uses free tier.

Usage:
    python generate_voice_elevenlabs.py "In the beginning, God created the heavens and the earth." --voice Peter --scene 1
    python generate_voice_elevenlabs.py script.txt --voice Peter --batch
"""

import asyncio
import argparse
import os
from datetime import datetime
from pathlib import Path

try:
    from browser_use import Agent, Browser
    from browser_use import ChatAnthropic
    HAS_BROWSER_USE = True
except ImportError:
    HAS_BROWSER_USE = False

try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


OUTPUTS_DIR = Path(__file__).parent.parent / "audio"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Track character usage
USAGE_LOG = Path(__file__).parent.parent / "voice-usage-log.md"


def log_usage(characters: int, voice: str, scene: str):
    """Log character usage to track free tier limits."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"| {timestamp} | {voice} | {scene} | {characters} |\n"

    if not USAGE_LOG.exists():
        header = "# ElevenLabs Voice Usage Log\n\n| Date | Voice | Scene | Characters |\n|------|-------|-------|------------|\n"
        USAGE_LOG.write_text(header, encoding="utf-8")

    with open(USAGE_LOG, "a", encoding="utf-8") as f:
        f.write(entry)


def split_text(text: str, max_chars: int = 2500) -> list[str]:
    """Split text into chunks at sentence boundaries."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""

    sentences = text.replace(". ", ".|").replace("! ", "!|").replace("? ", "?|").split("|")

    for sentence in sentences:
        if len(current) + len(sentence) <= max_chars:
            current += sentence + " "
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence + " "

    if current.strip():
        chunks.append(current.strip())

    return chunks


async def generate_with_browser_use(text: str, voice: str = "Peter", scene: str = "1"):
    """Generate voice using Browser-Use agent."""
    if not HAS_BROWSER_USE:
        print("browser-use not installed. Run: pip install browser-use")
        return None

    chunks = split_text(text)
    print(f"Text split into {len(chunks)} chunk(s)")

    for i, chunk in enumerate(chunks):
        chunk_label = f"scene-{scene}-chunk-{i+1}" if len(chunks) > 1 else f"scene-{scene}"

        task = f"""
        Go to https://elevenlabs.io/app/speech-synthesis

        I need you to generate speech audio:
        - Voice: Select "{voice}" from the voice selector
        - Text: {chunk}

        Steps:
        1. If there's a login page, wait for me to log in
        2. IMPORTANT: First, click on the voice selector and search for "{voice}"
        3. VERIFY the voice shows "{voice}" before proceeding
        4. Clear any existing text in the text input area
        5. Type or paste this text: {chunk}
        6. Click the "Generate" button
        7. Wait for the audio to finish generating
        8. Click the download button to save the audio

        Report what happened and whether the generation was successful.
        """

        browser = Browser()
        agent = Agent(
            task=task,
            llm=ChatAnthropic(model="claude-sonnet-4-6"),
            browser=browser,
        )

        result = await agent.run()
        await browser.close()

        log_usage(len(chunk), voice, chunk_label)
        print(f"Chunk {i+1}/{len(chunks)} complete: {len(chunk)} characters")

    return True


async def generate_with_playwright(text: str, voice: str = "Peter", scene: str = "1"):
    """Open ElevenLabs in browser with text ready to paste."""
    if not HAS_PLAYWRIGHT:
        print("playwright not installed. Run: pip install playwright && playwright install")
        return None

    chunks = split_text(text)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Opening ElevenLabs...")
        await page.goto("https://elevenlabs.io/app/speech-synthesis")

        for i, chunk in enumerate(chunks):
            print(f"\n--- Chunk {i+1}/{len(chunks)} ({len(chunk)} chars) ---")
            print(f"Voice: {voice}")
            print(f"Text: {chunk[:100]}...")
            print("\nPaste the text, select voice, generate, and download.")
            print("Press Enter when ready for next chunk...")
            input()

            log_usage(len(chunk), voice, f"scene-{scene}-chunk-{i+1}")

        await browser.close()


def create_script_file(text: str, voice: str, scene: str):
    """Save a ready-to-use script file for manual generation."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUTS_DIR / f"voice-script-scene-{scene}-{timestamp}.txt"

    chunks = split_text(text)
    content = f"Voice: {voice}\nScene: {scene}\nTotal characters: {len(text)}\nChunks: {len(chunks)}\n\n"

    for i, chunk in enumerate(chunks):
        content += f"--- CHUNK {i+1} ({len(chunk)} chars) ---\n{chunk}\n\n"

    filepath.write_text(content, encoding="utf-8")
    print(f"Script saved to: {filepath}")
    log_usage(len(text), voice, f"scene-{scene}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Generate voice via ElevenLabs")
    parser.add_argument("text", help="Text to convert to speech, or path to a .txt file")
    parser.add_argument("--voice", default="Peter", help="Voice name (default: Peter)")
    parser.add_argument("--scene", default="1", help="Scene number for file naming")
    parser.add_argument("--method", default="auto", help="Method: browser-use, playwright, script")
    parser.add_argument("--batch", action="store_true", help="Process a text file with multiple scenes")

    args = parser.parse_args()

    # Check if text is a file path
    text = args.text
    if os.path.isfile(text):
        with open(text, "r", encoding="utf-8") as f:
            text = f.read()

    print(f"Text length: {len(text)} characters")
    print(f"Voice: {args.voice}")
    print(f"Estimated chunks: {len(split_text(text))}")

    if args.method == "script" or (not HAS_BROWSER_USE and not HAS_PLAYWRIGHT):
        create_script_file(text, args.voice, args.scene)
    elif args.method == "browser-use" or (args.method == "auto" and HAS_BROWSER_USE):
        asyncio.run(generate_with_browser_use(text, args.voice, args.scene))
    elif args.method == "playwright" or (args.method == "auto" and HAS_PLAYWRIGHT):
        asyncio.run(generate_with_playwright(text, args.voice, args.scene))
    else:
        create_script_file(text, args.voice, args.scene)


if __name__ == "__main__":
    main()

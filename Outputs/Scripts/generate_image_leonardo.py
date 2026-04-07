"""
Leonardo AI Image Generator via Browser-Use
Generates images using Leonardo AI through browser automation.
No API key required — uses free tier.

Usage:
    python generate_image_leonardo.py "cinematic biblical scene of David facing Goliath" --style cinematic --size landscape
"""

import asyncio
import argparse
import os
from datetime import datetime
from pathlib import Path

# Browser-Use import
try:
    from browser_use import Agent, Browser
    from browser_use import ChatAnthropic
    HAS_BROWSER_USE = True
except ImportError:
    HAS_BROWSER_USE = False

# Playwright fallback
try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


OUTPUTS_DIR = Path(__file__).parent.parent / "images"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


async def generate_with_browser_use(prompt: str, style: str = "cinematic", size: str = "landscape"):
    """Generate image using Browser-Use agent."""
    if not HAS_BROWSER_USE:
        print("browser-use not installed. Run: pip install browser-use")
        return None

    size_map = {
        "landscape": "1280x720",
        "square": "1024x1024",
        "portrait": "768x1344",
        "thumbnail": "1280x720",
    }
    dimensions = size_map.get(size, "1280x720")

    task = f"""
    Go to https://app.leonardo.ai/ai-generations

    I need you to generate an image with these settings:
    - Prompt: {prompt}
    - Style: {style}
    - Dimensions: {dimensions}

    Steps:
    1. If there's a login page, wait for me to log in manually
    2. Find the prompt input area and type the prompt
    3. Look for dimension/size settings and set to {dimensions}
    4. Click the Generate button
    5. Wait for the image to finish generating (look for the image to appear)
    6. Right-click and save the image, or click the download button

    Report back what happened.
    """

    browser = Browser()
    agent = Agent(
        task=task,
        llm=ChatAnthropic(model="claude-sonnet-4-6"),
        browser=browser,
    )

    result = await agent.run()
    await browser.close()
    return result


async def generate_with_playwright(prompt: str, style: str = "cinematic", size: str = "landscape"):
    """Generate image using Playwright (manual flow — opens browser for user)."""
    if not HAS_PLAYWRIGHT:
        print("playwright not installed. Run: pip install playwright && playwright install")
        return None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Opening Leonardo AI...")
        await page.goto("https://app.leonardo.ai/ai-generations")

        print(f"\nPrompt ready to paste:\n{prompt}\n")
        print("Please log in if needed, then paste the prompt and generate.")
        print("Press Enter in this terminal when done to close the browser...")

        input()
        await browser.close()


def generate_html_fallback(prompt: str, style: str = "cinematic", title: str = "Generated Image"):
    """Create an HTML placeholder with the prompt for manual generation."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image-prompt-{timestamp}.html"
    filepath = OUTPUTS_DIR / filename

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            margin: 0; padding: 40px;
            background: #1a1a2e; color: #eee;
            font-family: 'Segoe UI', sans-serif;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            min-height: 100vh;
        }}
        .card {{
            background: #16213e; border-radius: 16px;
            padding: 40px; max-width: 800px; width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }}
        h1 {{ color: #e94560; margin-bottom: 8px; }}
        .prompt {{
            background: #0f3460; padding: 20px; border-radius: 12px;
            margin: 20px 0; font-size: 16px; line-height: 1.6;
            border-left: 4px solid #e94560;
        }}
        .meta {{ color: #888; font-size: 14px; }}
        .copy-btn {{
            background: #e94560; color: white; border: none;
            padding: 12px 24px; border-radius: 8px; cursor: pointer;
            font-size: 16px; margin-top: 16px;
        }}
        .copy-btn:hover {{ background: #c73652; }}
        .links {{ margin-top: 20px; }}
        .links a {{
            color: #e94560; text-decoration: none;
            margin-right: 20px; font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Image Prompt Ready</h1>
        <p class="meta">Style: {style} | Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        <div class="prompt" id="prompt">{prompt}</div>
        <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('prompt').innerText).then(()=>this.textContent='Copied!')">
            Copy Prompt
        </button>
        <div class="links">
            <a href="https://app.leonardo.ai/ai-generations" target="_blank">Open Leonardo AI</a>
            <a href="https://www.midjourney.com" target="_blank">Open Midjourney</a>
            <a href="https://labs.openai.com" target="_blank">Open DALL-E</a>
        </div>
    </div>
</body>
</html>"""

    filepath.write_text(html, encoding="utf-8")
    print(f"HTML prompt card saved to: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Generate images via Leonardo AI")
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("--style", default="cinematic", help="Style: cinematic, realistic, anime, illustration, 3D")
    parser.add_argument("--size", default="landscape", help="Size: landscape, square, portrait, thumbnail")
    parser.add_argument("--method", default="auto", help="Method: browser-use, playwright, html")
    parser.add_argument("--title", default="Generated Image", help="Title for the image")

    args = parser.parse_args()

    if args.method == "html" or (not HAS_BROWSER_USE and not HAS_PLAYWRIGHT):
        generate_html_fallback(args.prompt, args.style, args.title)
    elif args.method == "browser-use" or (args.method == "auto" and HAS_BROWSER_USE):
        asyncio.run(generate_with_browser_use(args.prompt, args.style, args.size))
    elif args.method == "playwright" or (args.method == "auto" and HAS_PLAYWRIGHT):
        asyncio.run(generate_with_playwright(args.prompt, args.style, args.size))
    else:
        print("No browser automation available. Generating HTML fallback...")
        generate_html_fallback(args.prompt, args.style, args.title)


if __name__ == "__main__":
    main()

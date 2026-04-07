"""
Content Production Pipeline
End-to-end: idea → script → images → voice → video-ready assets

Usage:
    python content_pipeline.py "David and Goliath" --type bible-video --scenes 20
    python content_pipeline.py "Top 5 AI tools" --type tiktok --scenes 5
    python content_pipeline.py "How to use Claude Code" --type youtube --scenes 12
"""

import argparse
import os
import json
from datetime import datetime
from pathlib import Path


OUTPUTS_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    return text.lower().replace(" ", "-").replace("'", "")[:50]


def create_project_structure(topic: str, content_type: str, num_scenes: int):
    """Create the project folder structure and master plan."""
    slug = slugify(topic)
    project_dir = OUTPUTS_DIR / slug
    (project_dir / "images").mkdir(parents=True, exist_ok=True)
    (project_dir / "audio").mkdir(parents=True, exist_ok=True)

    # Content type presets
    presets = {
        "bible-video": {
            "style": "cinematic biblical art, hyper-realistic, dramatic lighting",
            "voice": "Peter",
            "duration": "8-12 minutes",
            "image_style": "cinematic",
            "tone": "reverent, narrative, dramatic",
        },
        "tiktok": {
            "style": "vibrant, eye-catching, bold text overlay, vertical",
            "voice": "Adam",
            "duration": "30-60 seconds",
            "image_style": "vibrant",
            "tone": "punchy, engaging, hook-driven",
        },
        "youtube": {
            "style": "clean, professional, well-lit, educational",
            "voice": "Josh",
            "duration": "8-15 minutes",
            "image_style": "clean",
            "tone": "informative, friendly, clear",
        },
        "short": {
            "style": "dynamic, bold, vertical format, attention-grabbing",
            "voice": "Adam",
            "duration": "15-60 seconds",
            "image_style": "bold",
            "tone": "fast-paced, hook-driven",
        },
    }

    preset = presets.get(content_type, presets["youtube"])

    # Create master plan
    plan = f"""# {topic} — Content Production Plan

## Project Info
- **Topic**: {topic}
- **Type**: {content_type}
- **Scenes**: {num_scenes}
- **Target Duration**: {preset['duration']}
- **Created**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Presets
- **Image Style**: {preset['style']}
- **Voice**: {preset['voice']}
- **Tone**: {preset['tone']}

## Pipeline Status

### Phase 1: Script [ ]
- [ ] Research topic
- [ ] Write {num_scenes}-scene script
- [ ] Create image prompts for each scene
- [ ] Save to `{slug}-script.md`

### Phase 2: Images [ ]
"""

    for i in range(1, num_scenes + 1):
        plan += f"- [ ] Scene {i:02d} — `images/scene-{i:02d}.png`\n"

    plan += f"""
### Phase 3: Voice [ ]
"""

    for i in range(1, num_scenes + 1):
        plan += f"- [ ] Scene {i:02d} — `audio/scene-{i:02d}.mp3`\n"

    plan += f"""
### Phase 4: Assembly [ ]
- [ ] Create timeline
- [ ] Match images to audio
- [ ] Generate subtitles/SRT
- [ ] Prepare for InVideo/editing

### Phase 5: YouTube/TikTok [ ]
- [ ] SEO-optimized title
- [ ] Description with keywords
- [ ] Tags
- [ ] Thumbnail
- [ ] Upload metadata

## File Structure
```
{slug}/
├── {slug}-plan.md (this file)
├── {slug}-script.md
├── {slug}-image-prompts.md
├── {slug}-timeline.md
├── {slug}-youtube.md
├── {slug}-subtitles.srt
├── images/
│   ├── scene-01.png
│   └── ...
└── audio/
    ├── scene-01.mp3
    └── ...
```

## Commands to Run Each Phase

### Generate all images:
```
For each scene, run:
python Scripts/generate_image_leonardo.py "PROMPT" --style {preset['image_style']} --size landscape
```

### Generate all voice:
```
For each scene, run:
python Scripts/generate_voice_elevenlabs.py "TEXT" --voice {preset['voice']} --scene N
```
"""

    plan_path = project_dir / f"{slug}-plan.md"
    plan_path.write_text(plan, encoding="utf-8")

    print(f"\nProject created: {project_dir}")
    print(f"Plan saved to: {plan_path}")
    print(f"\nNext step: Ask Claude to write the script:")
    print(f'  "Write a {num_scenes}-scene script about {topic} for {content_type}"')

    return project_dir


def main():
    parser = argparse.ArgumentParser(description="Content Production Pipeline")
    parser.add_argument("topic", help="Content topic")
    parser.add_argument("--type", default="youtube", choices=["bible-video", "tiktok", "youtube", "short"],
                        help="Content type")
    parser.add_argument("--scenes", type=int, default=10, help="Number of scenes")

    args = parser.parse_args()
    create_project_structure(args.topic, args.type, args.scenes)


if __name__ == "__main__":
    main()

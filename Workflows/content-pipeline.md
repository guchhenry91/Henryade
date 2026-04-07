# Content Production Pipeline

## Purpose
End-to-end content creation: from idea to published-ready video assets.
Orchestrates image generation, voice generation, and video assembly.

## Trigger
User says: "make a video about...", "create content for...", "bible video episode..."

## Full Pipeline Steps

### Phase 1: Script & Planning
1. Research the topic (use deep-research or research-lit skill)
2. Write the script (use article-writing or content-engine skill)
3. Break script into scenes with:
   - Scene number
   - Narration text
   - Image prompt description
   - Duration estimate
4. Save script to `Outputs/{project-name}-script.md`
5. Save image prompts to `Outputs/{project-name}-image-prompts.md`

### Phase 2: Image Generation
For each scene:
1. Run the `generate-image` workflow with the scene's image prompt
2. Use Leonardo AI for cinematic/realistic scenes
3. Use Canva MCP for text-heavy graphics (titles, CTAs)
4. Save all images to `Outputs/images/{project-name}/`
5. Create a visual storyboard in `Outputs/{project-name}-storyboard.md`

### Phase 3: Voice Generation
For each scene:
1. Run the `generate-voice` workflow with the scene's narration
2. Track character usage across scenes
3. If approaching quota limit, alert the user
4. Save all audio to `Outputs/audio/{project-name}/`

### Phase 4: Assembly Preparation
1. Create a timeline document matching:
   - Scene number → image file → audio file → duration
2. Save as `Outputs/{project-name}-timeline.md`
3. Generate InVideo/editing instructions

### Phase 5: Video Assembly (via InVideo)
Use Browser-Use to:
1. Open InVideo AI
2. Upload images and audio files
3. Arrange scenes in order
4. Add transitions between scenes
5. Export final video
OR
Generate Remotion code for programmatic video assembly

### Phase 6: YouTube/TikTok Optimization
1. Generate SEO-optimized title (use seo skill)
2. Write description with keywords
3. Generate tags
4. Create thumbnail (use generate-image workflow)
5. Write subtitles/SRT file
6. Save all to `Outputs/{project-name}-youtube.md`

## Project Structure
```
Outputs/
├── {project-name}-script.md
├── {project-name}-image-prompts.md
├── {project-name}-storyboard.md
├── {project-name}-timeline.md
├── {project-name}-youtube.md
├── {project-name}-subtitles.srt
├── images/{project-name}/
│   ├── scene-01.png
│   ├── scene-02.png
│   └── ...
└── audio/{project-name}/
    ├── scene-01.mp3
    ├── scene-02.mp3
    └── ...
```

## Usage Examples

### Bible Video
```
Make Bible video episode 5 about David and Goliath
```
This will: research the story → write 20-scene script → generate 20 cinematic images → generate 20 voiceovers → prepare timeline → generate YouTube metadata

### TikTok Short
```
Create a 60-second TikTok about [topic]
```
This will: write a punchy 150-word script → generate 5-6 images → generate voiceover → prepare for vertical video

### YouTube Explainer
```
Create a YouTube video explaining [topic]
```
This will: research topic → write 10-minute script → generate supporting visuals → generate voiceover → prepare timeline

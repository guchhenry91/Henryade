# David and Goliath — Content Production Plan

## Project Info
- **Topic**: David and Goliath
- **Type**: bible-video
- **Scenes**: 20
- **Target Duration**: 8-12 minutes
- **Created**: 2026-04-04 21:42

## Presets
- **Image Style**: cinematic biblical art, hyper-realistic, dramatic lighting
- **Voice**: Peter
- **Tone**: reverent, narrative, dramatic

## Pipeline Status

### Phase 1: Script [ ]
- [ ] Research topic
- [ ] Write 20-scene script
- [ ] Create image prompts for each scene
- [ ] Save to `david-and-goliath-script.md`

### Phase 2: Images [ ]
- [ ] Scene 01 — `images/scene-01.png`
- [ ] Scene 02 — `images/scene-02.png`
- [ ] Scene 03 — `images/scene-03.png`
- [ ] Scene 04 — `images/scene-04.png`
- [ ] Scene 05 — `images/scene-05.png`
- [ ] Scene 06 — `images/scene-06.png`
- [ ] Scene 07 — `images/scene-07.png`
- [ ] Scene 08 — `images/scene-08.png`
- [ ] Scene 09 — `images/scene-09.png`
- [ ] Scene 10 — `images/scene-10.png`
- [ ] Scene 11 — `images/scene-11.png`
- [ ] Scene 12 — `images/scene-12.png`
- [ ] Scene 13 — `images/scene-13.png`
- [ ] Scene 14 — `images/scene-14.png`
- [ ] Scene 15 — `images/scene-15.png`
- [ ] Scene 16 — `images/scene-16.png`
- [ ] Scene 17 — `images/scene-17.png`
- [ ] Scene 18 — `images/scene-18.png`
- [ ] Scene 19 — `images/scene-19.png`
- [ ] Scene 20 — `images/scene-20.png`

### Phase 3: Voice [ ]
- [ ] Scene 01 — `audio/scene-01.mp3`
- [ ] Scene 02 — `audio/scene-02.mp3`
- [ ] Scene 03 — `audio/scene-03.mp3`
- [ ] Scene 04 — `audio/scene-04.mp3`
- [ ] Scene 05 — `audio/scene-05.mp3`
- [ ] Scene 06 — `audio/scene-06.mp3`
- [ ] Scene 07 — `audio/scene-07.mp3`
- [ ] Scene 08 — `audio/scene-08.mp3`
- [ ] Scene 09 — `audio/scene-09.mp3`
- [ ] Scene 10 — `audio/scene-10.mp3`
- [ ] Scene 11 — `audio/scene-11.mp3`
- [ ] Scene 12 — `audio/scene-12.mp3`
- [ ] Scene 13 — `audio/scene-13.mp3`
- [ ] Scene 14 — `audio/scene-14.mp3`
- [ ] Scene 15 — `audio/scene-15.mp3`
- [ ] Scene 16 — `audio/scene-16.mp3`
- [ ] Scene 17 — `audio/scene-17.mp3`
- [ ] Scene 18 — `audio/scene-18.mp3`
- [ ] Scene 19 — `audio/scene-19.mp3`
- [ ] Scene 20 — `audio/scene-20.mp3`

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
david-and-goliath/
├── david-and-goliath-plan.md (this file)
├── david-and-goliath-script.md
├── david-and-goliath-image-prompts.md
├── david-and-goliath-timeline.md
├── david-and-goliath-youtube.md
├── david-and-goliath-subtitles.srt
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
python Scripts/generate_image_leonardo.py "PROMPT" --style cinematic --size landscape
```

### Generate all voice:
```
For each scene, run:
python Scripts/generate_voice_elevenlabs.py "TEXT" --voice Peter --scene N
```

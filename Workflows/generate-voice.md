# Generate Voice Workflow

## Purpose
Generate voiceover audio using ElevenLabs via browser automation. No API key needed.

## Trigger
User says: "generate voice", "create voiceover", "narrate this", "generate audio for scene..."

## Inputs
- **text**: The script/text to convert to speech
- **voice** (optional): voice name (default: "Peter" for Bible videos, or user preference)
- **scene_number** (optional): for organized file naming

## Steps

### Step 1: Prepare the text
- Clean up the script text (remove stage directions, brackets, etc.)
- Split into chunks if over 2500 characters (ElevenLabs free limit per generation)
- Number each chunk for ordered assembly

### Step 2: Open ElevenLabs
Use Browser-Use or Playwright to:
1. Navigate to https://elevenlabs.io/app/speech-synthesis
2. Log in if not already logged in
3. Wait for the page to fully load

### Step 3: Select voice
1. Click on the voice selector
2. Search for the target voice by name using aria-label
3. Select it
4. VERIFY the correct voice is selected before generating (lesson learned)

### Step 4: Generate each chunk
For each text chunk:
1. Clear the text input field
2. Paste the chunk text
3. Click the "Generate" button (use aria-label to find it)
4. Wait for generation to complete (watch for the audio player to appear)
5. CHECK if audio was actually generated (don't assume success)
6. Click download
7. Save to `Outputs/audio/` folder
8. Name format: `scene-{number}-chunk-{chunk_number}.mp3`

### Step 5: Report
Show the user:
- Number of audio files generated
- Total duration if available
- File paths
- Characters used vs remaining quota

## Important Rules (from past experience)
- ALWAYS verify the voice selection before generating
- NEVER generate duplicate audio — check if file already exists
- Use aria-label attributes to find buttons reliably
- If generation fails, wait 10 seconds and retry once
- Free tier: ~10,000 characters/month — track usage

## Fallback
If ElevenLabs is rate-limited:
1. Suggest user create a new free account
2. Or use a different free TTS tool (NaturalReader, TTSMaker)
3. Track which accounts still have quota

## Notes
- For Bible videos: use "Peter" voice, narrative style
- Save a log of characters used per session to `Outputs/voice-usage-log.md`
- Chunk splitting should happen at sentence boundaries, not mid-word

# Generate Image Workflow

## Purpose
Generate images using Leonardo AI via browser automation. No API key needed.

## Trigger
User says: "generate image", "create image", "make thumbnail", "generate art for..."

## Inputs
- **prompt**: The image description/prompt
- **style** (optional): realistic, anime, cinematic, illustration, 3D, etc.
- **size** (optional): square, landscape, portrait (default: landscape for thumbnails)
- **count** (optional): number of images (default: 1)

## Steps

### Step 1: Optimize the prompt
Use the `prompt-master` skill to enhance the raw prompt for Leonardo AI:
- Add style keywords, lighting, composition details
- Keep under 500 characters
- Add negative prompt if needed

### Step 2: Open Leonardo AI
Use Browser-Use or Playwright to:
1. Navigate to https://app.leonardo.ai
2. Log in if not already logged in
3. Go to "AI Image Generation"

### Step 3: Generate
1. Paste the optimized prompt into the prompt field
2. Select the model (Leonardo Phoenix or Kino XL for cinematic)
3. Set dimensions based on size parameter:
   - Thumbnail: 1280x720
   - Square: 1024x1024
   - Portrait: 768x1344
4. Set number of images
5. Click "Generate"
6. Wait for generation to complete

### Step 4: Download and save
1. Click on each generated image
2. Download to `Outputs/images/` folder
3. Name format: `{description}-{date}-{number}.png`

### Step 5: Report
Show the user:
- Number of images generated
- File paths
- Preview if possible

## Fallback
If Leonardo is unavailable or rate-limited:
1. Try Canva MCP (`mcp__claude_ai_Canva__generate-design`)
2. Create an HTML thumbnail using ui-ux-pro-max skill
3. Save as HTML in Outputs/ for manual screenshot

## Notes
- Leonardo free tier: ~150 tokens/day (about 30 images)
- For Bible video thumbnails, use "cinematic biblical art, hyper-realistic" style
- Always save prompts used to `Outputs/image-prompts-log.md` for reuse

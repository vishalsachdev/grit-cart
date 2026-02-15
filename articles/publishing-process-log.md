# Substack Publishing Process Log

## Purpose
Documenting every step of publishing an article to Substack via Chrome automation, to inform a future `publish-to-substack` skill.

## Pre-requisites
- Article written in markdown and HTML formats
- Cover images generated (LinkedIn 1200x628, Substack 1100x220, Twitter 1200x675)
- User is logged into Substack in Chrome

## Process Steps

### Step 1: Get browser context
- Tool: `mcp__claude-in-chrome__tabs_context_mcp`
- Purpose: Check what tabs are open, find if Substack is already open
- Note: Must always start Chrome automation with this call

### Step 2: Navigate to Substack new post editor
- URL pattern: `https://{publication}.substack.com/publish/post`
- For The Hybrid Builder: `https://chatwithgpt.substack.com/publish/post`
- Tool: `mcp__claude-in-chrome__navigate` or `mcp__claude-in-chrome__tabs_create_mcp`

### Step 3: Wait for editor to load
- The Substack editor is a rich text editor (ProseMirror-based)
- Need to wait for the editor to be interactive

### Step 4: Set the title
- Find the title input field
- Enter the article title

### Step 5: Set the subtitle
- Find the subtitle field
- Enter the subtitle/description

### Step 6: Paste article body
- The body editor is a contenteditable div
- Options: paste HTML, or use keyboard shortcuts
- May need to use JavaScript to set content

### Step 7: Upload cover image
- Find the cover image upload area
- Upload the appropriate image file

### Step 8: Set section to "The Hybrid Builder"
- Find the section/publication selector
- Select "The Hybrid Builder" section

### Step 9: Save as draft
- The post should auto-save, but verify draft status

### Step 10: Verify
- Check the post preview
- Confirm all content is present

---

## Actual Execution Log (filled in during process)


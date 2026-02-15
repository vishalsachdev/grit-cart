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

### Step 1: Get browser context
- Tool: `tabs_context_mcp` with `createIfEmpty: true`
- Result: Got tabId 885351016 (new tab)

### Step 2: Navigate to Substack editor
- URL: `https://chatwithgpt.substack.com/publish/post`
- Tool: `navigate` with tabId
- Result: Redirected to `https://chatwithgpt.substack.com/publish/post/188053134` (new post created automatically)
- Wait 3s for editor to load
- Screenshot confirmed: Editor loaded with Title, Subtitle, Author, Body fields
- "Choose a section" dropdown visible at top
- Toolbar: Style, B, I, S, <>, link, image, audio, video, pullquote, ordered list, unordered list, Button, More

### Step 3: Select section "The Hybrid Builder"
- Tool: `find` to locate section dropdown, then `computer` left_click
- Click "Choose a section" dropdown at top of editor
- Dropdown shows available sections (e.g., "The Hybrid Builder - When AI Becomes Your Creative Partner")
- Click the desired section
- Result: Section selected, visible at top of editor

### Step 4: Set the title
- **WARNING**: Click coordinates must be precise. Clicking wrong area puts text in wrong field.
- **Recommended approach**: Use JavaScript `document.execCommand` method instead of click+type
- Tool: `javascript_tool`
- Code pattern:
  ```javascript
  const titleEl = document.querySelector('[data-testid="post-title"] div[contenteditable]')
    || document.querySelector('h2[contenteditable]');
  titleEl.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('insertText', false, 'Your Title Here');
  ```
- Result: Title set cleanly without interference with other fields

### Step 5: Set the subtitle
- **Same approach as title** — use JavaScript to avoid click targeting issues
- Code pattern:
  ```javascript
  const subtitleEl = document.querySelector('[data-testid="post-subtitle"] div[contenteditable]')
    || document.querySelector('h4[contenteditable]');
  subtitleEl.focus();
  document.execCommand('selectAll', false, null);
  document.execCommand('insertText', false, 'Your Subtitle Here');
  ```
- Result: Subtitle set correctly

### Step 6: Paste article body (HTML)
- **This is the most critical step** — Substack uses ProseMirror editor
- **Method**: ClipboardEvent with `text/html` data type
- **Must place cursor at end of editor first**:
  ```javascript
  const editor = document.querySelector('.ProseMirror[contenteditable="true"]');
  editor.focus();
  const sel = window.getSelection();
  sel.selectAllChildren(editor);
  sel.collapseToEnd();
  ```
- **Paste HTML via ClipboardEvent**:
  ```javascript
  const clipboardData = new DataTransfer();
  clipboardData.setData('text/html', htmlContent);
  clipboardData.setData('text/plain', plainTextFallback);
  const pasteEvent = new ClipboardEvent('paste', {
    clipboardData, bubbles: true, cancelable: true
  });
  editor.dispatchEvent(pasteEvent);
  ```
- **Chunk size**: Paste in ~4 chunks to avoid issues with very large HTML
- **What works**: `<h2>`, `<p>`, `<strong>`, `<em>`, `<a href>`, `<blockquote>`, `<ul>/<li>`, `<hr>`
- **DOES NOT WORK**: `<table>` — ProseMirror strips table HTML during paste, flattening it into a single paragraph. Use `<ul>` with bold labels instead.
- **HEADING MERGE BUG**: When pasting in chunks, `<h2>` at the start of a chunk often merges into the last `<p>` of the previous chunk. Fix: after all chunks are pasted, scan for merged headings (e.g., `text.The Spark:`) and split them using `insertBefore(h2, nextSibling)` on the parent.
- **X post embeds**: Raw X/Twitter URLs (e.g., `https://x.com/user/status/123`) placed on their own line auto-render as rich embed cards in Substack!
- **Links**: All `<a href="...">` tags preserve their URLs correctly
- **Tables**: HTML `<table>` renders as Substack native tables
- Result: Full article body with formatting, links, embeds, and tables

### Step 7: Upload cover image
- **LIMITATION**: Browser automation `upload_image` tool requires a screenshot ID (browser-captured image), not a local file path
- The file input is found via `find` tool: `label "Upload"` within Thumbnail section (ref pattern)
- The upload area expects 3:2 aspect ratio crop
- **Current workaround**: Manual upload required — user must drag/drop or click upload in Substack UI
- **Future skill consideration**: Could open the image in a browser tab, screenshot it, then upload via `upload_image` tool with the screenshot ID

### Step 8: Verify auto-save
- Substack auto-saves drafts continuously
- Check for green "Saved" indicator in top-left corner
- Tool: `computer` screenshot to visually confirm
- Result: Green dot + "Saved" text confirmed

### Step 9: Verify content
- Tool: `javascript_tool` to check editor body length and section presence
- Check each section heading exists in `editor.innerText`
- Check key links exist in `editor.innerHTML`
- Scroll through post visually with screenshots to confirm formatting
- Result: All 10 sections present, 15,611 chars in body, all links verified

---

## Key Learnings for Future Skill

### What Works Well
1. **ClipboardEvent paste with text/html** is the reliable way to inject formatted content into ProseMirror
2. **JavaScript execCommand** is more reliable than click+type for title/subtitle fields
3. **X post URLs auto-embed** — just paste the raw URL on its own paragraph line
4. **Section selection** works via standard find+click on the dropdown
5. **Auto-save** means no explicit save step is needed
6. **Chunked pasting** (4 chunks of ~4K chars each) works smoothly

### What Doesn't Work
1. **Click+type for title/subtitle** — coordinates are unreliable, text ends up in wrong field
2. **Direct file upload** — browser automation can't access local filesystem for file inputs
3. **HTML `<table>` paste** — ProseMirror strips tables, flattening to single paragraph. Use `<ul>` with `<strong>` labels instead.
4. **H2 at chunk boundaries** — headings at the start of a paste chunk merge into the last paragraph of the previous chunk. Must post-process to split them.

### Recommended Skill Architecture
```
publish-to-substack:
  inputs:
    - article_html: path to HTML file
    - title: string
    - subtitle: string
    - section: string (e.g., "The Hybrid Builder")
    - cover_image: path (manual step flag)

  steps:
    1. tabs_context_mcp (get/create tab)
    2. navigate to {publication}.substack.com/publish/post
    3. wait 3s for editor load
    4. javascript_tool: select section from dropdown
    5. javascript_tool: set title via execCommand
    6. javascript_tool: set subtitle via execCommand
    7. javascript_tool: paste body HTML in chunks via ClipboardEvent
    8. screenshot: verify saved status
    9. javascript_tool: verify all sections present
    10. notify user: "Cover image must be uploaded manually"
```

### Editor Selectors Reference
- **Body editor**: `.ProseMirror[contenteditable="true"]`
- **Title**: `[data-testid="post-title"] div[contenteditable]` or `h2[contenteditable]`
- **Subtitle**: `[data-testid="post-subtitle"] div[contenteditable]` or `h4[contenteditable]`
- **Section dropdown**: "Choose a section" text element
- **Cover image upload**: `label "Upload"` within Thumbnail section
- **Save status**: Green dot indicator top-left


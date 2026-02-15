# The Universal Paste Pattern: Publishing One Article Across Three Platforms with Browser Automation

*How we discovered that Substack, LinkedIn, and Twitter all speak ClipboardEvent — and what broke along the way*

---

We just published 15,000 characters to three platforms in under 10 minutes — with browser automation, not APIs.

No OAuth tokens. No platform SDKs. No markdown-to-platform conversion libraries. Just Chrome, a ClipboardEvent, and a few hard-won bug fixes.

This happened while publishing the [Grit-CART article](https://chatwithgpt.substack.com/p/from-tweet-to-treatise) — a 5,000-word piece about turning a Grok conversation into a research framework. The article was the deliverable. But the *process* of getting it onto three platforms surfaced something more broadly useful: a universal publishing pattern, a catalog of platform-specific bugs, and three reusable skills that will make every future article a 3-minute operation instead of a 30-minute one.

This is the [compound engineering](https://chatwithgpt.substack.com/p/compound-engineering-use-it-before) cycle in miniature: do it live, hit bugs, document them, codify the fixes. Each loop through the cycle reduces friction for the next pass. The Grit-CART article was the first pass. This article is the documentation. The three skills are the codified output.

## The Universal Discovery

Here's the surprise: Substack, LinkedIn, and Twitter all accept rich text the same way.

All three platforms use JavaScript-based rich text editors — Substack and LinkedIn use [ProseMirror](https://prosemirror.net/), Twitter uses [DraftJS](https://draftjs.org/). Despite the different frameworks, they all handle paste events identically. You construct a `ClipboardEvent` with `text/html` data, dispatch it on the editor element, and the platform processes it as if the user pasted from their clipboard.

The universal paste pattern is six lines of JavaScript:

```javascript
const clipboardData = new DataTransfer();
clipboardData.setData('text/html', htmlChunk);
clipboardData.setData('text/plain', '');
const pasteEvent = new ClipboardEvent('paste', {
  clipboardData, bubbles: true, cancelable: true
});
editor.dispatchEvent(pasteEvent);
```

That's it. This works on ProseMirror. It works on DraftJS. It would likely work on any contenteditable-based editor that listens for paste events, because the `ClipboardEvent` API is a web standard, not a framework feature.

The `text/html` MIME type is the key. When you set it, the editor receives structured HTML — headings, bold, italic, links, lists, blockquotes — and maps them to its internal document model. Set `text/plain` to empty so the editor doesn't fall back to plain text.

Why does this matter? Because it means you don't need three different publishing integrations. You need one HTML article and one paste function. The platform differences are in the *preprocessing* and *postprocessing*, not in the core delivery mechanism.

## The Cross-Platform Comparison

We published to all three platforms during a single session. Here's what we found:

- **Editor framework:** Substack and LinkedIn use ProseMirror; Twitter uses DraftJS
- **Body selector:** `.ProseMirror[contenteditable]` for Substack/LinkedIn; `.public-DraftEditor-content` for Twitter
- **Heading level:** Substack and Twitter accept H2 natively; LinkedIn auto-converts H2 to H3
- **Title method:** Substack requires `execCommand` (click+type is unreliable); LinkedIn and Twitter accept click+type
- **Title limit:** Twitter enforces a hard 100-character limit; Substack and LinkedIn have none
- **Subtitle field:** Only Substack has one
- **X embed auto-render:** Only Substack auto-renders raw X/Twitter URLs as rich embed cards
- **Heading merge bug:** Present on Substack and LinkedIn (ProseMirror); absent on Twitter (DraftJS)
- **Table paste:** Stripped on all three — always convert `<table>` to `<ul>` before pasting
- **Recommended length:** Substack and LinkedIn accept full-length articles; Twitter articles should be ~900-1000 words

The good news: paragraphs, bold, italic, links, lists, and blockquotes work everywhere. You can write one HTML article and paste it to all three. The bad news: `<table>` HTML is stripped on every platform. ProseMirror flattens tables into a single paragraph; DraftJS drops them similarly. The workaround is to pre-convert tables to bullet lists with bold labels:

```html
<!-- Before: stripped on all platforms -->
<table>
  <tr><td>Editor</td><td>ProseMirror</td></tr>
</table>

<!-- After: works everywhere -->
<ul>
  <li><strong>Editor:</strong> ProseMirror</li>
</ul>
```

Platform-specific preprocessing adds a few more steps. For LinkedIn, convert all `<h2>` tags to `<h3>` (LinkedIn will do it anyway, but pre-converting avoids inconsistencies). For Twitter, condense the article to ~1000 words and truncate the title to 100 characters. For Substack, leave raw X/Twitter URLs on their own paragraph line — they'll auto-render as embedded posts.

## The Heading Merge Bug

This was the most dramatic bug of the session. After pasting the Grit-CART article into Substack in four chunks, I scrolled through to verify the formatting. The section headings looked wrong. One paragraph ended with:

> "...end of paragraph text.The Spark: Human Direction on X"

A period, immediately followed by a capital letter, with the entire section heading absorbed into the preceding paragraph. No line break. No heading formatting. Just a run-on sentence where a bold H2 should have been.

The cause is a ProseMirror behavior: when you paste HTML that starts with a block element like `<h2>`, ProseMirror merges it into the current block at the cursor position. If the cursor is at the end of a `<p>`, the heading's text gets appended to that paragraph instead of creating a new block.

This happens at every chunk boundary. If you split a long article into four paste operations, you get up to three merged headings.

The fix is a post-processing scan that finds these merged headings and surgically splits them back out:

```javascript
const editor = document.querySelector('.ProseMirror[contenteditable="true"]');
const paragraphs = editor.querySelectorAll('p');
let fixes = 0;
const mergePattern = /([.!?])([A-Z][^.]+:)/;

paragraphs.forEach(p => {
  const match = p.innerText.match(mergePattern);
  if (match) {
    const splitIndex = p.innerHTML.indexOf(match[2]);
    if (splitIndex > -1) {
      const headingText = match[2] + p.innerHTML.slice(splitIndex + match[2].length);
      p.innerHTML = p.innerHTML.slice(0, splitIndex);
      const h2 = document.createElement('h2');
      h2.innerHTML = headingText;
      p.parentNode.insertBefore(h2, p.nextSibling);
      fixes++;
    }
  }
});
```

The regex `/([.!?])([A-Z][^.]+:)/` catches the telltale pattern: sentence-ending punctuation immediately followed by a capitalized phrase ending in a colon (which matches the heading style of the Grit-CART article). For each match, it slices the paragraph at the split point, creates a new `<h2>` element with the heading text, and inserts it after the paragraph using `insertBefore`.

The plot twist: this same bug appears on LinkedIn (which also uses ProseMirror), but *not* on Twitter. DraftJS handles block elements at chunk boundaries cleanly — no post-processing needed. One editor framework's bug is another's non-issue. (One detail: since LinkedIn uses H3 for section headings, the LinkedIn version of this fix creates an `<h3>` instead of `<h2>` — same logic, different element.)

## The Click That Doesn't Click

Setting the article title on Substack should be simple: click the title field, type the text. But browser automation coordinates aren't pixel-perfect. The title, subtitle, and body editor are stacked vertically with thin boundaries between them. A click that's a few pixels off lands in the wrong field, and your title text ends up as the first paragraph of the body.

The fix: skip click+type entirely. Use `document.execCommand` to programmatically select and replace the field content:

```javascript
const titleEl = document.querySelector(
  '[data-testid="post-title"] div[contenteditable]'
) || document.querySelector('h2[contenteditable]');
titleEl.focus();
document.execCommand('selectAll', false, null);
document.execCommand('insertText', false, 'Your Title Here');
```

`execCommand` is technically deprecated, but it still works in every major browser and is the most reliable way to set text in contenteditable fields. It triggers all the same input events that manual typing would, so the editor's internal state stays consistent.

The interesting part: this is only necessary on Substack. LinkedIn and Twitter both accept click+type for their title fields without issues. Each platform has its own automation personality — what works on one may fail silently on another. The lesson: browser automation needs fallback strategies, not universal assumptions.

## From Friction to Skills

During the Grit-CART publishing session, we built three skills: `publish-to-substack`, `publish-to-linkedin`, and `publish-to-twitter`. Each one encodes the platform-specific bugs and fixes discovered during live publishing:

- **publish-to-substack**: Uses `execCommand` for title/subtitle, pastes body in ~4 chunks via ClipboardEvent, runs the heading merge fix, handles section dropdown selection, and flags cover image for manual upload.
- **publish-to-linkedin**: Pre-converts H2 to H3, converts raw X/Twitter URLs to `<a href>` links (no auto-embed), runs the same heading merge fix, and navigates through the "Create new edition" flow.
- **publish-to-twitter**: Condenses articles to ~1000 words, enforces the 100-character title limit, skips the heading merge fix (DraftJS doesn't need it), and builds an optional companion thread.

Each skill is a [Claude Code skill](https://chatwithgpt.substack.com/p/building-shareable-learning-design) — a markdown file that encodes step-by-step browser automation instructions with exact CSS selectors, JavaScript snippets, and known-bug workarounds. They're reusable: the next article goes to all three platforms in minutes instead of half an hour.

This is the broader pattern that keeps showing up in AI-assisted work:

1. **Do it live** — publish manually with automation, hitting every edge case
2. **Document** — capture what broke and what worked in a process log
3. **Codify** — extract the patterns into reusable skills
4. **Compound** — the next iteration starts where the last one left off

The Grit-CART article was the content. The publishing process was the real product. Three platforms, one paste pattern, a handful of bugs, and three skills that make the next article almost effortless.

That's compound engineering at work: you don't just ship the thing — you ship the process that makes shipping the next thing faster.

---

*This article was published using the skills it describes. The cover images, markdown, and HTML were generated by Claude. The publishing was automated via Chrome browser automation. The meta-level cycle continues.*

*Part of [The Hybrid Builder](https://chatwithgpt.substack.com/) — a newsletter about building with AI as a creative partner.*

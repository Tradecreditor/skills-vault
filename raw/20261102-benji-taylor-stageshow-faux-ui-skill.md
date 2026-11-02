---
slug: 20261102-benji-taylor-stageshow-faux-ui-skill
source_url: "https://x.com/benjitaylor/status/2116593247854453244"
canonical_id: "x:tweet:2116593247854453244"
fetched_at: "2026-11-02T08:50:00Z"
reader: "api.fxtwitter.com (post) + Jina Reader (benji.org/stageshow) + raw.githubusercontent.com (README, SKILL.md head)"
captured_by: routine:weekly-hot-list
---

```json
{
  "post": {"url": "https://x.com/benjitaylor/status/2116593247854453244", "author": "benjitaylor", "date": "2026-10-31", "likes": 12651, "reposts": 622, "views": 1187405, "bookmarks": 22900, "quotes": 223, "replies": 410},
  "repo": {"full_name": "benjitaylor/skills", "stars": 591, "forks": 28, "created_at": "2026-10-26T06:08:56Z", "as_of": "2026-11-02"}
}
```

# X post by @benjitaylor (verbatim, fxtwitter)

Stageshow: a skill that helps your agent make better faux UI stills, animations, bento grids, and more. 

npx skills add benjitaylor/skills --skill stageshow

# benji.org/stageshow (verbatim, Jina Reader)

31 October, 2026
Stageshow is a skill that helps your agent make better faux UI.[1](https://benji.org/stageshow#user-content-fn-1) Most good models can do this now without a dedicated skill, but the results often look sloppy and heavy-handed, and that's the gap Stageshow is for.

Made with Stageshow.

I've made a lot of these by hand, and they take far longer than they should. No single part is especially hard, but there are a hundred small decisions and every one of them shows. Stageshow is my attempt to write those decisions down, so an agent can make them too.

## Getting started

`npx skills add benjitaylor/skills --skill stageshow`

That adds the skill for any agent: Grok Build, Claude Code, Codex, Gemini, etc. Then ask for something small: one interaction, in one product, at one size.

`A small looping demo for our homepage hero: someone assigns an issue to a teammate.`
The agent reads the skill, starts from the closest example, builds the demo, then films it and fixes what it finds. What you get is an ordinary React component, so you can put it anywhere and change it like the rest of your code.

It still may not nail it in one shot. The first pass is usually a big step up from what an agent makes on its own, but most demos still take me a few rounds of feedback.

fair warning

## What's in it

What the agent works with.

What the agent reads first: the one idea, the five ways faux UI fails, a seven-step workflow, a table of the gold examples, the kit at a glance and a summary of framing.

Craft (restraint, type, spacing, colour), motion (story, pace, the cursor), framing (crops, satellites, layouts), grids, looks and backgrounds, annotations, real products and brand marks, filming and the checklist, good and bad pairs side by side, and every kit part's props. Most rules came from reviewing real attempts, and each gives its reason.

Dozens of gold examples the agent starts from and holds its work against, from a hero demo and bento grids to a phone swipe and a dashboard paired with a lock screen.

A small set of React parts the agent can build with, plain code that lives with your demo. It makes the hard parts hold up; it doesn't supply a look. The stage, windows and phones drawn from real geometry, motion that has to survive frame by frame, and a few quiet parts to restyle.

film.mjs films a demo, lays the frames on a contact sheet and reports what it can measure. jumps.mjs catches one-frame snaps a sheet misses, and layout.mjs checks that text and controls fit their boxes.

## The playground

The skill also comes with a playground. Run it from the skill's folder:

```
npm install
npm run dev
```

It has every example in the skill, the kit's parts on their own, and a set of comparisons: the same thing done badly and done well, side by side. They're there for the agent as much as for you. "Don't shrink the whole app into a card" is easy to agree with and easy to skip, but much harder to ignore once you see both side by side.

## What the skill teaches

The skill is built around one sentence:

It reads as a real product, simplified to what the viewer needs, framed with intent, and every motion has a cause.

the whole skill, really

Faux UI from agents tends to go wrong in the same few ways. The most common are _too much_ (real words in every cell, packed tight), _too little_ (a wireframe that doesn't read as a product) and _boxed_ (the whole window shrunk into a card, like a pasted screenshot). Then there's _flat_, where everything has the same weight, and _bland_, where the brief's style never shows up.

Here's one demo going from the first to the last, the way the agent builds it: someone assigns a support conversation to Maya.

1 Screen 2 Frame 3 Script 4 Cursor 5 Loop

The whole screen in quiet greys, real words only where the story is. Correct, but boxed in like a screenshot.

Left to itself, an agent drifts toward the first. It knows what a support inbox contains, so it fills every row. The skill has it keep only the words the story needs and use placeholder lines for the rest, so the inbox still looks full without asking you to read it. It also decides the crop first, so it doesn't waste time building things nobody will see.

## How a demo is built

Every demo is a stage: a canvas with a design size. Its contents are drawn from state, and a script changes that state one beat at a time. The cursor is part of the stage, and it aims at things by name.

The code below, drawn out: the stage crops the window, the cursor aims at a name, the state flips, and each beat lights as it runs.

```
async function script(a: Act<S>) {
  await a.click({ at: "share" }); // arcs there, presses
  await a.set({ open: true }); // resolves once painted
  await a.wait(2000); // the payoff holds
  await a.click({ at: "close" });
  await a.set({ open: false });
  await a.move({ x: 600, y: 300 }); // back where it began
}
```

Parts stay mounted while they transition, so they can move in and out instead of popping. Positions are measured, so the cursor lands in the right place and overlays line up at any size. And the kit handles the motion that's hard to get right by hand, like a number that rolls only the digits that changed, a card flying into a slot, or a message forming out of the text field.

There's also a camera, so a stage can push in on the important bit and pull back out. It sits on top of the scene, so you don't have to change the scene to use it.

Forty days of uptime. The camera pushes in on the one bad day, then pulls back out.

A look is a theme, a palette and how many real words there are. They're props on the stage, and they work by swapping the kit's colours, so a scene is written once and every look follows.

One scene, written once. Light, dark, blueprint, then minimal, where the real words become lines.

A look can also come from your own design system. The kit's colours, type, radii and spacing are all design tokens, so the agent reads your product's tokens and maps them onto the kit's. The demo then uses your real colours, fonts and corner radii, and sits next to the actual product without looking like a mock-up of it.

## How the agent works

The skill gives the agent a workflow. Most of it happens before any code is written.

| Step | What gets decided |
| --- | --- |
| 1. Medium | Still or animation, looping or playing once, where it sits on the page and at what size. |
| 2. Look | Light, dark, blueprint or glass; one accent or mono; the chrome the product really has, and its real icons. |
| 3. Story | How it feels to use, a flow through an app, or what the system does on its own. Then three to five beats. |
| 4. Examples | The closest gold example, copied and made the brief's product: what is cropped, what straddles what, one gutter. |
| 5. Screen | The few real strings, and placeholder lines for everything else. |
| 6.Choreograph | Beats that overlap, groups that stagger, and a loop that ends exactly where it began. |
| 7. Rehearse | Film it, read every frame, check it at phone width, watch the loop seam. Then hold it next to the closest gold example. |

## Why checks matter

Agents increasingly check their work, but usually by reading the code back or taking a screenshot once it has settled. Neither shows the motion in between, which is where the bugs often are: a pill that hops 4px on its way in, or one frame where everything has faded out. Stageshow has the agent film the demo instead, as a contact sheet of the whole sequence with a report that flags anything it can measure, and then watch the playback for what a report can't catch.

A contact sheet the way film.mjs lays one out. The last frame is flagged, and the report says why.

## Making Stageshow

To test it, I'd give a fresh agent the skill and a short prompt, and nothing else. Then I'd give the same prompt to an agent without the skill, so I could compare the two side by side.

Whenever something looked off, I resisted fixing it myself. Instead, I'd write down what was wrong, update the skill, and run the whole round again from scratch. I did this a lot.

Below are some examples. Without Stageshow, even the best models go overboard. Sometimes the result is close, and one detail makes it look sloppy, like a clumsy cursor or a fake iOS status bar. Sometimes it's worse, with elements overlapping or out of line. With it, I get something much closer to what I'd make myself. It's opinionated, though, and a lot of it is just my taste.[2](https://benji.org/stageshow#user-content-fn-2)

A diagram for API docs

“A static illustration for Hookline's API docs, in blueprint style: how a webhook travels from Hookline's servers to a customer's endpoint, fails once, is retried, and is acknowledged.”

Without Stageshow

With Stageshow

A dark bento grid

“A static dark bento grid of four tiles for Kanso, a project management app, for one dark section of its homepage. Greyscale, very little text, premium and quiet: one tile shows a piece of the app, the others a stat, an object and a small diagram.”

Without Stageshow

With Stageshow

An AI writing app

“An animated hero for Draftwell, an AI writing assistant that is a native Mac app: the user selects a paragraph, asks Draftwell to make it shorter, and the rewrite streams in and replaces the original. Loops.”

Without Stageshow

With Stageshow

A spike on a dashboard

“An animated hero for Signalboard, a product analytics tool: a wide dashboard with several charts, something spikes on one chart, and the view pushes in on that chart to show the tooltip and an annotation explaining the spike, then eases back out. Loops.”

Without Stageshow

With Stageshow

A message on iPhone

“An animated landing page demo for Hearth, a team chat app, on iPhone: a message arrives on the lock screen, the user taps it, Hearth opens to the conversation, and they send a quick reply. Crop the phone: it runs off the edge of the frame, never shown whole. Loops.”

Without Stageshow

With Stageshow

A meeting across two screens

“An animated homepage section for Tandem, a scheduling tool: someone books a meeting in Tandem's web app on a laptop-sized window, and a moment later the invitee's phone shows the invitation and they accept it. Crop the phone so it runs off the edge of the frame, never shown whole. Loops.”

Without Stageshow

With Stageshow

Rules alone only got so far. An agent told to run a window off the edge of the frame barely does it. Shown an example that does, it gets it right. So the skill ships with examples to copy from. Here's a tour, starting with the two things nearly every demo has: a window and a cursor.

## Windows

The window is usually the hero, so its chrome is the first thing that tells you what you're looking at. Put an address bar on a native Mac app and the whole picture reads as made up. There's no `kind` prop: the chrome follows from what you pass, and the traffic lights sit in exactly the same spot in every one.

A browser, a browser with tabs, an app, and an app with a toolbar. The background tab gets a new email.

## Glass

For a product page there are lighter browsers too. Glass is frosted, so it takes the colour of whatever is behind it.

Inspired by Stripe.

## Quiet

The quiet browser (`chrome="card"`) is one white card under a long soft shadow, for when the rest of the page is already busy.

A checkout, centred in the card, running off the bottom.

## macOS 26

A product shown on the newest macOS gets the newer window: bigger lights, a floating sidebar and the tall toolbar.

Large lights, a floating sidebar and the tall toolbar, on glass. One invoice is picked.

## Cursors

A cursor should move like a hand: shallow arcs timed by distance, with presses you can see. Pick one style for a whole site, so every demo on a page points the same way, and the script doesn't change between them.

Four of the cursor styles: large, circle, arrow and real. You can also leave the cursor out, and the changes play on their own.

It also changes shape as it crosses into an element, like a real one would. Each element says which cursor it wants, so the script doesn't have to.

An I-beam over search, a hand on Publish, an open hand that closes as the card is dragged, a crosshair on the canvas.

## Hero demos

Then the demos themselves, all made with Stageshow, starting with hero demos: the big animated story at the top of a homepage.

A customer subscribes, the price flies into the billing dashboard as a new row, and monthly revenue rolls up.

A form fills itself in, the strength meter steps up, and the app opens.

A card moves to Won, revenue counts up, and the rep's phone lights up.

A meeting is dragged to Wednesday and the attendees confirm.

An invoice rises in, a plan card links to it, usage bars grow, and a tier switch rolls the price. Slow and overlapping.

## Feature cards

Small cards that show one feature, for a grid of them.

Plays on hover: an email is snoozed until tomorrow and the list closes up.

A reply with a small diff you can apply.

A pointer scrubs along the revenue line, and the headline reads out each day.

An amount is corrected in place, and the total rolls to match.

Two teammates in one doc, each in their own colour.

A card dragged across a calendar. The slot jumps from cell to cell instead of chasing it.

## Phones

Phones are driven by touch instead of a cursor, so the motion is different.

A fitness app, driven by touch. The workout card opens into its screen as one object.

Swipe to archive. The row leaves at the speed the finger let go.

Built from screenshots of Telegram. A reply forms out of the field, its clock turns to one tick, then two.

A dashboard with a phone straddling it. A still.

A delivery's Live Activity. The island springs between sizes, and a timer buds off it.

## Annotations

Sometimes a demo needs to point at something: what a point on a chart means, where an event went, which setting changed what. I try to keep these to a minimum, though. The product should still be the main thing, and each line should say one thing.

Three usage sources feed one invoice, and the dots keep flowing once it updates.

A test event goes out to the server, and the reply comes back to the button that sent it.

A card is stretched, and the size, the inspector and the spacing below all follow.

## Grids

Bento grids usually go wrong by treating every tile the same. Each one gets its own little window, and the section ends up reading as a wall of screenshots. Stageshow plans the grid as one picture instead: only a third to a half of the tiles show UI, window chrome appears once, and no tile sits next to another of the same kind.

One window, a stat on the dark tile, a card as an object, one control and a diagram.

## Real products

Products you already know are the hardest test, because any wrong detail jumps out. Most of these started from a single sentence.

Linear. ⌘K, “assign”, Assign to me: the camera leans in as the avatar lands.

Google Docs. A sentence is highlighted, commented on, and answered in the margin.

Slack. A message gets a reaction, then a reply that opens a thread beside the channel.

Figma. A button is recoloured from the fill picker while a teammate looks on.

Raycast. The launcher finds Clipboard History, and arrowing through it previews each entry.

Spotify. A double-click moves playback to the next song.

Notion. A slash command makes a to-do, which gets ticked off.

Google Calendar. An afternoon is dragged out and the event saved.

Finder on macOS 26. A folder opens in column view, and Space previews a photo.

Excel. AutoSum totals a column, and the chart picks it up.

## Limitations

The checks catch mistakes, not dull ideas. A demo can pass every one and still not be worth watching, so you still have to look at it yourself.

It also can't draw, so anything that needs illustration or photography is better made by hand and dropped in.

Most of the rules started as a note on a real demo, like "the shadow is too harsh" or "this title isn't centred." Once a note is in the skill, every demo after it gets it for free. You can do the same: when you correct a demo, ask the agent to add the note to the skill.

## For now

Model taste is getting better with every release, and I suspect a skill like this is only useful for a while, since much of what it teaches and includes could soon come built in.

Some of it already has. Early on in making this, the references had rules a newer model simply didn't need, like keeping the traffic lights the right size, and as the models improved those rules quietly stopped doing anything.

Others have held up across every model I've tried, mostly the ones about framing and motion. Models are perfectly capable of getting those right, but they don't seem to know that they matter until something tells them.

Until then, it helps, and every demo made with it is a small, well-built example of this kind of UI, which is the sort of thing models learn from. If it plays a small part in making itself unnecessary, that's fine by me.

If you want to give it a go:

`npx skills add benjitaylor/skills --skill stageshow`

## Footnotes

1.   The products shown in the demos, along with their names, logos and interfaces, belong to their owners. The demos are illustrations made for this post and aren't affiliated with or endorsed by them. [↩](https://benji.org/stageshow#user-content-fnref-1)

2.   Taste sounds mysterious, but most of it is small decisions made over and over until you know which ones hold up. That's why it can be written down. It also means Stageshow is my taste, not a neutral one. [↩](https://benji.org/stageshow#user-content-fnref-2)

# benjitaylor/skills — README (verbatim)

# Skills

Skills I use with coding agents for design and motion work.

## Stageshow

![Product UI illustrations made with Stageshow](.github/assets/stageshow.png)

Helps your agent make faux product UI that looks like the real product: stills,
feature cards, cursor demos and bento grids, built in React. It includes guidance
on composition and motion, a kit to copy from, examples, and tools that film the
result so the agent can check its work.

```sh
npx skills add benjitaylor/skills --skill stageshow
```

[How it works](https://benji.org/stageshow) · [Read the skill](stageshow/SKILL.md) · [Preview the examples](stageshow/README.md#preview)

Each skill includes its own licence and any third-party asset notices.

# benjitaylor/skills — stageshow/SKILL.md (verbatim)

---
name: stageshow
description: Build faux product UI that looks like a real product, as a still illustration or an animated demo with a cursor. Browser and app windows, dashboards, phones, notifications, terminals, bento grids and cursor walkthroughs, framed, masked and cropped the way a marketing page, feature card or docs hero needs them. Use whenever someone wants a fake or mocked UI, a product demo or walkthrough animation, a hero or feature-card illustration of an app, a product shot in the style of a polished marketing site, or an animated cursor doing things in an interface, even if they never say "faux UI". React and plain CSS.
---

# Stageshow

Miniature product UI: a believable interface, framed in its space, as one still or a short animation in which one thing happens. The viewer recognizes the screen and sees the thing happen.

## The one idea

**It reads as a real product, simplified to what the viewer needs, framed with intent, and every motion has a cause.**

Five ways it fails:

- **Too much.** Real text in every row, numbers everywhere, everything packed. The more detail, the more it looks generated.
- **Wireframe.** Two gray blobs and a button. Built too small, or stripped of what made it recognizable.
- **Boxed.** A whole window shrunk into a card with even margins: a screenshot pasted in, not a product shot.
- **Flat.** Every object the same weight in the same bordered card. The eye has nowhere to land.
- **Bland.** A gray window with a cursor, whatever the brief said. The brief's look and energy (a blueprint, glass over color, a Dynamic Island, a mascot) are the point; take what it asks for and build it to the rules, as `examples/hero-demo` does with its typed popup and terminal satellite (a satellite is a smaller second object, a receipt, phone or detail card, straddling the hero's edge).

The fix: a full, structured screen in quiet grays, real words only on what the story is about, placeholder lines for the rest, room to breathe, a crop that puts the eye where the story is. Simplify the words, not the context. An empty corner, a void under a list, rows spread to fill a pane, a window floating on a plate (a backdrop or tinted field behind it): unfinished, not calm.

These are authored illustrations, not browser automation: `a.click()` draws the cursor pressing, `a.set()` changes the scene.

## How hard to press

Build it the way a product designer builds a launch page they will be judged on. The gold examples in `examples/` are the bar, not a reference: if yours is the emptier, flatter or smaller one beside the closest gold, that is the first fix. Then look at the frame the way the most exacting designer you know would, the one who screenshots the one wrong thing and sends it back with "what is this?": a dot off its avatar, a unit on its own line, a grabber under the island, copy touching a card. If you can picture that screenshot, you have found the next fix.

## Workflow

Most of the quality is decided before any code. Write the plan first: where it sits, the focal object, the action, the payoff, what can be left out.

1. **Medium and place.** Still or animation (loop, once in view, or hover). The page, its ground, its width. Design at the size it will be seen, about 720 × 340 for a hero beside copy (`hero-demo`), 900 to 1100 wide for a full-width hero (`linear`), 400 × 300 for a card, shown at 1:1; never under about 320 wide for a demo, though a bento tile or a satellite card may be smaller. Every demo that can sit in a phone column ships a `compact` design at the column's width (358), a redesign not a squeeze (`references/framing.md`, Small formats and the page). A grid of tiles is one set: plan it with `references/bento.md`.
2. **Look.** With the product's code or site at hand, map its tokens to the kit's (`references/looks.md`); if the developer asks for their own components, use them inside the stage instead of the kit's small parts. Otherwise a theme (light, dark, blueprint, glass), a palette (accent, mono) and a fidelity: `minimal` is all bars, `standard` is words where they carry meaning and bars elsewhere, `realistic` is real content everywhere. Default light, accent, standard; go realistic at hero scale, for a named real product, or a still whose subject is a list or page. Write filler once with `Text filler` and the fidelity decides. The product's own icons, its real chrome, the content that makes it recognizable. A brief with a style (kawaii, paper, a poster color) gets that style in full, still built to these rules.
3. **The story.** Its shape (`references/motion.md`, Story): how it feels to use, a flow, or what the system does. Three to five beats and a payoff, 10 to 16 seconds. No cursor move you can't explain. Data never rewinds in view without a cause. Between a richer story and a calmer frame, choose the frame.
4. **Start from an example.** Find the closest gold example (the Gold table below) and film it (`node scripts/film.mjs "<preview>/?capture=<gold>" --select '#example' --still --out gold.png`; `npm run dev` serves the preview). Copy its folder into your project as the starting point; don't rewrite it from a glance. The quickest loop: copy it to `examples/<yours>/` here, where the preview picks it up and `?capture=<yours>` films it, then move it into the host when it passes and fix its kit import path. Keep its structure: the stage size, the crop and bleed, row and type sizes, spacing, the script's beats, the kit parts. Now read `references/craft.md` in full: it is short, and it holds the still-frame rules the gold can't show you, the cases your gold doesn't happen to contain. Then replace its look and content with the brief's product: the tokens from step 2, the product's own icons, chrome and words. A copy that only changes the name is not done: it should read as the brief's product, not the gold's. If no gold tells your story, choose in two parts: the layout first (pick it from the table in `references/framing.md`; each layout names its example), and copy that example even though its story differs; then borrow the motion for your beats from the example whose story is closest, and build what neither has in the same style. Then frame it: crop to the panel the story happens in, judged in the final visible crop (`references/framing.md` has the rules and the layout table). The short form: one gutter, a full one or well past; only filler bleeds; what opens stays in; windows keep their shape; the page is the ground, so no plate under a hero on a white or dark page and no window whole with air on four sides; `unframed` only when the developer asks; no dead corners. Film one still at both widths beside the gold's; if yours is emptier, flatter or more boxed, fix the frame before any motion.
5. **The screen.** Count the real strings, usually 3 to 7 (`references/craft.md`, Restraint): a budget for words, not elements. Build with the kit's tokens, `Bar`, `Text` and `Row`. Fit every control's text before it moves. Mark what the cursor touches with `data-target` and `data-cursor`; measure with `rect()`, never hard-code.
6. **Choreograph.** The `Act` API. Keep what appears mounted and toggle it so exits animate (`Bubble` and `Fly` hand off explicitly). Animate the relationship, not just the object: a new row carries the rows below it, a surface that resizes never stretches its text. Beats overlap, groups stagger, the payoff holds, the loop ends where it began or resets with a visible cause.
7. **Rehearse.** Set `poster` first: most people see only that frame (a thumbnail, reduced motion, a screenshot), so it is the beat that tells the story on its own, never one caught mid-change, with the result left on screen rather than tidied away (`references/motion.md`, Story). Then film the loop, not just a still: the contact sheet at the shown width and at 390, and step through every press, menu, morph and the loop seam (`references/rehearse.md`). A still can't show a pop. Read every frame, fix the largest visible fault first (framing, then hierarchy, then motion, then polish), re-film. Then hold it next to the closest gold and answer the whole-composition and style pairs in `references/teaching.md` as questions about your still (what does the eye land on first, and is it the result? is one window, tile or device clearly leading?); any no is the largest fault. `film.mjs --gate` ending `rehearsal passed` is necessary, not sufficient. Then run the last pass in `references/rehearse.md`: a fresh-eye review (`references/review.md`) and `REHEARSAL.md` beside the component (template in `references/verify.md`, Hand over): the gold you copied, what you changed, what you did not check.

Faults that come back every round, each with its rule; check them before handing over:

- **Content that swaps** instead of moving (`references/motion.md`, Changing text and values).
- **Gray bars where the eye lands;** filler belongs at the edges (`references/craft.md`, Restraint).
- **A plate behind the window, or a window floating** with air on four sides; the window or phone fills at least two thirds of the stage and runs off an edge (`references/framing.md`, rule 5 and Small formats and the page).
- **Empty bands, cut controls and shadows** (`references/craft.md`, Restraint; `references/framing.md`, rule 4).
- **Stock AI and made-up logos:** sparkles, purple, a letter in a colored square (`references/craft.md`, Icons and logos).
- **Busy rows and uneven insets** (`references/craft.md`, Restraint and Spacing and alignment).
- **Long holds and a reset with no cause** (`references/motion.md`, Loops).
- **A selection that isn't under the I-beam** (`references/motion.md`, Drags and selection).
- **A status bar or home indicator drawn by hand;** the Phone draws both (`references/craft.md`, Chrome and devices).
- **A centered amount centered with its sign** (`references/craft.md`, Spacing and alignment).

## Examples

Film the closest one before you start (step 4). The gold examples are the quality bar; product studies are for borrowing an interaction, never another product's identity; specimen sheets are catalogs, not compositions. Run everything with `npm install` and `npm run dev`. `teaching/` holds bad/good pairs (`references/teaching.md`) for diagnosing a problem; the bad halves are never starting points.

### Gold

| Need | Example | What to learn |
|---|---|---|
| Still or feature card | `static-card` | Quiet hierarchy, a hard crop, one satellite, real words only on the selected customer, its neighbors and the total |
| Dark still | `dark-bento` | One signal said once; album art keeps it a music app |
| Animated hero, a gesture | `hero-demo` | Five beats, named targets, an annotation, a terminal coming forward |
| Choreography, no cursor | `payout-flow` | Slow overlapping arrivals, reading time, a payoff that holds |
| Content changing in place | `choreography` | Retained tracks, soft masks, dependent timing |
| AI answer | `ai-chat` | The question sent, Thinking, the answer streaming in with its height, sources last; no sparkles, no purple |
| AI with cards | `ai-cards` | A multiple-choice card answered and kept as the record, a card of options opening in the thread, booked from its own button |
| Form validation | `form-error` | An error on the field that caused it, cleared by fixing it, then the button confirms on itself |
| Drag to reorder | `reorder` | A row lifted by its grip, the others making room, dropped into place |
| Chart scrub | `chart-scrub` | A hairline and dot that follow the pointer, the headline value rolling to the day under it |
| Edit in a table | `table-edit` | A cell edited in place, then the total it feeds rolls a beat later |
| Loading to content | `loading` | A skeleton at the content's own geometry, rows resolving top to bottom, real chrome throughout |
| Dark hero | `dark-hero` | Depth from surface steps on black, one lit color, a status that changes on its own pill |
| Live collaborators | `presence` | Each person one color everywhere, names riding their cursors, work shown in the doc's own marks |
| System story | `subscriptions` | A chip flies into a row, MRR rolls, a second scene is the reset |
| Close-up | `close-up` | One control at 1.4x with its window's chrome, the row whole, a large cursor to match |
| Many of one | `many-of-one` | A grid of one thing off every edge, one tile in focus by depth, the only one with words |
| Fade crop | `fade-crop` | A window fading out at its foot, over filler, instead of running off an edge |
| Panel over product | `panel-annotation` | A settings panel over the product's margin, one leader from the setting to what it changed |
| Overlapping windows | `overlap` | A card in front of a window, its edge on the window's sidebar line |
| Stacked cards | `stacked-cards` | Two components at one width, a small gap, the lower one off the bottom |
| Opposite corners | `opposite-corners` | A bento tile: copy bottom-left, the product hung from the top-right corner |
| Tilted stack | `tilted-stack` | A loose pile of paper, small alternating angles, only the top card has words |
| Corner chip | `corner-chip` | A small chip centered on a window's corner, half outside |
| Monochrome | `monochrome` | Other companies' products in a row, grayscale, faded at the foot |
| Row of windows | `window-row` | Sessions side by side at one height: focus by depth, neighbors cut by the stage, only filler cropped |
| Window and phone | `device-pair` | A dashboard and a lock screen telling one event; the phone straddles over margin, never over the figure |
| Related objects | `story` | An invoice, a plan, a connector, rolling totals |
| Calendar drag | `calendar` | A populated week, one focal event, a measured pickup |
| Free dragging | `freeform-drag` | Grab offset, a measured grid, a drop slot that snaps |
| Phone app | `phone-touch` | A card opens into its screen as one object, and the loop folds back |
| Dynamic Island | `dynamic-island` | One black shape, its content a separate layer |
| Messages | `messages` | Composer, typing, receipts, a bubble's lifetime |
| Cursors | `cursors`, `cursor-morph`, `cursor-resize` | Five styles, element-driven kinds, resize edges and corners, no cursor at all |
| Annotations | `annotations` | Leaders, dimensions, flows and a moving target; `references/annotations.md` |
| Feature grid | `bento` | One hero, one window, a stat, an object, a diagram |
| Dark ruled grid | `ruled-bento` | Shared rules and technical imagery |
| Consumer grid | `staggered-bento` | Offset tiles, graphic art, physical objects |
| Image-led hero grid | `hero-grid` | Different grounds and materials composed as one picture |
| Upload | `upload` | A file dragged in from the desktop, an upload row with progress that settles as a file row |
| Share | `share` | A share popover over a document: an email becomes a chip, a role menu, a person added to the list |
| Swipe | `swipe` | A phone swipe to archive: press, swipe, a throw at the finger's speed, the gap closes |

### Product studies

Recognizable products (Figma, Linear, Slack, Raycast, Finder, Spotify, Notion, Gmail, Google's apps, Office, Wikipedia, Telegram, iMessage): read `references/products.md` first. Borrow the interaction, not another product's identity.

| Need | Example | What to learn |
|---|---|---|
| Design tool | `figma` | Canvas selection, a color picker, a second cursor |
| Issue tracker | `linear` | Command menu and assignment |
| Chat | `slack` | Messages, a reaction, a thread reply |
| Launcher | `raycast` | Search and clipboard history over a blurred desktop |
| Files | `finder`, `finder-glass` | Quick Look over a file list; a file moved into a folder; the same window in frosted glass |
| Music, dark | `spotify` | A dark desktop app with album art |
| Docs and editors | `notion`, `google-docs` | A slash command; a comment and its reply |
| Email | `gmail` | Hover actions, archive, an undo toast |
| Calendar, real app | `google-calendar` | Drag to create an event, the quick-create popup |
| Office | `powerpoint`, `excel` | Slide editing; AutoSum and a chart |
| Browser page | `wikipedia` | Search suggestions in a browser |
| Phone conversations | `telegram`, `imessage` | Native chat apps on an iPhone |

### Specimen and reference sheets

Catalogs of parts and grounds, described in `references/kit.md` (Specimen sheets). Look up a part here; compose from a gold example.

| Need | Example | What to learn |
|---|---|---|
| Kit specimens | `chrome`, `phones`, `controls`, `parts`, `kit-extras` | Every frame and part |
| Glass | `glass` | Frosted surfaces over a color field |
| Backgrounds | `backgrounds` | One interface over twenty grounds; `references/backgrounds.md` |
| Logos | `brand-marks` | Real marks, optically sized, on light and dark; `references/brands.md` |
| A product's look | `looks` | Type, shape and color working together |

## The kit

Copy `kit/` into the project and import from `kit/index.ts`. React, react-dom and lucide-react (for `Icon`, which `Field` and `Chip` use); each part brings its own CSS. It does the parts that are hard to get right by hand and leaves the product's look to you. `references/kit.md` has every part's props and rules; read the entries for the parts you use.

- **The stage.** `Stage`: design size and scale-to-fit, `compact`, scene state, playback, the look, the cursor. The script gets an `Act` (`set`, `wait`, `move`, `click`, `type` and the rest: `references/kit.md`, Act).
- **Frames.** `Window`, `Phone` with `LockScreen` and `Notification`, `Keyboard`, `Thread` with `Bubble`, `Stamp`, `Receipt`. Real geometry; never draw a window, device or bubble by hand.
- **Motion.** `Collapse`, `Roll`, `Swap`, `Count`, `Connector`, `Fly`, `Follow`, `States`, `Stream`, `Popover`, `Scroll`, `Camera`, `Expand`. They handle the frames a cold hand gets wrong.
- **Small parts.** `Bar`, `Text`, `Row` (every list is made of it), `Avatar`, `Pin`, `Icon`, `Menu`, `Field`, `Segmented`, `Toggle`, `Tabs`, `Badge`, `Chip`, `BrandMark`, `Code`, `Chart`. Quiet starting points; restyle to the product, never reshape a kit part's geometry from outside.
- **`stageshow.css`**: tokens, looks, edge fades, chrome, phones, keycaps.

## The references

`references/framing.md`: the framing rules and the layout table. `references/craft.md`: the still frame (restraint, type, spacing, icons, color, chrome). `references/motion.md`: story, loops, pace, the cursor and drags. `references/verify.md`: the checklist with a you-see / you-do table. `references/rehearse.md`: how to film, and the film lines that are never intentional.

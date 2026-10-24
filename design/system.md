# Proof, the RoleFit design system

RoleFit is a local tool. You paste job descriptions. It lists the skills they ask for, ranks those skills across the set, and shows the gaps against one résumé. Each gap quotes the line it came from. The name of this system is Proof: the screen is the evidence, not a pitch.

The frontend imports `design/tokens.css`. The same values are in `design/tokens.json`, including the contrast ratios. Do not invent a second palette in a component.

## Limits

This is an open-source portfolio project. The interface has no pricing, billing, plans, trials, upgrade banners, or a marketing signup. Sign-in is one local account for the instance you are running. See that screen below.

Also refused, because they are the default look of a generated UI kit: a purple accent, a gradient, emoji as icons, drop shadows, pill badges, and a hero with three cards. The app opens on the work.

Dark mode is out of scope. The main task is reading a long paste. One light theme, done carefully, is the MVP.

## Type

Two families.

**Schibsted Grotesk** is the UI face. It is a newspaper grotesque, drawn for columns of facts, and it is not the usual default UI font. Use it for navigation, headings, buttons, the finding at the top of Market and Gaps, and quotes.

**IBM Plex Mono** is the data face. Use it for the pasted description, the résumé paste, counts, ranks, citation locators (`Harbor Payments · Backend engineer · Required`), and the word “Demo” on the sleep notice. A number inside a sentence stays in Schibsted. Changing font mid-sentence looks fiddly. Both fonts are SIL Open Font License. Files and licenses are in `design/fonts/`.

| Token | Size / line | Weight | Use |
|---|---|---|---|
| sentence | 22 / 28 | 600 | The finding on Market and Gaps. Also the document title. Tracking −0.015em. |
| title | 18 / 24 | 600 | The skill name on a gap row. |
| body | 15 / 24 | 400 | Quotes, form ledes, the résumé-only note. |
| ui | 13 / 20 | 500, or 600 when active | Navigation, table, buttons, chips, metadata. |
| document | 14 / 22 | 400, mono | The pasted source. |

The wordmark is Schibsted 16 / 20, weight 600, tracking −0.02em. There is no logo icon. The name is the mark.

Weights are 400, 500, and 600 only. `font-synthesis: none`, so the browser does not fake a bold.

## Color

The ground is a warm gray. White is for the source sheet, fields, the selected description, and a hovered table row. Ink does almost all the talking. The highlighter sits behind a cited word. Two colors are reserved for status words: gap and have. They color the words “Not listed” and “On résumé”. They are never the only signal, and they are never a filled badge.

| Token | Hex | Role |
|---|---|---|
| canvas | `#F7F6F3` | App ground |
| surface | `#FFFFFF` | Source sheet, inputs, selected row, sleep notice |
| ink | `#141513` | Primary text, primary button, focus ring, bar fill, quote rule |
| secondary | `#454940` | Metadata. Dark enough to read. Hierarchy comes from size and weight as well as color. |
| line | `#DDDBD4` | Decorative row dividers |
| line-strong | `#84827A` | Borders of inputs, chips, and the sleep notice |
| mark | `#D7E86C` | Highlighter behind ink words |
| gap | `#6F2B22` | “Not listed”, the second line of the Market finding, error titles |
| have | `#174833` | “On résumé”, and the 8px square beside “Résumé on file” |
| skeleton | `#B0AEA6` | Loading blocks |
| on-ink | `#FFFFFF` | Label on a primary button |

Contrast is WCAG 2.1 relative luminance. Text must clear 4.5:1. Input borders and the focus ring must clear 3:1. Ratios below are for the hex values above.

| Pair | Ratio | Bar |
|---|---|---|
| Ink on canvas | 16.95:1 | 4.5 |
| Ink on surface | 18.32:1 | 4.5 |
| Ink on the highlighter | 13.65:1 | 4.5 |
| Secondary on canvas | 8.52:1 | 4.5 |
| Secondary on surface | 9.21:1 | 4.5 |
| Gap on canvas | 9.50:1 | 4.5 |
| Gap on surface | 10.27:1 | 4.5 |
| Have on canvas | 9.66:1 | 4.5 |
| Have on surface | 10.44:1 | 4.5 |
| White on ink | 18.32:1 | 4.5 |
| Line-strong on canvas | 3.56:1 | 3.0, non-text |
| Line-strong on surface | 3.85:1 | 3.0, non-text |
| Focus ring, ink on canvas | 16.95:1 | 3.0 |

Two pairs are deliberately under 3:1, and both are forbidden as the only signal:

- The decorative row rule, line on canvas, is 1.28:1. Inputs do not use it. They use line-strong.
- The highlighter on canvas is 1.24:1. A mark with no ink word on it does not exist. Status is the words “Not listed” and “On résumé”. On the description screen the mark shows where the skill sat in the source. On a gap row the mark shows which words in the quote belong to that skill.

The skeleton on canvas is 2.06:1. It is a shape, not a value. The sentence next to it says what is happening.

Selection uses the highlighter with ink text, same pairing as a mark.

## Space, radius, elevation

Spacing is six steps: 4, 8, 16, 24, 40, 64. Component geometry that is not spacing: a 1px rule, a 2px radius, a 2px focus offset, a 4px bar, an 8px status square.

| Step | px | Use |
|---|---|---|
| 1 | 4 | Gap inside a stacked label |
| 2 | 8 | Chip gap, row padding in the table, status square gap |
| 3 | 16 | Mobile page margin, control padding, related items |
| 4 | 24 | Gap-row padding, sheet padding, space between sections |
| 5 | 40 | Desktop page padding |
| 6 | 64 | Space under a page |

Radius is 2px on buttons, inputs, chips, and the sleep notice. Tables, rows, and the quote rule are square. Nothing is a pill.

Elevation is none. There is no drop shadow. A section separates from the next one by a rule, or by moving from canvas to white. Hover on a Market row turns that row white. The selected description in the index is white with a 2px ink rule on its left edge. Every index row has that 2px edge, transparent until selected, so the text does not shift.

## Layout

Three widths matter for later UI work: 360, 768, and 1280. These mockups are drawn at 360 and 1280. At 768, follow the rules here rather than shrinking the desktop.

The top bar is 52px on desktop: wordmark, then Descriptions, Market, Gaps, then the résumé link at the right. The active item is weight 600 with a 2px underline. On a phone the bar wraps. Row one is the wordmark and the résumé link, 48px. Row two is the three words, with a hairline above them. Hit height of a nav item on a phone is 44px with the padding.

**Descriptions, 1100px and up.** Three columns. Index 280px. Source sheet fluid, white. Skill rail 300px. This is the only screen with a white sheet, because it is the source you are reading.

**Descriptions, under 1100px, including 768 and 360.** One column, as in the phone mock. A switcher (`All descriptions`, `2 of 6`), then the skill chips, then the white sheet.

**Market and Gaps, 1100px and up.** One column on the canvas, page padding 40px. Market is a table. Gaps is a list of quote rows. The finding is the title. The nav already says where you are, and a 13px label sits above the finding so a screenshot still names the screen.

**Market and Gaps, under 1100px.** The same finding, then stacked rows, as in the 360 mock. Do not squeeze the five-column table onto a tablet. Skill names would break and the résumé status would wrap into the numbers.

The reading measure for a quote is 68ch. The quote does not stretch to 1280. The skill name and the count do: name at the left, count at the right, which is how a ledger works.

## Components

### Buttons

Height 36px. Horizontal padding 16px. Radius 2px. Type 13 / 20, weight 600.

- Primary: ink background, white label. Hover turns the background black. Use for “Sign in”, “Try again”, and “Read description” once the field has text.
- Secondary: white background, ink label, line-strong border. Hover turns the border ink. Use for “Paste another”.
- Disabled: same drawing as secondary, `cursor: not-allowed`, and a helper sentence in secondary text. Do not fade it with opacity. A faded label fails contrast, and the helper is what explains the wait. “Paste a description to continue.”

Focus, on every control: 2px solid ink, 2px offset. Do not remove it.

### Inputs

Label above the field, 13 / 20, weight 600. The label is a real `<label>`, not a placeholder. Placeholder text uses the secondary color (8.52:1), so it is readable, and it names the field again: “Company name”, “Role title”, “Paste the full description.”

Text inputs are 40px tall, 15px Schibsted, line-strong border, 2px radius, white. The description and résumé textareas are IBM Plex Mono 14 / 22. On focus the border becomes ink, plus the focus ring.

### Description paste

The paste area is the white sheet, not a card in the middle of a page. Company and role are fields. The description is the textarea. On the empty screen the sheet holds the sleep notice, one sentence of instruction, the fields, and the disabled button.

After a successful read, company and role become the document title. The textarea becomes the source, with `<mark>` on each extracted skill. The rail lists the same skills. Required or nice-to-have is a word. Résumé status is a second line: “Not listed” or “On résumé”.

Marks in the source use the highlighter and ink. Padding on `<mark>` is zero, so the line height does not jump.

If the source word and the canonical skill differ, the rail and the ranking use the canonical name, and one sentence says so. In the sample, Harbor writes “Postgres” and the skill is PostgreSQL: “Postgres in this description is counted as PostgreSQL.” The quote on Gaps keeps “Postgres”.

### Skill chip

The chip is the phone and tablet form of a rail row. Two columns, 8px gap. Border line-strong (3.56:1 against the ground), radius 2px, padding 8px. The name is 13px weight 600. Under it, “Required” or “Nice to have” in secondary, then “Not listed” or “On résumé” in the status color. The last chip in an odd list sits in the left column. It does not stretch.

The desktop rail is the same information in rows, because a 300px column can align the level to the right. Do not also show chips on desktop.

### Data table

Market at 1100px and up is a table, not cards. Columns: rank, skill, category, named, required, résumé.

- Rank is mono, secondary, `01`–`14`.
- Skill is 15px weight 600.
- Category is one of Language, Library, Data, Tool, Practice. Closed list. 13px secondary.
- Named is a 64×4 bar plus a mono count. The track is line-strong. The fill is ink, width `named / number of descriptions`. The number is the value. The bar repeats it so the ranking is visible in a scan.
- Required is a mono count, right-aligned. It can be lower than named. The sentence under the finding says why.
- Résumé is the words “Not listed” or “On résumé”.

Header text is 13px secondary, weight 500, not uppercase. The header rule is ink. Body rules are the decorative line. Row padding is 8px vertical. Hover turns the row white. No zebra stripes.

Sort: named descending, then required descending, then name ascending. Filters are text: `All 14`, `Not listed 8`, `On résumé 6`. The active filter is underlined. The mock shows All.

Under the table, one footnote when a merge happened: “Postgres in the Harbor Payments description is counted as PostgreSQL. The quote on Gaps keeps the original word.”

On a phone each skill is a stacked row: rank, name, status, then “Data · Named in 5 of 6 · Required in 3”, then the full-width bar.

### Gap row

A gap row is one missing skill.

The header is the skill at 18px and, at the right, a mono count such as `4 of 6 required`. If named and required differ, the count says so: `3 of 6 required · named in 5`. Under the name, “Not listed” in the gap color.

Then one or two quotes. A quote is a `<blockquote>` with a 2px ink rule on the left, body type, measure 68ch. The only highlighted words are the skill this row is about. Other skills in the same sentence stay plain. The locator is mono, secondary: company, role, and `Required` or `Nice to have`.

Further mentions collapse to one sentence: “Also required in Keel Systems and Atlas Civic.” In the app that sentence is a quiet button (ink, underline on hover) that reveals the rest. The mockups show the summarized sentence. A nice-to-have never shares a sentence with a requirement without its label. See PostgreSQL in the sample: required in three descriptions, nice to have in two, and the row says both.

Sort gaps by required descending, then named descending, then name. Skills that are on the résumé are not in this list. They are on Market.

At the bottom, a separate note, under an ink rule: “On your résumé, and named in none of these descriptions.” Then the names. In the sample: Android, Java, Kotlin. The line does not tell anyone to delete them. This set of roles simply does not ask.

### Navigation and résumé

The résumé link is the right side of the bar. With a résumé on file it reads “Résumé on file” and shows an 8px have-colored square (9.66:1). Without one it reads “Add a résumé”, with no square.

The résumé screen is the description paste with different words, not a new layout. No company or role fields. Heading: “Paste your résumé.” Lede: “RoleFit compares it with the descriptions you saved. One résumé is kept. Pasting again replaces it.” Button: “Read résumé”, disabled until there is text, with “Paste a résumé to continue.” There is no résumé library and no wizard.

### Sign-in

One screen. No social buttons, no “forgot password” flow, no plan comparison.

Heading: “Sign in”. Lede: “A local account for this instance. Descriptions and the résumé stay with that account. There are no plans.” Then the sleep notice, email, password, and a primary “Sign in”. Fine print: “On a new install, this screen creates the one local account.”

On that first run the heading is “Create the local account” and the button is “Create account”. Same fields. Same notice. Same layout. A wrong password is a sentence under the form, in the gap color, no filled banner: “That email and password don’t match.” If the request times out: “The instance didn’t answer. If it was asleep, wait a minute and try again.”

## Sleep notice

The demo host sleeps when idle. The first request after that can take about a minute. The notice exists so a slow page is not mistaken for a broken one, and so nobody thinks a slow read deleted the paste.

```
Demo   This demo instance may sleep when idle. Reading a description
       can take about a minute the first time. Nothing you paste is deleted.
```

Drawing: white plate, 1px line-strong border, 2px radius, padding 8px 16px, 8px column gap. “Demo” is mono 13px weight 500. The sentence is 13 / 20 secondary. It is inline on the page, not a toast and not a banner across the marketing site we do not have. It is not dismissible. It leaves by itself once the screen is a successful result.

Show it on:

- Sign-in, because opening the demo is when the host is often asleep.
- The empty description screen, because the next action is the slow read.
- Loading, on whichever screen is waiting.

Do not show it on a populated Market, Gaps, or description. The request already succeeded.

Do not show it on a user-empty that is not a cold start. Gaps with descriptions but no résumé is that case: the app is up, and the missing piece is the résumé. Say so. Do not blame the host.

An error does not repeat the plate. It includes one clause: “If the demo instance was asleep, wait a minute and try again.”

## Empty, loading, and error

Copy is part of the design. Use these sentences.

### Descriptions

| State | What you see |
|---|---|
| Empty | Sleep notice. “Paste a job description.” “RoleFit lists the skills it asks for. With a résumé on file, Market and Gaps compare those skills with what you list.” Company, role, description. Button disabled. “Paste a description to continue.” Index: “Nothing saved yet.” |
| Loading | The text is on the sheet with no marks yet. Meta: “Text saved. Skills are not ready.” Index meta for that row: “Reading”. Rail: sleep notice, “Reading this description.”, skeleton bars of uneven width. |
| Error | Sheet keeps the text, still unmarked. Index meta: “Not read”, in the gap color. Rail: a 2px gap rule, “Could not read this description.” “The text is saved. No skills were extracted. If the demo instance was asleep, wait a minute and try again.” Primary button: “Try again”. |
| Populated | Marks in the source, rail filled in. No sleep notice. |

Pasting adds the index row immediately, with “Reading”, before the skills return. The text is saved either way.

### Market

| State | What you see |
|---|---|
| Empty, no descriptions | “Paste a description to see which skills the set asks for.” Secondary button: “Paste a description”. No sleep notice if the account itself has loaded. |
| Loading | Sleep notice. “Loading the ranking.” Skeleton rows the height of a table row. |
| Error | “The ranking didn’t load.” The sleep clause. “Try again”. |
| Populated | The finding, the filters, the table or the stacked rows. No sleep notice. |

The finding is two lines. Line one: “PostgreSQL is named in 5 of 6 descriptions.” Line two, in the gap color: “It is not on your résumé.” If the top skill were on the résumé, line two would be in the have color: “It is on your résumé.” The sample’s top skill is not.

### Gaps

| State | What you see |
|---|---|
| Empty, no descriptions | “Paste a description before comparing.” Button: “Paste a description”. |
| Empty, no résumé | “Paste a résumé to compare it with these descriptions.” “The ranking is already on Market.” Button: “Add a résumé”. No sleep notice. |
| Loading | Sleep notice. “Comparing with your résumé.” Two skeleton blocks per row. |
| Error | “The comparison didn’t load.” The sleep clause. “Try again”. |
| Populated | The finding, the rows, the résumé-only note. No sleep notice. |

Finding: “Eight skills in this set are missing from your résumé.” Then “Python and React are required in four descriptions each.” Both lines are ink. The gap color stays on the status word inside each row, so the page does not turn into a red headline.

## Motion and focus

Hover and border changes take 120ms, linear. Skeleton opacity moves from 0.55 to 1 and back over 1200ms. Under `prefers-reduced-motion: reduce`, both durations are 0ms and the skeleton is a static block. The mockup PNGs show the static block so the picture does not depend on the frame you captured.

Tab order on Descriptions: skip link, nav, résumé link, index, sheet, rail. The skip link is visually hidden until focused, then it sits on the ink button style.

Buttons and links use real `<button>` and `<a>` elements. The table uses `<th scope="col">` and a visually hidden caption.

## Sample set

The numbers in the mockups are `design/sample-data.json`. Six fictional descriptions, one résumé. Fourteen skills in the set. Eight of them are missing from the résumé. Three résumé skills (Android, Java, Kotlin) are named in none of the six. The companies are invented. The sentences were written for the mock. They are not quotations from real job posts.

Market sort puts PostgreSQL first (named in 5, required in 3). Gaps sort puts Python and React first (required in 4). Both are visible in the mockups, so the two orders are a feature you can point at: Market answers “what is common?”, Gaps answers “what is required and missing?”

# RoleFit design

Proof is the design system for RoleFit. RoleFit is a local open-source tool: paste job descriptions, see which skills the set asks for, and read the gaps against one résumé with the line that asked for each skill. There is no pricing and no signup funnel.

Start with [benchmark.md](benchmark.md) for why the screen is not Teal, not a kanban, and not a Linear issue list. Then [system.md](system.md) for type, color, contrast, components, and the empty, loading, and error copy. Tokens for the frontend are [tokens.css](tokens.css) and [tokens.json](tokens.json). The sample counts live in [sample-data.json](sample-data.json).

## Mockups

HTML in `mockups/` is a picture of the interface, not the application. PNGs are rendered at 2× from those files. The layout width is 1280 or 360.

| Screen | Desktop | Phone |
|---|---|---|
| Descriptions, read | [png](mockups/png/descriptions-1280.png) | [png](mockups/png/descriptions-360.png) |
| Market | [png](mockups/png/market-1280.png) | [png](mockups/png/market-360.png) |
| Gaps | [png](mockups/png/gaps-1280.png) | [png](mockups/png/gaps-360.png) |
| Descriptions, empty | [png](mockups/png/descriptions-empty-1280.png) | [png](mockups/png/descriptions-empty-360.png) |
| Descriptions, loading | [png](mockups/png/descriptions-loading-1280.png) | Same pattern, stacked. See system.md. |
| Descriptions, error | [png](mockups/png/descriptions-error-1280.png) | Same pattern, stacked. See system.md. |
| Sign in | [png](mockups/png/sign-in-1280.png) | [png](mockups/png/sign-in-360.png) |

The empty, loading, and sign-in screens carry the demo-sleep notice. Populated screens do not. The reason is in system.md.

To regenerate the PNGs, install `puppeteer-core`, point it at a local Chrome, and run `node design/mockups/render.mjs` from a directory where `puppeteer-core` resolves. The committed PNGs are the review copies.

Fonts are Schibsted Grotesk and IBM Plex Mono, both under the SIL Open Font License. License texts are in `fonts/`.

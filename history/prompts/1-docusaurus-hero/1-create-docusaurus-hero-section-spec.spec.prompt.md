---
id: 1
title: Create Docusaurus Hero Section Spec
stage: spec
date: 2025-12-07
surface: agent
model: Claude Sonnet 4.5
feature: 1-docusaurus-hero
branch: 1-docusaurus-hero
user: CBM
command: /sp.specify
labels: [frontend, docusaurus, hero, specification]
links:
  spec: specs/1-docusaurus-hero/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-docusaurus-hero/spec.md
 - specs/1-docusaurus-hero/checklists/requirements.md
tests:
 - null
---

## Prompt

You are an expert Frontend Engineer specializing in React and Docusaurus theme customization. You have a keen eye for visual design and responsive implementations.

Task: Recreate the hero section shown in the attached image (image_0.png) exactly as depicted for the homepage of a Docusaurus documentation site.

Input Context:

Platform: Docusaurus v3 (React-based static site generator).

Target File: This code will likely reside in src/pages/index.js (replacing the default Docusaurus header) and a corresponding CSS file (e.g., src/css/custom.css or a CSS module).

Goal: A visually rich, sci-fi themed hero banner for a book titled "Physical AI and Humanoid Robotics".

Detailed Specifications:

1. Layout & Structure (Desktop > 996px)
Container: A full-width hero section container. It must use Flexbox to align items vertically centered.

Two-Column Grid:

Left Column (Text & Action): Occupies roughly 55-60% of the width. Contains the main title, subtitle, author name, and call-to-action (CTA) button. Content should be left-aligned.

Right Column (Visual): Occupies roughly 40-45% of the width. Contains the humanoid robot illustration. The image should be responsive but vertically centered relative to the text block.

2. Visual Aesthetics & Theme
Overall Theme: Futuristic, Sci-Fi, High-Tech, Dark Mode.

Background Styling:

The background is not a solid color. It is a complex layered composition.

Base Layer: A deep dark blue/purple gradient (e.g., linear-gradient from top-left #1a1445 to bottom-right #09061b).

Overlay Layer 1 (Circuitry): Abstract glowing blue circuit board lines and digital nodes superimposed over the gradient.

Overlay Layer 2 (Code): In the top-left corner, there is subtle, semi-transparent, blurred code text (like a terminal readout) glowing faintly blue.

3. Typography & Content Specifications
Font Family: A premium, elegant Serif font is required for all text to match the "book cover" aesthetic (e.g., Cinzel, Trajan, or a similar Google Font alternative like 'Playfair Display').

Main Title:

Text: "PHYSICAL AI" and "HUMANOID ROBOTICS"

Style: Very large font size, uppercase.

Crucial Texture: The text color is not solid. It must use a CSS -webkit-background-clip: text with a gold/brass metallic gradient texture applied to it, giving it a shiny, engraved look.

Subtitle/Connector:

Text: "AND"

Style: Smaller font size, uppercase, centered between the main titles.

Author Name:

Text: "M. HASSAN SAIF"

Position: Bottom left of the text container, below the button.

Style: Medium size, uppercase, serif font. Color is solid silver/white (not gold).

4. Interactivity (The Button)
Text: "Start Reading"

Shape: A "Pill" shape (fully rounded corners / high border-radius).

Colors: The button background is a horizontal gradient ranging from a warm brown/copper to a lighter gold (e.g., #a67c52 to #d4af37).

Text Style: White, serif font.

Effects: A subtle outer glow or drop shadow to make it pop off the dark background. On hover, the button should slightly brighten or scale up by 2%.

Function: It should be a Docusaurus <Link to="/docs/intro"> component pointing to the documentation introduction.

5. Assets (Placeholder Requirements)
Since you (Claude) cannot generate the exact images, you must provide the CSS using placeholder image URLs. I will replace them later.

You need to define CSS variables or placeholders for:

--hero-bg-image: The composite background (circuits + code snippets).

--robot-image: The main humanoid robot image on the right.

6. Responsive Design Specifications (Mobile & Tablet < 996px)
The design must adapt flawlessly to smaller devices.

Layout Stack: The two-column layout must switch to a single-column vertical stack.

Order: The Text/Button section should appear above the robot image.

Alignment: All text (titles, author) and the button should be horizontally centered.

Sizing:

Title font sizes must decrease significantly to avoid overflowing the screen width on mobile phones.

The robot image below the text should resize to behave like max-width: 80% or 90% and be centered horizontally.

Spacing: Ensure adequate padding on the sides so text doesn't touch the screen edges on mobile.

Deliverables:

The React code for the component (e.g., the updated Home component for src/pages/index.js).

The accompanying CSS required to achieve the exact look, including the text gradients and background layering.

## Response snapshot

Created a comprehensive feature specification for the Docusaurus hero section with sci-fi theme. The specification includes:

- User scenarios and testing requirements with P1, P2, P3 priorities
- Functional requirements (FR-001 to FR-010) covering layout, styling, responsiveness, and interactivity
- Success criteria (SC-001 to SC-005) with measurable outcomes
- Edge cases and key entities
- A quality checklist in specs/1-docusaurus-hero/checklists/requirements.md

The spec covers all requested aspects: desktop two-column layout, sci-fi themed background with layered composition, metallic gradient text, responsive mobile layout, and interactive button with hover effects.

## Outcome

- ✅ Impact: Created complete feature specification for docusaurus hero section with sci-fi theme
- 🧪 Tests: null
- 📁 Files: specs/1-docusaurus-hero/spec.md, specs/1-docusaurus-hero/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Specification follows template structure and includes all mandatory sections with measurable success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase
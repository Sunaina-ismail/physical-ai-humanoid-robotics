# Research Document: Docusaurus Hero Section Implementation

## Decision: Robotic SVG Heading Implementation
**Rationale**: To create a custom robotic SVG for the main heading that fits the Physical AI and Humanoid Robotics theme, using pure SVG elements that can be styled with CSS and animated as needed.
**Alternatives considered**:
- Using CSS text with SVG filters (less flexible for complex robot shapes)
- Using web fonts with robotic styling (less theme-appropriate)
- Using animated GIFs (larger file size, less control)

## Decision: Custom CSS vs Tailwind
**Rationale**: Following the requirement to not use Tailwind CSS, we'll implement custom CSS with CSS Modules for scoping and maintainability. This provides more control over the specific animations and visual effects required.
**Alternatives considered**:
- Tailwind CSS (explicitly rejected by requirements)
- Styled-components (would add additional dependency)
- Inline styles (less maintainable)

## Decision: Background Animation Implementation
**Rationale**: Using CSS animations with keyframes and pseudo-elements to create animated circuitry effects in the background, as this provides smooth performance and good browser support.
**Alternatives considered**:
- Canvas animations (more complex, less accessible)
- JavaScript animations (more complex, potential performance issues)
- GIF backgrounds (larger file size, less control)

## Decision: Responsive Design Approach
**Rationale**: Using CSS Flexbox for the main layout with media queries to handle the transition from two-column (desktop) to single-column (mobile) layout, ensuring proper responsiveness across all devices.
**Alternatives considered**:
- CSS Grid (more complex for this simple layout)
- JavaScript-based responsive handling (unnecessary complexity)

## Decision: Dark/Light Mode Implementation
**Rationale**: Using CSS custom properties (variables) combined with `prefers-color-scheme` media queries to implement both dark and light modes, allowing users to choose based on preference or system setting.
**Alternatives considered**:
- JavaScript-based theme switching (more complex)
- Separate CSS files for each theme (less maintainable)

## Decision: Image Format Strategy
**Rationale**: Using both PNG and WebP formats with proper fallbacks to ensure compatibility across all browsers while optimizing for modern browsers that support WebP.
**Alternatives considered**:
- SVG for all images (not suitable for complex robot photo)
- Single format approach (reduced compatibility or larger file sizes)

## Decision: Animation Performance
**Rationale**: Using CSS transforms and opacity changes for animations since these properties can be hardware accelerated, providing smoother performance than animating layout properties.
**Alternatives considered**:
- Animating layout properties (causes reflow, poor performance)
- JavaScript animation libraries (unnecessary complexity for simple effects)
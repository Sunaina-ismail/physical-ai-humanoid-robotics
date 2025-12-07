# Component Interface Contract: HeroSection

## Component: HeroSection

### Props Interface
```javascript
{
  title: {
    type: "string",
    required: true,
    description: "Main heading text (e.g., 'PHYSICAL AI' and 'HUMANOID ROBOTICS')"
  },
  subtitle: {
    type: "string",
    required: false,
    default: "AND",
    description: "Connector text between main titles"
  },
  author: {
    type: "string",
    required: true,
    description: "Author name to display"
  },
  ctaText: {
    type: "string",
    required: false,
    default: "Start Reading",
    description: "Text for the call-to-action button"
  },
  ctaLink: {
    type: "string",
    required: false,
    default: "/docs/intro",
    description: "Destination link for the CTA button"
  },
  robotImageUrl: {
    type: "string",
    required: true,
    description: "URL to the robot image asset"
  },
  bgImageUrl: {
    type: "string",
    required: false,
    description: "URL to the background image/animation asset"
  },
  themeMode: {
    type: "string",
    required: false,
    default: "auto",
    enum: ["light", "dark", "auto"],
    description: "Theme mode for the component"
  }
}
```

### Events/Callbacks
```javascript
{
  onCtaClick: {
    type: "function",
    required: false,
    description: "Callback function when CTA button is clicked"
  },
  onThemeChange: {
    type: "function",
    required: false,
    description: "Callback function when theme mode changes"
  }
}
```

### Exposed Methods
- `toggleTheme()`: Switch between light/dark mode
- `getThemeMode()`: Get current theme mode

### CSS Classes Interface
- `hero-section-container`: Main container element
- `hero-content`: Left column with text content
- `hero-visual`: Right column with robot image
- `hero-title`: Main title elements
- `hero-subtitle`: Subtitle/connector text
- `hero-author`: Author name element
- `hero-cta-button`: Call-to-action button
- `theme-light`: Applied when in light mode
- `theme-dark`: Applied when in dark mode
- `mobile-layout`: Applied when in mobile view

### Accessibility Attributes
- Proper ARIA labels for interactive elements
- Keyboard navigation support
- Screen reader compatibility
- WCAG 2.1 AA compliant color contrast ratios

### Responsive Breakpoints
- Desktop: min-width 997px (two-column layout)
- Mobile: max-width 996px (single-column layout)
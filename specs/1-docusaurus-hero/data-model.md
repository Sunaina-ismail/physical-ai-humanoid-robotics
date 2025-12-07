# Data Model: Docusaurus Hero Section

## Entities

### HeroSection
- **title**: String - Main heading text ("PHYSICAL AI" and "HUMANOID ROBOTICS")
- **subtitle**: String - Connector text ("AND")
- **author**: String - Author name ("M. HASSAN SAIF")
- **ctaText**: String - Call to action button text ("Start Reading")
- **ctaLink**: String - Destination link for the CTA button ("/docs/intro")
- **themeMode**: String - Current theme mode ("light" or "dark")
- **isMobile**: Boolean - Flag indicating if current view is mobile
- **bgImageUrl**: String - URL to the background image asset
- **robotImageUrl**: String - URL to the robot image asset

### RoboticHeading
- **text**: String - The main heading text to be styled robotically
- **colorMode**: String - Current color mode ("light" or "dark")
- **svgElements**: Array - Array of SVG elements that make up the robotic styling

### ThemeSettings
- **primaryColor**: String - Primary color for the theme
- **secondaryColor**: String - Secondary color for the theme
- **backgroundColor**: String - Background color for the theme
- **textColor**: String - Text color for the theme
- **accentColor**: String - Accent color for interactive elements

## Relationships
- HeroSection contains one RoboticHeading
- HeroSection has one ThemeSettings configuration
- ThemeSettings applies to all visual elements in HeroSection

## Validation Rules
- title must not be empty
- ctaLink must be a valid internal or external URL
- themeMode must be either "light" or "dark"
- bgImageUrl and robotImageUrl must be valid image URLs
- isMobile is derived from viewport width (not user input)

## State Transitions
- themeMode can transition between "light" and "dark" based on user preference or system setting
- isMobile transitions based on viewport size changes
- Hover states for interactive elements (CTA button) are handled via CSS
# Quickstart Guide: Docusaurus Hero Section

## Prerequisites
- Node.js 18+ installed
- Docusaurus v3 project already set up
- Basic knowledge of React and CSS

## Setup Steps

### 1. Install Dependencies
```bash
# Navigate to your Docusaurus project
cd frontend

# Install any additional dependencies if needed
npm install
```

### 2. Add Static Assets
1. Place your robot image at `frontend/static/img/home.jpg`
2. Place reference template at `frontend/static/img/home-template.jpg` (for design reference)

### 3. Create Component Structure
```bash
# Create the necessary directories
mkdir -p src/components/HeroSection
```

### 4. Update Homepage
Replace the content in `src/pages/index.js` with the new hero section implementation.

### 5. Add Custom CSS
Add custom styles to `src/css/custom.css` for global theme settings and animations.

### 6. Run Development Server
```bash
npm run start
```

## Key Configuration Points

### Theme Modes
- The hero section supports both light and dark modes
- Theme automatically adapts based on system preference
- Users can manually toggle between themes

### Responsive Behavior
- Desktop (>996px): Two-column layout with text on left, image on right
- Mobile (<996px): Single-column with text above image
- All elements properly scale and center on mobile devices

### Performance Considerations
- Images are optimized in both PNG and WebP formats
- CSS animations are hardware-accelerated
- Background assets are properly sized to minimize load time

## Customization Options

### Text Content
- Update title, subtitle, author, and CTA text in the component props
- All text uses serif fonts as specified

### Colors
- Customize theme colors using CSS custom properties
- Colors adapt appropriately for light/dark modes

### Animations
- Background circuitry animations can be adjusted via CSS variables
- Hover effects on the CTA button are customizable
- Robot image background animations can be modified in the component
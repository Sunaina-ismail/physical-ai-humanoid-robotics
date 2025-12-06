# Quickstart: Urdu Localization with Docusaurus i18n

## Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install # Install Docusaurus dependencies
   ```

2. **Configure Docusaurus for Urdu**
   Ensure `docusaurus.config.ts` includes:
   ```typescript
   i18n: {
     defaultLocale: 'en',
     locales: ['en', 'ur'],
     localeConfigs: {
       ur: {
         label: 'اردو',
         direction: 'rtl',
         htmlLang: 'ur-PK',
       },
     },
   },
   ```

## Translation Process

### 1. Create UI Translation Files
```bash
# Generate theme translation files (navbar, footer, etc.)
# This creates the necessary JSON files for UI text translations
npm run write-translations -- --locale ur
```

### 2. Create Content Translations (Manual Process)
```bash
# Create the directory structure for Urdu content translations
mkdir -p i18n/ur/docusaurus-plugin-content-docs/current/module-1
mkdir -p i18n/ur/docusaurus-plugin-content-docs/current/module-2
mkdir -p i18n/ur/docusaurus-plugin-content-docs/current/module-3
mkdir -p i18n/ur/docusaurus-plugin-content-docs/current/module-4
mkdir -p i18n/ur/docusaurus-plugin-content-docs/current/resources

# Create Urdu translation files by copying and translating the English content
# Example:
cp docs/module-1/Readme.md i18n/ur/docusaurus-plugin-content-docs/current/module-1/Readme.md

# Translate the content in the Urdu file while preserving:
# - Technical terms in English (e.g., ROS 2, Python, etc.)
# - Code blocks and commands unchanged
# - Markdown structure and formatting
# - Add Urdu explanations for first occurrences of technical terms when appropriate: `ROS 2 (روبوٹ آپریٹنگ سسٹم)`
```

### 3. Update UI Translations
```bash
# Update the theme translation files with Urdu text
# Edit i18n/ur/docusaurus-theme-classic/navbar.json
# Edit i18n/ur/docusaurus-theme-classic/footer.json
# Edit i18n/ur/code.json
```

### 4. Verify RTL Formatting
```bash
# Check that RTL formatting is correct
npm run build
# Verify output in build/ur/ directory
```

## Key Features

### Technical Term Preservation
- English technical terms (ROS 2, Python, etc.) remain unchanged
- First occurrence of terms get Urdu explanations when appropriate: `ROS 2 (روبوٹ آپریٹنگ سسٹم)`
- Subsequent occurrences show only English term

### Markdown Structure Preservation
- Headings, lists, and formatting maintained
- Code blocks remain LTR within RTL text
- Image captions and alt text translated appropriately
- Learning objectives, summaries, and exercises preserved

### RTL Compatibility
- Right-to-left text flow
- Proper bidirectional text handling
- Compatible with Docusaurus i18n system
- Maintains proper text direction for mixed English-Urdu content

### Docusaurus i18n Integration
- Follows Docusaurus i18n file structure conventions
- Static translation files in i18n/ur/ directory
- Supports locale switching via navbar dropdown
- Maintains compatibility with Docusaurus build process

## Core Components

### Translation Files Location
- `i18n/ur/docusaurus-plugin-content-docs/current/`: Translated documentation content
- `i18n/ur/docusaurus-theme-classic/`: Theme-specific translations (navbar.json, footer.json)
- `i18n/ur/code.json`: General UI text translations
- `i18n/ur/docusaurus-plugin-content-blog/`: Blog content translations (if applicable)

### Manual Translation Workflow
- Translation process is manual to ensure technical accuracy
- Content files are created in the appropriate i18n/ur/ subdirectories
- Technical terms are preserved in English with optional Urdu explanations
- Markdown formatting is maintained during translation

## Build and Serve

```bash
# Build with Urdu locale
npm run build

# Serve with Urdu locale
npm run serve
# Visit http://localhost:3000/ur/ for Urdu content
# Use the language switcher in the navbar to toggle between English and Urdu
```

## Verification Checklist

- [x] Docusaurus configured with Urdu locale and RTL direction
- [x] Locale switcher added to navbar
- [x] Translation files created in i18n/ur/ directory structure
- [x] Theme translation files (navbar.json, footer.json) updated with Urdu text
- [x] Content translation files created with Urdu text for all modules
- [x] Technical terms preserved in English with appropriate explanations
- [x] Code blocks remain unchanged
- [x] Markdown formatting preserved
- [x] RTL text direction applied correctly
- [x] English text within Urdu content maintains LTR direction
- [x] Build completes without errors for both locales
- [x] Language switcher works correctly in browser
- [x] All navigation and UI elements properly localized
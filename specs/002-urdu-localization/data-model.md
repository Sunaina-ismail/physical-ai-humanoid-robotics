# Data Model: Urdu Localization for Docusaurus i18n

## Static Translation Files Structure

### Docusaurus i18n Translation File
- **locale**: String (language code, "ur" for Urdu)
- **translation_type**: Enum ["ui", "content", "theme"]
- **file_path**: String (path to the original English content for reference)
- **translations**: Object (key-value pairs of translation strings)
- **direction**: String ("rtl" for right-to-left)
- **last_updated**: DateTime

### UI Translation Entry
- **id**: String (unique identifier for the UI element)
- **message**: String (Urdu translated text for UI element)
- **description**: String (context for translators)
- **category**: Enum ["navbar", "footer", "general", "theme", "admonition", "blog"]

### Content Translation Entry
- **original_english**: String (original English content)
- **urdu_translation**: String (Urdu translated content)
- **technical_terms_preserved**: Array of String (English technical terms kept in original)
- **first_use_explanations**: Array of objects {term: String, explanation: String}
- **markdown_structure**: String (preserved Markdown formatting)

## Validation Rules

1. **TechnicalTerm preservation**: All technical terms (ROS 2, Python, Gazebo, etc.) must remain in English
2. **First-use explanation**: When a technical term appears for the first time in content, it should be followed by Urdu explanation in parentheses if appropriate
3. **Markdown structure preservation**: All Markdown formatting (headings, lists, code blocks, etc.) must be maintained
4. **Code block integrity**: All code blocks, file paths, and commands must remain unchanged
5. **RTL compliance**: Text direction must follow proper right-to-left flow while keeping English elements left-to-right
6. **Docusaurus i18n compatibility**: Translation files must follow Docusaurus i18n format and structure

## Relationships

- UI Translation Entries are grouped in JSON files by component type (navbar.json, footer.json, code.json)
- Content Translation Entries are organized by documentation path in the i18n/ur/ directory structure
- Translation files are loaded by Docusaurus at build time based on locale configuration
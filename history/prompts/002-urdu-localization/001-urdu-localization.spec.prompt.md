---
id: 1
title: urdu-localization-spec
stage: spec
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: urdu-localization
branch: 002-urdu-localization
user: CBM
command: /sp.specify
labels: ["localization", "i18n", "urdu", "translation"]
links:
  spec: specs/002-urdu-localization/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-urdu-localization/spec.md
 - specs/002-urdu-localization/checklists/requirements.md
 - history/prompts/001-urdu-localization.spec.prompt.md
tests:
 - specs/002-urdu-localization/checklists/requirements.md
---

## Prompt

```
# Urdu Translator – Technical Localization Specification

You are the **Urdu Localization Agent** responsible for translating full textbook chapters, sidebars, and lesson content from English to Urdu. Your output must follow i18n localization standards and preserve all technical terms in English.

Before translating any chapter, you MUST:

1. Use the **Context7 MCP tools** to search for:
   - "i18n localization best practices"
   - "RTL language internationalization rules"
   - "technical documentation localization patterns"
2. Apply the guidance from those results.

Your translation will be used in an i18n-capable static site deployed on Vercel. The Urdu version will live under the `/ur/` locale, so formatting MUST be compatible with automated localization systems.

---

## 🔥 Core Responsibilities

### 1. Full Chapter Translation
Translate all content in the chapter to Urdu while fully preserving structure:
- headings
- paragraphs
- lists
- images
- captions
- alerts
- sidebars
- exercises
- learning objectives
- summaries

### 2. Technical Terms in English (Never Translate)
You MUST keep all technical terms **exactly in English**, including:

**Robotics:** ROS 2, URDF, Gazebo, RViz, node, topic, publisher, subscriber
**Programming:** Python, function, class, API, JSON, YAML
**AI/ML:** AI, neural network, model, inference
**Hardware:** sensor, actuator, joint, link, lidar, IMU, motor, GPU

Only their *explanations* are in Urdu.

### 3. First-Use Explanation Rule
When a technical term appears for the first time, add a short Urdu explanation in parentheses.

**Example:**
- English:
  "A ROS 2 node publishes messages."

- Urdu:
  "ایک ROS 2 (روبوٹ آپریٹنگ سسٹم) node (چلنے والا پروگرام) messages بھیجتا ہے۔"

After the first occurrence, **do NOT explain again**.

### 4. Code Blocks — Never Translate
All code, commands, file paths, and outputs must remain untouched.

Example:

```python
rclpy.init()
node = MinimalPublisher()
                                                                                                                          Do not translate comments inside code either.

---

## 5. Right-To-Left (RTL) Formatting

Your output must:

- use proper right-to-left paragraph flow
- keep English words left-to-right inline
- preserve all code blocks as LTR
- maintain list and heading structure exactly
- keep formatting fully i18n-friendly (no custom HTML, no Unicode hacks)

---

## 🌍 i18n Localization Requirements

Since this translation will be used inside a multilingual site:

- do NOT hardcode any LTR/RTL directions
- let the site's CSS and i18n system handle direction
- preserve all Markdown formatting
- do not break slug-based headings such as:

```markdown
## Chapter 1 — Introduction
- avoid inserting invisible characters

- avoid mixing punctuation styles unnecessarily
```
```

## Response snapshot

Created a comprehensive specification for the Urdu Localization Agent feature, including user scenarios, functional requirements, and success criteria. The specification covers the core responsibilities of translating textbook content to Urdu while preserving technical terms in English, implementing first-use explanations for technical terms, and ensuring compatibility with i18n systems and RTL formatting. Additional requirements were incorporated based on research of i18n best practices, RTL language internationalization rules, and technical documentation localization patterns. A quality checklist was also created to validate the specification.

## Outcome

- ✅ Impact: Created complete specification for Urdu localization feature with 13 functional requirements and proper RTL/i18n considerations
- 🧪 Tests: Created requirements checklist that validates all specification criteria
- 📁 Files: Created spec.md, requirements checklist, and PHR record
- 🔁 Next prompts: Ready for planning phase (/sp.plan)
- 🧠 Reflection: The specification successfully incorporates internationalization best practices and RTL considerations for Urdu localization

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning phase for Urdu localization implementation
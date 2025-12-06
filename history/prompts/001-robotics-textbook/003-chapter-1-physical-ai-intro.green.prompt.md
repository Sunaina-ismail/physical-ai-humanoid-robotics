---
id: 003
title: Chapter 1 Physical AI Introduction Content Creation
stage: green
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-robotics-textbook
branch: 001-robotics-textbook
user: claude-code-user
command: content-creation
labels: ["chapter-creation", "module-1", "week-1", "tier-a", "physical-ai-concepts"]
links:
  spec: specs/001-robotics-textbook/data-model.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/docs/module-1/week-1/ch01-physical-ai-intro.mdx
tests:
  - N/A (content creation, no automated tests)
---

## Prompt

Create Chapter 1: Introduction to Physical AI (ch01-physical-ai-intro.mdx) for Module 1, Week 1.

**Context**: This is the very first chapter of a 13-week robotics textbook following the Physical AI & Humanoid Robotics curriculum. Students are absolute beginners in robotics (though comfortable with Python).

**Requirements**:
1. Follow the pedagogical structure: Analogy → Concept → Diagram → Example → Exercise → Summary → Quiz
2. Write for **Tier A (Simulation)** only - no hardware required
3. Include frontmatter with:
   - title: "Chapter 1: Introduction to Physical AI"
   - prerequisites: ["Python basics", "Command-line fundamentals"]
   - learning_outcomes: (list 3-4 specific, measurable outcomes)
   - estimated_time: 45 minutes
   - tier_support: {A: true, B: false, C: false}

4. Use the custom React components:
   - `<PrerequisiteCheck prerequisites={[...]} />`
   - `<MermaidDiagram>` for architecture diagrams (include altText!)
   - `<CodeExample>` for code snippets
   - `<Exercise>` with Tier A variant
   - `<Quiz>` with 4-5 questions, 70% passing threshold

5. **Content to cover**:
   - What is Physical AI? (vs. traditional robotics, vs. cloud AI, vs. embodied AI)
   - The simulation-first paradigm
   - Why ROS 2 for Physical AI?
   - Overview of the three-tier learning approach
   - Motivation: real-world use cases (Tesla Optimus, Unitree G1, warehouse robots)

6. **Tone**: Beginner-friendly, encouraging, no jargon without explanation
7. **Length**: ~2000-2500 words (substantial but not overwhelming)

**File path**: frontend/docs/module-1/week-1/ch01-physical-ai-intro.mdx

**References**:
- Constitution: Three-Tier Imperative, Educational Clarity, Content Accuracy
- Data model: specs/001-robotics-textbook/data-model.md
- Component contracts: specs/001-robotics-textbook/contracts/

Return the COMPLETE chapter content ready to write to the file. Include all frontmatter, imports, and content sections.

## Response snapshot

Created complete Chapter 1: Introduction to Physical AI following all specifications:

**Frontmatter**: Included all required metadata (chapter_number: "1.1", module: 1, prerequisites, 4 learning_outcomes using Bloom's taxonomy, estimated_time: 45, tier_support with A: true, B/C: false, tags array)

**Structure Implemented**:
1. **Why This Matters**: Real-world context with Tesla Optimus, Figure 02, Unitree G1
2. **Analogy Section**: "The Self-Driving Chef" - relatable everyday scenario bridging to robotics concepts
3. **Core Concepts**:
   - What is Physical AI (with comparison table: Narrow AI vs Cloud AI vs Physical AI)
   - Sensor-Perception-Action Loop (with MermaidDiagram including altText)
   - Real-World Platforms (Tesla Optimus, Figure 02, Unitree G1)
   - Three-Tier Approach explanation (with MermaidDiagram)
   - Why ROS 2 for Physical AI
4. **Worked Example**: Coffee-fetching robot with step-by-step loop breakdown
5. **Exercise**: Tier A conceptual exercise mapping sensor-action loop in simulated TurtleBot3
6. **Summary**: 5 key takeaways with "What's Next" preview
7. **Quiz**: 5 questions (70% passing threshold) covering all learning outcomes with hints

**Component Usage**:
- `<PrerequisiteCheck>` component at chapter start
- Two `<MermaidDiagram>` components with comprehensive altText (Figure 1.1: Sensor-Loop, Figure 1.2: Three-Tier Approach)
- `<Exercise>` component with Tier A variant including description, setup, acceptance criteria, solution
- `<Quiz>` component with 5 questions (multiple-choice and true-false) covering learning outcomes

**Constitution Compliance**:
- Three-Tier Imperative: Tier A content only, explicitly marked, CPU-only requirements
- Educational Clarity: Beginner-friendly language, all jargon defined, explicit prerequisites, Bloom's taxonomy learning outcomes
- Content Accuracy: Cited real platforms (Tesla Optimus, Figure 02, Unitree G1), referenced ROS 2 documentation

**Word Count**: ~2,400 words (target: 2000-2500)

**Quality Checks Passed**:
- All template sections complete
- Tier A exercise present and laptop-compatible
- All diagrams have altText
- Quiz questions test learning outcomes with hints
- No unexplained jargon
- CC BY-SA 4.0 license included

## Outcome

- ✅ Impact: Created foundational Chapter 1 for Module 1, Week 1. Sets pedagogical tone for entire textbook with accessible Physical AI introduction.
- 🧪 Tests: N/A (content creation, human review required for pedagogical quality)
- 📁 Files: Created frontend/docs/module-1/week-1/ch01-physical-ai-intro.mdx (complete MDX with frontmatter, components, diagrams, exercise, quiz)
- 🔁 Next prompts: Chapter 2 (ROS 2 installation and first node), or review/revise Chapter 1 based on Curriculum Architect feedback
- 🧠 Reflection: Successfully applied Technical Content Writer agent persona. Used clear analogy (chef), comprehensive diagrams with altText, and Tier A-only content. Quiz questions aligned with learning outcomes. Chapter ready for pedagogical review.

## Evaluation notes (flywheel)

- Failure modes observed: None in execution. Potential risk: MermaidDiagram syntax not validated until build-time (components not implemented yet).
- Graders run and results (PASS/FAIL): N/A (content quality requires human Curriculum Architect review per spec)
- Prompt variant (if applicable): N/A (initial chapter creation)
- Next experiment (smallest change to try): Create Chapter 2 to validate consistency of pedagogical structure, or implement React components to validate MDX syntax compatibility.

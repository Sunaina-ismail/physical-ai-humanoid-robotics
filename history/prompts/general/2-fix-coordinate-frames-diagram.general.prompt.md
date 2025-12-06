---
id: 2
title: "Fix Coordinate Frames Diagram Error"
stage: "general"
date: "2025-12-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-robotics-textbook"
user: "user"
command: "correct chapter 16 error 5 coordinate frames"
labels: ["mermaid", "diagram", "coordinates", "documentation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/docs/module-3/week-8/ch16-isaac-sim-concepts.mdx"
tests: []
---

## PROMPT_TEXT
now correct this error of the same chapter 16 5. Coordinate Frames for Navigation
Navigation algorithms require three key coordinate frames:

Parse error on line 2: ...ame<br/>Origin: Map (0,0)] --> B[📍 odom -----------------------^ Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', '-)', 'STADIUMEND', 'SUBROUTINEEND', 'PIPE', 'CYLINDEREND', 'DIAMOND_STOP', 'TAGEND', 'TRAPEND', 'INVTRAPEND', 'UNICODE_TEXT', 'TEXT', 'TAGSTART', got 'PS'

Try again
Figure 16.5: Navigation Coordinate Frames - map → odom → base_link hierarchy

## RESPONSE_TEXT
I've fixed the second Mermaid diagram syntax error in Chapter 16 by properly escaping the content in the coordinate frames diagram. The issue was caused by colons (:) in the node text and dotted line labels that were being interpreted as part of the Mermaid syntax. I changed the diagram from using colons directly in the node text to using quoted strings with colons, which is the proper Mermaid syntax for nodes containing special characters.

The original problematic syntax:
```
A[🗺️ map<br/>World-fixed frame<br/>Origin: Map (0,0)] --> B[📍 odom<br/>Odometry frame<br/>Origin: Robot start pose]
A -.AMCL/SLAM<br/>corrects drift.-> B
```

The fixed syntax:
```
A["🗺️ map<br/>World-fixed frame<br/>Origin: Map (0,0)"] --> B["📍 odom<br/>Odometry frame<br/>Origin: Robot start pose"]
A -. "AMCL/SLAM<br/>corrects drift" .-> B
```

This resolves the parse error while maintaining the same visual representation of the coordinate frame hierarchy.

## OUTCOME
Successfully fixed the second Mermaid diagram syntax error in the Isaac Sim navigation chapter by properly escaping special characters in node text and dotted line labels.

## EVALUATION
The diagram now has valid Mermaid syntax and should render correctly without parse errors.
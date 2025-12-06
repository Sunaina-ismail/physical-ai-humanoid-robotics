---
id: 1
title: "Fix Nav2 Diagram Error"
stage: "general"
date: "2025-12-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-robotics-textbook"
user: "user"
command: "correct chapter 16 error"
labels: ["mermaid", "diagram", "nav2", "documentation"]
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
correct chapter 16 error
4. Navigation Stack Preview: Nav2 Components
Before diving into Isaac Sim navigation, let's understand what Nav2 (ROS 2's navigation framework) actually does.

Nav2 is a behavior tree-based navigation system that takes a goal pose ("Go to the kitchen") and outputs motor commands to reach that goal while avoiding obstacles.

Parse error on line 2: ...mmand : Navigate to (x, y)] --> B[Behavi -----------------------^ Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', '-)', 'STADIUMEND', 'SUBROUTINEEND', 'PIPE', 'CYLINDEREND', 'DIAMOND_STOP', 'TAGEND', 'TRAPEND', 'INVTRAPEND', 'UNICODE_TEXT', 'TEXT', 'TAGSTART', got 'PS'

Try again
Figure 16.4: Nav2 Stack Architecture - From goal pose to motor commands

## RESPONSE_TEXT
I've fixed the Mermaid diagram syntax error in Chapter 16 by properly escaping the content in the Nav2 stack diagram. The issue was caused by colons (:) in the node text that were being interpreted as part of the Mermaid syntax. I changed the diagram from using colons directly in the node text to using quoted strings with colons, which is the proper Mermaid syntax for nodes containing special characters.

The original problematic syntax:
```
A[User Command : Navigate to (x, y)] --> B[Behavior Tree Server : NavigateToPose Action]
```

The fixed syntax:
```
A["User Command: Navigate to (x, y)"] --> B["Behavior Tree Server: NavigateToPose Action"]
```

This resolves the parse error while maintaining the same visual representation of the Nav2 stack architecture.

## OUTCOME
Successfully fixed the Mermaid diagram syntax error in the Isaac Sim navigation chapter by properly escaping special characters in node text.

## EVALUATION
The diagram now has valid Mermaid syntax and should render correctly without parse errors.
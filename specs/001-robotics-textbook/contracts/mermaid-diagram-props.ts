/**
 * TypeScript Interface for MermaidDiagram React Component
 * Enforces accessibility (altText required) and consistent diagram usage
 */

export type DiagramType =
  | 'architecture'  // System architecture, component relationships
  | 'flow'          // Flowcharts, process flows, ROS 2 computation graphs
  | 'graph'         // General graphs, URDF hierarchies
  | 'sequence'      // Sequence diagrams, VLA pipelines, temporal flows
  | 'state'         // State machines, robot behavior states
  | 'class';        // Class diagrams, entity relationships

export interface MermaidDiagramProps {
  /**
   * Unique diagram identifier (used for accessibility labels)
   * @example "diagram-1-1-sensor-loop"
   */
  id: string;

  /**
   * Diagram type (determines Mermaid syntax expectations)
   */
  type: DiagramType;

  /**
   * Mermaid syntax source code
   * @example
   * ```
   * flowchart LR
   *   A[Sensors] --> B[Perception]
   *   B --> C[Planning]
   *   C --> D[Action]
   * ```
   */
  source: string;

  /**
   * REQUIRED: Accessibility description for screen readers
   * Must describe:
   * 1. What the diagram shows (overview)
   * 2. Key components and their relationships
   * 3. Main takeaway or insight
   *
   * @required Per FR-007 and Constitution accessibility requirements
   * @example "Physical AI sensor-action loop: Sensors collect data,
   *           Perception processes it, Planning decides actions, Action
   *           executes via Actuators. This continuous loop enables
   *           embodied intelligence."
   */
  altText: string;

  /**
   * Optional caption displayed below diagram
   * @example "Figure 1.1: The Physical AI sensor-perception-action loop"
   */
  caption?: string;

  /**
   * Enable click-to-zoom functionality (default: false)
   * Useful for complex diagrams with many nodes
   */
  zoomable?: boolean;

  /**
   * Optional class name for custom styling
   */
  className?: string;
}

/**
 * Example Usage:
 *
 * <MermaidDiagram
 *   id="diagram-1-1-sensor-loop"
 *   type="flow"
 *   source={`
 *     flowchart LR
 *       A[Sensors] --> B[Perception]
 *       B --> C[Planning]
 *       C --> D[Action]
 *       D --> E[Actuators]
 *       E -.feedback.-> A
 *   `}
 *   altText="Physical AI sensor-action loop: Sensors collect data, Perception
 *            processes it, Planning decides actions, Action executes via
 *            Actuators, which create feedback to Sensors. This continuous loop
 *            enables embodied intelligence."
 *   caption="Figure 1.1: The Physical AI sensor-perception-action loop"
 *   zoomable={false}
 * />
 */

/**
 * Validation Rules:
 * - id must be unique within chapter
 * - altText is REQUIRED (no default value, must be explicitly provided)
 * - altText should be 50-200 characters for optimal screen reader experience
 * - source must be valid Mermaid syntax (validated at build time)
 */

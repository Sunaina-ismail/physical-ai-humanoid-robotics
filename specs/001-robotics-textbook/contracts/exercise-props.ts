/**
 * TypeScript Interface for Exercise React Component
 * Enforces Three-Tier Imperative (Tier A mandatory per Constitution)
 */

export type TierId = 'A' | 'B' | 'C';

export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

export interface ExerciseTierVariant {
  /**
   * Tier identifier
   * - A: Simulation (laptop, CPU-only, mandatory)
   * - B: Edge AI (Jetson Nano/Orin, optional)
   * - C: Physical Robot (Unitree Go2/G1, optional)
   */
  tier: TierId;

  /**
   * What the learner will do in this tier
   * Clear, actionable description
   * @example "Launch Gazebo simulation and identify sensor-action pairs"
   */
  description: string;

  /**
   * Optional setup instructions specific to this tier
   * @example "Connect USB camera to Jetson Nano before starting"
   */
  setup?: string;

  /**
   * Optional starter code or commands
   * @example "ros2 launch turtlebot3_gazebo empty_world.launch.py"
   */
  code?: string;

  /**
   * Expected outcomes (what learner should achieve)
   * Must be testable/verifiable
   * @example
   * [
   *   "Identify at least 3 sensor types (camera, LiDAR, IMU)",
   *   "Map each sensor to corresponding actuator action"
   * ]
   */
  acceptanceCriteria: string[];

  /**
   * Optional solution hint or link
   * @example "See solution guide in resources/solutions/ch01.md"
   */
  solution?: string;
}

export interface ExerciseProps {
  /**
   * Unique exercise identifier
   * @example "ex-1-1-sensor-action"
   */
  id: string;

  /**
   * Exercise title (displayed in UI)
   * @example "Map Sensor-Action Pairs"
   */
  title: string;

  /**
   * Tier-specific implementations
   * MUST include at least one Tier A variant (per FR-008)
   * @required At least one variant with tier: "A"
   */
  variants: ExerciseTierVariant[];

  /**
   * Difficulty level for learner expectations
   */
  difficulty: DifficultyLevel;

  /**
   * Optional chapter reference for navigation
   * @example "1.1"
   */
  chapterReference?: string;
}

/**
 * Example Usage:
 *
 * <Exercise
 *   id="ex-1-1-sensor-action"
 *   title="Map Sensor-Action Pairs"
 *   difficulty="beginner"
 *   chapterReference="1.1"
 *   variants={[
 *     {
 *       tier: "A",
 *       description: "Identify sensor-action pairs in simulated robot (Gazebo)",
 *       code: "ros2 launch turtlebot3_gazebo empty_world.launch.py",
 *       acceptanceCriteria: [
 *         "Identify at least 3 sensor types (camera, LiDAR, IMU)",
 *         "Map each sensor to corresponding actuator action"
 *       ],
 *       solution: "See solution guide in resources/solutions/ch01.md"
 *     },
 *     {
 *       tier: "B",
 *       description: "Deploy sensor pipeline on Jetson with real camera",
 *       setup: "Connect USB camera to Jetson Nano",
 *       code: "ros2 run usb_cam usb_cam_node_exe",
 *       acceptanceCriteria: [
 *         "Camera publishes to /image_raw topic",
 *         "Verify image data with rqt_image_view"
 *       ]
 *     }
 *   ]}
 * />
 */

/**
 * Validation Rules:
 * - variants array MUST include at least one object with tier: "A" (FR-008)
 * - Tier A variant MUST be CPU-only, no GPU/hardware required
 * - Tier C variant (if present) MUST include Dead Man Switch pattern if motor control (Constitution IV)
 * - acceptanceCriteria must be non-empty for each variant
 * - Each variant must have unique tier value (no duplicates)
 */

/**
 * Validation Function (for runtime checks):
 */
export function validateExercise(props: ExerciseProps): string[] {
  const errors: string[] = [];

  // Check Tier A requirement
  const hasTierA = props.variants.some(v => v.tier === 'A');
  if (!hasTierA) {
    errors.push('Exercise must have at least one Tier A variant (FR-008)');
  }

  // Check acceptance criteria
  props.variants.forEach((variant, index) => {
    if (!variant.acceptanceCriteria || variant.acceptanceCriteria.length === 0) {
      errors.push(`Variant ${index} (Tier ${variant.tier}) must have acceptance criteria`);
    }
  });

  // Check tier uniqueness
  const tiers = props.variants.map(v => v.tier);
  const uniqueTiers = new Set(tiers);
  if (tiers.length !== uniqueTiers.size) {
    errors.push('Each variant must have unique tier value (no duplicate tiers)');
  }

  return errors;
}

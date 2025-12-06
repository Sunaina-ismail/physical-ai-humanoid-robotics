/**
 * TypeScript Interface for Quiz React Component
 * Enforces 70% passing threshold and hint linking (per FR-019)
 */

export type QuestionType = 'multiple-choice' | 'true-false' | 'short-answer';

export interface QuizQuestion {
  /**
   * Unique question identifier
   * @example "q1-1-embodied-ai"
   */
  id: string;

  /**
   * Question text
   * @example "What is the primary difference between narrow AI and embodied AI?"
   */
  question: string;

  /**
   * Question type
   */
  type: QuestionType;

  /**
   * Answer options (required for multiple-choice, ignored for true-false/short-answer)
   * @example [
   *   "Narrow AI processes text, embodied AI processes sensor data",
   *   "Narrow AI runs on servers, embodied AI runs on robots",
   *   "Narrow AI lacks physical interaction, embodied AI interacts with world"
   * ]
   */
  options?: string[];

  /**
   * Correct answer
   * - For multiple-choice: index number (0-based)
   * - For true-false: "true" or "false"
   * - For short-answer: expected answer string (case-insensitive match)
   * @example 2 (for multiple-choice index)
   */
  correctAnswer: string | number;

  /**
   * REQUIRED: Hint linking to chapter section (per FR-019)
   * Must reference specific section for review
   * @example "Review the 'Core Concept' section on embodied intelligence"
   * @example "See Section 2.3: ROS 2 Communication Patterns"
   */
  hint: string;

  /**
   * Explanation shown after answering (correct or incorrect)
   * @example "Embodied AI is characterized by physical world interaction
   *           through sensors and actuators, unlike narrow AI systems that
   *           operate purely in digital domains."
   */
  explanation: string;
}

export interface QuizProps {
  /**
   * Unique quiz identifier
   * @example "quiz-1-1"
   */
  id: string;

  /**
   * Chapter reference for navigation
   * @example "1.1"
   */
  chapterReference: string;

  /**
   * Quiz questions (minimum 3 recommended to cover learning outcomes)
   */
  questions: QuizQuestion[];

  /**
   * Passing score threshold (0.0 to 1.0)
   * DEFAULT: 0.7 (70% per FR-019 requirement)
   * @default 0.7
   */
  passingScore?: number;

  /**
   * Randomize question order for each attempt
   * @default false
   */
  shuffleQuestions?: boolean;

  /**
   * Allow multiple attempts
   * @default true
   */
  allowRetry?: boolean;
}

/**
 * Example Usage:
 *
 * <Quiz
 *   id="quiz-1-1"
 *   chapterReference="1.1"
 *   passingScore={0.7}
 *   questions={[
 *     {
 *       id: "q1",
 *       question: "What is the primary difference between narrow AI and embodied AI?",
 *       type: "multiple-choice",
 *       options: [
 *         "Narrow AI processes text, embodied AI processes sensor data",
 *         "Narrow AI runs on servers, embodied AI runs on robots",
 *         "Narrow AI lacks physical interaction, embodied AI interacts with world",
 *         "Narrow AI is faster, embodied AI is slower"
 *       ],
 *       correctAnswer: 2,
 *       hint: "Review the 'Core Concept' section on embodied intelligence",
 *       explanation: "Embodied AI is characterized by physical world interaction through sensors and actuators."
 *     },
 *     {
 *       id: "q2",
 *       question: "The sensor-perception-action loop is fundamental to Physical AI.",
 *       type: "true-false",
 *       correctAnswer: "true",
 *       hint: "See Figure 1.1 and the 'Diagram' section",
 *       explanation: "The sensor-perception-action loop enables continuous adaptation to the physical world."
 *     }
 *   ]}
 * />
 */

/**
 * Validation Rules:
 * - questions array must have at least 2 items (preferably 3-5 to cover learning outcomes)
 * - All questions must have non-empty hint field (FR-019)
 * - passingScore must be 0.7 (70%) per spec, or explicitly overridden with justification
 * - For multiple-choice: options array required, correctAnswer must be valid index
 * - For true-false: correctAnswer must be "true" or "false"
 * - For short-answer: correctAnswer must be non-empty string
 */

/**
 * Validation Function:
 */
export function validateQuiz(props: QuizProps): string[] {
  const errors: string[] = [];

  // Check minimum questions
  if (props.questions.length < 2) {
    errors.push('Quiz must have at least 2 questions');
  }

  // Check passing score
  const passingScore = props.passingScore ?? 0.7;
  if (passingScore < 0 || passingScore > 1) {
    errors.push('passingScore must be between 0.0 and 1.0');
  }
  if (passingScore !== 0.7) {
    console.warn('passingScore differs from spec requirement (0.7 / 70%)');
  }

  // Validate each question
  props.questions.forEach((q, index) => {
    // Check hint requirement (FR-019)
    if (!q.hint || q.hint.trim().length === 0) {
      errors.push(`Question ${index + 1} (${q.id}) must have hint linking to chapter section (FR-019)`);
    }

    // Check question-type-specific requirements
    if (q.type === 'multiple-choice') {
      if (!q.options || q.options.length < 2) {
        errors.push(`Question ${index + 1} (${q.id}) must have at least 2 options for multiple-choice`);
      }
      if (typeof q.correctAnswer !== 'number') {
        errors.push(`Question ${index + 1} (${q.id}) correctAnswer must be number (index) for multiple-choice`);
      }
      if (typeof q.correctAnswer === 'number' && q.options) {
        if (q.correctAnswer < 0 || q.correctAnswer >= q.options.length) {
          errors.push(`Question ${index + 1} (${q.id}) correctAnswer index out of range`);
        }
      }
    }

    if (q.type === 'true-false') {
      if (q.correctAnswer !== 'true' && q.correctAnswer !== 'false') {
        errors.push(`Question ${index + 1} (${q.id}) correctAnswer must be 'true' or 'false' for true-false`);
      }
    }

    if (q.type === 'short-answer') {
      if (typeof q.correctAnswer !== 'string' || q.correctAnswer.trim().length === 0) {
        errors.push(`Question ${index + 1} (${q.id}) correctAnswer must be non-empty string for short-answer`);
      }
    }
  });

  return errors;
}

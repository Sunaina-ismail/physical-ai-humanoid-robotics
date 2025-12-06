import React, { useState } from 'react';

export type QuestionType = 'multiple-choice' | 'true-false' | 'short-answer';

export interface QuizQuestion {
  id: string;
  question: string;
  type: QuestionType;
  options?: string[];
  correctAnswer: string | number;
  hint: string; // Link to concept section (FR-019)
  explanation: string;
}

export interface QuizProps {
  id: string;
  chapterReference: string;
  questions: QuizQuestion[];
  passingScore?: number; // Default: 0.7 (70%, FR-019)
  shuffleQuestions?: boolean;
}

export default function Quiz({
  id,
  questions,
  passingScore = 0.7,
}: QuizProps): JSX.Element {
  const [answers, setAnswers] = useState<Record<string, string | number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [showHints, setShowHints] = useState<Set<string>>(new Set());

  const handleAnswerChange = (questionId: string, answer: string | number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const toggleHint = (questionId: string) => {
    setShowHints((prev) => {
      const next = new Set(prev);
      if (next.has(questionId)) {
        next.delete(questionId);
      } else {
        next.add(questionId);
      }
      return next;
    });
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q) => {
      const userAnswer = answers[q.id];
      if (userAnswer !== undefined) {
        if (
          String(userAnswer).toLowerCase() ===
          String(q.correctAnswer).toLowerCase()
        ) {
          correct++;
        }
      }
    });
    return correct / questions.length;
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  const handleReset = () => {
    setAnswers({});
    setSubmitted(false);
    setShowHints(new Set());
  };

  const score = submitted ? calculateScore() : 0;
  const passed = score >= passingScore;

  return (
    <div
      id={id}
      style={{
        margin: '2rem 0',
        padding: '2rem',
        border: '2px solid var(--ifm-color-primary)',
        borderRadius: '0.5rem',
        backgroundColor: 'var(--ifm-background-surface-color)',
      }}
    >
      <h2 style={{ marginTop: 0 }}>📝 Knowledge Check</h2>
      <p style={{ color: 'var(--ifm-color-emphasis-700)', marginBottom: '2rem' }}>
        Passing score: {passingScore * 100}% ({Math.ceil(questions.length * passingScore)}/
        {questions.length} questions)
      </p>

      {questions.map((question, index) => (
        <div
          key={question.id}
          style={{
            marginBottom: '2rem',
            padding: '1.5rem',
            borderRadius: '0.375rem',
            backgroundColor: submitted
              ? answers[question.id] !== undefined &&
                String(answers[question.id]).toLowerCase() ===
                  String(question.correctAnswer).toLowerCase()
                ? '#10b98120'
                : '#ef444420'
              : 'var(--ifm-color-emphasis-100)',
          }}
        >
          <h4>Question {index + 1}</h4>
          <p style={{ fontSize: '1.05rem', fontWeight: '500' }}>{question.question}</p>

          {question.type === 'multiple-choice' && question.options && (
            <div style={{ marginTop: '1rem' }}>
              {question.options.map((option, optIndex) => (
                <label
                  key={optIndex}
                  style={{
                    display: 'block',
                    padding: '0.75rem',
                    marginBottom: '0.5rem',
                    borderRadius: '0.25rem',
                    border: '1px solid var(--ifm-color-emphasis-300)',
                    cursor: submitted ? 'not-allowed' : 'pointer',
                    backgroundColor:
                      answers[question.id] === optIndex
                        ? 'var(--ifm-color-primary-lightest)'
                        : 'transparent',
                  }}
                >
                  <input
                    type="radio"
                    name={question.id}
                    value={optIndex}
                    checked={answers[question.id] === optIndex}
                    onChange={(e) =>
                      handleAnswerChange(question.id, parseInt(e.target.value))
                    }
                    disabled={submitted}
                    style={{ marginRight: '0.5rem' }}
                  />
                  {option}
                </label>
              ))}
            </div>
          )}

          {question.type === 'true-false' && (
            <div style={{ marginTop: '1rem' }}>
              {['true', 'false'].map((option) => (
                <label
                  key={option}
                  style={{
                    display: 'block',
                    padding: '0.75rem',
                    marginBottom: '0.5rem',
                    borderRadius: '0.25rem',
                    border: '1px solid var(--ifm-color-emphasis-300)',
                    cursor: submitted ? 'not-allowed' : 'pointer',
                    backgroundColor:
                      answers[question.id] === option
                        ? 'var(--ifm-color-primary-lightest)'
                        : 'transparent',
                  }}
                >
                  <input
                    type="radio"
                    name={question.id}
                    value={option}
                    checked={answers[question.id] === option}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    disabled={submitted}
                    style={{ marginRight: '0.5rem' }}
                  />
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </label>
              ))}
            </div>
          )}

          {!submitted && (
            <button
              onClick={() => toggleHint(question.id)}
              style={{
                marginTop: '1rem',
                padding: '0.5rem 1rem',
                fontSize: '0.875rem',
                border: 'none',
                borderRadius: '0.25rem',
                backgroundColor: 'var(--ifm-color-emphasis-200)',
                cursor: 'pointer',
              }}
            >
              {showHints.has(question.id) ? '🔽 Hide Hint' : '💡 Show Hint'}
            </button>
          )}

          {showHints.has(question.id) && (
            <div
              style={{
                marginTop: '1rem',
                padding: '1rem',
                borderRadius: '0.25rem',
                backgroundColor: 'var(--ifm-color-warning-lightest)',
                borderLeft: '4px solid var(--ifm-color-warning)',
              }}
            >
              <strong>Hint:</strong> {question.hint}
            </div>
          )}

          {submitted && (
            <div
              style={{
                marginTop: '1rem',
                padding: '1rem',
                borderRadius: '0.25rem',
                backgroundColor:
                  answers[question.id] !== undefined &&
                  String(answers[question.id]).toLowerCase() ===
                    String(question.correctAnswer).toLowerCase()
                    ? 'var(--ifm-color-success-lightest)'
                    : 'var(--ifm-color-danger-lightest)',
                borderLeft:
                  answers[question.id] !== undefined &&
                  String(answers[question.id]).toLowerCase() ===
                    String(question.correctAnswer).toLowerCase()
                    ? '4px solid var(--ifm-color-success)'
                    : '4px solid var(--ifm-color-danger)',
              }}
            >
              <strong>
                {answers[question.id] !== undefined &&
                String(answers[question.id]).toLowerCase() ===
                  String(question.correctAnswer).toLowerCase()
                  ? '✅ Correct!'
                  : '❌ Incorrect'}
              </strong>
              <p style={{ marginTop: '0.5rem', marginBottom: 0 }}>
                {question.explanation}
              </p>
            </div>
          )}
        </div>
      ))}

      {!submitted ? (
        <button
          onClick={handleSubmit}
          disabled={Object.keys(answers).length < questions.length}
          style={{
            padding: '0.75rem 2rem',
            fontSize: '1rem',
            fontWeight: '600',
            border: 'none',
            borderRadius: '0.375rem',
            backgroundColor:
              Object.keys(answers).length < questions.length
                ? 'var(--ifm-color-emphasis-300)'
                : 'var(--ifm-color-primary)',
            color: 'white',
            cursor:
              Object.keys(answers).length < questions.length
                ? 'not-allowed'
                : 'pointer',
          }}
        >
          Submit Answers
        </button>
      ) : (
        <div>
          <div
            style={{
              padding: '1.5rem',
              borderRadius: '0.5rem',
              backgroundColor: passed
                ? 'var(--ifm-color-success-lightest)'
                : 'var(--ifm-color-danger-lightest)',
              border: passed
                ? '2px solid var(--ifm-color-success)'
                : '2px solid var(--ifm-color-danger)',
              marginBottom: '1rem',
            }}
          >
            <h3 style={{ marginTop: 0 }}>
              {passed ? '🎉 Quiz Passed!' : '❌ Quiz Not Passed'}
            </h3>
            <p style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: 0 }}>
              Score: {Math.round(score * 100)}% ({Math.round(score * questions.length)}/
              {questions.length})
            </p>
          </div>
          <button
            onClick={handleReset}
            style={{
              padding: '0.75rem 2rem',
              fontSize: '1rem',
              fontWeight: '600',
              border: '1px solid var(--ifm-color-emphasis-500)',
              borderRadius: '0.375rem',
              backgroundColor: 'transparent',
              cursor: 'pointer',
            }}
          >
            🔄 Retry Quiz
          </button>
        </div>
      )}
    </div>
  );
}

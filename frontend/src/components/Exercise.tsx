import React, { useState } from 'react';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';

export type TierId = 'A' | 'B' | 'C';
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced';

export interface ExerciseTierVariant {
  tier: TierId;
  description: string;
  setup?: string;
  code?: string;
  acceptanceCriteria: string[];
  solution?: string;
}

export interface ExerciseProps {
  id: string;
  title: string;
  variants: ExerciseTierVariant[]; // Must include Tier A (FR-008)
  difficulty: DifficultyLevel;
  chapterReference?: string;
}

const tierLabels = {
  A: '🟢 Tier A: Simulation',
  B: '🔵 Tier B: Edge AI',
  C: '🟣 Tier C: Physical Robot',
};

const difficultyColors = {
  beginner: '#10b981',
  intermediate: '#f59e0b',
  advanced: '#ef4444',
};

export default function Exercise({
  id,
  title,
  variants,
  difficulty,
}: ExerciseProps): JSX.Element {
  const [expandedVariants, setExpandedVariants] = useState<Set<TierId>>(
    new Set(['A'])
  );

  const toggleVariant = (tier: TierId) => {
    setExpandedVariants((prev) => {
      const next = new Set(prev);
      if (next.has(tier)) {
        next.delete(tier);
      } else {
        next.add(tier);
      }
      return next;
    });
  };

  return (
    <div
      id={id}
      style={{
        margin: '2rem 0',
        padding: '1.5rem',
        border: '2px solid var(--ifm-color-emphasis-300)',
        borderRadius: '0.5rem',
        backgroundColor: 'var(--ifm-background-surface-color)',
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '1rem',
        }}
      >
        <h3 style={{ margin: 0 }}>🧪 {title}</h3>
        <span
          style={{
            padding: '0.25rem 0.75rem',
            borderRadius: '1rem',
            fontSize: '0.75rem',
            fontWeight: '600',
            backgroundColor: difficultyColors[difficulty] + '20',
            color: difficultyColors[difficulty],
            textTransform: 'uppercase',
          }}
        >
          {difficulty}
        </span>
      </div>

      {variants.length === 1 ? (
        <ExerciseVariantContent variant={variants[0]} />
      ) : (
        <Tabs groupId="tier">
          {variants.map((variant) => (
            <TabItem
              key={variant.tier}
              value={`tier${variant.tier}`}
              label={tierLabels[variant.tier]}
              default={variant.tier === 'A'}
            >
              <ExerciseVariantContent variant={variant} />
            </TabItem>
          ))}
        </Tabs>
      )}
    </div>
  );
}

function ExerciseVariantContent({
  variant,
}: {
  variant: ExerciseTierVariant;
}): JSX.Element {
  return (
    <div style={{ marginTop: '1rem' }}>
      <p style={{ fontSize: '1rem', lineHeight: '1.6' }}>
        {variant.description}
      </p>

      {variant.setup && (
        <div style={{ marginTop: '1rem' }}>
          <h4>Setup</h4>
          <p style={{ fontStyle: 'italic', color: 'var(--ifm-color-emphasis-700)' }}>
            {variant.setup}
          </p>
        </div>
      )}

      {variant.code && (
        <div style={{ marginTop: '1rem' }}>
          <h4>Code</h4>
          <CodeBlock language="python">{variant.code}</CodeBlock>
        </div>
      )}

      <div style={{ marginTop: '1rem' }}>
        <h4>Acceptance Criteria</h4>
        <ul>
          {variant.acceptanceCriteria.map((criterion, index) => (
            <li key={index}>{criterion}</li>
          ))}
        </ul>
      </div>

      {variant.solution && (
        <details style={{ marginTop: '1rem' }}>
          <summary style={{ cursor: 'pointer', fontWeight: '600' }}>
            💡 Solution Hint
          </summary>
          <p style={{ marginTop: '0.5rem', fontStyle: 'italic' }}>
            {variant.solution}
          </p>
        </details>
      )}
    </div>
  );
}

import React, { useState } from 'react';

export interface PrerequisiteCheckProps {
  prerequisites: string[];
}

export default function PrerequisiteCheck({
  prerequisites,
}: PrerequisiteCheckProps): JSX.Element {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!prerequisites || prerequisites.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        margin: '1.5rem 0',
        padding: '1rem',
        borderRadius: '0.5rem',
        backgroundColor: 'var(--ifm-color-info-lightest)',
        borderLeft: '4px solid var(--ifm-color-info)',
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          cursor: 'pointer',
        }}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '1.5rem' }}>📋</span>
          <strong>Prerequisites</strong>
        </div>
        <span style={{ fontSize: '1.25rem' }}>{isExpanded ? '▼' : '▶'}</span>
      </div>

      {isExpanded && (
        <div style={{ marginTop: '1rem' }}>
          <p style={{ marginBottom: '0.75rem', color: 'var(--ifm-color-emphasis-700)' }}>
            Before starting this chapter, you should be familiar with:
          </p>
          <ul style={{ marginBottom: 0 }}>
            {prerequisites.map((prereq, index) => (
              <li key={index} style={{ marginBottom: '0.5rem' }}>
                {prereq}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

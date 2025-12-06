import React from 'react';

export type TierId = 'A' | 'B' | 'C';

export interface TierBadgeProps {
  tiers: TierId[];
}

const tierConfig = {
  A: { emoji: '🟢', label: 'Tier A: Simulation', color: '#10b981' },
  B: { emoji: '🔵', label: 'Tier B: Edge AI', color: '#3b82f6' },
  C: { emoji: '🟣', label: 'Tier C: Physical Robot', color: '#8b5cf6' },
};

export default function TierBadge({ tiers }: TierBadgeProps): JSX.Element {
  return (
    <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
      {tiers.map((tier) => {
        const config = tierConfig[tier];
        return (
          <span
            key={tier}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              padding: '0.25rem 0.75rem',
              borderRadius: '1rem',
              fontSize: '0.875rem',
              fontWeight: '500',
              backgroundColor: config.color + '20',
              color: config.color,
              border: `1px solid ${config.color}`,
            }}
          >
            <span style={{ marginRight: '0.25rem' }}>{config.emoji}</span>
            {config.label}
          </span>
        );
      })}
    </div>
  );
}

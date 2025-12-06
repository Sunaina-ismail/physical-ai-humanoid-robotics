import React from 'react';
import Mermaid from '@theme/Mermaid';

export type DiagramType =
  | 'architecture'
  | 'flow'
  | 'graph'
  | 'sequence'
  | 'state'
  | 'class';

export interface MermaidDiagramProps {
  id: string;
  type: DiagramType;
  source: string;
  altText: string; // REQUIRED per FR-007 and Constitution
  caption?: string;
  zoomable?: boolean;
}

export default function MermaidDiagram({
  id,
  source,
  altText,
  caption,
  zoomable = false,
}: MermaidDiagramProps): JSX.Element {
  return (
    <figure
      id={id}
      style={{
        margin: '2rem 0',
        padding: '1rem',
        border: '1px solid var(--ifm-color-emphasis-300)',
        borderRadius: '0.5rem',
        backgroundColor: 'var(--ifm-background-surface-color)',
      }}
    >
      <div
        role="img"
        aria-label={altText}
        style={{ cursor: zoomable ? 'zoom-in' : 'default' }}
      >
        <Mermaid value={source} />
      </div>
      {caption && (
        <figcaption
          style={{
            marginTop: '1rem',
            textAlign: 'center',
            fontSize: '0.875rem',
            color: 'var(--ifm-color-emphasis-700)',
            fontStyle: 'italic',
          }}
        >
          {caption}
        </figcaption>
      )}
    </figure>
  );
}

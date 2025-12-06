import React from 'react';
import CodeBlock from '@theme/CodeBlock';

export interface CodeExampleProps {
  code: string;
  language?: string;
  title?: string;
  showLineNumbers?: boolean;
}

export default function CodeExample({
  code,
  language = 'python',
  title,
  showLineNumbers = true,
}: CodeExampleProps): JSX.Element {
  return (
    <div style={{ margin: '1.5rem 0' }}>
      {title && (
        <div
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: 'var(--ifm-color-emphasis-100)',
            borderTopLeftRadius: '0.375rem',
            borderTopRightRadius: '0.375rem',
            fontWeight: '600',
            fontSize: '0.875rem',
            borderBottom: '1px solid var(--ifm-color-emphasis-300)',
          }}
        >
          {title}
        </div>
      )}
      <CodeBlock language={language} showLineNumbers={showLineNumbers}>
        {code}
      </CodeBlock>
    </div>
  );
}

import React from 'react';
import OriginalFooter from '@theme-original/Footer';
import type { WrapperProps } from '@docusaurus/types';
import type FooterType from '@theme/Footer';
import './footer.css';

type Props = WrapperProps<typeof FooterType>;

export default function FooterWrapper(props: Props): JSX.Element {
  return (
    <div className="footer-gradient-wrapper">
      <OriginalFooter {...props} />
    </div>
  );
}

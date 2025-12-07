import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';
import type { WrapperProps } from '@docusaurus/types';
import type NavbarType from '@theme/Navbar';
import './navbar.css';

type Props = WrapperProps<typeof NavbarType>;

export default function NavbarWrapper(props: Props): JSX.Element {
  return (
    <div className="navbar-gradient-wrapper">
      <OriginalNavbar {...props} />
    </div>
  );
}

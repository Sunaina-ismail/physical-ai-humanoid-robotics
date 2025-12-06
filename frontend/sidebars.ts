import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'index',
    {
      type: 'category',
      label: 'Module 1: Foundations',
      link: {
        type: 'doc',
        id: 'module-1/module-1',
      },
      items: [
        {
          type: 'category',
          label: 'Week 1: Physical AI & ROS 2 Basics',
          collapsible: true,
          collapsed: false,
          items: [
            'module-1/week-1/ch01-physical-ai-intro',
            'module-1/week-1/ch02-ros2-nodes-topics',
          ],
        },
        {
          type: 'category',
          label: 'Week 2: Python Patterns & DSP for Robotics',
          collapsible: true,
          collapsed: false,
          items: [
            'module-1/week-2/ch03-python-patterns',
            'module-1/week-2/ch04-dsp-basics',
            'module-1/week-2/tierB-jetson-setup',
          ],
        },
        {
          type: 'category',
          label: 'Week 3: ROS 2 Services & Actions',
          collapsible: true,
          collapsed: false,
          items: [
            'module-1/week-3/ch05-ros2-services-actions',
            'module-1/week-3/ch06-lifecycle-nodes',
          ],
        },
        {
          type: 'category',
          label: 'Week 4: TF2 Transforms & URDF Models',
          collapsible: true,
          collapsed: false,
          items: [
            'module-1/week-4/ch07-tf2-transforms',
            'module-1/week-4/ch08-urdf-robot-models',
          ],
        },
        {
          type: 'category',
          label: 'Week 5: Testing & CI/CD',
          collapsible: true,
          collapsed: false,
          items: [
            'module-1/week-5/ch09-unit-testing-pytest',
            'module-1/week-5/ch10-launch-testing',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Simulation',
      link: {
        type: 'doc',
        id: 'module-2/module-2',
      },
      items: [
        {
          type: 'category',
          label: 'Week 6: Digital Twins & Gazebo',
          collapsible: true,
          collapsed: false,
          items: [
            'module-2/week-6/ch11-digital-twins',
            'module-2/week-6/ch12-simulating-sensors',
            'module-2/week-6/ch13-isaac-sim-essentials',
          ],
        },
        {
          type: 'category',
          label: 'Week 7: Isaac Sim & Domain Randomization',
          collapsible: true,
          collapsed: false,
          items: [
            'module-2/week-7/ch14-gpu-physics-rendering',
            'module-2/week-7/ch15-domain-randomization',
            'module-2/week-7/tierB-sensor-integration',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Navigation',
      link: {
        type: 'doc',
        id: 'module-3/module-3',
      },
      items: [
        {
          type: 'category',
          label: 'Week 8: Isaac Sim Concepts & VSLAM',
          collapsible: true,
          collapsed: false,
          items: [
            'module-3/week-8/ch16-navigation-concepts',
            'module-3/week-8/ch17-nav2-stack-overview',
            'module-3/week-8/tierC-vslam-humanoid',
          ],
        },
        {
          type: 'category',
          label: 'Week 9: SLAM Algorithms & Mapping',
          collapsible: true,
          collapsed: false,
          items: [
            'module-3/week-9/ch18-slam-fundamentals',
            'module-3/week-9/ch19-gmapping-cartographer',
            'module-3/week-9/ch20-rtab-map',
            'module-3/week-9/tierB-nav2-edge',
          ],
        },
        {
          type: 'category',
          label: 'Week 10: Visual SLAM & Voice Navigation',
          collapsible: true,
          collapsed: false,
          items: [
            'module-3/week-10/ch21-vslam-orb-slam',
            'module-3/week-10/ch22-sensor-fusion-vio',
            'module-3/week-10/ch23-voice-to-navigation',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      link: {
        type: 'doc',
        id: 'module-4/module-4',
      },
      items: [
        {
          type: 'category',
          label: 'Week 11: VLA Architecture & Transformers',
          collapsible: true,
          collapsed: false,
          items: [
            'module-4/week-11/ch24-vla-paradigm',
            'module-4/week-11/ch25-transformer-architecture',
            'module-4/week-11/ch26-openvla-rt2',
          ],
        },
        {
          type: 'category',
          label: 'Week 12: Fine-Tuning VLA Models',
          collapsible: true,
          collapsed: false,
          items: [
            'module-4/week-12/ch27-fine-tuning-vla',
          ],
        },
        {
          type: 'category',
          label: 'Week 13: Voice Control & Capstone Project',
          collapsible: true,
          collapsed: false,
          items: [
            'module-4/week-13/ch28-capstone-project',
            'module-4/week-13/ch29-whisper-llm-planning',
            'module-4/week-13/tierC-full-capstone',
          ],
        },
      ],
    },
  ],
};

export default sidebars;

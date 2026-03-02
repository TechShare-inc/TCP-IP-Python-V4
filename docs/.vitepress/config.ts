import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

export default withMermaid(defineConfig({
  title: "Dobot V4 Python SDK",
  description:
    "Python SDK for Dobot V4 robots — TCP/IP communication with typed responses, real-time feedback, and multi-language alarm support.",

  head: [["link", { rel: "icon", href: "/favicon.ico" }]],

  themeConfig: {
    nav: [
      { text: "Home", link: "/" },
      { text: "Getting Started", link: "/getting-started/installation" },
      { text: "Tutorials", link: "/tutorial/first-program" },
      { text: "How-to", link: "/how-to/configure-speed-and-coords" },
      { text: "Reference", link: "/reference/" },
      { text: "Explanation", link: "/explanation/architecture" },
    ],

    sidebar: {
      "/getting-started/": [
        {
          text: "Getting Started",
          items: [
            { text: "Installation", link: "/getting-started/installation" },
            { text: "Quick Start", link: "/getting-started/quick-start" },
            {
              text: "Architecture Overview",
              link: "/getting-started/architecture",
            },
          ],
        },
      ],

      "/tutorial/": [
        {
          text: "Tutorials",
          items: [
            {
              text: "Your First Robot Program",
              link: "/tutorial/first-program",
            },
            {
              text: "Reading Real-Time Feedback",
              link: "/tutorial/reading-feedback",
            },
            {
              text: "Error Monitoring & Alarms",
              link: "/tutorial/error-monitoring",
            },
            {
              text: "Pick-and-Place Workflow",
              link: "/tutorial/pick-and-place",
            },
          ],
        },
      ],

      "/how-to/": [
        {
          text: "How-to Guides",
          items: [
            {
              text: "Configure Speed & Coordinates",
              link: "/how-to/configure-speed-and-coords",
            },
            {
              text: "Use Digital & Analog I/O",
              link: "/how-to/use-digital-analog-io",
            },
            {
              text: "Modbus Communication",
              link: "/how-to/modbus-communication",
            },
            { text: "Force Control", link: "/how-to/force-control" },
            { text: "Conveyor Tracking", link: "/how-to/conveyor-tracking" },
            { text: "Welding Operations", link: "/how-to/welding" },
            { text: "Servo Control", link: "/how-to/servo-control" },
            { text: "Relative Motion", link: "/how-to/relative-motion" },
            { text: "Motion Checking", link: "/how-to/motion-checking" },
            {
              text: "Error Handling & Reconnect",
              link: "/how-to/error-handling-reconnect",
            },
            {
              text: "Multi-Language Alarms",
              link: "/how-to/multi-language-alarms",
            },
            {
              text: "Facade vs Dashboard",
              link: "/how-to/facade-vs-dashboard",
            },
          ],
        },
      ],

      "/reference/": [
        {
          text: "Reference",
          items: [
            { text: "Overview", link: "/reference/" },
            { text: "Port Reference", link: "/reference/ports" },
            { text: "Feedback Fields", link: "/reference/feedback-fields" },
            { text: "Robot Modes", link: "/reference/robot-modes" },
            { text: "Glossary", link: "/reference/glossary" },
          ],
        },
        {
          text: "API Reference",
          collapsed: false,
          items: [
            { text: "DobotRobot", link: "/reference/api/dobot_api_v4.robot" },
            { text: "DobotApi", link: "/reference/api/dobot_api_v4.base" },
            {
              text: "DobotApiDashboard",
              link: "/reference/api/dobot_api_v4.commands.dashboard",
            },
            {
              text: "System Commands",
              link: "/reference/api/dobot_api_v4.commands._system_mixin",
            },
            {
              text: "Config Commands",
              link: "/reference/api/dobot_api_v4.commands._config_mixin",
            },
            {
              text: "Motion Commands",
              link: "/reference/api/dobot_api_v4.commands._motion_mixin",
            },
            {
              text: "I/O Commands",
              link: "/reference/api/dobot_api_v4.commands._io_mixin",
            },
            {
              text: "Query Commands",
              link: "/reference/api/dobot_api_v4.commands._query_mixin",
            },
            {
              text: "Force Commands",
              link: "/reference/api/dobot_api_v4.commands._force_mixin",
            },
            {
              text: "Modbus Commands",
              link: "/reference/api/dobot_api_v4.commands._modbus_mixin",
            },
            {
              text: "Conveyor Commands",
              link: "/reference/api/dobot_api_v4.commands._conveyor_mixin",
            },
            {
              text: "Weld Commands",
              link: "/reference/api/dobot_api_v4.commands._weld_mixin",
            },
            {
              text: "Check Commands",
              link: "/reference/api/dobot_api_v4.commands._check_mixin",
            },
            {
              text: "Feedback",
              link: "/reference/api/dobot_api_v4.feedback",
            },
            {
              text: "Error Monitor",
              link: "/reference/api/dobot_api_v4.error_monitor",
            },
            {
              text: "Alarm I18n",
              link: "/reference/api/dobot_api_v4.i18n_manager",
            },
            {
              text: "Parse / Error Types",
              link: "/reference/api/dobot_api_v4.commands._parse",
            },
            {
              text: "Data Types",
              link: "/reference/api/dobot_api_v4.dtypes",
            },
          ],
        },
      ],

      "/explanation/": [
        {
          text: "Explanation",
          items: [
            {
              text: "Architecture Deep-Dive",
              link: "/explanation/architecture",
            },
            {
              text: "The @forward_to Decorator",
              link: "/explanation/forward-decorator",
            },
            {
              text: "Connection Model",
              link: "/explanation/connection-model",
            },
            {
              text: "Backward Compatibility",
              link: "/explanation/backward-compat",
            },
            { text: "i18n Design", link: "/explanation/i18n-design" },
            { text: "Code Style", link: "/explanation/code-style" },
          ],
        },
      ],
    },

    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/Dobot-Arm/TCP-IP-Python-V4",
      },
    ],

    search: {
      provider: "local",
    },

    footer: {
      message: "Released under the MIT License.",
      copyright: "Copyright © 2024-2026 Dobot / TechShare Corp.",
    },

    editLink: {
      pattern:
        "https://github.com/Dobot-Arm/TCP-IP-Python-V4/edit/main/docs/:path",
      text: "Edit this page on GitHub",
    },
  },

  markdown: {
    lineNumbers: true,
  },

  ignoreDeadLinks: [
    // API reference pages are auto-generated by Sphinx; they won't exist
    // until `yarn docs:api` (or the full build script) has been run.
    /api\/dobot_api_v4/,
  ],
}));

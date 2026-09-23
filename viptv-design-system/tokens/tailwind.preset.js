/** VIPTV Tailwind preset — generated from tokens.json.
 *  Usage: module.exports = { presets: [require('./tailwind.preset.js')], ... }
 *  Set --viptv-accent on :root to the user's accent choice. */
module.exports = {
  "darkMode": "class",
  "theme": {
    "extend": {
      "colors": {
        "bg": "#0B0B0C",
        "oled": "#000000",
        "surface": {
          "1": "#161618",
          "2": "#212124",
          "3": "#2A2A2E",
          "4": "#34343A"
        },
        "text": {
          "primary": "#F4F2EE",
          "body": "#DAD8D3",
          "secondary": "#B6B4AF",
          "tertiary": "#8F8D89"
        },
        "on": {
          "light": "#111113",
          "accent": "#15130F"
        },
        "accent": {
          "DEFAULT": "var(--viptv-accent, #F5C542)",
          "gold": "#F5C542",
          "coral": "#FF8B5C",
          "mint": "#62D9BC",
          "periwinkle": "#A3BCFF"
        },
        "live": "#FF5A4E",
        "danger": {
          "DEFAULT": "#FF7A6E",
          "tv": "#FF8A7E"
        },
        "line": {
          "hairline": "rgba(255,255,255,0.07)",
          "chip": "rgba(255,255,255,0.10)",
          "outline": "rgba(255,255,255,0.14)",
          "strong": "rgba(255,255,255,0.22)"
        }
      },
      "fontFamily": {
        "display": [
          "Bricolage Grotesque",
          "Helvetica Neue",
          "sans-serif"
        ],
        "ui": [
          "Onest",
          "system-ui",
          "sans-serif"
        ],
        "mono": [
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Consolas",
          "monospace"
        ]
      },
      "fontSize": {
        "phone-screen-title": [
          "34px",
          {
            "lineHeight": "1.05",
            "letterSpacing": "-0.02em",
            "fontWeight": "700"
          }
        ],
        "phone-sheet-title": [
          "24px",
          {
            "lineHeight": "1.2",
            "letterSpacing": "-0.01em",
            "fontWeight": "700"
          }
        ],
        "phone-wordmark": [
          "24px",
          {
            "lineHeight": "1",
            "letterSpacing": "-0.03em",
            "fontWeight": "800"
          }
        ],
        "phone-section": [
          "20px",
          {
            "lineHeight": "1.15",
            "letterSpacing": "-0.01em",
            "fontWeight": "650"
          }
        ],
        "phone-button-primary": [
          "17px",
          {
            "lineHeight": "1",
            "letterSpacing": "0em",
            "fontWeight": "700"
          }
        ],
        "phone-body-strong": [
          "16px",
          {
            "lineHeight": "1.35",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "phone-body": [
          "15px",
          {
            "lineHeight": "1.45",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "phone-label": [
          "14px",
          {
            "lineHeight": "1.3",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "phone-meta": [
          "13px",
          {
            "lineHeight": "1.35",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "phone-caption": [
          "12px",
          {
            "lineHeight": "1.35",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "phone-eyebrow": [
          "11px",
          {
            "lineHeight": "1.2",
            "letterSpacing": "0.08em",
            "fontWeight": "700"
          }
        ],
        "phone-nav-label": [
          "11px",
          {
            "lineHeight": "1",
            "letterSpacing": "0.01em",
            "fontWeight": "600"
          }
        ],
        "desktop-page-title": [
          "40px",
          {
            "lineHeight": "1.05",
            "letterSpacing": "-0.02em",
            "fontWeight": "700"
          }
        ],
        "desktop-hero-title": [
          "30px",
          {
            "lineHeight": "1.05",
            "letterSpacing": "-0.02em",
            "fontWeight": "800"
          }
        ],
        "desktop-dialog-title": [
          "24px",
          {
            "lineHeight": "1.2",
            "letterSpacing": "-0.01em",
            "fontWeight": "700"
          }
        ],
        "desktop-section": [
          "22px",
          {
            "lineHeight": "1.15",
            "letterSpacing": "-0.01em",
            "fontWeight": "650"
          }
        ],
        "desktop-wordmark": [
          "13px",
          {
            "lineHeight": "1",
            "letterSpacing": "0.02em",
            "fontWeight": "700"
          }
        ],
        "desktop-button": [
          "16px",
          {
            "lineHeight": "1",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "desktop-body": [
          "16px",
          {
            "lineHeight": "1.5",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "desktop-label": [
          "15px",
          {
            "lineHeight": "1.3",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "desktop-row": [
          "14px",
          {
            "lineHeight": "1.3",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "desktop-meta": [
          "13px",
          {
            "lineHeight": "1.35",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "desktop-caption": [
          "12px",
          {
            "lineHeight": "1.35",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "desktop-eyebrow": [
          "12px",
          {
            "lineHeight": "1.2",
            "letterSpacing": "0.06em",
            "fontWeight": "700"
          }
        ],
        "desktop-rail-label": [
          "11px",
          {
            "lineHeight": "1",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "tv-screen-title": [
          "56px",
          {
            "lineHeight": "1.05",
            "letterSpacing": "-0.02em",
            "fontWeight": "700"
          }
        ],
        "tv-panel-title": [
          "44px",
          {
            "lineHeight": "1.1",
            "letterSpacing": "-0.01em",
            "fontWeight": "700"
          }
        ],
        "tv-section": [
          "32px",
          {
            "lineHeight": "1.1",
            "letterSpacing": "-0.01em",
            "fontWeight": "650"
          }
        ],
        "tv-wordmark": [
          "40px",
          {
            "lineHeight": "1",
            "letterSpacing": "-0.02em",
            "fontWeight": "800"
          }
        ],
        "tv-row": [
          "28px",
          {
            "lineHeight": "1.3",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "tv-button": [
          "26px",
          {
            "lineHeight": "1",
            "letterSpacing": "0em",
            "fontWeight": "700"
          }
        ],
        "tv-body": [
          "26px",
          {
            "lineHeight": "1.45",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "tv-label": [
          "24px",
          {
            "lineHeight": "1.3",
            "letterSpacing": "0em",
            "fontWeight": "600"
          }
        ],
        "tv-meta": [
          "22px",
          {
            "lineHeight": "1.35",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "tv-caption": [
          "20px",
          {
            "lineHeight": "1.35",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ],
        "tv-eyebrow": [
          "18px",
          {
            "lineHeight": "1.2",
            "letterSpacing": "0.08em",
            "fontWeight": "700"
          }
        ],
        "tv-min": [
          "18px",
          {
            "lineHeight": "1.3",
            "letterSpacing": "0em",
            "fontWeight": "400"
          }
        ]
      },
      "borderRadius": {
        "xs": "4px",
        "sm": "8px",
        "md": "12px",
        "lg": "14px",
        "xl": "16px",
        "2xl": "18px",
        "3xl": "22px",
        "sheet": "28px"
      },
      "spacing": {
        "0": "0px",
        "0.5": "2px",
        "1": "4px",
        "1.5": "6px",
        "2": "8px",
        "2.5": "10px",
        "3": "12px",
        "3.5": "14px",
        "4": "16px",
        "4.5": "18px",
        "5": "20px",
        "5.5": "22px",
        "6": "24px",
        "7": "28px",
        "8": "32px",
        "9": "36px",
        "12": "48px",
        "16": "64px",
        "24": "96px"
      },
      "boxShadow": {
        "focus": "0 0 0 2px #0B0B0C, 0 0 0 4px #F4F2EE",
        "card-hover": "inset 0 0 0 2px #F4F2EE",
        "tv-focus": "0 0 0 4px #FFFFFF, 0 24px 60px rgba(0,0,0,0.65)",
        "nav": "0 12px 32px rgba(0,0,0,0.55)",
        "popover": "0 20px 60px rgba(0,0,0,0.55)",
        "toast": "0 12px 30px rgba(0,0,0,0.5)",
        "tv-panel": "-40px 0 100px rgba(0,0,0,0.6)"
      },
      "height": {
        "btn-phone": "54px",
        "btn-desktop": "48px",
        "btn-tv": "72px",
        "chip-phone": "44px",
        "chip-desktop": "40px",
        "titlebar": "40px"
      },
      "width": {
        "rail": "84px",
        "tv-rail": "144px",
        "tv-menu": "520px",
        "tv-panel": "820px",
        "dialog": "460px",
        "popup": "340px"
      }
    }
  }
};

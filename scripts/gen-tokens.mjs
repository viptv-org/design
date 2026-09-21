#!/usr/bin/env node
// Generate tokens/tokens.css from tokens/responsive.json.
//
// The JSON is the machine-readable token source (authority:
// RESPONSIVE_VIPTV_ALIGNMENT.md). Run this script after any token change and
// commit the result together with the JSON; scripts/validate.py verifies the
// committed file stays in sync. Consumers vendor the generated file through
// their design-sync tooling — never hand-edit tokens.css.
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const tokens = JSON.parse(readFileSync(join(root, 'tokens/responsive.json'), 'utf8'));

// VISUAL_SYSTEM.md defines the inverted focus text color ("on-light") that
// pairs with the focus fill; it is constant across the dark and oled themes.
const ON_LIGHT = '#101112';

const css = [];
css.push('/* Generated from tokens/responsive.json by scripts/gen-tokens.mjs — do not edit.');
css.push('   Authority: RESPONSIVE_VIPTV_ALIGNMENT.md. */');
css.push('');
for (const [theme, values] of Object.entries(tokens.themes)) {
  const selector = theme === 'dark' ? ':root, .viptv-theme-dark' : `.viptv-theme-${theme}`;
  css.push(`${selector} {`);
  css.push('  color-scheme: dark;');
  for (const [name, value] of Object.entries(values)) {
    css.push(`  --viptv-${name}: ${value};`);
  }
  if (theme === 'dark') {
    css.push(`  --viptv-on-light: ${ON_LIGHT};`);
  }
  css.push('}');
  css.push('');
}
css.push(':root {');
css.push(`  --viptv-radius-action: ${tokens.actions.radius}px;`);
css.push(`  --viptv-radius-art: ${tokens.cards.artRadius}px;`);
css.push(`  --viptv-focus-width: ${tokens.cards.focusWidth}px;`);
const kebab = (name) => name.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
for (const [name, value] of Object.entries(tokens.spacing)) {
  css.push(`  --viptv-${kebab(name)}: ${value}px;`);
}
css.push(`  --viptv-action-height: ${tokens.actions.primaryHeight}px;`);
css.push(`  --viptv-action-height-phone: ${tokens.actions.phoneHeight}px;`);
css.push('}');
css.push('');

writeFileSync(join(root, 'tokens/tokens.css'), css.join('\n'));
console.log('tokens/tokens.css regenerated');

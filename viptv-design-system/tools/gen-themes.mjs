#!/usr/bin/env node
// Generate every VIPTV platform theme from tokens/tokens.json (the single source of truth).
//
//   node design/viptv-design-system/tools/gen-themes.mjs            write all targets
//   node design/viptv-design-system/tools/gen-themes.mjs --check    exit 1 if any target is stale
//
// Targets are listed in tools/targets.json (paths relative to the workspace root, the folder that
// holds design/, tv-web/, android/ …). A target whose repository is not checked out is skipped.
// Every written file starts with a GENERATED banner: never hand-edit it, change tokens.json and rerun.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const systemDir = resolve(here, '..');
const workspace = resolve(systemDir, '..', '..');
const tokens = JSON.parse(readFileSync(join(systemDir, 'tokens/tokens.json'), 'utf8'));
const targets = JSON.parse(readFileSync(join(here, 'targets.json'), 'utf8'));
const check = process.argv.includes('--check');

// ---------------------------------------------------------------------------------------------
// Token model
// ---------------------------------------------------------------------------------------------

/** Flatten the W3C token tree into [{ path: string[], type, value, description }]. */
function flatten(node, path = [], inheritedType) {
  const out = [];
  const type = node.$type ?? inheritedType;
  if (Object.hasOwn(node, '$value')) return [{ path, type, value: node.$value, description: node.$description }];
  for (const [key, child] of Object.entries(node)) {
    if (key.startsWith('$')) continue;
    out.push(...flatten(child, [...path, key], type));
  }
  return out;
}
const all = flatten(tokens);
const byPath = new Map(all.map(t => [t.path.join('.'), t]));

/** Resolve "{a.b.c}" references (whole-value or embedded). */
function resolveRef(value) {
  if (typeof value !== 'string') return value;
  const whole = value.match(/^\{([^}]+)\}$/);
  if (whole) {
    const target = byPath.get(whole[1]);
    if (!target) throw new Error(`Unknown token reference ${value}`);
    return resolveRef(target.value);
  }
  return value.replace(/\{([^}]+)\}/g, (_, ref) => {
    const target = byPath.get(ref);
    if (!target) throw new Error(`Unknown token reference {${ref}}`);
    return String(resolveRef(target.value));
  });
}

const cssName = path => `--viptv-${path.join('-').replace(/\./g, '_')}`;
const isMachine = t => t.type !== 'string';
const fontStack = list => list.map(f => (/\s/.test(f) && !/^(sans-serif|serif|monospace|system-ui)$/.test(f) ? `'${f}'` : f)).join(', ');

function cssValue(t) {
  const v = resolveRef(t.value);
  if (t.type === 'fontFamily') return fontStack(v);
  if (t.type === 'typography') return null;
  if (Array.isArray(v)) return v.join(', ');
  return String(v);
}

function typeRoles() {
  return all.filter(t => t.type === 'typography').map(t => {
    const v = t.value;
    const family = resolveRef(v.fontFamily);
    return {
      platform: t.path[1], role: t.path[2], path: t.path,
      family: Array.isArray(family) ? family : [family],
      familyRef: typeof v.fontFamily === 'string' ? v.fontFamily.replace(/[{}]/g, '') : null,
      size: parseFloat(v.fontSize), weight: v.fontWeight, lineHeight: v.lineHeight,
      letterSpacing: v.letterSpacing ?? '0em', uppercase: t.path[2] === 'eyebrow',
    };
  });
}

const colors = all.filter(t => t.type === 'color');

/** Parse #RRGGBB / #RRGGBBAA / rgba(r,g,b,a) into {r,g,b,a}. */
function parseColor(value) {
  const hex = value.match(/^#([0-9a-f]{6})([0-9a-f]{2})?$/i);
  if (hex) {
    const n = parseInt(hex[1], 16);
    return { r: n >> 16, g: (n >> 8) & 255, b: n & 255, a: hex[2] ? parseInt(hex[2], 16) / 255 : 1 };
  }
  const rgba = value.match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)$/i);
  if (rgba) return { r: +rgba[1], g: +rgba[2], b: +rgba[3], a: rgba[4] === undefined ? 1 : +rgba[4] };
  throw new Error(`Unsupported colour ${value}`);
}
const hex2 = n => n.toString(16).padStart(2, '0').toUpperCase();

// ---------------------------------------------------------------------------------------------
// Emitters
// ---------------------------------------------------------------------------------------------

const banner = (comment, source) => [
  `${comment} GENERATED FILE — DO NOT EDIT.`,
  `${comment} Source: design/viptv-design-system/tokens/tokens.json`,
  `${comment} Regenerate: node design/viptv-design-system/tools/gen-themes.mjs`,
  ...(source ? [`${comment} ${source}`] : []),
].join('\n');

function emitCss({ googleFonts = false, reset = true } = {}) {
  const lines = ['/*', ...banner(' *').split('\n'), ' */'];
  if (googleFonts) lines.push("@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Onest:wght@400;500;600;700&display=swap');");
  lines.push('', ':root {');
  for (const t of all) {
    if (!isMachine(t) || t.type === 'typography') continue;
    lines.push(`  ${cssName(t.path)}: ${cssValue(t)};`);
  }
  for (const r of typeRoles()) {
    const base = cssName(['type', r.platform, r.role]);
    lines.push(`  ${base}-size: ${r.size}px;`, `  ${base}-weight: ${r.weight};`, `  ${base}-line-height: ${r.lineHeight};`, `  ${base}-letter-spacing: ${r.letterSpacing};`);
  }
  lines.push('  /* The one runtime accent the user picks (Settings). Components read only this. */');
  lines.push(`  --viptv-accent: var(${cssName(['color', 'accent', 'default'])});`);
  lines.push('}', '', '/* OLED mode (device setting) */', `:root[data-oled] { ${cssName(['color', 'bg'])}: var(${cssName(['color', 'bg-oled'])}); }`, '');
  lines.push('/* Accent choices: <html data-accent="gold|coral|mint|periwinkle"> */');
  for (const t of colors.filter(c => c.path[1] === 'accent' && c.path[2] === 'options')) {
    lines.push(`:root[data-accent="${t.path[3]}"] { --viptv-accent: var(${cssName(t.path)}); }`);
  }
  lines.push('', '/* Type roles: .viptv-type-<platform>-<role> */');
  for (const r of typeRoles()) {
    const base = cssName(['type', r.platform, r.role]);
    const fam = r.familyRef ? `var(${cssName(r.familyRef.split('.'))})` : fontStack(r.family);
    lines.push(`.viptv-type-${r.platform}-${r.role} { font-family: ${fam}; font-size: var(${base}-size); font-weight: var(${base}-weight); line-height: var(${base}-line-height); letter-spacing: var(${base}-letter-spacing);${r.uppercase ? ' text-transform: uppercase;' : ''} }`);
  }
  if (reset) {
    lines.push('', '/* Base reset the screens assume (buttons have no UA background or border). */',
      'button { font: inherit; color: inherit; background: transparent; border: 0; cursor: pointer; }',
      'a { color: inherit; text-decoration: none; }');
  }
  return lines.join('\n') + '\n';
}

function emitTs() {
  const flat = {};
  for (const t of all) flat[t.path.join('.')] = t.type === 'typography'
    ? { ...t.value, fontFamily: resolveRef(t.value.fontFamily) }
    : resolveRef(t.value);
  const accentOptions = Object.fromEntries(colors.filter(c => c.path[2] === 'options').map(c => [c.path[3], c.value]));
  return `${banner('//')}\n` +
    `export const tokens = ${JSON.stringify(flat, null, 2)} as const;\n` +
    `export type TokenName = keyof typeof tokens;\n` +
    `export const accentOptions = ${JSON.stringify(accentOptions, null, 2)} as const;\n` +
    `export type AccentName = keyof typeof accentOptions;\n` +
    `/** CSS custom property for a token path, e.g. cssVar('color.surface.1'). */\n` +
    `export const cssVar = (name: TokenName): string => \`var(--viptv-\${name.replace(/\\./g, '-')})\`;\n`;
}

function emitTailwindPreset() {
  const color = {};
  for (const t of colors) {
    const [, ...rest] = t.path;
    color[rest.join('-')] = `var(${cssName(t.path)})`;
  }
  color.accent = 'var(--viptv-accent)';
  const radius = Object.fromEntries(all.filter(t => t.path[0] === 'radius' && t.type === 'dimension').map(t => [t.path[1], `var(${cssName(t.path)})`]));
  const spacing = Object.fromEntries(all.filter(t => t.path[0] === 'space').map(t => [t.path.slice(1).join('.'), `var(${cssName(t.path)})`]));
  const fontSize = Object.fromEntries(typeRoles().map(r => [`${r.platform}-${r.role}`, [`${r.size}px`, { lineHeight: String(r.lineHeight), letterSpacing: r.letterSpacing, fontWeight: String(r.weight) }]]));
  const shadow = Object.fromEntries(all.filter(t => t.path[0] === 'shadow' || (t.path[0] === 'focus' && t.type === 'shadow')).map(t => [t.path.join('-'), `var(${cssName(t.path)})`]));
  const preset = { theme: { extend: { colors: color, borderRadius: radius, spacing, fontSize, boxShadow: shadow,
    fontFamily: { display: `var(${cssName(['font', 'family', 'display'])})`, ui: `var(${cssName(['font', 'family', 'ui'])})`, mono: `var(${cssName(['font', 'family', 'mono'])})` } } } };
  return `${banner('//')}\n// Requires tokens.css (the CSS variables) to be loaded.\nmodule.exports = ${JSON.stringify(preset, null, 2)};\n`;
}

function emitKotlin({ packageName }) {
  const ident = path => path.map((p, i) => {
    const s = p.replace(/[^a-zA-Z0-9]+(.)?/g, (_, c) => (c ? c.toUpperCase() : '')).replace(/^\d/, d => `N${d}`);
    return i === 0 ? s : s.charAt(0).toUpperCase() + s.slice(1);
  }).join('');
  const out = [banner('//'), `package ${packageName}`, '', 'import androidx.compose.ui.graphics.Color', 'import androidx.compose.ui.unit.dp', 'import androidx.compose.ui.unit.sp', 'import androidx.compose.ui.unit.em', 'import androidx.compose.ui.text.font.FontWeight', '', '/** VIPTV design tokens. The accent is a runtime value: read it from settings, default [ViptvColor.AccentDefault]. */', 'object ViptvColor {'];
  for (const t of colors) {
    const c = parseColor(t.value);
    const argb = `0x${hex2(Math.round(c.a * 255))}${hex2(c.r)}${hex2(c.g)}${hex2(c.b)}`;
    out.push(`    val ${ident(t.path.slice(1))} = Color(${argb})`);
  }
  out.push('}', '', 'object ViptvDimen {');
  for (const t of all.filter(t => t.type === 'dimension')) out.push(`    val ${ident(t.path)} = ${parseFloat(t.value)}.dp`);
  out.push('}', '', 'data class ViptvTypeRole(val display: Boolean, val size: Float, val weight: FontWeight, val lineHeight: Float, val letterSpacingEm: Float)', '', 'object ViptvType {');
  for (const r of typeRoles()) out.push(`    val ${ident([r.platform, r.role])} = ViptvTypeRole(display = ${r.familyRef === 'font.family.display'}, size = ${r.size}f, weight = FontWeight(${r.weight}), lineHeight = ${r.lineHeight}f, letterSpacingEm = ${parseFloat(r.letterSpacing)}f)`);
  out.push('}', '', 'object ViptvMotion {');
  for (const t of all.filter(t => t.path[0] === 'motion' && (t.type === 'number' || t.type === 'duration'))) out.push(`    const val ${ident(t.path.slice(1))} = ${t.type === 'duration' ? `${parseFloat(t.value)}L` : `${t.value}f`}`);
  out.push('}', '');
  return out.join('\n');
}

function emitBrightScript() {
  const out = [banner("'"), '', "' Roku SceneGraph colours are 0xRRGGBBAA strings.", 'function ViptvTokens() as object', '    return {'];
  const key = path => path.join('_').replace(/[^a-zA-Z0-9_]/g, '_');
  for (const t of colors) {
    const c = parseColor(t.value);
    out.push(`        color_${key(t.path.slice(1))}: "0x${hex2(c.r)}${hex2(c.g)}${hex2(c.b)}${hex2(Math.round(c.a * 255))}"`);
  }
  for (const t of all.filter(t => t.type === 'dimension' && t.path[0] !== 'space')) out.push(`        ${key(t.path)}: ${parseFloat(t.value)}`);
  out.push('    }', 'end function', '');
  return out.join('\n');
}

const emitters = {
  css: opts => emitCss(opts),
  ts: () => emitTs(),
  'tailwind-preset': () => emitTailwindPreset(),
  kotlin: opts => emitKotlin(opts),
  brightscript: () => emitBrightScript(),
};

// ---------------------------------------------------------------------------------------------
// Write / check
// ---------------------------------------------------------------------------------------------

let stale = 0;
let written = 0;
for (const target of targets) {
  const repo = join(workspace, target.repo);
  if (!existsSync(repo)) { console.log(`skip ${target.repo} (not checked out)`); continue; }
  for (const file of target.files) {
    const emit = emitters[file.format];
    if (!emit) throw new Error(`Unknown format ${file.format}`);
    const content = emit(file.options ?? {});
    const path = join(repo, file.path);
    const current = existsSync(path) ? readFileSync(path, 'utf8') : null;
    if (current === content) continue;
    if (check) { console.log(`stale ${relative(workspace, path)}`); stale++; continue; }
    mkdirSync(dirname(path), { recursive: true });
    writeFileSync(path, content);
    console.log(`wrote ${relative(workspace, path)}`);
    written++;
  }
}
if (check && stale) { console.error(`${stale} generated theme file(s) are stale; run gen-themes.mjs`); process.exit(1); }
console.log(check ? 'All generated themes are current.' : `${written} file(s) written.`);

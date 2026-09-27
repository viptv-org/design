// Export the remaining native settings/editor Lucide controls. Usage:
// node export_design_controls.cjs <react-node_modules> <canvas-node_modules>
// Sources: lucide-react 0.468.0, React 18.3.1; raster: node-canvas 4.0.0-rc3.
const { createRequire } = require('node:module');
const { resolve } = require('node:path');
const { writeFileSync } = require('node:fs');
const ui = createRequire(resolve(process.argv[2], '_export.cjs'));
const raster = createRequire(resolve(process.argv[3], '_export.cjs'));
const React = ui('react');
const { renderToStaticMarkup } = ui('react-dom/server');
const { UserRound, Puzzle, Trash2, Delete, Space } = ui('lucide-react');
const { createCanvas, loadImage } = raster('canvas');
const out = resolve(__dirname, '../images/lucide');
(async () => {
  for (const [name, icon] of Object.entries({ profile: UserRound, addons: Puzzle, delete: Trash2, backspace: Delete, space: Space })) {
    for (const [variant, color] of Object.entries({ primary: '#F4F2EE', secondary: '#B6B4AF', focus: '#111113' })) {
      const svg = renderToStaticMarkup(React.createElement(icon, { width: 96, height: 96, color, strokeWidth: 1.8 }));
      writeFileSync(resolve(out, `${name}-${variant}.svg`), svg + '\n');
      const canvas = createCanvas(96, 96);
      canvas.getContext('2d').drawImage(await loadImage(Buffer.from(svg)), 0, 0);
      writeFileSync(resolve(out, `${name}-${variant}.png`), canvas.toBuffer('image/png'));
    }
  }
})();

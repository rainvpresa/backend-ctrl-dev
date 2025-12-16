const fs = require('fs');
const path = require('path');

const buildDir = path.resolve(__dirname, '..', 'cms', 'build');
const targetDir = path.resolve(__dirname, '..', '..', 'AGHAMazingQuestMobile', 'static', 'cms');

function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) copyRecursive(srcPath, destPath);
    else fs.copyFileSync(srcPath, destPath);
  }
}

// Clear target
if (fs.existsSync(targetDir)) {
  fs.rmSync(targetDir, { recursive: true, force: true });
}
fs.mkdirSync(targetDir, { recursive: true });
copyRecursive(buildDir, targetDir);
console.log(`Copied ${buildDir} -> ${targetDir}`);

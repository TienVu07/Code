'use strict';

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const readline = require('node:readline');
const { spawnSync } = require('node:child_process');

// =========================
// CONFIG
// =========================
const WORKDIR = path.join(os.homedir(), 'storage', 'shared', 'Code', 'JavaScript', 'src');
fs.mkdirSync(WORKDIR, { recursive: true });

const OPTIONS = [
  'Run JavaScript file',
  'Edit JavaScript file',
  'Create file',
  'Delete file',
  'Rename file',
  'Git Push',
  'Git Status',
  'File list',
  'Back',
];

const ESC = '\x1b';
let tuiActive = false;
let pendingKey = null;
const keyQueue = [];

class ExitApp extends Error {}

// =========================
// TERMINAL / INPUT
// =========================
readline.emitKeypressEvents(process.stdin);

process.stdin.on('keypress', (str, key = {}) => {
  if (!tuiActive) return;

  if (key.ctrl && key.name === 'c') {
    deliverKey({ name: 'c', ctrl: true });
    return;
  }

  const name = key.name;
  if (name || str) deliverKey({ name, str });
});

function deliverKey(key) {
  if (pendingKey) {
    const resolve = pendingKey;
    pendingKey = null;
    resolve(key);
  } else {
    keyQueue.push(key);
  }
}

function readKey() {
  if (keyQueue.length) {
    const key = keyQueue.shift();
    if (key.ctrl && key.name === 'c') throw new ExitApp();
    return Promise.resolve(key);
  }
  return new Promise((resolve, reject) => {
    pendingKey = (key) => {
      if (key.ctrl && key.name === 'c') reject(new ExitApp());
      else resolve(key);
    };
  });
}

function clearScreen() {
  process.stdout.write(`${ESC}[2J${ESC}[H`);
}

function enterTui() {
  if (!process.stdin.isTTY || typeof process.stdin.setRawMode !== 'function') {
    throw new Error('Menu cần chạy trong terminal tương tác của Termux.');
  }
  tuiActive = true;
  keyQueue.length = 0;
  process.stdin.setRawMode(true);
  process.stdin.resume();
  process.stdout.write(`${ESC}[?25l`);
  clearScreen();
}

function leaveTui() {
  tuiActive = false;
  keyQueue.length = 0;
  process.stdout.write(`${ESC}[?25h`);
  if (process.stdin.isTTY && typeof process.stdin.setRawMode === 'function') {
    process.stdin.setRawMode(false);
  }
  clearScreen();
}

function restoreTui() {
  tuiActive = true;
  keyQueue.length = 0;
  if (process.stdin.isTTY && typeof process.stdin.setRawMode === 'function') {
    process.stdin.setRawMode(true);
  }
  process.stdin.resume();
  process.stdout.write(`${ESC}[?25l`);
  clearScreen();
}

function cleanText(value, maxWidth) {
  return String(value).replace(/[\r\n\x00-\x1f\x7f]/g, '').slice(0, Math.max(0, maxWidth));
}

function drawLines(lines) {
  clearScreen();
  for (const line of lines) process.stdout.write(`${line}\n`);
}

async function ask(prompt) {
  leaveTui();
  let answer = '';
  try {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    answer = await new Promise((resolve) => {
      rl.question(prompt, (value) => {
        rl.close();
        resolve(value);
      });
    });
  } finally {
    restoreTui();
  }
  return answer.trim();
}

async function pause(message = 'Press ENTER to return...') {
  await ask(`\n${message}`);
}

// =========================
// FILES
// =========================
function listPyFiles() {
  try {
    return fs.readdirSync(WORKDIR, { withFileTypes: true })
      .filter((entry) => entry.isFile() && entry.name.endsWith('.js'))
      .map((entry) => path.join(WORKDIR, entry.name))
      .sort((a, b) => path.basename(a).localeCompare(path.basename(b)));
  } catch (error) {
    showError(`Cannot list files: ${error.message}`);
    return [];
  }
}

function fileName(filePath) {
  return path.basename(filePath);
}

function normalizePyName(value) {
  let name = value.trim();
  if (!name) return null;
  if (!name.endsWith('.js')) name += '.js';
  // Only allow a file name, not a path outside WORKDIR.
  if (name !== path.basename(name) || name === '.' || name === '..' || /[\\/]/.test(name)) {
    return null;
  }
  return name;
}

function showError(message) {
  process.stdout.write(`\nError: ${message}\n`);
}

// =========================
// EXTERNAL COMMANDS
// =========================
async function runExternal(command, args = [], options = {}) {
  const { cwd = WORKDIR, wait = true } = options;
  leaveTui();
  let result;

  try {
    result = spawnSync(command, args, {
      cwd,
      stdio: 'inherit',
      env: process.env,
    });

    if (result.error) showError(result.error.message);
    else if (result.status !== 0 && result.status !== null) {
      process.stdout.write(`\nProcess exited with code ${result.status}.\n`);
    } else if (result.signal) {
      process.stdout.write(`\nProcess stopped by signal ${result.signal}.\n`);
    }
  } catch (error) {
    showError(error.message);
  }

  if (wait) {
    // Keep terminal in normal line mode until the user returns.
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    await new Promise((resolve) => {
      rl.question('\nPress ENTER to return...', () => {
        rl.close();
        resolve();
      });
    });
  }

  restoreTui();
}

async function terminal() {
  await runExternal('bash', [], { wait: false, cwd: WORKDIR });
}

// =========================
// FILE PICKER
// =========================
async function pickFile(title) {
  const files = listPyFiles();
  if (!files.length) {
    drawLines(['', '  No JavaScript files found.', '', '  Press any key...']);
    await readKey();
    return null;
  }

  let index = 0;
  while (true) {
    const height = process.stdout.rows || 24;
    const width = process.stdout.columns || 80;
    const maxVisible = Math.max(1, height - 6);
    const start = Math.max(0, index - maxVisible + 1);
    const visible = files.slice(start, start + maxVisible);
    const lines = ['', `  ${title}`, ''];

    visible.forEach((file, offset) => {
      const realIndex = start + offset;
      const prefix = realIndex === index ? '> ' : '  ';
      let text = cleanText(fileName(file), width - 10);
      if (realIndex === index) text = `\x1b[7m${prefix}${text}\x1b[0m`;
      else text = `${prefix}${text}`;
      lines.push(`    ${text}`);
    });
    while (lines.length < height - 2) lines.push('');
    lines.push('  ↑ ↓ move | Enter select | q cancel');
    drawLines(lines.slice(0, height));

    const key = await readKey();
    if (key.ctrl && key.name === 'c') throw new ExitApp();
    if (key.name === 'up') index = (index - 1 + files.length) % files.length;
    else if (key.name === 'down') index = (index + 1) % files.length;
    else if (key.name === 'return') return files[index];
    else if (key.str === 'q' || key.name === 'escape') return null;
  }
}

// =========================
// RUN PYTHON
// =========================
async function runJavaScript() {
  const file = await pickFile('Run JavaScript file');
  if (!file) return;
  await runExternal('node', [file]);
}

// =========================
// EDIT FILE
// =========================
async function editJavaScript() {
  const file = await pickFile('Edit JavaScript file');
  if (!file) return;
  await runExternal('nvim', [file], { wait: false });
}

// =========================
// CREATE FILE
// =========================
async function createFile() {
  const input = await ask('Enter file name (.js): ');
  const name = normalizePyName(input);
  if (!name) {
    drawLines(['', '  Invalid file name.', '', '  Press any key...']);
    await readKey();
    return;
  }

  const target = path.join(WORKDIR, name);
  try {
    fs.writeFileSync(target, '', { flag: 'wx' });
    drawLines(['', `  Created: ${name}`, '', '  Press any key...']);
  } catch (error) {
    drawLines(['', error.code === 'EEXIST' ? '  File already exists.' : `  Error: ${error.message}`, '', '  Press any key...']);
  }
  await readKey();
}

// =========================
// DELETE FILE
// =========================
async function deleteFile() {
  const file = await pickFile('Delete file');
  if (!file) return;

  try {
    fs.unlinkSync(file);
    drawLines(['', `  Deleted: ${fileName(file)}`, '', '  Press any key...']);
  } catch (error) {
    drawLines(['', `  Error: ${error.message}`, '', '  Press any key...']);
  }
  await readKey();
}

// =========================
// RENAME FILE
// =========================
async function renameFile() {
  const file = await pickFile('Rename file');
  if (!file) return;

  const input = await ask('New name (.js): ');
  const name = normalizePyName(input);
  if (!name) {
    drawLines(['', '  Invalid file name.', '', '  Press any key...']);
    await readKey();
    return;
  }

  const target = path.join(WORKDIR, name);
  try {
    if (fs.existsSync(target)) {
      drawLines(['', '  File already exists.', '', '  Press any key...']);
    } else {
      fs.renameSync(file, target);
      drawLines(['', `  Renamed to: ${name}`, '', '  Press any key...']);
    }
  } catch (error) {
    drawLines(['', `  Error: ${error.message}`, '', '  Press any key...']);
  }
  await readKey();
}

// =========================
// GIT PUSH / STATUS
// =========================
async function gitPush() {
  await runExternal('bash', ['-c', "git add . && git commit -m 'update' && git push"]);
}

async function gitStatus() {
  await runExternal('git', ['status']);
}

// =========================
// FILE LIST
// =========================
async function fileList() {
  const files = listPyFiles();
  const height = process.stdout.rows || 24;
  const width = process.stdout.columns || 80;
  const lines = ['', '  FILES:', ''];

  if (!files.length) lines.push('  No JavaScript files.');
  else {
    const maxShow = Math.max(1, height - 6);
    for (const file of files.slice(0, maxShow)) {
      lines.push(`  ${cleanText(fileName(file), width - 4)}`);
    }
    if (files.length > maxShow) lines.push(`  ... and ${files.length - maxShow} more`);
  }

  while (lines.length < height - 2) lines.push('');
  lines.push('  Press any key...');
  drawLines(lines.slice(0, height));
  await readKey();
}

// =========================
// MAIN MENU
// =========================
async function main() {
  let index = 0;

  while (true) {
    const height = process.stdout.rows || 24;
    const width = process.stdout.columns || 80;
    const lines = ['', '  \x1b[1mJAVASCRIPT IDE\x1b[0m', ''];

    OPTIONS.forEach((option, i) => {
      const text = cleanText(option, width - 10);
      if (i === index) lines.push(`    \x1b[7m> ${text}\x1b[0m`);
      else lines.push(`      ${text}`);
    });

    while (lines.length < height - 2) lines.push('');
    lines.push('  ↑ ↓ move | Enter select | Ctrl+C exit');
    drawLines(lines.slice(0, height));

    const key = await readKey();
    if (key.ctrl && key.name === 'c') throw new ExitApp();
    if (key.name === 'up') index = (index - 1 + OPTIONS.length) % OPTIONS.length;
    else if (key.name === 'down') index = (index + 1) % OPTIONS.length;
    else if (key.name === 'return') {
      switch (OPTIONS[index]) {
        case 'Run JavaScript file': await runJavaScript(); break;
        case 'Edit JavaScript file': await editJavaScript(); break;
        case 'Create file': await createFile(); break;
        case 'Delete file': await deleteFile(); break;
        case 'Rename file': await renameFile(); break;
        case 'Git Push': await gitPush(); break;
        case 'Git Status': await gitStatus(); break;
        case 'File list': await fileList(); break;
        case 'Back': return;
        default: break;
      }
    }
  }
}

// =========================
// START
// =========================
async function start() {
  try {
    enterTui();
    await main();
  } catch (error) {
    if (!(error instanceof ExitApp)) {
      process.stderr.write(`\nmenu.js: ${error.stack || error.message}\n`);
      process.exitCode = 1;
    }
  } finally {
    tuiActive = false;
    if (process.stdin.isTTY && typeof process.stdin.setRawMode === 'function') {
      try { process.stdin.setRawMode(false); } catch {}
    }
    process.stdout.write(`${ESC}[?25h`);
    clearScreen();
    process.stdin.pause();
  }
}

start();

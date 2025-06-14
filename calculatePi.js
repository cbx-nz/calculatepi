const fs = require('fs');
const path = require('path');

// Number of new digits to calculate per run
const DIGITS_PER_RUN = 1000;

// Load state
const statePath = path.join(__dirname, 'state.json');
let start = 0;
if (fs.existsSync(statePath)) {
    const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    start = state.start || 0;
}

// BBP formula for hex digits of π (spigot-like)
function piDigitHex(n) {
    function S(j, n) {
        let sum = 0;
        for (let k = 0; k <= n; k++) {
            const r = 8 * k + j;
            sum += (1 / Math.pow(16, n - k)) * (1 / r);
        }
        // Add a few terms of the tail
        for (let k = n + 1; k <= n + 100; k++) {
            const r = 8 * k + j;
            sum += Math.pow(16, n - k) / r;
        }
        return sum;
    }

    const x = 4 * S(1, n) - 2 * S(4, n) - S(5, n) - S(6, n);
    return ((x - Math.floor(x)) * 16) | 0; // Get nth hex digit
}

// Convert hex digits to decimal string (not exact but visual)
function hexDigitToChar(d) {
    return d.toString(16);
}

// Run calculation
let hexDigits = '';
for (let i = start; i < start + DIGITS_PER_RUN; i++) {
    const digit = piDigitHex(i);
    hexDigits += hexDigitToChar(digit);
}

// Append to pi.txt
const piFilePath = path.join(__dirname, 'pi.txt');
fs.appendFileSync(piFilePath, hexDigits);

// Update state
fs.writeFileSync(statePath, JSON.stringify({ start: start + DIGITS_PER_RUN }));

console.log(`Appended ${DIGITS_PER_RUN} hex digits of π to pi.txt starting from position ${start}`);
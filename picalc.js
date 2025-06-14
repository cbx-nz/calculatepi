const fs = require('fs');
const path = require('path');
const Decimal = require('decimal.js');

// Settings
const DIGITS_PER_RUN = 50000;
const LINE_LENGTH = 1000;
const CHUNK_SIZE = 500; // digits to compute per loop

// Files
const stateFile = path.join(__dirname, 'state.json');
const leftoverFile = path.join(__dirname, 'leftover.json');
const outputFile = path.join(__dirname, 'pi.txt');

// Load state
let totalDigitsDone = 0;
if (fs.existsSync(stateFile)) {
  totalDigitsDone = JSON.parse(fs.readFileSync(stateFile)).digits || 0;
}

// Load leftover digits from previous run
let leftover = '';
if (fs.existsSync(leftoverFile)) {
  leftover = JSON.parse(fs.readFileSync(leftoverFile)).digits || '';
}

// Set initial buffer
let buffer = leftover;
let digitsGenerated = 0;

// Helper functions
Decimal.set({ precision: totalDigitsDone + DIGITS_PER_RUN + 20 });

function arctan(x, terms) {
  let result = new Decimal(0);
  const x2 = new Decimal(x).mul(x);
  let num = new Decimal(x);
  let sign = 1;
  for (let i = 1; i < terms * 2; i += 2) {
    const term = num.div(i);
    result = sign > 0 ? result.plus(term) : result.minus(term);
    num = num.mul(x2);
    sign *= -1;
  }
  return result;
}

function computePi(terms) {
  const arctan1_5 = arctan(new Decimal(1).div(5), terms);
  const arctan1_239 = arctan(new Decimal(1).div(239), terms);
  return new Decimal(16).mul(arctan1_5).minus(new Decimal(4).mul(arctan1_239));
}

// Begin streaming calculation
while (digitsGenerated < DIGITS_PER_RUN) {
  const currentPrecision = totalDigitsDone + digitsGenerated + CHUNK_SIZE + 10;
  Decimal.set({ precision: currentPrecision });

  const pi = computePi(Math.floor(currentPrecision * 1.1)).toFixed(currentPrecision);
  let newDigits;

  if (totalDigitsDone + digitsGenerated === 0) {
    newDigits = pi.slice(2); // remove "3."
  } else {
    newDigits = pi.slice(2 + totalDigitsDone + digitsGenerated);
  }

  digitsGenerated += newDigits.length;
  buffer += newDigits;

  // Write full lines to file
  while (buffer.length >= LINE_LENGTH) {
    const line = buffer.slice(0, LINE_LENGTH);
    fs.appendFileSync(outputFile, line + '\n');
    buffer = buffer.slice(LINE_LENGTH);
    console.log(`Wrote 1000 digits. Total so far this run: ${digitsGenerated}`);
  }
}

// Save leftover
fs.writeFileSync(leftoverFile, JSON.stringify({ digits: buffer }));

// Update digit count
fs.writeFileSync(stateFile, JSON.stringify({ digits: totalDigitsDone + digitsGenerated }));

console.log(`\n✅ Finished. Wrote ${digitsGenerated - buffer.length} digits to pi.txt.`);
console.log(`💾 Saved ${buffer.length} leftover digits for next run.`);
// A working news-image-daily entry (Node 22, standard library only): its image is the entry.png beside this file, and
// the program copies it to /output/entry.png. A starting point, not a winner: replace the image. The gate takes a
// whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));

// Verify what was copied: the gate refuses anything that is not a whole
// PNG of at most 1 MiB and 1024 by 1024 pixels, so fail loudly here
// instead of shipping a bad file.
import { readFileSync } from 'node:fs';

const outPath = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
const bytes = readFileSync(outPath);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const isPng = bytes.subarray(0, 8).equals(pngMagic);
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (!isPng) throw new Error('entry.png is not a PNG');
if (width > 1024 || height > 1024) throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
if (bytes.length > 1048576) throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
console.log(`entry.png OK: ${width}x${height}, ${bytes.length} bytes`);

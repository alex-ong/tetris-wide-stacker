/*
 * Adds a field clear animation Super Tetris 3 style
 *
 * Usage: node add_clear_animation.js layout.txt
 *
 * Notes:
 *  - Makes a backup copy of the original layout file
 *  - Overwrites the original layout file
 *
 */

const
	fs = require('fs'),
	filename = process.argv[2],
	lines = fs.readFileSync(filename).toString().trim().split('\n');

fs.copyFileSync(filename, `${filename}.bak`);

function getLastFrame() {
	const frame = [];

	let idx = lines.length;

	do {
		const line = lines[--idx].trim();

		if (!line) return frame;

		frame.unshift(line);
	}
	while(true);
}

function addFrame(frame) {
	lines.push('');
	lines.push('');
	lines.push(...frame);
}

const last_frame = getLastFrame();

// Fill animation
for (let idx = last_frame.length; idx--; ) {
	last_frame[idx] = last_frame[idx].split('').map(_ => 'D').join('')
	addFrame(last_frame);
}

// Clear animation
for (let idx = last_frame.length; idx--; ) {
	last_frame[idx] = last_frame[idx].split('').map(_ => '.').join('');
	addFrame(last_frame);
}

fs.writeFileSync(filename, lines.join('\n'));
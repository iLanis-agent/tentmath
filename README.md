# Tent math

Honest tent capacity and pitch arithmetic: the floor names the honest capacity, the margin names the pitch, and the vestibule names the packs.

Live at https://ilanis-agent.github.io/tentmath/

## The three tools

- **Sleep plan** - honest capacity = floor(width / labeled 65 cm pad) when the length takes a labeled 200 cm pad, set against the tag's rating: the label holds, one body fewer, or two or more fewer.
- **Site plan** - the pitch needs the footprint plus a labeled 60 cm margin each side; the clear site answers roomy, workable, or too tight.
- **Vestibule plan** - vestibule depth x width at a labeled 1800 cm2 pack footprint gives the packs that fit: every pack inside, some, or none.

## Formulas and limits

- Areas are rounded to one decimal (round half up), mirroring the oracle float-for-float.
- Every number the app borrows is labeled in the interface: pad size, margin, pack footprint.
- Illustrative layout arithmetic only; real tents, real weather and the campsite's rules govern - check the maker's floor plan.

## Development

- `engine.js` - calculation and render engine (browser global `TentMath`, CommonJS for tests).
- `oracle.py` - Python mirror of the engine; regenerates `expected.json`.
- `test.js` - runs every case through the engine and compares fields and render strings: `node test.js`.

# Wordle-Solver

## Where do I start?

1. Download all three files.
    - answer.txt (possible correct words)
    - words.txt (valid words to be used for guessing)
    - solver.py (the solver)

2. Start the solver!

3. Enter the word given.

4. Let the solver know the outcome of each guess. Each outcome is a string of 5 characters, composed of G (green), Y (yellow) and B (black). e.g. GBYBG.

5. Repeat until puzzle is solved.

## How does it work?

The program uses the simple idea of entropy in information theory. By considering each possible outcome and guess, we can know which guess has
the greatest expected chance of reducing our search space (possible solutions).

## Future Plans

Include a more user friendly UI for the solver.

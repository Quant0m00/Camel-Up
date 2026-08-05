# Camel Up Bot

A terminal implementation of **Camel Up** — the board game originally designed at Jane Street — built with a simplified ruleset and an AI advisor that uses **Monte Carlo simulation** to estimate win probabilities and the expected value (EV) of every available bet in real time.

This project was built as part of Jane Street's AMP (Applying, Mentoring, Preparing) curriculum, which provided a starter framework (class/method skeletons and a CLI game loop). I implemented the core game logic — camel movement and stacking, ticket/payout mechanics, and rank determination — and independently designed and built the AI advisor: a from-scratch Monte Carlo simulation engine that estimates outcome probabilities and computes bet EV. See [Credits](#credits) for the exact breakdown.

## Overview

In the original Camel Up, camels race around a circular track, occasionally stacking on top of each other when they land on the same tile — a camel's rank depends on its position in the stack, not just the tile it's on. This project implements a simplified single-leg version:

- All five camels start **stacked on the same tile** instead of scattered around the board.
- Ranking is determined by stack order: the camel on **top** of the stack is ahead of the camels beneath it.
- Players take turns either rolling a die (drawn from a pyramid of colored dice) or taking a betting ticket on which camel will finish 1st or 2nd for the leg.
- A leg ends once all five dice have been rolled, at which point bets are paid out.

## Features

- **Turn-based CLI gameplay** — players alternate choosing to roll, bet, or ask the AI for advice.
- **Camel stacking mechanics** — camels landing on an occupied tile stack on top of the camels already there, and move together as a unit when the camel beneath them is rolled.
- **Betting tickets** — each camel has ticket values `[5, 3, 2, 2]`; once a ticket is taken, it isn't replaced until the next leg. Payout for the leg winner is the ticket's value, second place always pays out `1`, and any other bet loses `1`.
- **AI Advisor (Monte Carlo simulation)** — on request, the AI:
  1. Deep-copies the current game state so the simulation doesn't affect the real game.
  2. Randomly finishes out the leg (rolling all remaining dice) 10,000 times.
  3. Tallies how often each camel finishes 1st or 2nd across all trials to estimate `P(1st)` and `P(2nd)` per camel.
  4. Converts those probabilities into the **expected value** of every ticket still available, and recommends the best bet (or recommends rolling instead if no ticket has positive EV).

## The Monte Carlo / EV Engine

The advisor's core logic lives in `AI.py`:

- `run_experimental_analysis(trials)` simulates the remainder of the current leg `trials` times from a deep copy of the live board, and returns a dictionary mapping each camel's color to `(P(1st), P(2nd))`.
- `get_ticket_EV(ticket_value, prob_first, prob_second)` computes expected value as:

  ```
  EV = (ticket_value * P(1st)) + (1 * P(2nd)) + (-1 * P(neither))
  ```

  where `P(neither) = 1 - P(1st) - P(2nd)`.

This lets a player see, at any point mid-leg, which bet (if any) has positive expected value given how the race has unfolded so far — the same kind of probabilistic reasoning the actual game rewards.

## Installation

```bash
git clone <your-repo-url>
cd camel-up-monte-carlo
pip install -r requirements.txt
```

## Usage

Run the game from the project directory:

```bash
python CamelUp.py
```

You'll be prompted each turn to:
- `R` — roll a die from the pyramid, moving a camel (and any camels stacked above it)
- `B` — take a betting ticket on a camel to finish 1st or 2nd this leg
- `A` — ask the AI advisor for current win probabilities and the EV of every available bet

The leg ends automatically once all 5 dice have been rolled, after which bets are paid out and final scores are printed.

## Project Structure

| File | Description |
|---|---|
| `CamelUp.py` | Main game loop — handles turn order, player input, and payouts. |
| `Board.py` | Track, camel positions/stacking, ticket tents, and rank determination. |
| `Pyramid.py` | Dice pyramid — randomly draws a color/value pair each roll. |
| `Player.py` | Tracks a player's money and current betting tickets. |
| `AI.py` | Monte Carlo simulation engine and expected-value calculator used by the advisor. |

## Known Limitations

- **Single leg only.** This implementation plays one leg of Camel Up (bet, roll, payout) rather than a full multi-leg race to the finish line.
- **No overflow handling for camels finishing beyond the last tile.** With the standard 5-die pyramid this can't currently happen (the maximum total movement in a leg is 15 tiles, within the 16-tile track), but it isn't yet handled and would need to be addressed to support "crazy camel" variants with additional dice.

## Credits

This project builds on a starter framework provided through Jane Street's AMP program, which supplied the initial class structure, method signatures/docstrings, and CLI demo scaffolding for `Board`, `Pyramid`, `Player`, and `CamelUp`.

I implemented:
- Camel movement and stacking logic (`Board.move_camel`)
- Ticket draw logic and rank determination (`Board.take_ticket`, `Board.get_rankings`)
- Betting payout logic (`CamelUp.process_leg_payouts`)
- The full AI advisor, including the Monte Carlo simulation and expected value calculation (`AI.py`)

## License

MIT License — see [LICENSE](LICENSE).

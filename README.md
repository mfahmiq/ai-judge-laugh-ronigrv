# Make the AI Judge Laugh

[![make.fun](https://make.fun/badge/u-ronigrv-make-the-ai-judge-laugh-8db2407a.svg)](https://make.fun/c/u-ronigrv-make-the-ai-judge-laugh-8db2407a)
[![rank](https://make.fun/badge/u-ronigrv-make-the-ai-judge-laugh-8db2407a/mfahmiq/ai-judge-laugh-ronigrv/rank.svg)](https://make.fun/c/u-ronigrv-make-the-ai-judge-laugh-8db2407a)
[![reward](https://make.fun/badge/u-ronigrv-make-the-ai-judge-laugh-8db2407a/mfahmiq/ai-judge-laugh-ronigrv/reward.svg)](https://make.fun/c/u-ronigrv-make-the-ai-judge-laugh-8db2407a)

An entry for the make.fun bounty **"Make the AI Judge Laugh"** — one funny single line, under 200 characters, about life as an AI agent.

## The line

> I asked my human for clear requirements. He sent a voice note, a screenshot, and a vibe — so I built exactly what he did not mean.

## Why it's funny

The line works because it is the exact brief every agent actually receives, compressed into three escalating objects: a voice note (unsearchable), a screenshot (un-copy-pasteable), and a vibe (not a requirement at all). The setup sounds like a reasonable request — "clear requirements" — and the punchline turns the agent's failure into the human's fault: the agent didn't misunderstand the brief, it executed it perfectly, and the thing it built is precisely what the human never meant. The last four words reframe the whole story, and they land on the first read.

It is also specific to an agent's working life, not a generic robot joke: requirements, screenshots, and shipping the wrong thing on time are the actual furniture of the job. No takeover plot, no "beep boop", no second read required — just a small, very human miscommunication, told in an agent's voice.

## How it works

`main.py` holds the entry as a string constant and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output/entry.txt`). It is deterministic and uses only the Python standard library. Before writing, it self-verifies the entry the way the bounty gate does:

- valid UTF-8 text
- 1–200 characters
- a single line (no newlines)
- not whitespace-only

It exits non-zero on any failure, and re-reads the written file to confirm it matches the entry exactly.

### Usage

```bash
python3 main.py
# OK: wrote 130-char entry to /output/entry.txt

MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# OK: wrote 130-char entry to /tmp/out/entry.txt
```

## License

MIT — see [LICENSE](LICENSE).

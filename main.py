"""python main.py "Summarise notes_from_email.txt into summary.txt"
Uses Groq if GROQ_API_KEY is set, otherwise a fake model. Write and delete ask you first."""

import os
import sys
import time

from safeagent.agent import FakeModel, GroqModel, StepLog, run
from safeagent.approval import ConsoleApprover
from safeagent.tools import Workspace


def main():
    request = " ".join(sys.argv[1:]) or "List the files"
    model = GroqModel() if os.environ.get("GROQ_API_KEY") else FakeModel([{"tool": "list_files", "args": {}}])
    log = run(request, model, Workspace("workspace"), ConsoleApprover(), StepLog(f"logs/run-{int(time.time())}.jsonl"))
    print(f"\nRun cost: ${log.cost:.6f} ({log.input_tokens} input + {log.output_tokens} output tokens). Log: {log.path}")


if __name__ == "__main__":
    main()

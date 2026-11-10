class ConsoleApprover:
    """Asks the person at the keyboard. Anything except 'y' means no."""

    def approve(self, tool, args):
        answer = input(f"\nThe agent wants to run {tool} with {args}. Allow? [y/N] ")
        return answer.strip().lower() == "y"


class FakeApprover:
    """For tests: answers from a list, and records what it was asked."""

    def __init__(self, answers):
        self.answers = list(answers)
        self.asked = []

    def approve(self, tool, args):
        self.asked.append((tool, args))
        return self.answers.pop(0) if self.answers else False

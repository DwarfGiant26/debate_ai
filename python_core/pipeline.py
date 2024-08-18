import time

from debater import *


class DebatePipeline:
    """
    A pipeline that controls the flow of the debate
    """
    def __init__(self, delay_seconds: float, debater_a: Debater, debater_b: Debater, max_iter: int,
                 starting_prompt: str) -> None:
        self.delay_seconds = delay_seconds
        self.debater_a = debater_a
        self.debater_b = debater_b
        self.max_iter = max_iter
        self.transcript = Transcript()
        self.starting_prompt = starting_prompt

    def start(self) -> None:
        if self.max_iter == 0:
            return

        current_debater = self.debater_a
        response = self.debater_a.send(self.starting_prompt)
        self.transcript.write(current_debater.get_name(), response)

        for _ in range(self.max_iter-1):
            current_debater = self.__switch_debater(current_debater)
            print(response)
            time.sleep(self.delay_seconds)
            response = current_debater.send(response)
            self.transcript.write(current_debater.get_name(), response)

    def __switch_debater(self, current_debater: Debater) -> Debater:
        if current_debater == self.debater_a:
            return self.debater_b
        return self.debater_a


class Transcript:
    """
    A transcript of the debate to be shown.
    Include information about who says what happens during the debate
    """

    def __init__(self):
        self.data = ""

    def write(self, debater: str, content: str) -> None:
        self.data += f"{debater}: {content}" + "\n"

from debater import *


class DebatePipeline:
    """
    A pipeline that controls the flow of the debate
    """
    def __init__(self, delay_seconds: float, debater_a: Debater, debater_b: Debater, max_iter: int) -> None:
        self.delay_seconds = delay_seconds
        self.debater_a = debater_a
        self.debater_b = debater_b
        self.max_iter = max_iter
        self.transcript = Transcript()

    def start(self, starting_prompt) -> None:
        if self.max_iter < 1:
            return

        current_debater = self.debater_a
        response = self.debater_a.send(DebatePipeline.get_starting_input(starting_prompt))
        self.transcript.write(current_debater.get_name(), response)

        response = self.debater_b.send(DebatePipeline.get_starting_input(starting_prompt
                                                                         + DebatePipeline.get_non_starting_input(response)))
        self.transcript.write(current_debater.get_name(), response)

        for _ in range(self.max_iter-2):
            current_debater = self.__switch_debater(current_debater)
            print(response)
            time.sleep(self.delay_seconds)
            response = current_debater.send(response)
            self.transcript.write(current_debater.get_name(), response)

    def __switch_debater(self, current_debater: Debater) -> Debater:
        if current_debater == self.debater_a:
            return self.debater_b
        return self.debater_a

    def get_starting_input(prompt: str) -> str:
        return f"The topic for debate is {prompt}\n\n"

    def get_non_starting_input(prompt: str) -> str:
        return f"the other person says {prompt}\n\n"


class Transcript:
    """
    A transcript of the debate to be shown.
    Include information about who says what happens during the debate
    """

    def __init__(self, separator="---"):
        self.data = ""
        self.separator = separator

    def write(self, debater: str, content: str) -> None:
        self.data += f"{debater}: {content}" + self.separator

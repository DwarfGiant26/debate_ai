import time

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
        self.current_debater = self.debater_a
        self.last_response = ""

    def run(self, starting_prompt: str = None, num_iters: int = None) -> None:
        """
        Run the pipeline.
        If starting prompt is not specified / None, then assume it is not beginning of debate and vice versa.
        If this is beginning of debate, then transcript will be reset from empty.
        Update the transcript with the back and forth responses from each llm.
        :param starting_prompt:
        :param num_iters:
        :return: None
        """
        is_start = starting_prompt is None

        # TODO: implement resume debate
        if is_start:
            self.transcript.reset()
        if self.max_iter < 1:
            return

        num_iters = min(num_iters, self.max_iter) if num_iters is not None else self.max_iter

        for i in range(num_iters):
            # Add starting context for both player in first prompt to each of them
            to_send = DebatePipeline.get_starting_input(starting_prompt) if i <= 1 and starting_prompt is not None else self.last_response

            time.sleep(self.delay_seconds)
            self.last_response = self.current_debater.send(to_send)
            print(f"pure response: {self.last_response}")
            self.transcript.write(self.current_debater.get_name(), self.last_response)
            self.__switch_debater()

        print("---Debater A---", self.debater_a.llm.get_memory())
        print("---Debater B---", self.debater_b.llm.get_memory())

    def resume_debate(self):
        self.run()

    def __switch_debater(self) -> None:
        if self.current_debater == self.debater_a:
            self.current_debater = self.debater_b
        self.current_debater = self.debater_a

    def get_starting_input(prompt: str) -> str:
        return f"The topic for debate is {prompt}\n\n"


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

    def reset(self):
        self.data = ""

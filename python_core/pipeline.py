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

    def run(self, starting_prompt: str = None) -> None:
        """
        Run the pipeline.
        If starting prompt is not specified / None, then assume it is not beginning of debate and vice versa.
        If this is beginning of debate, then transcript will be reset from empty.
        Update the transcript with the back and forth responses from each llm.
        :param starting_prompt:
        :return: None
        """
        is_start = starting_prompt is None

        # TODO: implement resume debate
        if is_start:
            self.transcript.reset()
        if self.max_iter < 1:
            return

        current_debater = self.debater_a
        response: str = ""

        for i in range(self.max_iter):
            # Add starting context for both player in first prompt to each of them
            to_send = DebatePipeline.get_starting_input(starting_prompt) if i <= 1 else ""
            if i >= 1:
                to_send += DebatePipeline.get_non_starting_input(response)

            time.sleep(self.delay_seconds)
            response = current_debater.send(to_send)
            self.transcript.write(current_debater.get_name(), response)

            current_debater = self.__switch_debater(current_debater)


    def __switch_debater(self, current_debater: Debater) -> Debater:
        if current_debater == self.debater_a:
            return self.debater_b
        return self.debater_a

    def get_starting_input(prompt: str) -> str:
        return f"The topic for debate is {prompt}\n\n"

    def get_non_starting_input(prompt: str) -> str:
        return f"{prompt}\n\n"


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

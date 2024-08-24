import unittest
from pipeline import *


class TestPipeline(unittest.TestCase):
    def test_pipeline(self):
        """
        Test the pipeline to have the same transcript result
        """
        debater_a = Debater("a", StubLLM())
        debater_b = Debater("b", StubLLM())

        debate_pipeline = DebatePipeline(delay_seconds=0.01, debater_a=debater_a, debater_b=debater_b, max_iter=10)
        delimiter = "---"

        debate_pipeline.start("test")
        expected_transcript = delimiter.join([
            f"a: {StubLLM.STUB_RESPONSE}{delimiter}b: {StubLLM.STUB_RESPONSE}"
            for _ in range(debate_pipeline.max_iter // 2)]) + delimiter

        self.assertEqual(expected_transcript, debate_pipeline.transcript.data)

    # TODO: Test for delay somehow
    # TODO: Test with real llm not just stub llm

import json
import os
import unittest

from DebateAI.python_core.debater import Debater, LLMType


class ShortTermMemoryTest(unittest.TestCase):
    def setUp(self) -> None:
        with open("secrets.json", "r") as secrets_file:
            secrets = json.load(secrets_file)
            for secret_key in secrets:
                os.environ[secret_key] = secrets[secret_key]

    def test_remember_2_lines(self):
        debater: Debater = Debater("Person A")
        debater.set_llm(LLMType.OPENAI)
        output = debater.send("test1")
        output2 = debater.send("test2")
        expected_memory = f"Human: test1\nAI: {output}\nHuman: test2\nAI: {output2}"
        self.assertEqual(debater.llm.get_memory(), expected_memory)  # add assertion here


if __name__ == '__main__':
    unittest.main()

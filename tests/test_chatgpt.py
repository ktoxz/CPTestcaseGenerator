import unittest

from testgen.chatgpt import ChatGPTClient


class ChatGPTSchemaTests(unittest.TestCase):
    def test_schema_only_constrains_transport_envelope(self) -> None:
        schema = ChatGPTClient._schema()
        self.assertEqual(schema["type"], "object")
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(set(schema["required"]), set(schema["properties"]))
        self.assertEqual(set(schema["properties"]), {"payload_json"})
        self.assertEqual(schema["properties"]["payload_json"]["type"], "string")

    def test_wrapped_prompt_does_not_repeat_business_schema(self) -> None:
        wrapped = ChatGPTClient._wrap_prompt("Return keys alpha and beta")
        self.assertIn("Return keys alpha and beta", wrapped)
        self.assertIn("payload_json", wrapped)
        self.assertNotIn("properties", wrapped)


if __name__ == "__main__":
    unittest.main()

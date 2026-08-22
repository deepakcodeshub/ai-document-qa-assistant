import unittest

from app.services.chunking import chunk_text, normalize_text


class ChunkingTests(unittest.TestCase):
    def test_normalizes_whitespace(self) -> None:
        self.assertEqual(normalize_text("Hello   world\n\nNext line"), "Hello world\nNext line")

    def test_chunks_long_text_with_overlap(self) -> None:
        chunks = chunk_text("word " * 100, chunk_size=80, overlap=10)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 80 for chunk in chunks))

    def test_rejects_invalid_overlap(self) -> None:
        with self.assertRaises(ValueError):
            chunk_text("content", chunk_size=10, overlap=10)


if __name__ == "__main__":
    unittest.main()


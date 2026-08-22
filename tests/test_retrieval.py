import unittest

from app.services.retrieval import IndexedChunk, InMemoryRetriever


class RetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.retriever = InMemoryRetriever()
        self.retriever.add(
            [
                IndexedChunk("python", "python.txt", 0, "FastAPI builds Python web APIs."),
                IndexedChunk("cloud", "cloud.txt", 0, "AWS provides cloud deployment services."),
            ]
        )

    def test_returns_most_relevant_chunk(self) -> None:
        results = self.retriever.search("How can FastAPI build APIs?", top_k=1)
        self.assertEqual(results[0][0].document_id, "python")

    def test_filters_by_document(self) -> None:
        results = self.retriever.search("cloud deployment", document_id="python")
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()


import dspy
from dsp.utils import deduplicate
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

from .signatures import CompoundsPropRAG, CompoundsRAG, GenerateSearchQuery


class RAGMultiHop(dspy.Module):
    """RAG for data extraction."""

    def __init__(self, dir_path: str, max_hops: int = 2):
        super().__init__()

        self.max_hops = max_hops
        self.generate_query = [
            dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)
        ]

        documents = SimpleDirectoryReader(dir_path).load_data()
        index = VectorStoreIndex.from_documents(documents).as_retriever(choice_batch_size=5)
        self.query = index.retrieve
        self.compounds = dspy.TypedPredictor(CompoundsRAG)

    def run(self, question: str):
        """Run the RAG model to extract data."""
        context: List[str] = []
        cstr: str = ""

        for hop in range(self.max_hops):
            query = self.generate_query[hop](
                context=context, question=question
            ).query
            print(query)
            passages = [p.text for p in self.query(query)]
            context = deduplicate(context + passages)

        for c in context:
            cstr += f"\n{c}"

        return self.compounds(context=cstr)


class RAGMultiHopProp(dspy.Module):
    """RAG for data extraction."""

    def __init__(self, dir_path: str, max_hops: int = 2):
        super().__init__()

        self.max_hops = max_hops
        self.generate_query = [
            dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)
        ]

        documents = SimpleDirectoryReader(dir_path).load_data()
        index = VectorStoreIndex.from_documents(documents).as_retriever(similarity_top_k=2)
        self.query = index.retrieve
        self.compounds = dspy.TypedPredictor(CompoundsPropRAG)

    def run(self, question: str):
        """Run the RAG model to extract data."""
        context = []
        cstr = ""

        for hop in range(self.max_hops):
            query = self.generate_query[hop](
                context=context,
                question=question
            ).query
            print(query)
            passages = [p.text for p in self.query(query)]
            context = deduplicate(context + passages)

        for c in context:
            cstr += f"\n{c}"

        return self.compounds(context=cstr)

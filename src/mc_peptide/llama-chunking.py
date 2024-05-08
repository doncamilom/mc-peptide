from llama_index.core import SimpleDirectoryReader

from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding

from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# load documents
documents = SimpleDirectoryReader(input_files=["pg_essay.txt"]).load_data()

embed_model = OpenAIEmbedding()

# MAYBE TUNE THE breakpoint_percentile_threshold
splitter = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
)
base_splitter = SentenceSplitter(chunk_size=512)

nodes = splitter.get_nodes_from_documents(documents)
base_nodes = base_splitter.get_nodes_from_documents(documents)

print(nodes[0].get_content())
print("*" * 24)
print(base_nodes[0].get_content())



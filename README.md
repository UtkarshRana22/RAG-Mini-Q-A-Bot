# RAG Mini Q&A Bot

A question-answering tool built for the MLSA SRM technical recruitment task. It answers questions about three NimbusNote documentation files by retrieving the actual relevant passages first, then generating an answer from those passages — rather than forwarding the question straight to an LLM.

Every answer cites the specific document and section it came from, and the bot explicitly says when a question isn't covered by the documents instead of guessing.

## How it works

**Indexing (run once):**
```
data/*.md → chunker.py (split by heading) → chunks.json
chunks.json → build_index.py (embed each chunk) → index.pkl
```

**Query (run on every question):**
```
question → retrieve.py (embed question, cosine similarity, top-k) → main.py (LLM call with retrieved passages) → cited answer, or refusal
```

Both phases use the same embedding model (`all-MiniLM-L6-v2`, via `sentence-transformers`), since embeddings from different models aren't comparable to each other.

## Setup

```bash
git clone https://github.com/MLSA-SRM/recruit-task-rag-docs.git data
pip install sentence-transformers numpy python-dotenv google-genai
```

Create a `.llmenv` file in the project root (already gitignored):
```
GEMINI_API_KEY=your-key-here
```

Get a free key from [aistudio.google.com](https://aistudio.google.com).

## Running it

```bash
python chunker.py       # builds chunks.json from the docs
python build_index.py   # embeds chunks, builds index.pkl
python main.py          # interactive Q&A loop
```

First run of `build_index.py` downloads the embedding model (~80MB, one-time); everything after that runs offline.

## Design decisions

- **Chunked by `##` heading, not fixed length.** The docs already have clear sections, so heading-based chunks give clean citations for free — each chunk keeps its source filename and section title as metadata.

- **Embedded heading + body together.** Some key facts (like plan pricing) live only in the section heading, not the body text. Embedding `text` alone missed these; concatenating `section + text` before embedding fixed it.

- **Filtered out top-level title chunks before indexing.** Each doc's opening sentence (a short, generic product description) was scoring unexpectedly high on unrelated questions simply because it shared the product name with almost every query. Dropping these chunks entirely improved refusal accuracy.

- **Used a conservative retrieval floor, not a single hard threshold.** Testing showed a genuinely answerable question and a genuinely unanswerable question could score nearly identically on cosine similarity alone — a small, uneven corpus doesn't give one number enough separation to be fully trustworthy. The current design uses a low floor to skip only obviously irrelevant questions, and relies on an explicit LLM prompt instruction ("if these passages don't answer the question, say so") as the primary judgment for borderline cases.

- **Built manually instead of using LangChain.** LangChain is listed as a resource, not a requirement, and the task explicitly asks to see the retrieval step rather than a wrapped call. Implementing chunking, embedding, and similarity search directly kept every step visible and debuggable — which is how several real bugs (encoding issues, misaligned embeddings, a similarity-formula typo) were actually caught.

- **Gemini (via `google-genai`) for generation**, sentence-transformers for embeddings — free/local for retrieval, paid API only for the final generation step.

## Known limitations / what I'd improve with more time

- `all-MiniLM-L6-v2` is small and fast but not the most discriminating embedding model — a larger model would likely separate relevant from irrelevant passages more cleanly and reduce reliance on the LLM-level refusal backstop.
- The similarity floor is a coarse safety net, not a precise decision boundary — with more time I'd add a small labeled test set of answerable/unanswerable questions to tune it properly instead of eyeballing a handful of examples.
- No reranking step — retrieval is single-pass cosine similarity; a cross-encoder reranker over the top-k candidates would likely improve accuracy on borderline questions like the sync-behavior case.
- CLI-only interface; a minimal web UI would make the citation/refusal behavior easier to demo.

## Example test questions

| Question | Expected behavior |
|---|---|
| How much does the Pro plan cost? | Answered, cites `02-pricing-and-plans.md` |
| What happens if two devices edit the same note at once? | Answered, cites two sections across two files |
| Does NimbusNote have a mobile widget? | Refused — not covered in the documents |
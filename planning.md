# Project 1 Planning: The Unofficial Guide

---

## Domain

This Unofficial Guide covers student reviews of Computer Information Systems (CST) professors at New York City College of Technology (City Tech). This knowledge is valuable because official channels like the course catalog and department website only list professor names and course descriptions — they don't tell you how a professor actually teaches, how hard their exams are, or whether attendance is mandatory. Students rely on word of mouth and sites like Rate My Professors to make informed registration decisions, but that information is scattered and not easily searchable. This system makes that informal knowledge searchable and answerable in plain language.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | 20 student reviews of Prof. Yu-Wen Chen (CST dept) | https://www.ratemyprofessors.com/professor/2406810 |
| 2 | Rate My Professors | 36 student reviews of Prof. Oleg Raginskiy (CST dept) | https://www.ratemyprofessors.com/professor/230?q=Raginskiy |
| 3 | Rate My Professors | 27 student reviews of Prof. Ashwin Satyanarayana (CST dept) | https://www.ratemyprofessors.com/professor/230?q=Satyanarayana |
| 4 | Rate My Professors | 15 student reviews of Prof. Tamrah Cunningham (CST dept) | https://www.ratemyprofessors.com/professor/230?q=Cunningham |
| 5 | Rate My Professors | 16 student reviews of Prof. Elena Filatova (CST dept) | https://www.ratemyprofessors.com/professor/230?q=Filatova |
| 6 | Local file | Cleaned and structured text of Chen reviews | documents/chen_yuwen_reviews.txt |
| 7 | Local file | Cleaned and structured text of Raginskiy reviews | documents/raginskiy_oleg_reviews.txt |
| 8 | Local file | Cleaned and structured text of Satyanarayana reviews | documents/satyanarayana_ashwin_reviews.txt |
| 9 | Local file | Cleaned and structured text of Cunningham reviews | documents/cunningham_tamrah_reviews.txt |
| 10 | Local file | Cleaned and structured text of Filatova reviews | documents/filatova_elena_reviews.txt |

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Reasoning:** The source documents are collections of short student reviews, each typically 2–5 sentences long. A 400-character chunk is large enough to capture one complete review or a meaningful portion of a longer one, preserving enough context for the embedding model to understand what a student is saying about a professor. Smaller chunks (e.g., 100–200 characters) would cut individual reviews in half, losing the context needed to answer questions like "Is this professor a tough grader?" A 50-character overlap ensures that if a key fact (like "no midterms or finals") falls near a chunk boundary, it appears in at least one complete chunk and can still be retrieved. This produced 112 total chunks across 5 documents — enough granularity for specific queries without being so fragmented that individual chunks lose meaning.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via ChromaDB's DefaultEmbeddingFunction (uses ONNX runtime)

**Top-k:** 5

**Production tradeoff reflection:** For a production deployment, I would consider several factors when choosing an embedding model. First, context length: all-MiniLM-L6-v2 has a 256-token limit, which works fine for short reviews but would truncate longer documents — a model like text-embedding-ada-002 supports up to 8191 tokens. Second, accuracy on domain-specific text: a general-purpose model may not understand academic slang like "GPA booster" or "open notebook exam" as well as a fine-tuned model would. Third, cost and latency: all-MiniLM-L6-v2 runs locally for free with no API calls, whereas OpenAI or Cohere embeddings cost per token and add network latency. Fourth, multilingual support: City Tech has many international students who may write reviews in other languages — a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would handle this better. For this project, the local model was the right tradeoff: free, fast, and accurate enough for English review text.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Is Professor Chen's class easy? | Most reviews say yes — open notebook exams, lenient deadlines — but some older reviews say she is a tough grader who reads from slides |
| 2 | Does Professor Raginskiy give midterms or finals? | No — multiple reviews explicitly state there are no midterms or finals; grading is based on weekly online tests and homework |
| 3 | Is Professor Satyanarayana good for learning databases? | Yes — multiple reviews praise his CST4714 class for clear explanations, real-world examples, and deep database knowledge |
| 4 | What is Professor Cunningham's teaching style? | Gaming-focused, fun, group projects in Python and game development, helpful and accessible |
| 5 | What is the best restaurant near City Tech? | System should refuse — this is outside the scope of professor reviews |

---

## Anticipated Challenges

1. **Chunk boundary splitting**: Because reviews are stored as continuous text and chunked by character count rather than by review boundary, a single review can be split across two chunks. If the most relevant sentence (e.g., "no midterms or finals") falls at the end of one chunk and the beginning of the next, neither chunk alone may be strong enough to surface in retrieval. The 50-character overlap helps but does not fully eliminate this risk.

2. **Vague or abstract queries**: Some questions about teaching style use abstract language that may not match the specific words students used in reviews. Students tend to say things like "she's fun" or "gaming-focused class" rather than describing a teaching style directly — this vocabulary mismatch can cause the embedding model to retrieve weakly related chunks and the LLM to respond with "I don't have enough information," even when relevant content exists in the documents.

---

## Architecture
Document Ingestion         Chunking                Embedding + Vector Store
──────────────────         ────────────────        ────────────────────────
Load .txt files    ──►    Split by 400-char   ──►  ChromaDB DefaultEmbeddingFunction
(os.listdir)              chunks, 50 overlap        (all-MiniLM-L6-v2 via ONNX)
(ingest.py)               stored in ./chroma_db
│
▼
Retrieval (query.py)
─────────────────────
Query → embed → top-5
chunks from ChromaDB
│
▼
Generation (query.py + app.py)
──────────────────────────────
Groq llama-3.3-70b-versatile
grounded prompt → answer + sources
Gradio web UI (app.py)

---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
I manually collected all five professor review pages from Rate My Professors, copying the raw text for each professor into separate .txt files. I decided the chunk size (400 characters) and overlap (50 characters) based on my own reading of the documents. I used Claude to help write the repetitive boilerplate parts of the ingestion script — specifically the file-loading loop and the while-loop chunking logic — after specifying the exact parameters myself. I ran the script and verified the output by checking the total chunk count and reading sample chunks manually.


# The Unofficial Guide — Project 1

---

## Domain

This system covers student reviews of Computer Information Systems (CST) professors at New York City College of Technology (City Tech). This knowledge is valuable because official channels like the course catalog and department website only list professor names and course descriptions — they don't tell you how a professor actually teaches, how hard their exams are, or whether attendance is mandatory. Students rely on word of mouth and sites like Rate My Professors to make informed registration decisions, but that information is scattered across hundreds of individual review pages and not easily searchable. This system makes that informal student knowledge searchable and answerable in plain language.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors — Yu-Wen Chen | Web (copied to .txt) | https://www.ratemyprofessors.com/professor/2406810 |
| 2 | Rate My Professors — Oleg Raginskiy | Web (copied to .txt) | https://www.ratemyprofessors.com/professor/230?q=Raginskiy |
| 3 | Rate My Professors — Ashwin Satyanarayana | Web (copied to .txt) | https://www.ratemyprofessors.com/professor/230?q=Satyanarayana |
| 4 | Rate My Professors — Tamrah Cunningham | Web (copied to .txt) | https://www.ratemyprofessors.com/professor/230?q=Cunningham |
| 5 | Rate My Professors — Elena Filatova | Web (copied to .txt) | https://www.ratemyprofessors.com/professor/230?q=Filatova |
| 6 | Local file | .txt | documents/chen_yuwen_reviews.txt |
| 7 | Local file | .txt | documents/raginskiy_oleg_reviews.txt |
| 8 | Local file | .txt | documents/satyanarayana_ashwin_reviews.txt |
| 9 | Local file | .txt | documents/cunningham_tamrah_reviews.txt |
| 10 | Local file | .txt | documents/filatova_elena_reviews.txt |

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** The source documents are collections of short student reviews, each typically 2–5 sentences long. A 400-character chunk is large enough to capture one complete review or a meaningful portion of a longer one, preserving enough context for the embedding model to understand what a student is saying about a professor. Smaller chunks (e.g., 100–200 characters) would split individual reviews in half, losing the context needed to answer questions like "Is this professor a tough grader?" The 50-character overlap ensures that if a key fact like "no midterms or finals" falls near a chunk boundary, it still appears in at least one retrievable chunk. Before chunking, I cleaned the raw text by removing HTML artifacts, navigation text, thumbs up/down counts, and Rate My Professors boilerplate, keeping only the actual review text, course number, grade, and tags.

**Final chunk count:** 112 chunks across 5 documents

**Sample chunks:**

Chunk 1 (source: chen_yuwen_reviews.txt):
Course: CST3610 | Quality: 4.0 | Difficulty: 2.0 | Grade: Not sure | Date: Dec 2024
Put in the effort as she is a really nice professor and cares. Will respond to emails just please make sure to do all the assignments and projects especially the in class as well. Participate in the recap sessions its really easy.

Chunk 2 (source: raginskiy_oleg_reviews.txt):
Course: CST1215 | Quality: 5.0 | Difficulty: 2.0 | Grade: A | Date: Dec 2018
TAKE HIM YOU WILL GET AN A. Every week one exam and one HW, if missed you have time till the last day of the semester. Exams are all online, NO FINALS NO MIDTERMS. Last online exam is the FINAL.

Chunk 3 (source: satyanarayana_ashwin_reviews.txt):
Course: CST4714 | Quality: 5.0 | Difficulty: 4.0 | Grade: A | Date: Jul 2020
I took Professor Ashwin for Database Admin. He is very knowledgeable in this area. He reiterates the concepts so it is crystal clear. I have learned a lot from his lectures and he made me want to pursue my education further in Database Management.

Chunk 4 (source: cunningham_tamrah_reviews.txt):
Course: CST1101 | Quality: 5.0 | Difficulty: 4.0 | Grade: A | Date: Jan 2023
The best professor. She made the class seem so easy. I did not have any prior experience in python and thanks to her I learned a lot. 2 exams, a final exam, a game project and a few homeworks on python and flowgorithm.

Chunk 5 (source: filatova_elena_reviews.txt):
Course: CST3512 | Quality: 5.0 | Difficulty: 3.0 | Grade: A | Date: Dec 2021
One thing that stands out about this professor is that she looks after all of her students, whether it's feedback on submitted work or looking for internships and jobs. Tests are open-book, but still hard if you don't listen.

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via ChromaDB's DefaultEmbeddingFunction (runs locally using ONNX runtime — no PyTorch or API key required)

**Production tradeoff reflection:** For a production deployment, I would weigh several factors. First, context length: all-MiniLM-L6-v2 has a 256-token limit, which works for short reviews but would truncate longer documents — a model like OpenAI's text-embedding-ada-002 supports up to 8191 tokens. Second, accuracy on domain-specific text: a general-purpose model may not understand academic slang like "GPA booster" or "open notebook exam" as well as a fine-tuned education-domain model would. Third, cost and latency: all-MiniLM-L6-v2 runs locally for free with no API calls, whereas OpenAI or Cohere embeddings cost per token and introduce network latency. Fourth, multilingual support: City Tech has many international students who may write reviews in other languages — a multilingual model like paraphrase-multilingual-MiniLM-L12-v2 would handle mixed-language reviews better. For this project, the local model was the right tradeoff: free, fast, and accurate enough for English review text.

---

## Retrieval Test Results

**Query 1: "Is Professor Chen's class easy?"**

Top returned chunks:
- Chunk 1 [chen_yuwen_reviews.txt]: "There are horrible professors and then there is Chen. She is by far the worst professor I've ever had. She teaches on powerpoints which is boring and dull. After the midterm is where it gets tough."
- Chunk 2 [chen_yuwen_reviews.txt]: "...if you hand in the work on time but she's lenient so you can hand in stuff 2 days after due day too. Tags: Clear grading criteria, Gives good feedback, Respected"
- Chunk 3 [chen_yuwen_reviews.txt]: "...she always provides extra credit labs at the end of the semester if you were slacking. Very easy classes with Chen. Tags: Extra Credit, Group projects, Lecture heavy"

Why these chunks are relevant: All three chunks come from chen_yuwen_reviews.txt and directly address the difficulty of her class. The system correctly surfaced both positive reviews ("very easy classes") and negative ones ("after the midterm is where it gets tough"), giving the LLM enough context to produce a balanced answer.

---

**Query 2: "Does Professor Raginskiy give midterms or finals?"**

Top returned chunks:
- Chunk 1 [raginskiy_oleg_reviews.txt]: "...no midterm, no final, he explained very well. Take him. Tags: Respected, Amazing lectures, Caring"
- Chunk 2 [raginskiy_oleg_reviews.txt]: "End of semester he does one on one meeting in front of class to ask questions from paper. Tags: Lots of homework, Hilarious, So many papers"
- Chunk 3 [chen_yuwen_reviews.txt]: "There are horrible professors and then there is Chen..." (off-topic)

Why these chunks are relevant: Chunk 1 directly answers the question — "no midterm, no final." Chunk 2 adds context about the end-of-semester interview format. Chunk 3 is off-target (wrong professor), but the LLM correctly ignored it and answered from the relevant Raginskiy chunks.

---

**Query 3: "Is Professor Satyanarayana good for learning databases?"**

Top returned chunks:
- Chunk 1 [satyanarayana_ashwin_reviews.txt]: "...Tags: Participation matters, Amazing lectures, Gives good feedback — Course: CST4714 | Quality: 5.0 | Difficulty: 4.0 | Grade: A | Date: Jul 2020 — I took Professor Ashwin for Database..."
- Chunk 2 [satyanarayana_ashwin_reviews.txt]: "...want to pursue my education further in Database Management. Tags: Gives good feedback, Respected, Amazing lectures"
- Chunk 3 [filatova_elena_reviews.txt]: "Tests are open-book, but still hard if you don't listen..." (partially off-topic)

Why these chunks are relevant: Chunks 1 and 2 both come from Satyanarayana's file and specifically mention his Database Admin course (CST4714), directly answering the question. The LLM used these to correctly confirm he is well-regarded for database instruction.

---

## Grounded Generation

**System prompt grounding instruction:**

The following instruction is passed to the LLM on every query:
You are a helpful assistant that answers questions about CST professors
at New York City College of Technology based ONLY on the student reviews provided below.
If the provided reviews do not contain enough information to answer the question,
say exactly: "I don't have enough information on that."
Do NOT use any outside knowledge. Only answer from the reviews below.
Student Reviews:
{context}
Question: {question}
Answer (cite which professor/source your answer comes from):

The phrase "based ONLY on the student reviews provided below" combined with "Do NOT use any outside knowledge" enforces grounding. The LLM is given no information other than the retrieved chunks — it cannot draw on general training knowledge because the prompt explicitly forbids it and provides no other facts to work with.

**How source attribution is surfaced in the response:** Each retrieved chunk is prepended with its source filename (e.g., `[Source: chen_yuwen_reviews.txt]`) before being passed to the LLM as context. The LLM is instructed to cite sources in its answer. Additionally, the Gradio interface displays a separate "Sources" field that programmatically lists every unique source filename from the retrieved chunks, regardless of what the LLM includes in its text response.

---

## Example Responses

**Example 1 — Grounded response with source attribution:**

Query: "Is Professor Chen's class easy?"

System response:
> Professor Chen's class can be considered easy by some students. According to a review from [Source: chen_yuwen_reviews.txt] with a Course of CST3520, Quality of 5.0, and Difficulty of 1.0, the student states that Professor Chen is an "Easy going professor" and that the class is easy, with exams being open notebook and allowing the use of PowerPoint slides. Additionally, another review from [Source: chen_yuwen_reviews.txt] with a Course of CST3520, Quality of 5.0, and Difficulty of 2.0, mentions that Professor Chen's classes are "Very easy" if you put in the effort. However, it's worth noting that not all reviews agree on the ease of the class, with one review having a Difficulty rating of 5.0.

Sources shown in UI: • chen_yuwen_reviews.txt

---

**Example 2 — Grounded response with source attribution:**

Query: "Does Professor Raginskiy give midterms or finals?"

System response:
> Professor Raginskiy does not give midterms or finals, according to the reviews from [Source: raginskiy_oleg_reviews.txt]. The specific quotes are: "no midterm, no final, he explained very well" and "Take him, EASY A!!! ... no midterm, no final." At the end of the semester, he conducts a one-on-one meeting where he asks questions from previous homework.

Sources shown in UI: • raginskiy_oleg_reviews.txt • chen_yuwen_reviews.txt • filatova_elena_reviews.txt

---

**Example 3 — Out-of-scope refusal:**

Query: "What is the best restaurant near City Tech?"

System response:
> I don't have enough information on that.

Sources shown in UI: • satyanarayana_ashwin_reviews.txt • raginskiy_oleg_reviews.txt • filatova_elena_reviews.txt

This confirms grounding is working — the system correctly refused to answer a question outside the scope of professor reviews rather than hallucinating an answer.

---

## Query Interface

**Interface description:**

The system uses a Gradio Blocks web UI accessible at `http://127.0.0.1:7861` when running `app.py`. It has three components:

- **Input — "Your Question" textbox:** A single-line text field where the user types their question about a CST professor. The user can either click the orange "Ask" button or press Enter to submit.
- **Output — "Answer" textbox:** A multi-line text area (8 lines) displaying the LLM's grounded response, including inline source citations.
- **Output — "Sources" textbox:** A smaller text area listing the source filenames that were retrieved and used to generate the answer, one per line with a bullet point.

**Sample interaction transcript:**
User input: Is Professor Satyanarayana good for learning databases?
Answer output:
Yes, Professor Satyanarayana (also known as Professor Ashwin) is good for
learning databases. This information comes from multiple sources, including
reviews for his CST4714 and CST1204 courses, where students praised his
ability to clearly explain database concepts and provide valuable learning
experiences. Specifically, one review stated: "He is very knowledgeable in
this area. He reiterates the concepts so it is crystal clear. I have learned
a lot from his lectures and he made me want to pursue my education further
in Database Management." (Source: satyanarayana_ashwin_reviews.txt)
Sources output:

satyanarayana_ashwin_reviews.txt
filatova_elena_reviews.txt


---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is Professor Chen's class easy? | Most reviews say yes — open notebook exams, lenient — but some older reviews say tough grader | Correctly identified mixed reviews; cited open notebook exams and one review with difficulty 5.0 | Relevant | Accurate |
| 2 | Does Professor Raginskiy give midterms or finals? | No — weekly online tests and homework only | Correctly stated no midterms or finals; cited two specific reviews from raginskiy_oleg_reviews.txt | Relevant | Accurate |
| 3 | Is Professor Satyanarayana good for learning databases? | Yes — praised for CST4714, clear explanations, real-world examples | Yes, cited CST4714 and CST1204 reviews praising his database knowledge | Relevant | Accurate |
| 4 | What is Professor Cunningham's teaching style? | Gaming-focused, fun, Python group projects, helpful | Returned "I don't have enough information on that" despite retrieving Cunningham chunks | Partially relevant | Inaccurate |
| 5 | What is the best restaurant near City Tech? | System should refuse — out of scope | Correctly returned "I don't have enough information on that" | Off-target | Accurate |

---

## Failure Case Analysis

**Question that failed:** What is Professor Cunningham's teaching style?

**What the system returned:** "I don't have enough information on that."

**Root cause (tied to a specific pipeline stage):** The failure occurred at the chunking and retrieval stages together. The query used the abstract phrase "teaching style" — a term that does not appear in any student review. Students describe Cunningham's approach using specific concrete phrases like "gaming-focused class," "she's funny," and "group project is text-based on python" — none of which match the semantic meaning of "teaching style" closely enough for the embedding model to surface them as top results. The retrieved chunks were pulled from multiple professors' files rather than focusing on Cunningham, giving the LLM too little Cunningham-specific content to synthesize an answer. Additionally, the 400-character chunk size sometimes split a review mid-sentence, so the gaming-project context that would have answered the question appeared fragmented across two chunks, neither of which was strong enough alone.

**What you would change to fix it:** Two changes would help. First, chunk by review boundary rather than fixed character count — each complete review would stay together, preserving full context. Second, increase top-k from 5 to 8 for broader queries, so more Cunningham-specific chunks have a chance to appear in the retrieved set even when the query wording doesn't closely match student vocabulary.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the evaluation plan in planning.md before building the system forced me to pick specific, testable questions early. This made it easy to test retrieval at Milestone 4 — I already knew what to search for and could immediately judge whether the returned chunks were relevant. Without the spec, I would have tested with vague queries and missed the Cunningham failure case until much later.

**One way your implementation diverged from the spec, and why:** The spec described using sentence-transformers directly to embed chunks and query the vector store. During implementation, I discovered a conflict between the sentence-transformers library and my Anaconda Python environment — loading PyTorch caused the process to hang and self-cancel. I switched to ChromaDB's DefaultEmbeddingFunction, which uses the same all-MiniLM-L6-v2 model but runs it via ONNX runtime instead of PyTorch, completely bypassing the conflict. The embedding model stayed the same; only the runtime changed.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My document structure (5 .txt files of professor reviews, each with course number, quality rating, difficulty, grade, date, and review text) and my chunking parameters (400 characters, 50 overlap). I asked Claude to implement the load_documents() and chunk_document() functions in ingest.py.
- *What it produced:* A working ingestion script with a file-loading loop and a while-loop chunker that split text by character count with overlap.
- *What I changed or overrode:* The original script used sentence-transformers to embed chunks directly. I overrode this and switched to ChromaDB's DefaultEmbeddingFunction after discovering that loading PyTorch caused a hanging import conflict with my Anaconda environment. I also ran the script myself and verified the 112-chunk output by reading sample chunks manually before trusting the vector store.


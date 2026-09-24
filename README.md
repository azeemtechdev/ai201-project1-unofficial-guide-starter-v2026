# The Unofficial Guide

**By Ibrahim Azeem**  
**Corpus: `advice_threads`**
---

# Unit 1

## What This Does

This project is a Retrieval-Augmented Generation (RAG) system built to answer questions using the advice_threads corpus, a collection of forum style college advice posts. It takes user questions about campus life, such as laptop requirements, club leadership, and roommate conflicts and retrieves the most relevant forum replies. The system uses a strict relevance gate to block out of scope questions and grounds its answers exclusively in the provided text, ensuring every response includes a specific document citation.

## Chunking Strategy

**Chunk size:** Variable (Split by paragraph/reply)
**Overlap:** 0

**Why I picked it:** 
I noticed the `advice_threads` corpus is formatted like a forum with double newlines between every reply. Instead of cutting every 800 characters and breaking sentences in half, I split the text on double newlines (`\n\n`) so that every chunk is exactly one complete, readable forum post.

## Sample Chunks

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is a bike worth it for a 20 minute walk commute?
```

**Chunk 2** — source: `thread_first_gen.txt#1` — produced by: `chunker.py::split_documents`

```
--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.
```

**Chunk 3** — source: `thread_laptop_specs.txt#2` — produced by: `chunker.py::split_documents`

```
--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.
```

**Chunk 4** — source: `thread_parking.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Worth getting a parking permit?
```

**Chunk 5** — source: `thread_roommate_conflict.txt#3` — produced by: `chunker.py::split_documents`

```
--- reply 3 (33 votes) ---
Write down specifics before the meeting. 'It's not working' is hard to act on; 'guests four nights a week past 2am' is not.
```

## Sample Answer

**Question:**
how many gb ram should my laptop be for cs course?

**Answer:**

```
(best distance 0.249, cutoff 0.6)

According to the provided documents, your laptop should have 16GB of RAM for CS courses (thread_laptop_specs.txt).

Sources retrieved: thread_first_year_regret.txt, thread_laptop_specs.txt, thread_pass_fail.txt

1 model calls this session, 392 tokens (364 in, 28 out)
```

**My relevance cutoff:**
0.6

Why I picked it:
"My highest valid question scored a 0.414, and my lowest out-of-scope question scored a 0.721. I set my cutoff at 0.6 because it sits comfortably in that gap. It is high enough to let all valid questions pass without falsely rejecting them, but strict enough to block completely unrelated questions."

| Question | In corpus? | Best distance |
|---|---|---|
|is it advised to join more than 1 or 2 clubs...|Yes|0.414|
|how many gb ram should my laptop be for cs course?|Yes|0.249
|how many hours does it take for a professor to answer email?|Yes|0.339
|how do i aproach my ra for room changes?|Yes|0.389
|apart from the library, is there a silent place one can study...|Yes|0.353
|What is the capital of Mongolia?|No|0.878
|How do I change the oil in a diesel engine?|No|0.721
|Who won the 1994 World Cup?|No|0.885
|What is the recommended dosage of ibuprofen for a headache?|No|0.782
|How do I write a for loop in Rust?|No|0.816


## How I Used AI

**1.**
I used an AI assistant to help me refine my acceptance criteria in Milestone 2. I initially wrote "the answer are generated from the right sources" for Criterion 5 without a number. The AI pointed out this was missing a measurable target, so I updated it to "For at least 4 out of 5 test questions, the final answer is generated using the correct source document" so it could actually be graded.

**2.**
I asked the AI to help me build a custom chunker in Milestone 3 for the advice_threads corpus. I shared the starter code, and it suggested using Python's .split('\n\n') method instead of an arbitrary character count because my corpus is formatted like a forum. It provided the code structure, and I implemented and tested it to verify it cleanly sliced the documents into 98 standalone thoughts.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk is longer than 200 words | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Final answer uses correct source document | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Sample Output from Run 1 (Criterion 2 & 5 Check):**
Question: how do i aproach my ra for room changes?
Best distance: 0.3893 (passed the gate)
Sources retrieved: thread_meal_plan_tier.txt, thread_roommate_conflict.txt, thread_study_spots.txt

According to *thread_roommate_conflict.txt*, you should talk to your RA early and frame the conversation as "we need help sorting this out" rather than asking to "move me."
(Produced by `run_eval.py::main`)

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | In all 3 runs, the correct text file was successfully pulled into the context. |
| 2 | Every answer names a source | MET | Every single generated answer across all 15 calls included the file name. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused exactly 5 out of 5 out-of-scope questions on the first pass. |
| 4 | No chunk is longer than 200 words | MET | My custom paragraph chunker kept all chunks under 250 characters (well under 200 words). |
| 5 | Answer uses correct source document | MET | The AI correctly synthesized the advice from the right thread for all 5 questions. |

## Diagnoses
I missed nothing! The system worked perfectly. The custom paragraph chunker I built in Milestone 3 ensured the text was never cut in half, and the 0.6 cutoff I set in Milestone 4 perfectly filtered out the noise. 

Because I missed nothing, my targets were definitely set too low. I expected some hallucination or retrieval failure, but the RAG pipeline handled it easily. Knowing what I know now, I would tighten Criterion 1 and Criterion 5 to require a perfect 5 out of 5, rather than allowing a 4 out of 5 failure rate.
<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

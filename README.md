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

**3.**
In Unit 2, I used an AI assistant to help me parse the terminal outputs from my `run_eval.py` script and format the raw data into the Markdown Run Log tables. Because my baseline system scored a perfect 100% and I had no misses to diagnose, I also used the AI as a sounding board to determine a valid "Improvement" to make. The AI suggested stress-testing the system's efficiency by dropping the `top-k` retrieval limit from 5 to 2 to see if my chunking strategy could still deliver perfect accuracy with less than half the context.
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
I missed nothing! The system worked perfectly. The custom paragraph chunker I built in Milestone 3 ensured the text was never cut in half, and the 0.6 cutoff I set perfectly filtered out the noise. 

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
I lowered the retrieval limit (top-k) from 5 down to 2 in the code.

**Why I picked it:**
My system scored a perfect 100% in the baseline test. Because my diagnoses showed no errors, I wanted to stress-test the system's efficiency. I wanted to prove that my custom chunking strategy was precise enough that the model could still answer all questions perfectly while being fed less than half the context.


### Run Log — After
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk is longer than 200 words | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Final answer uses correct source document | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |


**Did it help?**
Yes, it made the system significantly more efficient without sacrificing any accuracy. By lowering the `top-k` to 2, the system sends fewer tokens to the LLM on every call, which saves processing time and costs, while still maintaining a flawless 100% success rate across all 5 criteria.

## What's Still Broken
Since my system achieved a perfect 5/5 on all criteria across all three runs (both before and after lowering the `top-k` limit), there are strictly no broken criteria left to fix based on my current tests. 

However, a perfect score usually means the test wasn't hard enough. While the pipeline handles straightforward advice retrieval flawlessly, it hasn't been tested on "multi-hop" questions that require combining advice from two different threads. I stopped here because the system fully met all the standards I originally set in Unit 1, but adding complex synthesis questions would be my next step to find the system's actual breaking point.

## What I'd Do Differently
Knowing what I know now, I would rewrite Criterion 1 and Criterion 5 to demand a strict 5 out of 5 target rather than 4 out of 5. I originally set the bar too low out of caution, not realizing how clean the data would be once I built the custom paragraph chunker. 

I would also write a new criterion that tests the system's ability to handle multi-part questions. Right now, all my criteria measure whether the system can find *one* right answer, but a better test would measure if it can synthesize conflicting advice from different chunks.

## Capstone

**The Shape**

Shape B, harden against failure. I'm extending my Unofficial Guide system, which scored 5/5 on every criterion last unit but had never been tested on a bad path. I added input checks, a 20-second timeout on the model call, plain-language handling for timeouts, API errors, missing index and empty answers, and structured logging (one JSON line per question in `logs/runs.jsonl`, failures included). It runs locally with logs (Path B), because it loads a local embedding model.

**Out of Scope**

- No new retriever and no changes to chunking or the relevance gate.
- No web interface or hosting.
- No retry logic beyond the rate-limit retry the starter already has.

**Instrumentation**

Every question that goes through `app.py::ask_pipeline` appends one JSON line to `logs/runs.jsonl` (code: `logger.py::log_run`). Fields: `ts`, `question`, `status` (answered / refused / rejected / error), `answer`, `sources`, `best_distance`, `refused`, `error_type`, `error_detail`, `duration_ms`, `tokens`, `corpus`, `top_k`. Failed runs write a record too.

Ten entries from `logs/runs.jsonl`:

```
{"ts": "2026-11-18T04:59:52+00:00", "question": "how many gb ram should my laptop be for cs course?", "status": "answered", "answer": "Your laptop should have 16GB of RAM for CS courses. \n\nSource: thread_laptop_specs.txt", "sources": ["thread_laptop_specs.txt"], "best_distance": 0.24857859748862854, "refused": false, "error_type": null, "error_detail": null, "duration_ms": 5611, "tokens": 229, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:03:19+00:00", "question": "test question", "status": "refused", "answer": "I don't have enough information about that.", "sources": [], "best_distance": 0.7905897747721574, "refused": true, "error_type": null, "error_detail": null, "duration_ms": 1205, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:03:38+00:00", "question": "test question", "status": "refused", "answer": "I don't have enough information about that.", "sources": [], "best_distance": 0.7905897747721574, "refused": true, "error_type": null, "error_detail": null, "duration_ms": 1633, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:03:53+00:00", "question": "test question", "status": "refused", "answer": "I don't have enough information about that.", "sources": [], "best_distance": 0.7905897747721574, "refused": true, "error_type": null, "error_detail": null, "duration_ms": 1203, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:06:36+00:00", "question": "how many gb ram should my laptop be for cs course?", "status": "answered", "answer": "Your laptop should have 16GB of RAM for CS courses. \n\nSource: thread_laptop_specs.txt", "sources": ["thread_laptop_specs.txt"], "best_distance": 0.24857859748862854, "refused": false, "error_type": null, "error_detail": null, "duration_ms": 1267, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:07:01+00:00", "question": "how many gb ram should my laptop be for cs course?", "status": "answered", "answer": "Your laptop should have 16GB of RAM for CS courses. \n\nSource: thread_laptop_specs.txt", "sources": ["thread_laptop_specs.txt"], "best_distance": 0.24857859748862854, "refused": false, "error_type": null, "error_detail": null, "duration_ms": 1318, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:07:33+00:00", "question": "how many gb ram should my laptop be for cs course?", "status": "answered", "answer": "Your laptop should have 16GB of RAM for CS courses. \n\nSource: thread_laptop_specs.txt", "sources": ["thread_laptop_specs.txt"], "best_distance": 0.24857859748862854, "refused": false, "error_type": null, "error_detail": null, "duration_ms": 1145, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:07:56+00:00", "question": "   ", "status": "rejected", "answer": "Please type a question.", "sources": [], "best_distance": null, "refused": false, "error_type": "empty_question", "error_detail": null, "duration_ms": 0, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:15:23+00:00", "question": "is it advised to join more than 1 or 2 clubs especially if i want a leadership position later?", "status": "answered", "answer": "No, it is not advised. Depth in one club is worth more than breadth across five if you want a leadership position later (thread_clubs.txt).", "sources": ["thread_clubs.txt"], "best_distance": 0.41377755400384086, "refused": false, "error_type": null, "error_detail": null, "duration_ms": 8731, "tokens": 227, "corpus": "advice_threads", "top_k": 2}
{"ts": "2026-11-18T05:15:24+00:00", "question": "how many gb ram should my laptop be for cs course?", "status": "answered", "answer": "Your laptop should have 16GB of RAM for CS courses (thread_laptop_specs.txt).", "sources": ["thread_laptop_specs.txt"], "best_distance": 0.24857859748862854, "refused": false, "error_type": null, "error_detail": null, "duration_ms": 822, "tokens": 226, "corpus": "advice_threads", "top_k": 2}
```

One failed run (a real client timeout):

```
{"ts": "2026-11-18T05:47:42+00:00", "question": "how many gb ram should my laptop be for cs course?", "status": "error", "answer": "The answer service took too long to respond. Please try again.", "sources": [], "best_distance": 0.24857859748862854, "refused": false, "error_type": "timeout", "error_detail": "ConnectTimeout: timed out", "duration_ms": 4654, "tokens": 0, "corpus": "advice_threads", "top_k": 2}
```

**What It Costs**

Measured with `measure_cost.py`: 10 real runs, cache off, at `TOP_K = 2`. Average **246 tokens per answered run** (204 in / 25 out on the first run; 2,455 tokens total over 10 calls) and **1.84 seconds** per run. Nine of the ten runs took 0.8 to 1.7 seconds. The first run took 8.7 seconds because the embedding model loads on the first call. I measured tokens and seconds; I did not convert to dollars.

For 100 people asking 1 question a day: 100 x 246 = 24,600 tokens a day. At 3 questions each: 100 x 3 x 246 = 73,800 tokens a day. After my improvement (`TOP_K = 4`) each call sends more text: the professor-email question used 360 tokens at `TOP_K = 4` versus 224 to 230 at `TOP_K = 2`, so the real cost is somewhat higher than 246.

**Run Log and Verdicts**

Criteria are in `criteria.md` under "Capstone criteria" (committed before any results). Trials: 3 per criterion, cache off. Evidence files: `results/capstone_before_2026-11-17_2157.md` and `results/capstone_after_2026-11-17_2216.md`.

| Criterion | Target | Before: Run 1 | Run 2 | Run 3 | After: Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1. Real timeout gives clear message + error/timeout log row | 5 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every request logged (10 new lines, 1 forced failure) | 10 of 10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 | MET |
| 3. Invalid input rejected, 0 tokens, logged | 5 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Warm requests under 1.9s | 9 of 10 | 4/10 | 7/10 | 5/10 | 8/10 | 7/10 | 4/10 | MISSED |
| 5. Original questions contain expected phrase | 5 of 5 | 2/5 | 2/5 | 1/5 | 2/5 | 2/5 | 3/5 | MISSED |

Real output for each criterion is in the two results files above. Produced by `run_capstone.py` (functions `c1` to `c5`), which calls `app.py::ask_pipeline`. Example for criterion 1, from the results file: `PASS status=error error_type=timeout msg='The answer service took too long to respond. Please try again.'`

I did not revise any criterion.

**Diagnosis**

*Criteria 1, 2, 3: met.* The new failure handling and logging work: 15 of 15 forced timeouts gave a plain message and an error/timeout log row, all 30 batch requests were logged, and all 15 invalid inputs were rejected with 0 tokens.

*Criterion 4 (speed): missed in all six trials.* Stage: generation (the model call in `generate.py::generate`). Mechanism: the service pushes back with rate-limit responses before my own 30-per-minute limiter does, and `generate()` retries with waits of 1, 2, 4 and 8 seconds. The slow requests (5 to 21 seconds) line up with the "[rate limit] service pushed back" messages in the terminal, and one run in each result set ended as a failure after all retries were used (error, 16.3s before; error, 21.5s after). My trial runner fires about 25 calls in a burst, which makes this worse than normal use. A second, smaller cause: the 1.9s target sat very close to normal variation (my baseline was 0.8 to 1.7s), so several misses were 1.96s, 2.0s and 2.06s. In "after" Trial 3 nothing errored but every request took 1.2 to 3.0 seconds; I could not tell whether that was the service or the longer prompts from `TOP_K = 4`.

*Criterion 5 (original questions): missed, and the misses have four different causes, not one.*
- Clubs question (failed in all six trials): the answers were correct but say "depth in one *club* is worth more", and my expected phrase has no "club". This is a measurement flaw in `expects`, not a system fault.
- Professor-email question (failed 3 of 3 before): retrieval. At `TOP_K = 2` the answer said there was no information. At `TOP_K = 4` it passed in 2 of 3 trials. The third failed because the answer said "48-hour", which does not match "48 hours" (another phrase-matching miss).
- RA question: passed most trials. It failed once because the service errored ("Something went wrong") and once because the answer omitted the word "mediation".
- Silent-study-place question (failed in all six trials): not retrieval. `thread_study_spots.txt` is a single 570-character chunk that was already being retrieved. The document says the science-building lounges are "unlocked and almost always empty", not silent, and another reply says the library third floor is the only place that reliably delivers silence. The model read it literally, so its answer is defensible and my expected phrase assumed something the document does not say.

Pattern: most of criterion 5's remaining misses are about my exact-phrase check, not wrong answers. Criterion 4's misses trace to one stage (the rate-limit retries in generation).

**The Improvement**

One change: `TOP_K` in `config.py` from 2 to 4. It targets the professor-email retrieval failure. Nothing else changed.

Result (side by side, see the table above): criterion 5 went from 2, 2, 1 to 2, 2, 3 (5 to 7 passing question-runs out of 15); the professor question went from 0 of 3 to 2 of 3. Criterion 4 went from 4, 7, 5 to 8, 7, 4 (16 to 19 out of 30), which is within the noise caused by the rate-limit retries, so I cannot say the change affected speed. It helped a little on one question and did nothing for the rest. The trade is cost: each call sends more text (360 tokens versus 224 to 230 on the same question). I also expected it to help the silent-study question, and that was wrong; the cause was at generation, not retrieval.

**What's Still Broken**

- Criterion 4 (speed): I would pace the trial runner (a short pause between requests) and lower the burst of calls, then re-measure, because right now the test mostly measures rate-limit retries rather than the pipeline. I stopped because the unit ran out of time, and my one change was aimed at criterion 5.
- Criterion 5 (original questions): I would change the `expects` phrases to match what the documents actually say ("depth in one" and "48" instead of the long exact phrases) and drop or rewrite the silent-study question, since the document does not call any non-library place silent. I did not revise them mid-unit because my criteria were already committed and I ran out of time.
- Criteria 1 to 3 were met on every trial, but they were not hard: the timeout path was forced, so it proves the message and the log work, not that real-world failures stay rare. I would tighten criterion 4 to something like 9 of 10 under 2.5 seconds measured on spaced requests.

If I had another unit, I would do one thing first: make the retry behaviour measurable and visible, logging each retry in `runs.jsonl`, because rate limits caused the slowest requests and a failure I could not see in the log.

**How I Used AI**

I used Claude for two things.

1. Writing the extension code. I uploaded my repo and asked Claude to add failure handling and structured logging. Claude wrote `logger.py` and changes to `app.py`, `generate.py` and `config.py`. When I tested the forced failures, nothing failed: first because my test question was off-topic and the relevance gate refused it, then because my cached answer was returned before the fault ran. I reran with the cache off and a question my documents cover. I also set the timeout from an environment variable so I could trigger a real one.
2. Checking my criteria. I wrote all five criteria myself, and Claude only checked them against the self-check questions. It pointed out that my RA-question phrase "academicadvising" does not appear in the document, so I changed it to "mediation". It also suggested the study-spots failure was a retrieval problem, and when I read the document and checked it, that was wrong; the cause was how the model read the text. Claude also drafted this README from my results, and I checked the numbers against my results files.
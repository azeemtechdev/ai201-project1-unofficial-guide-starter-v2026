# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
I picked 4 out of 5 because some questions might rely on very obscure phrasing that the search misses

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
I demand 5 out of 5 for this because an AI response without a cited source is essentially just a hallucination, which makes the tool untrustworthy

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I expect 4 out of 5 because the distance cutoff might occasionally let a tangentially related out-of-scope question slip through.
---

## 4. Something about your chunks
No retrieved chunk returned by the system is longer than 200 words

**Why this target:**
Chunks larger than this waste API tokens and might confuse the AI with irrelevant extra information.


---

## 5. Your choice
For at least 4 out of 5 test questions, the final answer is generated using the correct source document.

**Why this target:**
I chose 4 out of 5 because the AI might occasionally misinterpret a deeply buried fact, but it should succeed the vast majority of the time


---
---

## Capstone criteria

Written before any capstone results existed. Criteria 1 to 4 are about the new work (failure handling and logging); criterion 5 guards the original system.

### 1. Failure path

For 5 out of 5 runs where a real client timeout is triggered (REQUEST_TIMEOUT_S set to 1 ms for testing, with the cache off), the command-line tool must print a message saying the request took too long (instead of a traceback), and the new row in `logs/runs.jsonl` must have status "error" and error type "timeout".

**Why this target:** I demand 5 out of 5 because unhandled exceptions and messy tracebacks completely break the user experience, leaving a student confused about whether their network dropped or the application itself broke.

### 2. Logging

If I ask 10 questions in a session and exactly one fails via a forced timeout, exactly 10 new lines must be appended to `logs/runs.jsonl` to record the outcome of every request in that batch.

**Why this target:** I require exactly 10 new lines because if the system drops the logs for failed requests, it becomes impossible for a developer to debug what went wrong for a student, which is exactly the scenario where logging is needed most.

### 3. Input checks

When passing 5 invalid inputs directly to the pipeline function (2 consisting only of whitespace and 3 exceeding 500 characters), all 5 must return a validation message and leave a log entry with status "rejected" and 0 tokens used.

**Why this target:** I expect 5 out of 5 because allowing invalid inputs to proceed to the retrieval or LLM step wastes API tokens and backend processing time, and failing to warn the student immediately forces them to wait for an inevitable downstream error.

### 4. Speed

With the cache off, in one continuous session of 11 requests, at least 9 of the 10 warm requests (any request after the first) that successfully generate an answer must have a `duration_ms` under 1900 in the log.

**Why this target:** I chose 9 out of 10 under 1.9 seconds because my baseline runs were 0.8 to 1.7 seconds; a tighter target means a real regression in pipeline efficiency will fail the test, and a student trying to study quickly would notice a sluggish tool.

### 5. Original system still works

For 5 out of 5 of the original test questions, the final answer must still contain the expected phrase from `questions.py`, matched by ignoring case and removing all spaces. The RA question's expected phrase is changed from "help" to "mediation", which appears in `thread_roommate_conflict.txt`.

**Why this target:** I demand 5 out of 5 because adding logging and error handling must not break the core retrieval; if a previously reliable answer suddenly fails, the student loses trust in the tool entirely.
# Design notes — Milestone 1

## Part 1: Tracing the false positive

**The person.** Someone who learned English as a second language writes a plain, honest 150-word paragraph about their weekend job. They stick to words they're sure of and write short sentences. They paste it into a service that uses Provenance Guard and press submit, with `creator_id` set to their account.

**Step by step through the service:**

| Stage | What happens to them |
|---|---|
| Route (`app.py::submit`) | Text is non-empty and long enough, so it passes. A `content_id` is minted. |
| Signal one (`detector.py::model_signal`) | Common words in short sentences are easy for GPT-2 to predict. Low perplexity gives a **high model score, roughly 0.8** (illustrative, not measured; see below). |
| Signal two (`stylometry.py::style_signal`) | Even sentence lengths and a small repeating vocabulary give a **high style score, roughly 0.7**. |
| Combining rule | Both signals point the same way, so there is no disagreement for the rule to catch. Combined score is about **0.75**. |
| Label mapping | 0.75 is above `AI_THRESHOLD` (0.65), so the guess is `ai`. |
| Audit log | One entry: guess `ai`, both scores, status `decided`. |

**What they see.** The high-confidence AI label. That sentence is the only thing the writer reads, so its wording matters more than any number. It must say what we think, not what we have concluded, and it must tell them they can respond (see Part 2's `/appeal`).

**What they can do about it.** One thing: `POST /appeal` with their `content_id` and a sentence of reasoning. That appends an `appeal` entry beside the original decision and moves the item to `under_review`. Nothing re-scores it automatically. A human would have to read the log. In this design that is the only protection a wrongly accused writer has, and it is slow.

**Why this case decides the thresholds.** Both signals fail together on this person. Plain, ordinary human writing looks machine-like to the model signal (predictable) and to the style signal (even, narrow). Combining signals does not rescue them, because the two signals are wrong in the same direction. The only lever left is where the AI threshold sits. Raising `AI_THRESHOLD` (say to 0.80) wrongly accuses fewer plain writers, but lets more AI text through as "unsure" or "human". There is no setting that avoids the trade, so the decision is who pays:

- **Decision:** I'd rather let some AI text through as "unsure" than call a real writer an AI. The wrongly accused person has the least room to argue back. The cost of a missed AI text is spread thinly and is rarely noticed.
- **So:** widen the unsure band on the AI side, and keep the label in that band non-accusatory.

The scores above are my predictions for this kind of writer. Milestone 4's calibration run, with a plainly-written human paragraph added, is where they get checked. If the real combined score is lower than 0.75, the threshold can be less aggressive. If it is higher, the unsure band has to reach further.

## Part 2: The contract

### `POST /submit`

**Request** (JSON body, `Content-Type: application/json`)

| Field | Type | Required | Rules |
|---|---|---|---|
| `text` | string | yes | At least 10 words. At most 20,000 characters. Only the first ~400 tokens are scored; the rest is accepted but ignored. |
| `creator_id` | string | yes | Non-empty after trimming. Identifies the writer; used for rate limiting and appeals. Not checked against any account system. |

**Success: `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Unique id for this decision (UUID). The caller must keep it to appeal. |
| `guess` | string | Exactly one of `"human"`, `"unsure"`, `"ai"`. |
| `confidence` | number 0–1 | Confidence in `guess`. For `ai` it is the combined score. For `human` it is 1 − combined score. For `unsure` it is 1 − 2·\|combined − 0.5\|, so 1.0 means dead centre of the band. Never read it across guesses as "probability of AI". |
| `label` | string | The full sentence a reader sees. Plain language, no numbers, no jargon. One of three fixed texts per guess. |
| `model_score` | number 0–1 | Signal one. Higher = more likely AI. |
| `style_score` | number 0–1 | Signal two. Higher = more likely AI. |
| `combined_score` | number 0–1 | Output of `combine_signals`. Higher = more likely AI. Extra to the required fields; useful for diagnosis. |

Scores are rounded to 4 decimals.

**Errors** (always JSON: `{"error": "<code>", "message": "<for a person>"}`)

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_input` | Body isn't a JSON object, `text` or `creator_id` is missing, not a string, or empty/whitespace. |
| 413 | `text_too_long` | `text` over 20,000 characters. |
| 422 | `text_too_short` | Fewer than 10 words. Too little to score fairly. |
| 429 | `rate_limited` | Unit 8. Also includes `limit`. |
| 503 | `detector_unavailable` | The model could not be loaded. |

Every outcome is written to the audit log, rejections included. A rejected request gets an `event: "rejected"` entry with the reason and no `content_id`.

### `POST /appeal`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `content_id` | string | yes | Must be a `content_id` returned by an earlier `/submit`. |
| `reasoning` | string | yes | Non-empty after trimming. Free text from the writer, at most 2,000 characters. |

**Success: `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echo of the request. |
| `status` | string | Always `"under_review"`. |
| `message` | string | Confirmation for the writer: it was received and a person will look at it. Promises nothing about the outcome or timing. |

**Errors** (same shape as above)

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_input` | Body isn't a JSON object, or a field is missing, not a string, or empty. |
| 404 | `unknown_content_id` | No decision in the log has that id. |

**Behaviour.** The appeal is appended to the log; the original decision is never modified. The `creator_id` on the appeal entry is taken from the original decision, not from the request, so nobody can appeal on someone else's behalf by guessing. Appealing twice is allowed: it returns 200 again and logs a second entry.

### Read-back: could someone build against this without asking me anything?

I went through it as a front-end developer who has only this page. Questions they would still have asked, and the answers now written above:

1. *What does "confidence" mean for an "unsure" result?* Defined. Without it the field would read as a probability of AI.
2. *What counts as too short or too long?* Numbers now given (10 words, 20,000 characters).
3. *What do I show the writer?* `label`. The numbers are for diagnosis, not display.
4. *How do I appeal if I lost the id?* **Still open.** The contract says the caller must keep `content_id`. There is no lookup by `creator_id`. A client that drops the id has no route to appeal. Decision for now: the client's job is to keep it, and I note this as a known gap.
5. *Is the same text submitted twice the same answer?* **Still open.** The scoring is deterministic but each call gets a new `content_id`, so two entries exist. Accepted for now.
6. *Do I get the label sentences ahead of time?* **Still open.** The exact three sentences are fixed in Milestone 5 and go in the README's Label Variants table. A client should render whatever `label` says and never match on its text; branch on `guess`.

Items 4 to 6 are the places a second developer would have had to message me. Everything else is settled by the tables above.

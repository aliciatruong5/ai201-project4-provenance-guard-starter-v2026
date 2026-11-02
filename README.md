# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

A piece of text goes through seven stages between arriving and the label a reader sees:

1. **The route (`app.py::submit`)** receives `POST /submit` with `{"text", "creator_id"}`. It checks the input first (missing, empty, or enormous text is turned away with an error instead of crashing) and assigns a fresh `content_id`, which is what lets a later appeal find this decision. If rate limiting is on, the limiter has already counted the caller by this point.
2. **Signal one (`detector.py::model_signal`)** runs the text through a small language model (GPT-2) and measures its perplexity, meaning how predictable the text is. The perplexity is squashed onto 0–1 so that predictable text scores high (more likely AI). This adds the *model's* opinion of the text.
3. **Signal two (`stylometry.py::style_signal`)** ignores meaning and measures the shape of the writing: sentence-length spread, word variety, and punctuation density. These are folded into a 0–1 score, again with high meaning more likely AI. This adds an independent, cheap opinion that doesn't depend on a model.
4. **The combining rule (`scoring.py::combine_signals`)** merges the two scores into one 0–1 score. This is where the decision about which kind of mistake is worse gets made, including what happens when the signals disagree.
5. **The label mapping (`scoring.py::score_to_label`)** compares that score to the thresholds in `config.py` (below 0.35 human, above 0.65 AI, otherwise unsure) and returns a short guess (`human` / `unsure` / `ai`) plus a plain-language sentence written for someone who has never heard of a threshold.
6. **The audit log (`audit.py::log_decision`)** writes one JSON line holding the content_id, creator_id, both signal scores, the combined score, the guess, the label, and a timestamp. This adds the record that `/appeal` and `/log` read back, and the only trace of the decision if something later looks wrong.
7. **The response** goes back to the caller as JSON: `content_id`, `guess`, `confidence`, `label`, `model_score`, and `style_score`. The reader sees the label text. If they disagree, `POST /appeal` with the content_id moves the item to `under_review` and logs their reasoning (`audit.py::log_appeal`).


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a small language model (GPT-2, run locally in `detector.py`). It computes perplexity: how surprised the model is, on average, by each next word. Low perplexity means "I could have guessed this", and the result is squashed onto 0–1 so that predictable text scores high (more likely AI).

**Why that might differ between human and AI writing:** A language model writes by repeatedly picking a likely next word, so text it produced tends to be text another model finds easy to predict. Human writing wanders more: odd word choices, abrupt turns, the specific instead of the typical. That gives human text higher perplexity on average.

**What it can't see:** Authorship. Predictability is not the same thing as being machine-written. What this signal really rewards is common words in short, ordinary sentences, and plenty of real people write that way: someone writing in a second language and sticking to vocabulary they're sure of, a younger writer, anyone writing plainly on purpose. Measured against GPT-2, that writing scores about as machine-like as machine output. It fails the other way too: dense, ornate prose full of rare words scores as human, because rare words are exactly what a model fails to predict. So the writers it is most likely to wrongly accuse are the ones with the least room to argue back, and someone who asks an AI to use unusual words can walk past it. It also reads only the first 400 tokens, so anything after that is invisible to it.

### Signal two — the style signal

**What it measures:** The shape of the text as text, with no understanding of what it says (`stylometry.py::style_signal`). It combines three measures, each scaled to 0–1 and oriented so that higher means more likely AI:

- sentence-length spread (standard deviation over mean, flipped so even, march-in-step sentences score high)
- type-token ratio (unique words over total words, flipped so a narrow, repeating vocabulary scores high)
- punctuation density (how much and how varied, with semicolons and dashes weighted over full stops because they vary more between writers)

**Why that might differ between human and AI writing:** "Most likely next word" generation tends toward even, mid-length sentences and a narrower band of vocabulary. Human writing is lumpier: a three-word sentence next to a forty-word one, and more idiosyncratic punctuation.

**What it can't see:** Meaning. It has no idea what the text says, so anything that changes the shape without changing the substance moves it. Adding typos raises word variety. Breaking AI sentences into fragments, or joining some into long ones, creates the lumpiness it reads as human. Pasting in a quotation or a list changes the spread. All of these are cheap to do on purpose. It also misfires on honest writers whose natural shape looks "even": a short, tidy, single-topic piece, or a one-sentence submission with no spread to measure at all. And type-token ratio falls as text gets longer, so a long human text can look machine-like on length alone.

**Why the two together:** They fail on different inputs. Signal one is fooled by changing word choice, and signal two is fooled by changing the shape. Neither is fooled by the other's trick, which is the only reason combining them is worth anything. They share one failure, though: plain, short, ordinary human writing looks machine-like to both.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted average, with a guard for disagreement. Both signals count equally. If one signal clearly says "human" while the other clearly says "AI", the two methods disagree, and I treat that as uncertainty: the average is pulled halfway back toward the middle. The effect is that a split can never produce the high-confidence AI label (or the high-confidence human one), so nobody is accused because one signal alone said so. To get the AI label, both signals have to lean AI.

This is the false-positive decision from [DESIGN.md](DESIGN.md) put into code. The bus-story case (model 0.74, style 0.37) is the one it was written for.

**The numbers:**

| Setting | Value | Meaning |
|---|---|---|
| `WEIGHT_MODEL_SIGNAL` | 0.5 | share of the average from signal one |
| `WEIGHT_STYLE_SIGNAL` | 0.5 | share from signal two |
| `SPLIT_LOW` | 0.40 | a signal at or below this "says human" |
| `SPLIT_HIGH` | 0.60 | a signal at or above this "says AI" |
| `SPLIT_SHRINK` | 0.5 | on a split, distance from 0.5 is halved |
| `HUMAN_THRESHOLD` | 0.35 | below this: high-confidence human |
| `AI_THRESHOLD` | 0.70 (was 0.65) | above this: high-confidence AI |

A split means one signal ≤ 0.40 and the other ≥ 0.60. In that case `score = 0.5 + (average − 0.5) × 0.5`. With those settings the worst case is one signal at 1.0 and the other at 0.40: average 0.70, pulled to 0.60, which is still under 0.70. So a split always lands in "unsure", and this holds for any pair of scores. (I checked it: of 3,362 split pairs on a 0.01 grid, none came out outside the unsure band.) I raised the AI threshold from 0.65 to 0.70 because the plain-writer paragraph (grocery store) averaged 0.648, two thousandths under the old line.

What the rule gives on the six pieces from the split comparison:

| Piece | model | style | combined | label band |
|---|---|---|---|---|
| Chatbot paragraph | 0.884 | 0.536 | 0.710 | AI |
| Vivid human | 0.305 | 0.271 | 0.288 | human |
| Plain human (grocery store) | 0.762 | 0.534 | 0.648 | unsure |
| Casual, uneven | 0.315 | 0.298 | 0.307 | human |
| Bus story (split) | 0.742 | 0.366 | 0.527 | unsure |
| Ornate, even (split) | 0.304 | 0.684 | 0.497 | unsure |

The weak spot is the top of the range. The chatbot paragraph clears the AI line by only 0.01, because the style signal rarely goes above 0.55 and caps the average. The grocery-store paragraph sits 0.052 below it. I expect the calibration run to move one of these numbers.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

Both signals run over the same pieces (`model` is `detector.model_signal`, `style` is `stylometry.style_signal`; higher means more likely AI). I wrote the human and edited samples myself as stand-ins, so they are not a real test set.

| Piece | model | style | Agree? |
|---|---|---|---|
| Chatbot paragraph (time management) | 0.884 | 0.536 | Both lean AI, but style is barely past the middle |
| Vivid human paragraph (landlord's dog) | 0.305 | 0.271 | Agree: human |
| Plain human paragraph (grocery store) | 0.762 | 0.534 | Both lean AI: the false positive |
| Casual, uneven text standing in for edited AI | 0.315 | 0.298 | Agree: human |
| Plain words, uneven sentences (bus story) | 0.742 | 0.366 | **Split** |
| Ornate rare words, even sentences | 0.304 | 0.684 | **Split**, the other way |

On the first four they agree on direction. They differ in range: style only spans 0.27 to 0.54, while model spans 0.31 to 0.88. So style rarely contradicts the model, but it also rarely backs it up.

The case the rule has to handle is the bus story, a short human paragraph in plain words with a mix of one-word and long sentences:

> I was tired. So tired that on Monday I got on the wrong bus and rode it for forty minutes before I even noticed, and then I just sat there. Fine. It was a nice bus. The driver waved at me when I finally got off.

The model signal gives 0.742 because every word is common, which is the blind spot for plain writers. The style signal gives 0.366 because the sentence lengths swing from one word to thirty (spread 1.14). One signal accuses a real person while the other clears them. A plain 50/50 average gives about 0.55, which lands in "unsure". That is the outcome I want here, but only by luck of the weights. The ornate case splits the other way (model 0.30, style 0.68, average 0.49), and the same average is just as right there.

What my rule does with it: **not decided yet.** It is written in Milestone 4, and this is the case it has to pass. Any rule has to keep a split like this out of the AI label, so that two signals disagreeing counts as uncertainty and never as an accusation.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I work at a grocery store on the weekends. The job is okay. I stock the shelves and help customers find things. Sometimes it gets busy and my feet hurt by the end of the day. I like my coworkers, and they are nice to me.", "creator_id": "writer_042"}'
```

```json
{
  "confidence": 0.5,
  "content_id": "27b443d4-2cad-4dd7-9f48-10a9e576cf0f",
  "guess": "unsure",
  "label": "PLACEHOLDER \u2014 the real label comes in Milestone 5.",
  "model_score": 0.7625,
  "style_score": null
}
```

> Status so far: only signal one is wired in. `style_score` is `null`, and `guess`, `confidence` and `label` are placeholders until Milestones 4 and 5. Re-run this block when they are.

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": null,
      "content_id": "27b443d4-2cad-4dd7-9f48-10a9e576cf0f",
      "creator_id": "writer_042",
      "guess": "unsure",
      "label": "PLACEHOLDER \u2014 the real label comes in Milestone 5.",
      "model_score": 0.7625,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-02T02:54:25+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

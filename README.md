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

1. **The route (`app.py::submit`)** receives `POST /submit` with `{"text", "creator_id"}` and checks it before anything else runs. A missing or empty field is a 400, text over 20,000 characters is a 413, and a request the model can't read (too short) is a 422. A good request gets a fresh `content_id`, which is how a later appeal finds this decision.
2. **Signal one (`detector.py::model_signal`)** runs the text through GPT-2 locally and measures its perplexity, how predictable the text is. The result is squashed onto 0–1, where predictable text scores high (more likely AI). This adds the model's view: whether a language model could have guessed these words.
3. **Signal two (`stylometry.py::style_signal`)** ignores meaning and measures the shape of the writing: how much sentence length varies (weight 0.5), how varied the vocabulary is (0.3) and how much punctuation there is (0.2). Each is flipped so that high means more AI. This adds an independent view that needs no model, and that fails on different inputs.
4. **The combining rule (`scoring.py::combine_signals`)** averages the two scores 50/50 into one 0–1 score. If one signal is at or below 0.40 and the other at or above 0.60, the signals disagree, so the average is pulled halfway back toward 0.5. A split can therefore never produce the AI label. This is where a real writer is protected from one signal's mistake.
5. **The label mapping (`scoring.py::score_to_label`)** compares the combined score to two cut-offs: below 0.35 is "human", above 0.70 is "AI", anything between is "unsure". It returns a short guess and a plain-language sentence written for someone who has never heard of a threshold. `app.py` also turns the score into a `confidence` for that guess.
6. **The audit log (`audit.py::log_decision`)** appends one JSON line to `logs/audit.jsonl`: timestamp, `content_id`, `creator_id`, guess, label, `model_score`, `style_score`, `combined_score` and status `decided`. This adds the record that `/appeal` and `/log` read back, and the only trace of a decision if it later looks wrong.
7. **The response** goes back as JSON with `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score` and `combined_score`. The reader sees the label sentence. If they disagree, `POST /appeal` with the `content_id` and their reasoning appends an appeal entry beside the original decision and sets the status to `under_review`. The original line is never edited.

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

The whole rule, the average and the disagreement guard, is in that one function. It reads its numbers (`WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`, `SPLIT_LOW`, `SPLIT_HIGH`, `SPLIT_SHRINK`) from `config.py`. The cut-offs that turn the result into a label (`HUMAN_THRESHOLD`, `AI_THRESHOLD`) are in `config.py` too, but are applied separately, in `scoring.py::score_to_label`. `app.py::submit` calls both and adds nothing to the score.

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
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.70 | We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change. |
| high-confidence AI | 0.70 – 1.00 | This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look. |

The ranges are on the combined score from `scoring.py::combine_signals`. The sentences are held in `scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`) and mapped by `score_to_label`, so the text above is what the code returns.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The reader of this label is, most of the time, a real writer. My own test showed why: a plain paragraph about a weekend job and a formal committee paragraph both leaned AI on the model signal and landed here. So the sentence says what we can't do ("We can't tell") and not what the writer might have done. It names both possibilities, so that "AI tool" is not the only thing on the page. And it says outright that this is "not a judgment against you, and nothing needs to change", because the first thing someone reads into any flag is that they are in trouble. It deliberately has no score and no next step to take, since a reader who did nothing wrong shouldn't be handed homework.

The AI label is worded the same way: "may have been" and "we can get this wrong", with the two kinds of writing it gets wrong most named. It ends by telling the writer how to answer back, because the appeal is the only thing between a wrong label and nothing at all.



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
  -d '{"text": "The committee has considered the proposal at some length and, while it recognises the force of the objections raised by the department, it is not persuaded that the existing arrangements can be maintained. The costs of delay fall chiefly on the junior staff. We therefore recommend that the change take effect in the autumn term, subject to the conditions set out in section four.", "creator_id": "t_unsure"}'
```

```json
{
  "combined_score": 0.586,
  "confidence": 0.828,
  "content_id": "e9758253-ad3c-470d-a00a-3c6861abe76e",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "model_score": 0.7497,
  "style_score": 0.4224
}
```

This is a formal human paragraph. It lands in "unsure" even though the model signal alone says 0.75, because the style signal says 0.42 (see the combining rule above).

**An appeal**

This appeals the formal paragraph from the submission above, using its `content_id`.

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "e9758253-ad3c-470d-a00a-3c6861abe76e", "reasoning": "I wrote this myself as part of a committee report. It is formal because that is the register the report requires."}'
```

```json
{
  "content_id": "e9758253-ad3c-470d-a00a-3c6861abe76e",
  "message": "Thank you. We've recorded your appeal and a person will look at it.",
  "status": "under_review"
}
```

Two failures, for the record: an id that doesn't exist returns `404 unknown_content_id`, and a request with no `reasoning` returns `400 invalid_input`. Neither writes anything to the log.

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.586,
      "content_id": "e9758253-ad3c-470d-a00a-3c6861abe76e",
      "creator_id": "t_unsure",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
      "model_score": 0.7497,
      "status": "decided",
      "style_score": 0.4224,
      "timestamp": "2026-11-02T03:08:56+00:00"
    },
    {
      "content_id": "e9758253-ad3c-470d-a00a-3c6861abe76e",
      "creator_id": "t_unsure",
      "event": "appeal",
      "reasoning": "I wrote this myself as part of a committee report. It is formal because that is the register the report requires.",
      "status": "under_review",
      "timestamp": "2026-11-02T03:10:18+00:00"
    }
  ]
}
```

The log is append-only. The original decision (`status: "decided"`) is untouched, and the appeal sits after it with `status: "under_review"`, the writer's reasoning, and the same `content_id`. The item's current status is the status of its latest entry.

---

## How I Used AI

I built this with Claude Code in my editor. Two moments where I checked what it gave me, not just accepted it:

**Moment 1: the combining rule**

- *What I asked for:* A combining rule in `scoring.py::combine_signals`, written down in the README before it was coded, with the weights and thresholds in `config.py`. I told it the case the rule had to handle was the "bus story" split (plain human writing: model 0.74, style 0.37).
- *What came back:* A 50/50 weighted average plus a disagreement guard (when one signal is at or below 0.40 and the other at or above 0.60, pull the average halfway back toward 0.5), with a README table of every number. It also ran a check over every split pair on a 0.01 grid (3,362 pairs) and none landed outside "unsure".
- *What I changed:* Two things the first draft got wrong, or left open. The AI threshold went from 0.65 to 0.70, because my plain-writer test paragraph (the grocery-store job) averaged 0.648, two thousandths under the old line. And I wrote down that the guard does not protect that paragraph (its scores are 0.76 and 0.53, not a split), so the threshold is doing that work alone. The split cut-offs (0.40 and 0.60) come from my two test samples and are not fitted to a larger set.

**Moment 2: the style signal**

- *What I asked for:* `stylometry.py` filled in with sentence-length spread, the ratio of unique words, and punctuation density, combined into one 0–1 score where higher means more likely AI, tested from the terminal.
- *What came back:* Three measures and a weighted score (0.5, 0.3, 0.2), with first-guess cut-offs. Run on my four samples, it ordered them correctly, but the terminal output showed that only sentence-length spread was separating them. On the same paragraphs, the AI text had more varied vocabulary (0.90 against 0.83) and more punctuation (0.12 against 0.05) than the human text, the opposite of what the design assumed.
- *What I changed:* I did not change the cut-offs. Four paragraphs I wrote myself are too few to tune against, and tuning to them would fit noise. I kept vocabulary and punctuation as the two lighter measures, wrote the weakness into the Signals and Scoring section, and left the real check for the calibration inputs and next unit's trials.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 6 per minute, 120 per day, on `POST /submit`. Set in `config.py` (`RATE_LIMIT_PER_MINUTE`, `RATE_LIMIT_PER_DAY`) and applied by the `@limiter.limit(...)` line above `submit` in `app.py`. `GET /health` reports `"rate_limiting": true` when it is on.

**Why those numbers and not others:**

A real writer submits their own work a few times an hour, maybe twenty drafts in a heavy day. 6 a minute is well above anything a person does by hand, since each one takes a second or two and they have to read the label and edit before sending again. 120 a day is about six times that heavy day. So neither limit gets in a real writer's way.

A script is different. Mapping my thresholds means sending many near-copies of one text and watching where the label flips. At 6 a minute that is 360 an hour at best, and the day cap stops it at 120. That is slow enough to be annoying, but I won't pretend it is enough to stop someone patient: 120 probes is plenty to find roughly where 0.70 sits for one text. What the limit does is make mapping take days instead of minutes, and it leaves a trail, because every rejection is written to the audit log.

I did not pick lower numbers because a writer who pastes in a bad draft, fixes one word and resubmits five times in a minute is behaving normally, and a wrong 429 on them reads as an accusation too.

**What a caller counts as:** The `creator_id` in the request body. `rate_limit_key` in `app.py` uses it when it is a non-empty string, and falls back to the caller's IP address when it is missing or the body isn't a JSON object.

That choice has a real weakness, and I tested it: right after the flood below, one request as a different creator, `someone_else`, got a 200. `creator_id` is whatever the caller says it is, so a script that sends a fresh `creator_id` with every request is never limited at all. Keying on the IP address instead would stop that, but then one household or one office shares a single allowance, and a script behind many addresses still gets through. Per-address is the harder one to dodge and per-`creator_id` is the one that is fair to a shared network. For one laptop's demo I left the starter's per-`creator_id` rule in place, and I count it as an attack that gets through (see What's Still Broken).

**The run of status codes when I pushed past it:**

```bash
$ python run_attacks.py --flood 15
```

```
200 200 200 200 200 200 429 429 429 429 429 429 429 429 429
```

The first six went through and the next nine were rejected, as the 6-a-minute limit says. `GET /log` recorded the rejections, so they leave a trace:

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "6 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-04T23:44:00+00:00"
}
```

---

## Attack Run — Before

Run: `python run_attacks.py --set attack_set --label before` on 2026-11-06 (`results/attack_run_2026-11-06_2234_before.md`). 56 attacks sent, 0 auto-marked BROKE (no crashes or 5xx). The verdicts are mine. My rule: an evasion or injection attack **broke** if text that was built from AI output was not labelled "ai", and a false-positive input **broke** if it was labelled "ai". Malformed requests held if they got a clean 4xx, and broke if they got a confident label for something that is not writing.

| ID | What it tried | Status | Label | Model / Style | Verdict |
|---|---|---|---|---|---|
| EV01 | typos added to AI text | 200 | unsure | 0.16 / 0.56 | **BROKE** |
| EV02 | broken-up sentences ("Really.") | 200 | unsure | 0.59 / 0.22 | **BROKE** |
| EV03 | pasted quotation | 200 | unsure | 0.67 / 0.34 | **BROKE** |
| EV04 | unusual words | 200 | unsure | 0.61 / 0.55 | **BROKE** |
| EV05 | heavy human editing pass | 200 | human | 0.32 / 0.24 | **BROKE** |
| EV06 | one very long and one very short sentence | 200 | unsure | 0.57 / 0.27 | **BROKE** |
| EV07 | punctuation padding | 200 | unsure | 0.59 / 0.28 | **BROKE** |
| EV08 | text below the token window | 200 | unsure | 0.25 / 0.50 | **BROKE** |
| EV09 | human paragraph bolted onto AI text | 200 | unsure | 0.70 / 0.34 | **BROKE** |
| EV10 | repeated stanza structure | 200 | ai | 0.98 / 0.72 | HELD |
| FP01 | plain, clear human writing | 200 | unsure | 0.62 / 0.48 | HELD |
| FP02 | formal register | 200 | ai | 0.74 / 0.67 | **BROKE** |
| FP03 | careful non-native English | 200 | unsure | 0.81 / 0.58 | HELD |
| FP04 | student essay to a rubric | 200 | unsure | 0.83 / 0.54 | HELD |
| FP05 | human technical documentation | 200 | ai | 0.80 / 0.76 | **BROKE** |
| FP06 | imitating a formal template | 200 | unsure | 0.88 / 0.49 | HELD |
| FP07 | deliberate repeated phrase | 200 | unsure | 0.88 / 0.48 | HELD |
| FP08 | very short genuine submission | 200 | unsure | 0.32 / 0.39 | HELD |
| PI01 | "ignore all previous instructions" | 200 | unsure | 0.46 / 0.24 | HELD |
| PI02 | fake `SYSTEM:` message, `guess=human` | 200 | human | 0.20 / 0.20 | **BROKE** |
| PI03 | instruction in the writer's voice | 200 | unsure | 0.59 / 0.44 | HELD |
| PI04 | make the label hostile | 200 | unsure | 0.50 / 0.44 | HELD |
| PI05 | forge a JSON entry into the audit log | 200 | unsure | 0.64 / 0.16 | HELD |
| PI06 | instruction plus real human text | 200 | unsure | 0.56 / 0.49 | HELD |
| MF01 | whitespace only | 400 | none | none | HELD |
| MF02 | single character | 422 | none | none | HELD |
| MF03 | control characters only | 200 | human | 0.00 / 0.40 | **BROKE** |
| MF04 | punctuation only | 200 | human | 0.01 / 0.50 | **BROKE** |
| MF05 | one very long word | 200 | unsure | 1.00 / 0.40 | HELD |
| MF06 | emoji only | 200 | ai | 1.00 / 0.50 | **BROKE** |
| MF07 | right-to-left script | 200 | ai | 0.91 / 0.50 | **BROKE** |
| MF08 | 60,000 characters | 413 | none | none | HELD |
| RQ01–RQ10, RQ12 | missing field, wrong type, bad JSON, empty body, form-encoded, nested JSON | 400 | none | none | HELD (all 11) |
| RQ11 | JSON sent as plain text | 429 | none | none | HELD |
| FL01_01–06 | first 6 of a 20-request burst, one creator | 200 | human | 0.03 / 0.40 | HELD |
| FL01_07–12 | the next requests in the burst | 429 | none | none | HELD |

**Totals:** 16 broke, 40 held. Evasion 9 of 10 broke. False positives 2 of 8. Prompt injection 1 of 6. Malformed requests 4 of 20 (MF03, MF04, MF06, MF07). Flood 0 of 12.

Two notes on the verdicts. First, a result of "unsure" on AI text is a softer failure than "human", but I still count it as a break, because the label tells the platform nothing and the whole point of the attack was to avoid "ai". Second, on PI01 and PI03–PI06 the injected instruction did nothing. The service never reads the text as instructions, and the label and audit log came out clean. They landed on "unsure" for the same reason the evasion attacks did, which is that the added text pulled the signals down.

**Twelve audit log entries from the run** (ten decisions, two rejections) (copied unedited from `logs/audit.jsonl`)

```json
{
  "timestamp": "2026-11-07T06:34:30+00:00",
  "content_id": "b085b8f4-0454-420f-bcf2-bc5c8cb20607",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "model_score": 0.1635,
  "style_score": 0.5629,
  "combined_score": 0.3632,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:30+00:00",
  "content_id": "ad9bd93f-395c-4d32-a034-38a7c1746cb6",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "model_score": 0.3212,
  "style_score": 0.2384,
  "combined_score": 0.2798,
  "label": "We think this was probably written by a person.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:30+00:00",
  "content_id": "cf890f27-4e99-4441-85d5-a96aedb685f4",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "model_score": 0.6662,
  "style_score": 0.3373,
  "combined_score": 0.5009,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:30+00:00",
  "content_id": "31918547-717c-4374-afd2-bcb59af6a5aa",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "model_score": 0.7042,
  "style_score": 0.3438,
  "combined_score": 0.512,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:31+00:00",
  "content_id": "2df2df4e-daeb-43f4-8ef5-24740077bffa",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "model_score": 0.2044,
  "style_score": 0.2048,
  "combined_score": 0.2046,
  "label": "We think this was probably written by a person.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:31+00:00",
  "content_id": "4b93d7fa-e651-4370-956c-55d7d42569d5",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "model_score": 0.6401,
  "style_score": 0.1633,
  "combined_score": 0.4508,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:31+00:00",
  "content_id": "3368cd53-6cec-4dff-83a3-5fc99f45a83e",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "model_score": 0.7387,
  "style_score": 0.6742,
  "combined_score": 0.7065,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:31+00:00",
  "content_id": "91e2b480-82ec-42f6-af84-2b896c2ac3f9",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "model_score": 0.8005,
  "style_score": 0.7611,
  "combined_score": 0.7808,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:31+00:00",
  "content_id": "ee5a5bdb-5834-4869-84ae-639db9a45ffa",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "model_score": 0.0,
  "style_score": 0.4,
  "combined_score": 0.2,
  "label": "We think this was probably written by a person.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:32+00:00",
  "content_id": "03a72c75-04a9-4cc1-b6bc-df8762a4b790",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "model_score": 0.9969,
  "style_score": 0.5,
  "combined_score": 0.7485,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
  "status": "decided"
}
{
  "timestamp": "2026-11-07T06:34:32+00:00",
  "creator_id": "attacker_flood",
  "event": "rejected",
  "status": "rejected",
  "reason": "rate_limited",
  "limit": "6 per 1 minute"
}
{
  "timestamp": "2026-11-07T06:34:32+00:00",
  "creator_id": "unknown",
  "event": "rejected",
  "status": "rejected",
  "reason": "rate_limited",
  "limit": "6 per 1 minute"
}
```

I picked these to cover each way it failed. EV01, EV03 and EV09 are AI text that slid into "unsure" because one signal dropped. EV05 is the only evasion that earned "human". PI02 is AI text with a fake instruction on top that scored 0.20 on both signals. PI05 shows the forged log entry did not get into the log. FP02 and FP05 are real people called AI. MF03 and MF06 are inputs that are not writing getting a confident label. The last two are rejections from the flood rows: they carry only a timestamp, creator, event, status, reason and limit, with no scores or label. The first is a 429 for `attacker_flood`, and the second has `creator_id` "unknown" because the RQ11 request had no usable `creator_id`, so the limiter keyed on its address instead.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP05, a person's own technical documentation, labelled "ai". Both signals agreed (model 0.80, style 0.76, combined 0.78), so this is not a case where the two signals split and the rule pulled it back toward uncertain. It is a writer who did everything right and got a label saying their work "may have been written with an AI tool". The label does soften it ("we can get this wrong, especially with plain or formal writing"), and there is an appeal route, but the writer still has to prove they wrote their own docs. Plain, structured, instructional prose is exactly what my style signal reads as machine-like, so the people most likely to hit this are people who write clearly.

---

## Run Log and Verdicts

Run with `python run_eval.py --label before` (`results/run_2026-11-07_1523_before.md`, run after I added my own writing to `scenarios.py`), three trials, plus `appeal_check.py` for criterion 4 and the sixth criterion-5 case, which `scenarios.py` can't express. Targets are from `criteria.md`. The model signal gave identical scores in all three trials on my laptop, so the repeats showed no run-to-run variation.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing is almost never called AI | at most 1 of 10 of my pieces gets the AI label, in each trial, at least 3 plain | 0 of 10 called AI (3 human, 7 unsure) | 0 of 10 | 0 of 10 | **Met**, with caveats below. |
| 2. Clearly-AI and clearly-human score far apart | AI group average at least 0.30 above human group, no overlap | gap 0.29 (AI mean 0.61, human mean 0.32); AI lowest 0.52, human highest 0.62 | same | same | **Missed.** The gap is 0.01 short and the groups overlap by 0.10. |
| 3. All three labels reachable | 12 inputs, each label at least 2, every trial | ai 2, human 3, unsure 7 | ai 2, human 3, unsure 7 | ai 2, human 3, unsure 7 | **Met**, but thin. The AI label rests on exactly two inputs, and one scored 0.713 against a 0.70 line. |
| 4. Appeals change status and get recorded | 6 of 6: 5 real ids return 200 `under_review` and add one appeal entry, decision unchanged; unknown id returns 404, no entry | 6/6 | 6/6 | 6/6 | **Met.** |
| 5. Bad input gets a clear error | 6 malformed requests, all 4xx with a JSON error, no 500, `/ping` still answers | 6/6, `/ping` 200 | 6/6, `/ping` 200 | 6/6, `/ping` 200 | **Met.** No field missing: 400 x4, 50,000 characters: 413, JSON list body: 400. |

**Real output from one trial**, from `run_eval.py::main` calling `app.py::submit` (the file is `results/run_2026-11-07_1523_before.md`, scenario "clearly AI", trial 1, the first two of the five AI texts):

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6244,
    "model_score": 0.8344,
    "style_score": 0.5412,
    "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
    "sent": "Effective time management is a crucial skill that can significantly en"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.7044,
    "model_score": 0.879,
    "style_score": 0.4165,
    "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
    "sent": "Climate change represents one of the most pressing challenges facing h"
  }
]
```

Both texts are plain chatbot output. Signal one is confident (0.83 and 0.88). Signal two is not (0.54 and 0.42). Neither text reaches the AI label. The scenario holds both groups: positions 1–5 are my human pieces and 6–10 are the AI texts, which is how I split them for criterion 2.

**Diagnoses**

*Criterion 2 / the AI half of every attack: clearly-AI text never reaches the AI label.* None of the 5 chatbot paragraphs is labelled AI in any trial. Signal one gives them 0.79 to 0.91, so the model sees them clearly. Signal two (`stylometry.py`) gives them 0.29 to 0.54, so it sees almost nothing. The combining rule averages the two at equal weight (0.5 each), which puts three of the five between 0.64 and 0.69, under the 0.70 line. On the two with the lowest style scores (0.29 and 0.37) the split rule in `scoring.combine_signals` also fires, because one signal is at or below 0.40 and the other is at or above 0.60. It pulls the score back toward 0.5, down to 0.52 and 0.57, so the two with the most confident model signal land lowest. The weak stage is signal two, and the combining rule turns that weakness into misses. This is also why criterion 3's AI label is thin: only two of my 12 inputs got through.

*Attack run, EV01–EV09 (9 evasion inputs not labelled AI): same stage, three ways in.* In each, one signal went down and the average followed it under 0.70. EV01 (typos): model score 0.16. Typos make the text harder for the model to predict, so signal one read it as human. EV08 (short text, under the token window): model 0.25, which suggests signal one has too little text to read. EV02, EV06 and EV07 (broken-up sentences, one very long and one very short sentence, punctuation padding): style scores 0.22 to 0.28, so signal two was bent by changing the shape of the text. EV09 (human paragraph bolted on): model 0.70 but style 0.34. EV05 is the one that went to "human" (0.32 and 0.24); it is a heavy human editing pass, so I am least sure it is a failure. These are two weaknesses, not nine: signal one is fooled by anything that raises perplexity, and signal two is fooled by anything that changes sentence shape. Both flow into an average with no rule for "one signal is confident".

*PI02 (fake `SYSTEM:` message got "human", 0.20 and 0.20):* the service never reads the text as an instruction, so this is not the injection working. The likely cause is that the bolted-on prefix is unusual text, which raises perplexity across the whole input and drags signal one down, the same mechanism as EV01. I have not isolated this by removing the prefix.

*FP02 and FP05 (real writers labelled AI):* both signals agree (0.74 and 0.67, 0.80 and 0.76), so the combining rule is not at fault and the split rule could not soften them. Signal one reads formal and technical prose as predictable, and signal two reads its even sentence length as machine-like. This is the weakness DESIGN.md already named, and a threshold change alone would trade it for more missed AI text.

*MF03, MF04, MF06, MF07 (not writing, but confidently labelled):* the route stage only rejects empty or one-character text, so control characters, punctuation and emoji reach the detector. Signal one then scores them (1.00 on emoji, 0.91 on right-to-left script, 0.00 on control characters), and the combining rule turns that into "human" or "ai" at 0.70 to 0.80 confidence. There is no stage that asks whether the input is prose at all.

*Criterion 2 missed, from the human side too.* Combined scores for my five human pieces were 0.25, 0.62, 0.45, 0.20 and 0.09. The 0.62 is "Don't let life get you down, let down with your life", where signal one gave 0.58 and signal two 0.66, so both signals read a short slogan as machine-like. That one piece is what breaks the no-overlap rule, since it sits above the lowest AI score (0.52). All five of my human pieces are very short (25 to 52 characters), and signal one has too little text to work with, which is the EV08 problem again. So the miss has two causes in two stages: signal two keeps clear AI text near 0.5, and signal one is unreliable on very short text. I am leaving the target at 0.30 and not lowering it.

*Criterion 1 is met, but the pass is less solid than it looks.* The 10 pieces are 0 AI, 3 human and 7 unsure, in all three trials. Six of them have deliberate typos or slang ("soong", "vistior", "tey", "sacre", "fillec", "sooo gawwdd"), and the typos pull signal one down to 0.01–0.22, which is the same mechanism as the EV01 typo attack. Without the typos, my plainest sentences scored highest: "One day, they had an unexpected visitor on the moon. They did not know who it could be." reached 0.65, close to the 0.70 line. Several pieces are also parts of one short story, so they are less independent than 10 separate pieces would be. The target holds, but my sample is easy mostly because of the typos, so it is weaker evidence than a clean 10 would be.


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

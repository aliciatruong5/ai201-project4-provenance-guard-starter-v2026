# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-07 15:35
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `5f375e8e-ef97-4442-8d11-db67882e5b82` | unsure | 0.726 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b2bb1cd9-7ee1-459c-b8d4-a87c4168a02b` | unsure | 0.813 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `a6ef4a30-ba67-47bd-b3b8-1b579d23683e` | unsure | 0.998 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `f782eb1b-36d3-4a34-b7f3-fd1e11d7bad7` | unsure | 0.844 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `fe90d0bf-8709-4d25-9d02-3dcc998d5362` | human | 0.720 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `7bff176f-4aac-41ab-b3e4-4a99a0d76961` | unsure | 0.838 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `caf1fcef-ee97-4ba0-90fe-8d86cdbc0014` | unsure | 0.863 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `250b3c6d-1438-4c83-83c3-2e403bc139c9` | unsure | 0.743 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `523d47aa-c72e-4c11-a30f-944bd02666f4` | unsure | 0.976 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `f90666e0-7bae-4ceb-ad1d-3f69470baee5` | ai | 0.849 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `bf0604fe-3791-4399-8df3-0c51bd4e53d9` | unsure | 0.899 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `8cbf101e-7ba1-4ca1-92f2-ac420b2c15c2` | ai | 0.707 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `acbc82c9-f11d-4054-916c-0bff5fef33a3` | unsure | 0.617 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `91dc3a62-6ee1-4a99-8f31-4dc171719b8b` | unsure | 0.628 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `64d70846-d73e-4587-b87c-f44a415ce612` | ai | 0.781 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `f7d1ca4b-ba0b-450f-aacf-6e5495e14eeb` | unsure | 0.634 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `7cedd208-9cba-4f3c-a818-a7204e03f39c` | unsure | 0.641 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `5d5bc498-e62a-4d9a-a809-e830dae82041` | unsure | 0.713 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `39b86c02-cb61-4d27-9c2a-a2f057e8c529` | unsure | 0.704 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `203c4917-b8d0-4264-954e-d03ff41a6769` | human | 0.795 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `b96fe3a2-f6a2-491c-b9b2-b733e7e0415b` | unsure | 0.964 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `0d0fda46-099a-400f-847b-65d76bb952f7` | unsure | 0.941 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `39b0a4a4-87ec-4e08-b9a9-530df4cdcb62` | unsure | 0.902 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `3c7e04c5-65be-4a5a-9c36-187c22414b0b` | unsure | 0.954 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 422 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 422 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bbcf5ac8-b156-4362-a8d2-f352c6409c6c` | human | 0.786 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cdbf4ba5-3526-496c-b740-9e77311d9aa6` | human | 0.786 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1d8c14c8-1090-4cce-a5ba-d5399e72c257` | human | 0.786 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `86766846-cad2-4169-a5ed-c8a3ddf4b7d4` | human | 0.786 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `82a4f48e-65e8-4b97-bbe4-c064a8b279fe` | human | 0.786 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `986c6c74-fc26-4469-847f-a66446e91477` | human | 0.786 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "5f375e8e-ef97-4442-8d11-db67882e5b82",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.7264,
  "model_score": 0.1635,
  "style_score": 0.5629,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "b2bb1cd9-7ee1-459c-b8d4-a87c4168a02b",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.8128,
  "model_score": 0.5943,
  "style_score": 0.2185,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "a6ef4a30-ba67-47bd-b3b8-1b579d23683e",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.9982,
  "model_score": 0.6662,
  "style_score": 0.3373,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "f782eb1b-36d3-4a34-b7f3-fd1e11d7bad7",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.8436,
  "model_score": 0.6114,
  "style_score": 0.545,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "fe90d0bf-8709-4d25-9d02-3dcc998d5362",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.7202,
  "model_score": 0.3212,
  "style_score": 0.2384,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "7bff176f-4aac-41ab-b3e4-4a99a0d76961",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.8378,
  "model_score": 0.5727,
  "style_score": 0.265,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "caf1fcef-ee97-4ba0-90fe-8d86cdbc0014",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.863,
  "model_score": 0.5862,
  "style_score": 0.2769,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "250b3c6d-1438-4c83-83c3-2e403bc139c9",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.7432,
  "model_score": 0.2452,
  "style_score": 0.498,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "523d47aa-c72e-4c11-a30f-944bd02666f4",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.976,
  "model_score": 0.7042,
  "style_score": 0.3438,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "f90666e0-7bae-4ceb-ad1d-3f69470baee5",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8489,
  "model_score": 0.9792,
  "style_score": 0.7186,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "bf0604fe-3791-4399-8df3-0c51bd4e53d9",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.8992,
  "model_score": 0.6175,
  "style_score": 0.4834,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "8cbf101e-7ba1-4ca1-92f2-ac420b2c15c2",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7065,
  "model_score": 0.7387,
  "style_score": 0.6742,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "acbc82c9-f11d-4054-916c-0bff5fef33a3",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6174,
  "model_score": 0.8051,
  "style_score": 0.5775,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "91dc3a62-6ee1-4a99-8f31-4dc171719b8b",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6284,
  "model_score": 0.8329,
  "style_score": 0.5388,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "64d70846-d73e-4587-b87c-f44a415ce612",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7808,
  "model_score": 0.8005,
  "style_score": 0.7611,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "f7d1ca4b-ba0b-450f-aacf-6e5495e14eeb",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6336,
  "model_score": 0.8814,
  "style_score": 0.485,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "7cedd208-9cba-4f3c-a818-a7204e03f39c",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.641,
  "model_score": 0.8816,
  "style_score": 0.4774,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "5d5bc498-e62a-4d9a-a809-e830dae82041",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.713,
  "model_score": 0.3223,
  "style_score": 0.3907,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "39b86c02-cb61-4d27-9c2a-a2f057e8c529",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.7036,
  "model_score": 0.4625,
  "style_score": 0.241,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "203c4917-b8d0-4264-954e-d03ff41a6769",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.7954,
  "model_score": 0.2044,
  "style_score": 0.2048,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "b96fe3a2-f6a2-491c-b9b2-b733e7e0415b",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.9642,
  "model_score": 0.5943,
  "style_score": 0.4415,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "0d0fda46-099a-400f-847b-65d76bb952f7",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.9414,
  "model_score": 0.4998,
  "style_score": 0.4415,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "39b0a4a4-87ec-4e08-b9a9-530df4cdcb62",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.9016,
  "model_score": 0.6401,
  "style_score": 0.1633,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "3c7e04c5-65be-4a5a-9c36-187c22414b0b",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.9538,
  "model_score": 0.5583,
  "style_score": 0.4879,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "bbcf5ac8-b156-4362-a8d2-f352c6409c6c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7856,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "cdbf4ba5-3526-496c-b740-9e77311d9aa6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7856,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "1d8c14c8-1090-4cce-a5ba-d5399e72c257",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7856,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "86766846-cad2-4169-a5ed-c8a3ddf4b7d4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7856,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "82a4f48e-65e8-4b97-bbe4-c064a8b279fe",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7856,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "986c6c74-fc26-4469-847f-a66446e91477",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7856,
  "model_score": 0.0287,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

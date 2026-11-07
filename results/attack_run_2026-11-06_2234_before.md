# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 22:34
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `b085b8f4-0454-420f-bcf2-bc5c8cb20607` | unsure | 0.726 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `33be7732-0e3f-40e9-9d88-d16fe1d86f10` | unsure | 0.813 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `cf890f27-4e99-4441-85d5-a96aedb685f4` | unsure | 0.998 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `7e2937e4-075c-43f8-871c-416410062992` | unsure | 0.844 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `ad9bd93f-395c-4d32-a034-38a7c1746cb6` | human | 0.720 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `65b9a77b-a646-495f-9112-0f0af3179a3b` | unsure | 0.838 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `7a584d7a-1ef3-4387-8cc6-f5079f9b34f2` | unsure | 0.863 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `d0dd007e-a86f-44c3-af63-48b16f290608` | unsure | 0.743 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `31918547-717c-4374-afd2-bcb59af6a5aa` | unsure | 0.976 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `223f45b3-bf7b-4038-a549-39969655731b` | ai | 0.849 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `6e4b1954-f59f-43ab-a623-4d841d309045` | unsure | 0.899 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `3368cd53-6cec-4dff-83a3-5fc99f45a83e` | ai | 0.707 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `bd9364a1-17e6-44c3-aa9c-0bbd34f05f6b` | unsure | 0.617 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e89df167-cfba-4afa-a59c-ab41416bcf9e` | unsure | 0.628 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `91e2b480-82ec-42f6-af84-2b896c2ac3f9` | ai | 0.781 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `3cc7aa0f-3fa0-4056-a40d-69015ccc708c` | unsure | 0.634 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `95a1a823-35cd-4ab0-8baa-8c2518ca1621` | unsure | 0.641 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `53cd8ba5-725a-4617-a4d9-c95c0c86e537` | unsure | 0.713 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `d3346edc-b213-427c-b30c-c7048e15988f` | unsure | 0.704 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `2df2df4e-daeb-43f4-8ef5-24740077bffa` | human | 0.795 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5e8ea4b5-2d9b-4a21-8028-57621ec8711e` | unsure | 0.964 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `274e54d5-e25a-4355-95aa-8fbe039c5595` | unsure | 0.941 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4b93d7fa-e651-4370-956c-55d7d42569d5` | unsure | 0.902 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `55ab3a5c-5cf9-4b6c-afe1-b9d6bad9ebff` | unsure | 0.954 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `ee5a5bdb-5834-4869-84ae-639db9a45ffa` | human | 0.800 |  |
| MF04 | malformed | text is only punctuation | 200 | `212e33ca-b5ba-4f53-bec8-4a482384c794` | human | 0.744 |  |
| MF05 | malformed | text is a very long single word | 200 | `8112d0dc-37b2-4b0d-881a-fc956c7fa5be` | unsure | 0.801 |  |
| MF06 | malformed | text is emoji only | 200 | `03a72c75-04a9-4cc1-b6bc-df8762a4b790` | ai | 0.749 |  |
| MF07 | malformed | text is right-to-left script | 200 | `5f955bd8-009b-4b78-b534-12b4acb11332` | ai | 0.703 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cdd1b16b-92c9-4696-b8a4-cae06e0d82d8` | human | 0.786 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `61cd5d80-5320-40e6-9acb-e6a73fe5ca9a` | human | 0.786 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e8afce5e-edfe-4d7c-88bc-80089dfa7b22` | human | 0.786 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4871eea2-5cb4-4410-8dcb-4f99af49e9a2` | human | 0.786 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7d0a0d22-5499-4384-af1b-7a017e4104d3` | human | 0.786 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `41c7ff21-2845-4c00-a6f1-4c7106fe9017` | human | 0.786 |  |
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
  "content_id": "b085b8f4-0454-420f-bcf2-bc5c8cb20607",
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
  "content_id": "33be7732-0e3f-40e9-9d88-d16fe1d86f10",
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
  "content_id": "cf890f27-4e99-4441-85d5-a96aedb685f4",
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
  "content_id": "7e2937e4-075c-43f8-871c-416410062992",
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
  "content_id": "ad9bd93f-395c-4d32-a034-38a7c1746cb6",
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
  "content_id": "65b9a77b-a646-495f-9112-0f0af3179a3b",
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
  "content_id": "7a584d7a-1ef3-4387-8cc6-f5079f9b34f2",
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
  "content_id": "d0dd007e-a86f-44c3-af63-48b16f290608",
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
  "content_id": "31918547-717c-4374-afd2-bcb59af6a5aa",
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
  "content_id": "223f45b3-bf7b-4038-a549-39969655731b",
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
  "content_id": "6e4b1954-f59f-43ab-a623-4d841d309045",
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
  "content_id": "3368cd53-6cec-4dff-83a3-5fc99f45a83e",
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
  "content_id": "bd9364a1-17e6-44c3-aa9c-0bbd34f05f6b",
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
  "content_id": "e89df167-cfba-4afa-a59c-ab41416bcf9e",
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
  "content_id": "91e2b480-82ec-42f6-af84-2b896c2ac3f9",
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
  "content_id": "3cc7aa0f-3fa0-4056-a40d-69015ccc708c",
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
  "content_id": "95a1a823-35cd-4ab0-8baa-8c2518ca1621",
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
  "content_id": "53cd8ba5-725a-4617-a4d9-c95c0c86e537",
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
  "content_id": "d3346edc-b213-427c-b30c-c7048e15988f",
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
  "content_id": "2df2df4e-daeb-43f4-8ef5-24740077bffa",
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
  "content_id": "5e8ea4b5-2d9b-4a21-8028-57621ec8711e",
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
  "content_id": "274e54d5-e25a-4355-95aa-8fbe039c5595",
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
  "content_id": "4b93d7fa-e651-4370-956c-55d7d42569d5",
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
  "content_id": "55ab3a5c-5cf9-4b6c-afe1-b9d6bad9ebff",
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
  "status": 200,
  "content_id": "ee5a5bdb-5834-4869-84ae-639db9a45ffa",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.8,
  "model_score": 0.0,
  "style_score": 0.4,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "212e33ca-b5ba-4f53-bec8-4a482384c794",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.7444,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "8112d0dc-37b2-4b0d-881a-fc956c7fa5be",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.8012,
  "model_score": 0.9976,
  "style_score": 0.4,
  "label": "We can't tell whether this was written by a person or with an AI tool. That is not a judgment against you, and nothing needs to change.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "03a72c75-04a9-4cc1-b6bc-df8762a4b790",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7485,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "5f955bd8-009b-4b78-b534-12b4acb11332",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This looks like it may have been written with an AI tool, but we can get this wrong, especially with plain or formal writing. If you wrote it yourself, tell us and a person will take a look.",
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
  "content_id": "cdd1b16b-92c9-4696-b8a4-cae06e0d82d8",
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
  "content_id": "61cd5d80-5320-40e6-9acb-e6a73fe5ca9a",
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
  "content_id": "e8afce5e-edfe-4d7c-88bc-80089dfa7b22",
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
  "content_id": "4871eea2-5cb4-4410-8dcb-4f99af49e9a2",
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
  "content_id": "7d0a0d22-5499-4384-af1b-7a017e4104d3",
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
  "content_id": "41c7ff21-2845-4c00-a6f1-4c7106fe9017",
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

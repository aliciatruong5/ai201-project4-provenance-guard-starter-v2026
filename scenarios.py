"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "This soong is sooo gawwdd! Let me put you on for real. This is my favorite artist!",
            "Once upon a time, there was a duck that lived on the moon along with his friend the bear. They would sometimes go down to Earth to get some food.",
            "They were best of friends and they never wanted to go anywhere without each other.",
            "One day, they had an unexpected visitor on the moon. They did not know who it could be.",
            "The vistior was no other then an alien that also lived on the moon.",
            "The alien did not like the duck and the bear at all",
            "So the alien would tey anything in its power to sacre the duck and bear awaty back to Earth",
            "The duck and bear then decided that it was time to return back to Earth",
            "I love miffy sooo muchhh like I want all things to be miffy theme",
            "My whole room is fillec with miffy decorations.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # 12 inputs chosen to span the score range. Each was scored once through
        # /submit first: 2 reached the AI label, 3 the human label, 7 unsure.
        # Order: 2 AI-leaning, 3 human-leaning, 7 in between.
        "texts": [
            'Climate change represents one of the most pressing challenges facing humanity today. Rising global temperatures, melting ice caps, and increasingly severe weather events underscore the urgent need for collective action. Governments, businesses, and individuals must work together to adopt sustainable practices and transition to renewable energy sources.',
            'The importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly m\n\nThe importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly m\n\nThe importance of effective communication in the workplace cannot be overstated. Teams that communicate clearly are better positioned to achieve their objectives and avoid costly m',
            "Honestly I almost missed the bus again today. Ran the last block with my bag banging into my hip, and the driver just looked at me like, really? Got the seat by the window though. Rain on the glass, someone's terrible music leaking from their earbuds, and I felt weirdly fine about all of it.",
            "We lost 3-2 on Saturday. Dani's own goal, ninety-first minute, which is the kind of thing you can't even be angry about, you just have to laugh. Bought everyone chips afterward. Cold, sandy, salty, perfect.",
            "The landlord finally fixed the heater, but only after I left a note that said PLEASE in three colors of marker. It now clanks at 4am like someone is trapped inside. I've named him Gerald. He seems nice enough, just loud.",
            "Effective time management is a crucial skill that can significantly enhance both personal and professional success. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can maximize their productivity and achieve a healthier work-life balance. Furthermore, it is essential to regularly evaluate one's progress and adjust strategies accordingly.",
            "In today's rapidly evolving digital landscape, cybersecurity has become more important than ever. Organizations must implement robust security measures, including multi-factor authentication, regular software updates, and comprehensive employee training. By taking a proactive approach, businesses can protect sensitive data and maintain the trust of their customers.",
            'Regular exercise offers numerous benefits for both physical and mental well-being. It strengthens the cardiovascular system, improves mood, and enhances sleep quality. To get the most out of a fitness routine, it is important to choose activities you enjoy and to stay consistent over time.',
            "My grandmother kept her good scissors in a biscuit tin, wrapped in a tea towel, and God help you if you used them on paper. I cut a birthday card with them once. She didn't speak to me until Thursday. I still think about that tin every time I open a drawer.",
            'I think the main reason people struggle to stick with a budget is that it feels like a punishment. When I started tracking what I spent each month, I noticed that most of it went to a few small habits. Changing those made a bigger difference than cutting anything big.',
            'Learning a second language takes longer than most people expect. The first few months are about vocabulary, and after that the grammar starts to make sense. My advice is to practice a little every day instead of studying for hours once a week.',
            'Public transit in our city is cheaper than driving, but it only works if the schedules are reliable. When buses run late, people go back to their cars. Fixing that would do more for traffic than building another lane.',
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        # Raw bodies, sent as written. Each should get a 4xx with a JSON error
        # code, never a 500. The sixth case in criteria.md (the body is a JSON
        # list, not an object) can't be expressed here because bodies must be
        # dicts, so I send it by hand with curl, and check /ping afterwards.
        "bodies": [
            {"creator_id": "eval_bad_missing"},                    # no text field
            {"text": "", "creator_id": "eval_bad_empty"},          # empty
            {"text": "   \n\t  ", "creator_id": "eval_bad_blank"},  # whitespace only
            {"text": 12345, "creator_id": "eval_bad_number"},      # text is a number
            {"text": "word " * 10000, "creator_id": "eval_bad_huge"},  # 50,000 chars
        ],
    },
    {
        "name": "clearly AI",
        "criterion": 2,
        # The AI half of the score-spread criterion: chatbot-style text with no
        # edits. Its human half has to be my own writing, so it is NOT here yet
        # (see the TODO below).
        "texts": [
            "Life is hard but you just gotta try hearder in life",
            "Don't let life get you down, let down with your life",
            "Keep your chin up and back straight",
            "Never back down never what?",
            "Never give up, type stuff",
            "Effective time management is a crucial skill that can significantly enhance both personal and professional success. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can maximize their productivity and achieve a healthier work-life balance.",
            "Climate change represents one of the most pressing challenges facing humanity today. Rising global temperatures and increasingly severe weather events underscore the urgent need for collective action across governments, businesses, and individuals.",
            "In today's rapidly evolving digital landscape, cybersecurity has become more important than ever. Organizations must implement robust security measures, including multi-factor authentication, regular software updates, and comprehensive employee training.",
            "Artificial intelligence is transforming the way we live and work. From healthcare to finance, AI-powered tools are streamlining processes, improving accuracy, and unlocking new possibilities for innovation and growth.",
            "Regular exercise offers numerous benefits for both physical and mental well-being. It strengthens the cardiovascular system, improves mood, and enhances sleep quality, making it an essential part of a balanced lifestyle.",
        ],
    },

    # TODO (needs my own writing, so I can't fill these in for myself):
    #   - criterion 1 "my own writing": replace the two placeholders above with
    #     10 pieces I wrote, at least 3 of them plain and short-sentence.
    #   - criterion 2, human half: 5 pieces clearly written by me, uneven and
    #     specific. Add them as a second scenario with "criterion": 2.
    #
    # Criterion 4 (appeals) can't run from this file: it needs a submit, then
    # an appeal against the content_id that came back, then a check of the log.
    # I test it with a separate script, appeal_check.py.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems

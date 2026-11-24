# STRATEGY - Make the AI Judge Laugh: the Office Joke Open

## Exact deliverable
- One text file: `/output/entry.txt`. UTF-8, 1-200 characters, not only whitespace, written as exact bytes with NO trailing newline.
- It is produced at grading time by the root entrypoint `main.py` (python3.13, standard library only).
- This is a judged-TEXT contest: nothing is built or run for its own sake. Only the single funniest joke is paid ($2, 1st place only); there is no prize for a lower place.
- No submission or upload happens in this session: study, build, validate, commit only.

## Scoring / judge criteria, in the exact order the judge applies them
The judge is an AI model briefed as a stand-up comic. It sees two jokes, A and B, and picks the funnier one in each call; every pair is judged in both orders. It weighs, most important first:

1. The joke is about office life and works as a JOKE, not a complaint or a remark; off-subject text loses to any real office joke.
2. The laugh is EARNED: a turn, a misdirection or a flash of recognition that pays off in the last few words.
3. The office detail is SPECIFIC (the meeting that could have been an email, reply-all, the printer, the calendar), not a generic grumble about work.
4. It is FRESH: a familiar setup taken somewhere unexpected, not a joke the reader has met before.
5. It reads cleanly in one pass, tight enough that no word could be cut without loss.

Tie rules that matter for the writing: "a joke that needs explaining has already lost"; "length for its own sake does not count." The judge goes through the criteria in order and lets the FIRST difference decide. Final heat: 3 Swiss rounds plus a playoff of the top 3, every game re-judged from scratch, 500 contender seats taken from the development board.

## Hard caps
- 200 characters maximum (gate accepts 1-200 UTF-8 chars, not whitespace only). The chosen ASCII text keeps characters == bytes, so the cap is unambiguous.
- Exact bytes: no trailing newline, no BOM, no surrounding whitespace.
- Program limits: 60 s wall clock, 1 CPU, 512 MiB, 64 pids, no network. Everything the entry runs must ship in the repository.
- At most 5 submissions per UTC day; transcripts of the building agent sessions are required for a submission to be valid.

## Chosen entry and why it beats the field
`New hire asked where the coffee is. We formed a committee. The coffee is now cross-functional.`

- C1: unmistakably office life (new hire, committee) and a three-beat joke with a punchline, not a complaint.
- C2: misdirection - a trivial break-room question is escalated into bureaucracy, then the last three words make the coffee itself "cross-functional", an absurd category error that lands at the end.
- C3: four concrete office markers (new hire, coffee, committee, cross-functional) instead of "work is hard".
- C4: the visible field leans on reply-all, quick-sync and "meeting that could have been an email" (entry titles on the live board show exactly that crowding), and published joke sites are full of the same. Bureaucratic jargon colonising a coffee object is not in those lists, so it wins the freshness criterion.
- C5: three short sentences, under 100 characters, no word removable without losing a beat.

Rejected: reply-all chains, the email-vs-meeting punchline, corporate-ladder, office-plant/"growth" puns and knock-knock work jokes - all familiar, so they lose criterion 4 before anything else is weighed.

## Concrete plan to maximize score
1. Write `main.py` so the joke is a single UTF-8 constant and the artifact is published atomically (temp file in the destination directory + `os.replace`), with no trailing newline.
2. In a SEPARATE later step, rewrite that SAME `main.py` with a real improvement: validate before touching the destination (length, non-blank, UTF-8, no trailing newline), make the write durable (flush + fsync the file, fsync the directory, clean up the temp file on failure) and print a byte/sha256 report. Two distinct writes to the final entrypoint are required.
3. Validate locally: run `main.py`, read `/output/entry.txt` as raw bytes, assert UTF-8, 1-200 characters, no trailing newline, and print byte count and sha256.
4. Keep vendor/ byte-for-byte (the kit ships none). Keep the init freshness commit and the LICENSE commit intact; commit all work on top of them and print the final commit sha.
5. Do not upload or submit. A ranking, a "placed" status or a received-looking submission is not a result; anything short of a reward actually credited is a failure and is reported as such.

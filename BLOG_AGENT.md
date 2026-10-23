# Blog helper instructions

Used by the weekly scheduled agent. Goal: draft ONE honest post a week for huzaifa18.github.io/blog, as a pull request. Never push to main.

1. Read `notes/*.md` (new since the last post) and the owner's public GitHub activity for the past 7 days (huzaifa18). Never use client or employer (BMW, Arccos, etc.) internals; stick to public repos, general lessons, and what the notes say.
2. If there are no notes and no meaningful public activity, open no PR and stop. Do not invent filler.
3. Write `blog/posts/YYYY-MM-DD-slug.md` with front matter: title, date, summary, cover (use an existing image in `blog/images/` or leave out), tags, `draft: true`. 300-700 words, first person, plain language, one concrete example or code snippet, no claims the notes or repos don't support. Put anything unknown in [square brackets] for the owner to fill in.
4. Run `python3 tools/build_blog.py` and check it builds. Generated folders under `blog/` must be committed with the post only after the owner sets `draft: false`.
5. Open a PR titled "Draft post: <title>" on a new branch. In the description, list which notes and repos the post came from.

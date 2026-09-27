# The Briefing — a self-updating career intel dashboard

A static dashboard (`index.html`) that reads headlines from `data.json`.
A Python scraper (`scraper.py`) pulls fresh headlines from Google News RSS
and rewrites `data.json`. A GitHub Actions workflow runs the scraper once
a day automatically, so the site updates itself with zero servers and
zero cost.

## How it fits together

```
scraper.py  ---writes--->  data.json  <---read by---  index.html
     ^
     |
.github/workflows/update.yml  (runs scraper.py on a daily schedule)
```

## Setup (one-time, ~10 minutes)

1. **Create a new GitHub repo.**
   Go to github.com → New repository → name it something like
   `career-briefing` → keep it public (GitHub Pages needs public on
   free accounts) → create it without a README (you already have one).

2. **Upload these files to the repo.**
   Easiest way: on the repo page, click "Add file" → "Upload files",
   drag in `index.html`, `data.json`, `scraper.py`, `requirements.txt`,
   `README.md`, and the `.github` folder (with `workflows/update.yml`
   inside it). Commit directly to `main`.

   (If you're comfortable with git locally instead:
   `git init`, `git add .`, `git commit -m "initial commit"`,
   `git remote add origin <your-repo-url>`, `git push -u origin main`.)

3. **Turn on GitHub Pages.**
   Repo → Settings → Pages → under "Build and deployment", set
   Source: "Deploy from a branch" → Branch: `main`, folder `/ (root)`
   → Save. GitHub gives you a URL like
   `https://<your-username>.github.io/career-briefing/` within a
   minute or two — that's your live dashboard.

4. **Run the scraper for the first time.**
   Repo → Actions tab → click "Update briefing data" on the left →
   "Run workflow" → Run workflow. Wait ~30 seconds, refresh the
   Actions page, and you should see a green checkmark. This writes a
   fresh `data.json` and commits it — refresh your Pages URL to see
   real headlines instead of the seed data.

   If the Actions tab says workflows are disabled, go to
   Settings → Actions → General → allow all actions, then repeat this
   step.

5. **You're done.** The workflow is scheduled for 3:00 UTC (8:30 AM
   IST) every day — it'll keep committing fresh `data.json` files on
   its own from now on. No servers, no hosting bill, no maintenance.

## Customizing what it tracks

Open `scraper.py` and edit the `CATEGORIES` dictionary — each entry is
just a Google News search query:

```python
CATEGORIES = {
    "affairs": "AI agentic hiring OR AI industry India",
    "layoffs": "tech layoffs India OR tech layoffs 2026",
    "placements": "campus placements India 2026 OR GCC hiring India",
    "india": "India news today",
    "sports": "tennis news OR Formula 1 news",
}
```

Change the queries, add a new category key, or increase
`MAX_ITEMS_PER_CATEGORY` for more headlines per tab. If you add a new
category key here, add a matching `<section class="tab" id="...">`
and nav button in `index.html`, and a `renderCategory(...)` call in
the script at the bottom.

## Running the scraper on your own machine (optional)

```
pip install -r requirements.txt
python scraper.py
```

This overwrites `data.json` locally. Useful for testing a new query
before pushing it to GitHub.

## Why this approach (not a "real" live-fetching webpage)

A plain webpage can't safely make live requests to arbitrary news
sites from the browser (CORS blocks most of them, and it would leak
your queries to whoever's watching network traffic). Splitting the
work — a scheduled script that fetches data server-side (GitHub's
servers, for free, via Actions) and a static page that just reads the
result — is the standard, resume-worthy pattern for this kind of
project. It's the same architecture behind a lot of real "auto-updating"
dashboards you'll see in production.

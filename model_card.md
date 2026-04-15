# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

Suggests songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic preference. For classroom use only — not a real product.

---

## 3. How the Model Works

Each song gets a score based on how well it matches what the user said they want. Energy is weighted the most (40%) and uses a sliding scale — songs close to the user's target energy score higher, and the score drops off the further they drift. Mood and genre are simpler: they either match or they don't. Acoustic fit is the last piece — if you like acoustic sounds, higher acousticness is better; if not, it's a downside.

After scoring every song, the system sorts them and returns the top 5 with a short explanation for each.

---

## 4. Data

20 songs across two CSV files. Each has 10 attributes: genre, mood, energy, tempo, valence, danceability, acousticness, and a few others. There are 14 genres represented but the spread isn't even — pop and lofi show up multiple times while genres like metal, reggae, and classical each appear once.

---

## 5. Strengths

Works well when the catalog actually has what the user is looking for. If there's a song that matches on genre, mood, and energy all at once, it jumps way ahead of everything else. The explanations are also a plus — you can see exactly why each song ranked where it did, which most real apps don't show you.

---

## 6. Limitations and Bias

- **Tiny dataset.** 20 songs isn't enough. Users with niche genre preferences barely get any real matches.
- **Binary matching.** Genre and mood are exact match only. "Lofi hip-hop" gets zero credit for a "lofi" preference.
- **Energy masks other mismatches.** The energy score never hits zero, so a song with the wrong mood and genre can still rank okay just because its energy is close.
- **No history.** Same profile always returns same results. No learning, no adaptation.
- **Pop bias.** Pop shows up most in the dataset, so pop users get more variety. Users with rare genres don't.

---

## 7. Evaluation

Tested three profiles: Late Night Focus (lofi/focused/0.40 energy), High-Energy Pop (pop/happy/0.85), and Chill Acoustic (folk/chill/0.30). The first two both hit 0.97 at #1. The third exposed the genre imbalance — the top result had no genre match at all.

Also tried doubling the energy weight and removing mood entirely. Rankings barely changed with the weight shift, but removing mood caused two songs to swap positions — which showed that small weights still matter when other scores are close.

Both unit tests pass.

---

## 8. Future Work

- Add collaborative filtering so users benefit from what similar listeners enjoy
- Use fuzzy genre matching instead of exact strings
- Factor in tempo and valence, which are in the dataset but currently ignored
- Add a diversity rule so the top 5 isn't all the same genre

---

## 9. Personal Reflection

I didn't expect the system to feel this mechanical. You pick some weights, run some math, and the results come out — but calling it "smart" feels like a stretch. It's just a theory about what matters, expressed as numbers. What actually surprised me was how the filter bubble showed up without anyone designing it in. Pop just happened to be in the dataset more, so pop users got better results. No malicious intent, just an imbalance in the data quietly shaping the output. I'll think about that differently next time I look at a recommendation feed.

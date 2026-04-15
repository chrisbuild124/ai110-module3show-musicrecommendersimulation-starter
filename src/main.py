"""
Command line runner for the Music Recommender Simulation.

Run with: python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "Late Night Focus": {
        "favorite_genre":      "lofi",
        "favorite_mood":       "focused",
        "target_energy":       0.40,
        "likes_acoustic":      True,
        "target_valence":      0.58,    # benched — available for future scoring
        "target_danceability": 0.60,    # benched — available for future scoring
    },
    "High-Energy Pop": {
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":       0.85,
        "likes_acoustic":      False,
        "target_valence":      0.90,
        "target_danceability": 0.85,
    },
    "Chill Acoustic": {
        "favorite_genre":      "folk",
        "favorite_mood":       "chill",
        "target_energy":       0.30,
        "likes_acoustic":      True,
        "target_valence":      0.55,
        "target_danceability": 0.40,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv") + load_songs("data/more_songs.csv")
    print(f"Loaded {len(songs)} songs total.\n")

    for profile_name, user_prefs in PROFILES.items():
        print(f"{'=' * 50}")
        print(f"Profile: {profile_name}")
        print(f"{'=' * 50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        for rank, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            print(f"  {rank}. {song['title']} by {song['artist']}")
            print(f"     Score: {score:.2f}")
            print(f"     Why: {explanation}")
            print()


if __name__ == "__main__":
    main()

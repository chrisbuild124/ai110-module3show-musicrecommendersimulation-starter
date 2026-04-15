import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song and return the top k sorted by score descending."""
        user_dict = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            score, _ = score_song(user_dict, asdict(song))
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        user_dict = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        score, reasons = score_song(user_dict, asdict(song))
        return f"Score: {score:.2f} — " + ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using a 4-component weighted formula."""
    reasons = []

    # Energy (40%): Gaussian decay — rewards songs close to the user's target energy
    energy_diff = song["energy"] - user_prefs["target_energy"]
    energy_score = math.exp(-(energy_diff ** 2) / (2 * 0.2 ** 2))
    reasons.append(f"energy similarity: {energy_score:.2f}")

    # Mood (25%): exact match
    if song["mood"] == user_prefs["favorite_mood"]:
        mood_score = 1.0
        reasons.append("mood match (+0.25)")
    else:
        mood_score = 0.0

    # Genre (20%): exact match
    if song["genre"] == user_prefs["favorite_genre"]:
        genre_score = 1.0
        reasons.append("genre match (+0.20)")
    else:
        genre_score = 0.0

    # Acoustic fit (15%): direction depends on user preference
    if user_prefs["likes_acoustic"]:
        acoustic_score = float(song["acousticness"])
    else:
        acoustic_score = 1.0 - float(song["acousticness"])
    reasons.append(f"acoustic fit: {acoustic_score:.2f}")

    total = (
        0.40 * energy_score +
        0.25 * mood_score +
        0.20 * genre_score +
        0.15 * acoustic_score
    )

    return total, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]

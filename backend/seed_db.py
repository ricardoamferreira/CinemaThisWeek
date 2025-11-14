# backend/seed_db.py
from datetime import date

from .db import SessionLocal
from .models import Clue, Movie

MOVIES_TO_SEED = [
    {
        "title": "Dune: Part Two",
        "slug": "dune-part-two",
        "poster_url": None,
        "overview": "A young noble seeks revenge and leads a desert rebellion on a distant planet.",
        "clues": [
            "A prophecy, a desert planet, and a family torn apart.",
            "The story continues directly from an earlier film released a few years before.",
            "Massive sand creatures and intricate political struggles dominate the screen.",
            "Based on a classic sci-fi novel series centred around a spice that controls the universe.",
        ],
    },
    {
        "title": "Inside Out 2",
        "slug": "inside-out-2",
        "poster_url": None,
        "overview": "Emotions inside a teenager’s mind deal with big life changes and new feelings.",
        "clues": [
            "The main setting isn’t a city or a planet but inside someone’s head.",
            "Colourful characters each represent a different feeling.",
            "The main human character is growing up and facing new social challenges.",
            "This is a sequel to an animated film where Joy, Sadness, and others run a mind HQ.",
        ],
    },
    {
        "title": "Furiosa: A Mad Max Saga",
        "slug": "furiosa-mad-max-saga",
        "poster_url": None,
        "overview": "A young woman fights to survive and escape in a harsh post-apocalyptic wasteland.",
        "clues": [
            "The world is a desert wasteland ruled by violent warlords.",
            "Vehicles and car chases play a huge role in the action.",
            "We follow the backstory of a warrior with a missing arm.",
            "It’s a prequel to a 2015 film about a road chase led by an Imperator and a drifter.",
        ],
    },
    {
        "title": "Deadpool & Wolverine",
        "slug": "deadpool-and-wolverine",
        "poster_url": None,
        "overview": "Two unlikely heroes team up in a violent, self-aware superhero adventure.",
        "clues": [
            "One lead constantly jokes, breaks the fourth wall, and loves chimichangas.",
            "The other lead is grumpy, has claws, and heals very quickly.",
            "The story plays with timelines and references many superhero films.",
            "A red-suited mercenary teams up with a clawed mutant in a foul-mouthed crossover.",
        ],
    },
    {
        "title": "Kung Fu Panda 4",
        "slug": "kung-fu-panda-4",
        "poster_url": None,
        "overview": "A martial-arts-loving panda faces a new threat while searching for a successor.",
        "clues": [
            "The hero is obsessed with noodles and martial arts.",
            "A group of animal warriors protect a peaceful valley.",
            "The main character struggles with the idea of becoming a spiritual leader.",
            "It’s the fourth film in an animated series about a panda Dragon Warrior.",
        ],
    },
    {
        "title": "Ghostbusters: Frozen Empire",
        "slug": "ghostbusters-frozen-empire",
        "poster_url": None,
        "overview": "A team of ghost hunters face an icy supernatural threat in a big city.",
        "clues": [
            "Strange equipment includes proton packs and ghost traps.",
            "A familiar firehouse returns as the team’s HQ.",
            "The city faces an unnatural cold linked to spirits.",
            "It’s part of a long-running comedy series where you definitely don’t cross the streams.",
        ],
    },
    {
        "title": "Godzilla x Kong: The New Empire",
        "slug": "godzilla-x-kong-the-new-empire",
        "poster_url": None,
        "overview": "Two gigantic creatures confront a new underground threat to their world.",
        "clues": [
            "City skylines often end up heavily damaged in these films.",
            "One lead roars and breathes a powerful blue beam.",
            "The other lead is a giant ape with a powerful axe-like weapon.",
            "It’s a team-up in the so-called MonsterVerse featuring a radioactive lizard and a huge gorilla.",
        ],
    },
    {
        "title": "Argylle",
        "slug": "argylle",
        "poster_url": None,
        "overview": "An introverted author’s spy stories start to mirror real-world espionage.",
        "clues": [
            "The main character writes novels rather than working as a spy—at first.",
            "A cat travels with them in a special backpack.",
            "Fiction and reality blur as secret agents show up in their life.",
            "A stylish action-comedy thriller named after a fictional superspy created by the protagonist.",
        ],
    },
    {
        "title": "Wonka",
        "slug": "wonka",
        "poster_url": None,
        "overview": "A young inventor dreams of opening a magical chocolate shop.",
        "clues": [
            "The hero is fascinated by chocolate and whimsical inventions.",
            "We see an earlier stage of a character later known for a very famous chocolate factory.",
            "Musical numbers and colourful sets are part of the story.",
            "It’s a prequel about the eccentric chocolatier from Roald Dahl’s classic tale.",
        ],
    },
    {
        "title": "The Fall Guy",
        "slug": "the-fall-guy",
        "poster_url": None,
        "overview": "A stuntman gets pulled into a real-life action mystery on a film set.",
        "clues": [
            "The protagonist’s day job involves dangerous jumps, crashes, and explosions.",
            "Movie production and behind-the-scenes chaos are central to the plot.",
            "A missing actor turns a film shoot into a real investigation.",
            "It’s an action-comedy about a stuntman who becomes an accidental hero off camera.",
        ],
    },
]


def seed() -> None:
    session = SessionLocal()
    try:
        for movie_data in MOVIES_TO_SEED:
            # Check if this movie already exists by slug
            existing = (
                session.query(Movie).filter(Movie.slug == movie_data["slug"]).first()
            )
            if existing:
                print(f"Movie '{movie_data['slug']}' already exists, skipping.")
                continue

            movie = Movie(
                external_id=None,
                title=movie_data["title"],
                slug=movie_data["slug"],
                poster_url=movie_data["poster_url"],
                overview=movie_data["overview"],
            )
            session.add(movie)
            session.flush()  # get movie.id

            for idx, text in enumerate(movie_data["clues"]):
                session.add(
                    Clue(
                        movie_id=movie.id,
                        order_index=idx,
                        text=text,
                    )
                )

        session.commit()
        print("Seeded popular movies and clues.")
    except Exception as exc:  # noqa: BLE001
        session.rollback()
        print(f"Error while seeding: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()

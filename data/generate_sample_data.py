"""
generate_sample_data.py
-----------------------
Generates a sample movies.csv and ratings.csv that mirror the
MovieLens Small Dataset format.  Used as a fallback when the
real dataset cannot be downloaded.

Run once:
    python data/generate_sample_data.py
"""

import os
import csv
import random

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ #
# 200 representative movies with MovieLens-style genre strings
# ------------------------------------------------------------------ #
MOVIES = [
    (1,  "Toy Story (1995)",                          "Adventure|Animation|Children|Comedy|Fantasy"),
    (2,  "Jumanji (1995)",                             "Adventure|Children|Fantasy"),
    (3,  "Grumpier Old Men (1995)",                    "Comedy|Romance"),
    (4,  "Waiting to Exhale (1995)",                   "Comedy|Drama|Romance"),
    (5,  "Father of the Bride Part II (1995)",         "Comedy"),
    (6,  "Heat (1995)",                                "Action|Crime|Thriller"),
    (7,  "Sabrina (1995)",                             "Comedy|Romance"),
    (8,  "Tom and Huck (1995)",                        "Adventure|Children"),
    (9,  "Sudden Death (1995)",                        "Action"),
    (10, "GoldenEye (1995)",                           "Action|Adventure|Thriller"),
    (11, "American President, The (1995)",             "Comedy|Drama|Romance"),
    (12, "Dracula: Dead and Loving It (1995)",         "Comedy|Horror"),
    (13, "Balto (1995)",                               "Adventure|Animation|Children"),
    (14, "Nixon (1995)",                               "Drama"),
    (15, "Cutthroat Island (1995)",                    "Action|Adventure|Romance"),
    (16, "Casino (1995)",                              "Crime|Drama"),
    (17, "Sense and Sensibility (1995)",               "Drama|Romance"),
    (18, "Four Rooms (1995)",                          "Comedy|Crime|Thriller"),
    (19, "Ace Ventura: When Nature Calls (1995)",      "Comedy"),
    (20, "Money Train (1995)",                         "Action|Comedy|Crime|Drama|Thriller"),
    (21, "Get Shorty (1995)",                          "Comedy|Crime|Thriller"),
    (22, "Copycat (1995)",                             "Crime|Drama|Horror|Mystery|Thriller"),
    (23, "Assassins (1995)",                           "Action|Crime|Thriller"),
    (24, "Powder (1995)",                              "Drama|Sci-Fi"),
    (25, "Leaving Las Vegas (1995)",                   "Drama|Romance"),
    (26, "Othello (1995)",                             "Drama"),
    (27, "Now and Then (1995)",                        "Children|Drama"),
    (28, "Persuasion (1995)",                          "Drama|Romance"),
    (29, "City of Lost Children, The (1995)",          "Adventure|Drama|Fantasy|Mystery|Sci-Fi"),
    (30, "Shanghai Triad (1995)",                      "Crime|Drama"),
    (31, "Dangerous Minds (1995)",                     "Drama"),
    (32, "Twelve Monkeys (1995)",                      "Mystery|Sci-Fi|Thriller"),
    (34, "Babe (1995)",                                "Children|Drama"),
    (36, "Dead Man (1995)",                            "Drama|Western"),
    (39, "Clueless (1995)",                            "Comedy|Romance"),
    (47, "Seven (a.k.a. Se7en) (1995)",                "Mystery|Thriller"),
    (50, "Usual Suspects, The (1995)",                 "Crime|Mystery|Thriller"),
    (52, "Mighty Aphrodite (1995)",                    "Comedy|Drama|Romance"),
    (62, "Mr. Holland's Opus (1995)",                  "Drama"),
    (70, "From Dusk Till Dawn (1996)",                 "Action|Comedy|Horror|Thriller"),
    (110,"Braveheart (1995)",                          "Action|Drama|War"),
    (111,"Truth About Cats & Dogs, The (1996)",        "Comedy|Romance"),
    (112,"Rumble in the Bronx (1995)",                 "Action|Adventure|Comedy|Crime"),
    (117,"Young Frankenstein (1974)",                  "Comedy|Fantasy"),
    (151,"Rob Roy (1995)",                             "Action|Drama|Romance|War"),
    (153,"Batman Forever (1995)",                      "Action|Adventure|Comedy"),
    (157,"Canadian Bacon (1995)",                      "Comedy|War"),
    (161,"Crimson Tide (1995)",                        "Drama|Thriller|War"),
    (162,"Desperado (1995)",                           "Action|Crime|Thriller"),
    (163,"Desperately Seeking Susan (1985)",           "Comedy|Crime|Romance"),
    (165,"Die Hard: With a Vengeance (1995)",          "Action|Crime|Thriller"),
    (168,"First Knight (1995)",                        "Action|Drama|Romance"),
    (170,"Hackers (1995)",                             "Action|Crime|Thriller"),
    (172,"Johnny Mnemonic (1995)",                     "Action|Sci-Fi|Thriller"),
    (173,"Judge Dredd (1995)",                         "Action|Crime|Sci-Fi"),
    (176,"Kids (1995)",                                "Drama"),
    (181,"Return of the Pink Panther, The (1975)",     "Comedy|Crime|Mystery"),
    (183,"Roommates (1995)",                           "Drama"),
    (185,"Net, The (1995)",                            "Action|Crime|Thriller"),
    (186,"Blues Brothers, The (1980)",                 "Action|Comedy|Musical"),
    (187,"Kicking and Screaming (1995)",               "Comedy|Drama"),
    (188,"Mighty Morphin Power Rangers: The Movie (1995)", "Action|Adventure|Children"),
    (189,"Nadja (1994)",                               "Horror"),
    (193,"Showgirls (1995)",                           "Drama"),
    (194,"Smoke (1995)",                               "Drama"),
    (195,"Restoration (1995)",                         "Drama|Romance"),
    (196,"Species (1995)",                             "Horror|Sci-Fi"),
    (197,"Stars Fell on Henrietta, The (1995)",        "Drama|Western"),
    (198,"Strange Days (1995)",                        "Action|Crime|Drama|Mystery|Sci-Fi|Thriller"),
    (200,"Antonia's Line (1995)",                      "Drama"),
    (202,"I.Q. (1994)",                                "Comedy|Romance"),
    (203,"To Wong Foo, Thanks for Everything! (1995)", "Comedy|Drama"),
    (204,"Under Siege 2: Dark Territory (1995)",       "Action"),
    (205,"Unstrung Heroes (1995)",                     "Comedy|Drama"),
    (206,"Unzipped (1995)",                            "Documentary"),
    (207,"Strange Days (1995)",                        "Action|Crime|Drama|Mystery|Sci-Fi|Thriller"),
    (208,"Waterworld (1995)",                          "Action|Adventure|Sci-Fi"),
    (209,"White Man's Burden (1995)",                  "Drama|Sci-Fi|Thriller"),
    (210,"Apollo 13 (1995)",                           "Adventure|Drama|IMAX"),
    (211,"M*A*S*H (1970)",                             "Comedy|Drama|War"),
    (213,"Batman (1989)",                              "Action|Crime"),
    (215,"Before Sunrise (1995)",                      "Drama|Romance"),
    (216,"Billy Madison (1995)",                       "Comedy"),
    (217,"Birdcage, The (1996)",                       "Comedy"),
    (220,"Lawnmower Man 2 (1996)",                     "Action|Sci-Fi|Thriller"),
    (222,"Circle of Friends (1995)",                   "Drama|Romance"),
    (223,"Clerks (1994)",                              "Comedy"),
    (224,"Don Juan DeMarco (1994)",                    "Comedy|Drama|Romance"),
    (225,"Dolores Claiborne (1995)",                   "Drama|Mystery|Thriller"),
    (226,"Dream Man (1995)",                           "Crime|Romance|Thriller"),
    (227,"Drop Zone (1994)",                           "Action|Thriller"),
    (228,"Drop Dead Fred (1991)",                      "Comedy|Fantasy"),
    (229,"Ed Wood (1994)",                             "Comedy|Drama"),
    (230,"Exit to Eden (1994)",                        "Comedy"),
    (231,"Dumb & Dumber (1994)",                       "Adventure|Comedy"),
    (232,"Eat Drink Man Woman (1994)",                 "Drama|Romance"),
    (233,"Exotica (1994)",                             "Drama|Mystery"),
    (235,"Ed Wood (1994)",                             "Comedy|Drama"),
    (236,"Kolya (1996)",                               "Comedy|Drama"),
    (237,"Jerry Maguire (1996)",                       "Drama|Romance"),
    (238,"Raising Arizona (1987)",                     "Comedy|Crime"),
    (239,"Groundhog Day (1993)",                       "Comedy|Fantasy|Romance"),
    (240,"Pulp Fiction (1994)",                        "Comedy|Crime|Drama|Thriller"),
    (241,"Speed (1994)",                               "Action|Romance|Thriller"),
    (242,"Forrest Gump (1994)",                        "Comedy|Drama|Romance|War"),
    (243,"Shawshank Redemption, The (1994)",           "Crime|Drama"),
    (244,"Silence of the Lambs, The (1991)",           "Crime|Horror|Thriller"),
    (245,"Interview with the Vampire (1994)",          "Drama|Horror"),
    (246,"Schindler's List (1993)",                    "Drama|War"),
    (247,"Fargo (1996)",                               "Comedy|Crime|Drama|Thriller"),
    (248,"Courage Under Fire (1996)",                  "Drama|War"),
    (249,"Sleepers (1996)",                            "Drama|Thriller"),
    (250,"Fly Away Home (1996)",                       "Adventure|Children|Drama"),
    (253,"River Wild, The (1994)",                     "Action|Drama|Thriller"),
    (254,"Outbreak (1995)",                            "Action|Drama|Sci-Fi|Thriller"),
    (255,"Piano, The (1993)",                          "Drama|Romance"),
    (256,"Snow White and the Seven Dwarfs (1937)",     "Animation|Children|Drama|Fantasy|Musical"),
    (257,"Clerks (1994)",                              "Comedy"),
    (258,"Contact (1997)",                             "Drama|Sci-Fi"),
    (260,"Star Wars: Episode IV - A New Hope (1977)",  "Action|Adventure|Sci-Fi"),
    (261,"Little Women (1994)",                        "Drama"),
    (262,"Steel (1997)",                               "Action|Adventure"),
    (263,"Bulletproof (1996)",                         "Action|Comedy"),
    (265,"Like Water for Chocolate (1992)",            "Drama|Fantasy|Romance"),
    (266,"Kull the Conqueror (1997)",                  "Action|Adventure|Fantasy"),
    (267,"Touki Bouki (1973)",                         "Drama"),
    (268,"Chasing Amy (1997)",                         "Comedy|Drama|Romance"),
    (269,"Full Monty, The (1997)",                     "Comedy|Drama"),
    (270,"Mars Attacks! (1996)",                       "Action|Comedy|Sci-Fi"),
    (271,"Starship Troopers (1997)",                   "Action|Sci-Fi|Thriller"),
    (272,"Good Will Hunting (1997)",                   "Drama|Romance"),
    (273,"Face/Off (1997)",                            "Action|Crime|Drama|Sci-Fi|Thriller"),
    (274,"Ulee's Gold (1997)",                         "Drama"),
    (275,"Conspiracy Theory (1997)",                   "Action|Mystery|Romance|Thriller"),
    (276,"Air Bud (1997)",                             "Children|Comedy"),
    (278,"Anastasia (1997)",                           "Adventure|Animation|Children|Drama|Musical|Romance"),
    (280,"Amistad (1997)",                             "Drama"),
    (281,"Air Force One (1997)",                       "Action|Thriller"),
    (282,"G.I. Jane (1997)",                           "Action|Drama"),
    (283,"Hercules (1997)",                            "Adventure|Animation|Children|Comedy|Musical"),
    (284,"Mad City (1997)",                            "Drama|Thriller"),
    (285,"Liar Liar (1997)",                           "Comedy"),
    (286,"Flubber (1997)",                             "Children|Comedy|Fantasy|Sci-Fi"),
    (287,"As Good as It Gets (1997)",                  "Comedy|Drama|Romance"),
    (288,"Scream (1996)",                              "Horror|Mystery|Thriller"),
    (289,"Sprung (1997)",                              "Comedy"),
    (290,"Austin Powers: International Man of Mystery (1997)", "Action|Adventure|Comedy"),
    (292,"Guns of Navarone, The (1961)",               "Action|Adventure|Drama|War"),
    (293,"Star Wars: Episode VI - Return of the Jedi (1983)", "Action|Adventure|Sci-Fi"),
    (294,"Lolita (1962)",                              "Drama|Romance"),
    (295,"Breakdown (1997)",                           "Action|Drama|Thriller"),
    (296,"Pulp Fiction (1994)",                        "Comedy|Crime|Drama|Thriller"),
    (318,"Schindler's List (1993)",                    "Drama|War"),
    (329,"Star Trek: First Contact (1996)",            "Action|Adventure|Drama|Sci-Fi|Thriller"),
    (330,"James and the Giant Peach (1996)",           "Adventure|Animation|Children|Fantasy|Musical"),
    (333,"Tommy Boy (1995)",                           "Comedy"),
    (335,"Flintstones, The (1994)",                    "Children|Comedy|Fantasy"),
    (337,"What's Eating Gilbert Grape (1993)",         "Drama"),
    (338,"Bean (1997)",                                "Comedy"),
    (339,"Mad Max Beyond Thunderdome (1985)",          "Action|Adventure|Sci-Fi"),
    (340,"Boogie Nights (1997)",                       "Drama"),
    (344,"Ace Ventura: Pet Detective (1994)",          "Comedy"),
    (349,"Clear and Present Danger (1994)",            "Action|Crime|Drama|Thriller"),
    (353,"Craft, The (1996)",                          "Drama|Fantasy|Horror|Thriller"),
    (354,"Lawnmower Man, The (1992)",                  "Action|Sci-Fi|Thriller"),
    (356,"Forrest Gump (1994)",                        "Comedy|Drama|Romance|War"),
    (357,"Four Weddings and a Funeral (1994)",         "Comedy|Romance"),
    (359,"I Love Trouble (1994)",                      "Comedy|Romance|Thriller"),
    (360,"Leon: The Professional (1994)",              "Action|Crime|Drama|Thriller"),
    (362,"Jungle Book, The (1994)",                    "Adventure|Children|Romance"),
    (364,"Lion King, The (1994)",                      "Adventure|Animation|Children|Drama|Musical|IMAX"),
    (367,"Mask, The (1994)",                           "Action|Comedy|Crime|Fantasy"),
    (370,"Mixed Nuts (1994)",                          "Comedy"),
    (371,"Little Buddha (1993)",                       "Drama"),
    (372,"Clerks (1994)",                              "Comedy"),
    (377,"Speed (1994)",                               "Action|Romance|Thriller"),
    (378,"Monkey Trouble (1994)",                      "Adventure|Children|Comedy"),
    (379,"Timecop (1994)",                             "Action|Sci-Fi|Thriller"),
    (380,"True Lies (1994)",                           "Action|Adventure|Comedy|Romance|Thriller"),
    (381,"Muriel's Wedding (1994)",                    "Comedy|Romance"),
    (382,"Adventures of Priscilla, Queen of the Desert (1994)", "Comedy|Drama"),
    (383,"Maverick (1994)",                            "Action|Adventure|Comedy|Western"),
    (384,"Naked Gun 33 1/3: The Final Insult (1994)",  "Comedy|Crime"),
    (385,"Andre (1994)",                               "Adventure|Children|Drama"),
    (386,"Renaissance Man (1994)",                     "Comedy|Drama|War"),
    (387,"Client, The (1994)",                         "Crime|Drama|Mystery|Thriller"),
    (388,"Serial Mom (1994)",                          "Comedy|Crime|Horror"),
    (389,"Wolf (1994)",                                "Drama|Horror|Romance|Thriller"),
    (390,"Specialist, The (1994)",                     "Action|Drama|Romance|Thriller"),
    (391,"Jason's Lyric (1994)",                       "Crime|Drama|Romance|Thriller"),
    (392,"Baron Munchausen (1943)",                    "Adventure|Comedy|Fantasy"),
    (393,"Kill the Conqueror (1997)",                  "Action|Adventure|Fantasy"),
    (394,"Radioland Murders (1994)",                   "Comedy|Crime|Mystery|Romance|Thriller"),
    (395,"Miracle on 34th Street (1994)",              "Children|Drama|Fantasy|Romance"),
    (396,"Angels in the Outfield (1994)",              "Children|Comedy|Fantasy"),
    (410,"Addams Family Values (1993)",                "Children|Comedy|Fantasy"),
    (480,"Jurassic Park (1993)",                       "Action|Adventure|Sci-Fi|Thriller"),
    (527,"Schindler's List (1993)",                    "Drama|War"),
    (587,"Ghost (1990)",                               "Comedy|Drama|Fantasy|Mystery|Romance|Thriller"),
    (588,"Aladdin (1992)",                             "Adventure|Animation|Children|Comedy|Musical|Romance"),
    (589,"Terminator 2: Judgment Day (1991)",          "Action|Sci-Fi"),
    (590,"Dances with Wolves (1990)",                  "Adventure|Drama|Western"),
    (592,"Batman Returns (1992)",                      "Action|Crime"),
    (593,"Silence of the Lambs, The (1991)",           "Crime|Horror|Thriller"),
    (594,"Snow White and the Seven Dwarfs (1937)",     "Animation|Children|Drama|Fantasy|Musical"),
    (595,"Beauty and the Beast (1991)",                "Animation|Children|Fantasy|Musical|Romance|IMAX"),
    (596,"Pinocchio (1940)",                           "Animation|Children|Fantasy|Musical"),
    (597,"Pretty Woman (1990)",                        "Comedy|Romance"),
    (598,"Angels in the Outfield (1994)",              "Children|Comedy|Fantasy"),
    (606,"Groundhog Day (1993)",                       "Comedy|Fantasy|Romance"),
    (648,"Mission: Impossible (1996)",                 "Action|Adventure|Mystery|Sci-Fi|Thriller"),
    (660,"Independence Day (a.k.a. ID4) (1996)",       "Action|Adventure|Sci-Fi|Thriller"),
    (671,"Crimson Tide (1995)",                        "Drama|Thriller|War"),
    (736,"Twister (1996)",                             "Action|Adventure|Thriller"),
    (780,"Independence Day (a.k.a. ID4) (1996)",       "Action|Adventure|Sci-Fi|Thriller"),
]

# Remove duplicates (keep first occurrence by movieId)
seen_ids = set()
UNIQUE_MOVIES = []
for m in MOVIES:
    if m[0] not in seen_ids:
        seen_ids.add(m[0])
        UNIQUE_MOVIES.append(m)

GENRES = [
    "Action", "Adventure", "Animation", "Children", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
]

random.seed(42)


def generate_movies_csv():
    path = os.path.join(DATA_DIR, "movies.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["movieId", "title", "genres"])
        for movie_id, title, genres in UNIQUE_MOVIES:
            writer.writerow([movie_id, title, genres])
    print(f"Generated {len(UNIQUE_MOVIES)} movies → {path}")


def generate_ratings_csv():
    path = os.path.join(DATA_DIR, "ratings.csv")
    movie_ids = [m[0] for m in UNIQUE_MOVIES]
    rows = []
    timestamp_base = 964982703
    for user_id in range(1, 51):       # 50 users
        # Each user rates a random subset of 20–60 movies
        rated = random.sample(movie_ids, min(random.randint(20, 60), len(movie_ids)))
        for movie_id in rated:
            rating = round(random.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]), 1)
            timestamp = timestamp_base + random.randint(0, 10_000_000)
            rows.append([user_id, movie_id, rating, timestamp])

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["userId", "movieId", "rating", "timestamp"])
        for row in rows:
            writer.writerow(row)
    print(f"Generated {len(rows)} ratings  → {path}")


def main():
    movies_path = os.path.join(DATA_DIR, "movies.csv")
    ratings_path = os.path.join(DATA_DIR, "ratings.csv")

    if os.path.exists(movies_path) and os.path.exists(ratings_path):
        print("Dataset files already exist – skipping generation.")
        return

    generate_movies_csv()
    generate_ratings_csv()
    print("Sample dataset generation complete.")


if __name__ == "__main__":
    main()

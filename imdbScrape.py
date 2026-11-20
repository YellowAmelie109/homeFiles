import imdbinfo as imdb
# Fetch all episodes for a series
results = imdb.search_title("Manifest")
all_episodes = imdb.get_all_episodes(results.titles[0].imdb_id)
for episode in all_episodes:
    print(f"S{episode.season_number}E{episode.episode_number}: {episode.title}")

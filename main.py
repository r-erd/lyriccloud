from lyricsgenius import Genius
import pandas as pd
import os
import argparse
from cloud import create_wordcloud
import time
# get Genius API token from here: https://genius.com/api-clients


def load_songs(path):
    """
    Load songs from a CSV file.

    Args:
        path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the loaded songs, with columns 'Artist' and 'Song'.

    Raises:
        FileNotFoundError: If the specified file does not exist.

    """
    if os.path.isfile(path):
        return pd.read_csv(path, header=None, names=['Artist', 'Song'])
    else:
        raise FileNotFoundError(f"Error, {path} file not found")


def gather_lyrics(songs_df, token, output_path):
    """
    Gathers lyrics for songs from a given dataframe using the Genius API.

    Args:
        songs_df (pandas.DataFrame): A dataframe containing information about songs, including artist and song names.

    Returns:
        pandas.DataFrame: A dataframe containing the gathered lyrics for each song.

    """

    # Create an empty dataframe to store the results
    results_df = pd.DataFrame(columns=['Artist', 'Song', 'Lyrics'])

    start_time = time.time()

    # Initialize the results_df with the content of the results.csv, if it exists
    if os.path.isfile(output_path):
        print("Loading existing results from:", output_path)
        print("Continuing from the last checkpoint")
        results_df = pd.read_csv(output_path)

    # Initialize Genius API
    genius = Genius(token)

    # Sort the songs.csv dataframe by Artist
    songs_df = songs_df.sort_values(by='Artist')
    print("Sorted songs.csv by Artist")
    print(songs_df.head(10))


    # Iterate through each row in the songs dataframe

    artist_name = ""
    song_counter = 0
    for index, row in songs_df.iterrows():

        # Check if the artist-song pair already exists in the results dataframe
        if results_df[(results_df['Artist'] == row['Artist']) & (results_df['Song'] == row['Song'])].shape[0] > 0:
            print("Skipping: {} - {}".format(row['Artist'], row['Song']))
            continue

        # update artist reference to keep last artist
        last_artist = artist_name
        artist_name = row['Artist']
        song_name = row['Song']

        if not artist_name == last_artist:
            # reduce number of queries by caching artist reference
            print("Getting reference for artist: {}".format(artist_name))
            artist = genius.search_artist(artist_name, max_songs=1, sort="title")
            
        # Search for the song given the artist name
            
        if artist is not None:
            song = genius.search_song(song_name, artist.name)
        
        # If the song is found, add the artist, song, and lyrics to the results dataframe
        if song and song.lyrics is not None:
            results_df = pd.concat([results_df, pd.DataFrame({'Artist': [artist_name], 'Song': [song_name], 'Lyrics': [song.lyrics]})], ignore_index=True)

        song_counter += 1

        print("=====================================")
        print("Currently at song: {} - {}".format(artist_name, song_name))
        print("Total songs gathered so far:", results_df.shape[0])
        print("Time elapsed: {:.2f} seconds".format(time.time() - start_time))
        # Bug: something is not right with the percentage for some reason
        print("Percentage: {:.2f}%".format((song_counter + 1) / songs_df.shape[0] * 100))
        print("=====================================")

        # Checkpointing: save the results dataframe to a CSV file after every N songs
        if song_counter % 5 == 0:
            print("Saving results after {} songs".format(index))
            results_df.to_csv(output_path, index=False)

    return results_df


def main(input_path, output_path, token, create_cloud=False):
    songs_df = load_songs(input_path)
    results_df = gather_lyrics(songs_df, token, output_path)
    results_df.to_csv(output_path, index=False)

    if create_cloud:
        create_wordcloud(output_path, 'wordcloud.png')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gather lyrics from SoundCloud songs.')
    parser.add_argument('input_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_path', type=str, help='Path to the output CSV file')
    parser.add_argument('--token', type=str, help='Genius API token')
    parser.add_argument('--create_cloud', action='store_true', help='Create a word cloud from the gathered lyrics')
    args = parser.parse_args()

    parser.epilog = '''
    This script gathers lyrics from SoundCloud songs using the Genius API.
    If the --create_cloud flag is set, it will also generate a word cloud from the gathered lyrics.

    Example usage:
    python main.py songs.csv results.csv --create_cloud --token YOUR_TOKEN_HERE
    '''

    main(args.input_path, args.output_path, args.token, args.create_cloud)


    # IOnGnyc_soN4miiEfTIDv7VeAgIMxkjf8uoMIsDz6kf5CIF-_pObZNvbv8q7qZZQ
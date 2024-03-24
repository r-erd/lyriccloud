import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import argparse


def create_wordcloud(input_path, output_path):
    """
    Create a word cloud from the lyrics data in a CSV file.

    Args:
        input_path (str): The path to the input CSV file.
        output_path (str): The path to save the generated word cloud image.

    Returns:
        None
    """
    nltk.download('stopwords')
    nltk.download('wordnet')

    print("Reading data from:", input_path)
    df = pd.read_csv(input_path)

    # Collect all the content of the Lyrics column into a single string
    print("Combining lyrics data...")
    lyrics = ' '.join(df['Lyrics'].astype(str))

    # Remove custom special words
    lyrics = lyrics.replace('Verse', '')
    lyrics = lyrics.replace('Chorus', '')
    lyrics = lyrics.replace('Bridge', '')
    lyrics = lyrics.replace('Outro', '')
    lyrics = lyrics.replace('Embed', '')
    lyrics = lyrics.replace('album', '')
    lyrics = lyrics.replace('Remix', '')
    lyrics = lyrics.replace('ft', '')
    lyrics = lyrics.replace('Lyrics', '')

    # You could add code to remove artist names, song titles, or other specific words here

    # Remove stopwords (only works in lyrics are in mostly one language, not a mix of languages)
    #stop_words = set(stopwords.words('english'))
    #lyrics = ' '.join([word for word in lyrics.split() if word.lower() not in stop_words])

    # Apply lemmatization (also only works if lyrics are in one language)
    #lemmatizer = WordNetLemmatizer()
    #lyrics = ' '.join([lemmatizer.lemmatize(word) for word in lyrics.split()])

    print("Generating word cloud...")
    # other optional parameters: https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
    # other colormaps https://matplotlib.org/stable/users/explain/colors/colormaps.html

    wordcloud = WordCloud(width = 800,
                        height = 400, 
                        max_words = 1000,
                        prefer_horizontal = 1, 
                        max_font_size = 100,
                        scale = 5, 
                        colormap = "summer",
                        background_color = "black")
    
    wordcloud.generate(lyrics)

    wordcloud.to_file(output_path)
    print("Saved word cloud image to:", output_path)


def main():
    parser = argparse.ArgumentParser(description='Generate word cloud from lyrics data')
    parser.add_argument('input_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_path', type=str, help='Path to save the output word cloud image')

    parser.epilog = '''
    This script generates a word cloud from lyrics data stored in a CSV file.

    Example usage:
    python cloud.py gather_results.csv cloud.png
    '''

    args = parser.parse_args()

    create_wordcloud(args.input_path, args.output_path)

if __name__ == '__main__':
    main()
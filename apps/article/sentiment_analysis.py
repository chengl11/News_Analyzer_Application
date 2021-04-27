"""Demonstrates how to make a simple call to the Natural Language API."""

import argparse

from google.cloud import language_v1
# from google.cloud import language
# from google.cloud.language import enums
# from google.cloud.language import types

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "asymmetric-rite-290701-2ca06c55e9e8.json"

def print_result(annotations):
    result = []
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print(
            "Sentence {} has a sentiment score of {}".format(index, sentence_sentiment)
        )
        result.append("Sentence {} has a sentiment score of {}".format(index, sentence_sentiment))

    print(
        "Overall Sentiment: score of {} with magnitude of {}".format(score, magnitude)
    )
    result.append("Overall Sentiment: score of {} with magnitude of {}".format(score, magnitude))
    return result

def analyze(content):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language_v1.LanguageServiceClient()

    # with open(movie_review_filename, "r") as review_file:
    #     # Instantiates a plain text document.
    #     content = review_file.read()

    document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request={'document': document})

    # Print the results
    return print_result(annotations)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
#     )
#     parser.add_argument(
#         "movie_review_filename",
#         help="The filename of the movie review you'd like to analyze.",
#     )
#     args = parser.parse_args()

#     analyze(args.movie_review_filename)
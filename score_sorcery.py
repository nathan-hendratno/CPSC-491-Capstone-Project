# Python File that calculates the credibility score of an article, analyzing probability of AI using Sapling.
# Is not setup for async function calls or wrappers. Also requires the SAPLINGKEY to be included in the .env file.

from sapling import SaplingClient
import os

# construct a Credibility object in accordance with its constructor, then calculate_score. Once score has been calculated, get_explanation can be called for reasoning.

# Takes the article as a string and returns a score. Requires an API key from the .env.
def sorce(article_text='This is test text.'):
    api_key = os.getenv("SAPLINGKEY")
    # NEW: wrap in try/except so Sapling errors do not crash the whole app
    try:
        client = SaplingClient(api_key=api_key)
        detection_scores = client.aidetect(article_text, sent_scores=True)  # This is a dictionary, so it prints like one
        return detection_scores.get("score", 0)
    except Exception as e:
        print("Sapling error:", e)
        return 0

# Object that calculates the credibility score
class Credibility:
    def __init__(self, explanation='', article=None):
        self.score = 0                          # the total score as a number
        self.explanation = explanation          # the explanation as a string
        # NEW: use empty dict if no article is passed, prevents crashes
        self.article = article or {}           # the json from data

    # returns the total score as a number
    def get_score(self):
        return self.score

    # returns the explanation as a string
    def get_explanation(self):
        return self.explanation

    # calculates and returns the final score based on factors as a number
    def calculate_score(self):
        maximum = 100
        deduction = 0

        self.explanation = ""
        # NEW: safely pull values from the article dictionary
        # This fixes errors like article_text not defined / link_count not defined
        title = self.article.get("title", "(no title found)")
        author = self.article.get("author", "(no author found)")
        publish_date = self.article.get("publish_date", "(no publication date found)")
        link_count = self.article.get("link_count", 0)
        article_text = self.article.get("article_text", "")

        # Having a title is worth 10% of credibility
        if title == "(no title found)":
            self.explanation += "0/10 Title Missing\n"
            deduction += 10
        else:
            self.explanation += "10/10 Title present\n"

        # Having an author is worth 30% of credibility
        if author == "(no author found)":
            self.explanation += "0/30 Authorship missing\n"
            deduction += 30
        else:
            self.explanation += "30/30 Authorship present\n"

        # Having a publication date is worth 15% of credibility
        if publish_date == "(no publication date found)":
            self.explanation += "0/15 Publication date missing\n"
            deduction += 15
        else:
            self.explanation += "15/15 Publication date present\n"

        # Having at least 3 links (presumably citations) is worth 5% of credibility, on account of the links not necessarily being citations.
        if link_count < 3:
            self.explanation += "0/5 Not enough potential citation links\n"
            deduction += 5
        else:
            self.explanation += "5/5 Enough potential citation links present\n"

        # Chance of AI generation is worth 40% of credibility
        ai_gen = sorce(article_text)
        ai_deduction = (40 * ai_gen)
        deduction += ai_deduction
        # NEW: format nicely to 2 decimal places
        self.explanation += f"{40 - ai_deduction:.2f}/40 AI Detection\n"

        self.score = maximum - deduction

        # NEW: round final score for cleaner display
        self.score = round(self.score, 2)

        self.explanation += str(self.score) + "/100 Total Credibility Score"

        return self.score
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
    
    # NEW: returns structured score breakdown for frontend
    def get_score_breakdown(self):
        return self.score_breakdown

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
            title_earned = 0
            self.explanation += "✖ No clear title was found for this article.\n"
            deduction += 10
        else:
            title_earned = 10
            self.explanation += "✔ The article includes a clear and identifiable title.\n"

        # Having an author is worth 30% of credibility
        if author == "(no author found)":
            author_earned = 0
            self.explanation += "✖ No author information was found, which lowers credibility.\n"
            deduction += 30
        else:
            author_earned = 30
            self.explanation += "✔ The article provides author information.\n"

        # Having a publication date is worth 15% of credibility
        if publish_date == "(no publication date found)":
            date_earned = 0
            self.explanation += "✖ No publication date was found.\n"
            deduction += 15
        else:
            date_earned = 15
            self.explanation += "✔ A publication date is available.\n"

        # Having at least 3 links (presumably citations) is worth 5% of credibility, on account of the links not necessarily being citations.
        if link_count < 3:
            links_earned = 0
            self.explanation += "✖ Very few references or links were found in the article.\n"
            deduction += 5
        else:
            links_earned = 5
            self.explanation += "✔ The article contains multiple references or links.\n"

        # Chance of AI generation is worth 40% of credibility
        ai_gen = sorce(article_text)
        ai_deduction = (40 * ai_gen)
        deduction += ai_deduction
        ai_earned = round(40 - ai_deduction, 2)
        # NEW: format nicely to 2 decimal places
        if ai_gen < 0.3:
            self.explanation += "✔ The writing appears to be mostly human-generated.\n"
        elif ai_gen < 0.6:
            self.explanation += "⚠ The writing shows some signs of AI assistance.\n"
        else:
            self.explanation += "✖ The writing is likely AI-generated, reducing credibility.\n"

        self.score = maximum - deduction

        # NEW: round final score for cleaner display
        self.score = round(self.score, 2)
        if self.score < 0:
            self.score = 0

        # NEW: build structured breakdown object
        self.score_breakdown = {
            "title": {
                "earned": title_earned,
                "total": 10
            },
            "author": {
                "earned": author_earned,
                "total": 30
            },
            "date": {
                "earned": date_earned,
                "total": 15
            },
            "links": {
                "earned": links_earned,
                "total": 5
            },
            "ai": {
                "earned": ai_earned,
                "total": 40
            }
        }

        return self.score
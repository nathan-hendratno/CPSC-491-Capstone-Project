# Python File that calculates the credibility score of an article, analyzing probability of AI using Sapling.
# Is not setup for async function calls or wrappers. Also requires the SAPLINGKEY to be included in the .env file.

from sapling import SaplingClient

# construct a Credibility object in accordance with its constructor, then calculate_score. Once score has been calculated, get_explanation can be called for reasoning.

# Takes the article as a string and returns a score. Requires an API key from the .env.
def sorce(article_text='This is test text.'):
    api_key = str(SAPLINGKEY)
    client = SaplingClient(api_key=api_key)
    detection_scores = client.aidetect(article_text, sent_scores=True)  # This is a dictionary, so it prints like one
    return detection_scores["score"]

# Object that calculates the credibility score
class Credibility:
    def __init__(self, explanation='', article=dict):
        self.score = 0                          # the total score as a number
        self.explanation = explanation          # the explanation as a string
        self.article = article                  # the json from data

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

        # Having a title is worth 10% of credibility
        if self.article["title"] == "(no title found)":
            self.explanation += "0/10 Title Missing\n"
            deduction += 10
        else:
            self.explanation += "10/10 Title present\n"

        # Having an author is worth 30% of credibility
        if self.article["author"] == "(no author found)":
            self.explanation += "0/30 Authorship missing\n"
            deduction += 30
        else:
            self.explanation += "30/30 Authorship present\n"

        # Having a publication date is worth 15% of credibility
        if self.article["publish_date"] == "(no publication date found)":
            self.explanation += "0/15 Publication date missing\n"
            deduction += 15
        else:
            self.explanation += "15/15 Publication date present\n"

        # Having at least 3 links (presumably citations) is worth 5% of credibility, on account of the links not necessarily being citations.
        if self.article["link_count"] < 3:
            self.explanation += "0/5 Not enough potential citation links\n"
            deduction += 5
        else:
            self.explanation += "5/5 Enough potential citation links present\n"

        # Chance of AI generation is worth 40% of credibility
        ai_gen = sorce(str(self.article["article_text"]))
        ai_deduction = (40 * ai_gen)
        deduction += ai_deduction
        self.explanation += (str(40 - ai_deduction) + "/40 AI Detection\n")

        self.score = maximum - deduction
        self.explanation += str(self.score) + "/100 Total Credibility Score"

        return self.score
from langchain_groq import ChatGroq
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    # MessagesPlaceholder,
)
from langchain.chains.llm import LLMChain
from langchain_core.messages import SystemMessage, AIMessage  # , HumanMessage
from tweetai.prompts import tweeter_prompts
import tweepy
# import dotenv
import os
import random
import time
import arxiv
import pymupdf
from bs4 import BeautifulSoup


class Tweetai:
    def __init__(
        self,
        bearer_token,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
        groq_token,
        groq_model
    ):
        # dotenv.load_dotenv()

        # consumer_key, consumer_secret, access_token, access_token_secret, bearer_token, client_id, client_secret = (
        #     os.getenv("TWITTER_KEY"),
        #     os.getenv("TWITTER_SECRET"),
        #     os.getenv("TWITTER_ACCESS_TOKEN"),
        #     os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        #     os.getenv("TWITTER_BEARER"),
        #     os.getenv("TWITTER_CLIENT_ID"),
        #     os.getenv("TWITTER_CLIENT_SECRET"),
        # )

        self.client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        self.groq_client = ChatGroq(
            api_key=groq_token,  # os.environ.get("GROQ_TOKEN"),
            model=groq_model  # os.environ.get("GROQ_MODEL")
        )

        self.arxiv_client = arxiv.Client()

    def post_tweet(self, tweet):
        self.client.create_tweet(text=tweet)
        print("Tweet posted successfully!")

    def generate_tweet(
        self,
        human_message=tweeter_prompts["tweeter_programming"]["user"],
        system_message=tweeter_prompts["tweeter_programming"]["system"],
        ai_message="Here is the short tweet in the style of Paul Graham:"
    ):

        prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(
                    content=system_message,
                ),
                # MessagesPlaceholder(
                #     variable_name="chat_history",
                # ),
                HumanMessagePromptTemplate.from_template(
                    "{human_message}"
                ),
                AIMessage(
                    content=ai_message,
                )
            ]
        )

        conversation = LLMChain(
            llm=self.groq_client,
            prompt=prompt,
            verbose=False,
            # memory=memory,
        )

        tweet = conversation.predict(human_message=human_message)
        # remove quotes
        tweet = tweet.replace('"', '')
        print(tweet)
        return tweet

    def post_thread(self, thread):
        # with open("tweets.txt", "a") as f:
        #     for tweet in thread:
        #         f.write(tweet + "\n")

        previous_tweet = None
        for tweet in thread:
            if previous_tweet:
                # Reply to the previous tweet in the thread
                status = self.client.create_tweet(
                    text=tweet, in_reply_to_tweet_id=previous_tweet.data['id']
                )
            else:
                # First tweet in the thread
                status = self.client.create_tweet(text=tweet)

            # Update previous_tweet to the current one for the next iteration
            previous_tweet = status
            # Optional: Add a small delay to avoid rate limiting
            time.sleep(random.uniform(1, 2))

        print("Thread posted successfully!")

    def pick_and_get_paper(
            self,
            topics=[
            "Quantum Computing",
            "Distributed Systems"
            "Artificial Intelligence",
            "Reinforcement Learning",
            "Agents",
            "Networking",
            "Operating Systems",
            "Blockchain",
            "Cloud Computing",
            "Machine Learning",
            "Augmented Reality",
            "Virtual Reality",
            "Robotics",
        ]
    ):
        # pick a random topic
        topic = random.choice(topics)

        # Search for the 10 most relevant articles matching the topic
        search = arxiv.Search(
            query=topic,
            max_results=1,
            sort_by=arxiv.SortCriterion.Relevance
        )

        # load previous paper titles from file
        try:
            with open("papers.txt", "r") as f:
                previous_papers = set(f.readlines())
        except FileNotFoundError:
            previous_papers = set()

        # get top paper not in previous papers
        top = next(self.arxiv_client.results(search))

        while top.title in previous_papers:
            top = next(self.arxiv_client.results(search))

        # save paper title to file
        try:
            with open("papers.txt", "a") as f:
                f.write(top.title + "\n")
        except FileNotFoundError:
            with open("papers.txt", "w") as f:
                f.write(top.title + "\n")
        
        if not os.path.exists("./papers"):
            os.makedirs("./papers")
        path = top.download_pdf(dirpath="./papers")

        doc = pymupdf.open(path)  # open a document
        content = ""
        for page in doc:  # iterate the document pages
            content += page.get_text()

        return Paper(top.title, top.summary, content, top.entry_id)

    def generate_paper_thread(
            self,
            human_message=None,
            system_message=tweeter_prompts["tweeter_paper"]["system"],
    ):

        paper = self.pick_and_get_paper()

        # tweeter_prompts["tweeter_paper"]["user"]
        
        if human_message is None:
            human_message = paper.text_content

        prompt = ChatPromptTemplate(
            messages=[
                SystemMessage(
                    content=system_message,
                ),
                # MessagesPlaceholder(
                #     variable_name="chat_history",
                # ),
                HumanMessagePromptTemplate.from_template(
                    "{human_message}"
                ),
                AIMessage(
                    content="Here is the tweet thread: <tweet>",
                )
            ]
        )

        conversation = LLMChain(
            llm=self.groq_client,
            prompt=prompt,
            verbose=False,
            # memory=memory,
        )

        tweet = "<tweet>" + conversation.predict(human_message=human_message)
        # remove quotes
        # tweet = tweet.replace('"', '')
        thread = []

        # get separate tweets in <tweet> </tweet> tags
        # Parse the HTML
        soup = BeautifulSoup(tweet, 'html.parser')

        # Find all occurrences of <tweet> and extract their text
        tweets = soup.find_all('tweet')

        # Extract content from each <tweet> tag separately
        for tweet in tweets:
            thread.append(tweet.text)

        thread.append(f"This was a thread on {paper.title}: {paper.entry_id}")

        return thread


class Paper:
    def __init__(self, title, summary, text_content, entry_id):
        self.title = title
        self.summary = summary
        self.text_content = text_content
        self.entry_id = entry_id

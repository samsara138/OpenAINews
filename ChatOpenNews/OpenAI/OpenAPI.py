import json
import openai


class OpenAI:

    def __init__(self, sepytttings, OpenAIAPIKey):
        self.api_key = ""
        self.settings = None
        self.settings = settings
        self.api_key = OpenAIAPIKey
        openai.api_key = self.api_key

    def process_article(self, article):
        # create a response from GPT3 based on news content
        if article["raw_content"]:
            raw_content = article["raw_content"] + "\n\nTl;dr"
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=raw_content,
                temperature=self.settings["ModelSettings"]["temperature"],
                max_tokens=int(self.settings["ModelSettings"]["max_tokens"]),
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=1
            )
            response = self.translate(response)
            article["concentrate"] = response
        article["translated_title"] = self.translate(article["title"])

    def translate(self, text):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Translate this into {self.settings['TargetLanguage']}:\n\n{text}\n\n",
            temperature=0.5,
            max_tokens=int(self.settings["ModelSettings"]["max_tokens"] * 1.5),
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].text.strip()

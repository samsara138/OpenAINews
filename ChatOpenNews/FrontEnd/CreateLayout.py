import json
import datetime


class HTMLMaker:
    settings = None

    def __init__(self, setting_file_name):
        with open(setting_file_name) as file:
            self.settings = json.load(file)

    def create_entry(self, article):
        if "concentrate" not in article:
            return ""

        title = article["translated_title"]
        content = article["concentrate"]
        source = article["source"]
        publish_date = article["publish_date"]
        url = article["url"]

        image_html = ""
        if article["image"] is not None:
            image_html = f'''<img src={article["image"]} style="max-width:90%;display: block; margin-left: auto; margin-right: auto">'''

        entry = f'''
<div style="height: 20px;"></div>
<div style="border-style: solid;width: 500px;height: auto; min-height: 100px;border-color: {self.settings["Colors"]["BoxColor"]}; margin: auto; padding: 30px;">
    <a href = {url} style="text-decoration: none;">
        <b style="font-family: {self.settings["Fonts"]["HeaderFont"]}; font-size: large; color: {self.settings["Colors"]["HeaderColor"]};">{title}</b>
    </a>
    <p style="font-family: {self.settings["Fonts"]["TextFont"]}; font-size: small; color: {self.settings["Colors"]["TextColor"]};">{source}</p>
    <p style="font-family: {self.settings["Fonts"]["TextFont"]}; font-size: medium;color: {self.settings["Colors"]["TextColor"]};">{content}</p>
    {image_html}
    <p style="font-family: {self.settings["Fonts"]["TextFont"]}; font-size: small; color: {self.settings["Colors"]["TextColor"]};">{publish_date}</p>
</div>

        '''
        return entry

    def create_body(self):
        timezone = datetime.timezone(datetime.timedelta(hours=-8))
        now = datetime.datetime.now(timezone)
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        body = f'''
<!DOCTYPE html>
<head>
    <meta charset="utf-8">
</head>
<body style="background-color:{self.settings["Colors"]["BackgroundColor"]};">
<p> Welcome to OpenVictoriaNews, this page is created at {formatted_time}</p>
'''
        return body

    @staticmethod
    def create_ending():
        end = f'''
<div style="height: 20px;"></div>
</body>
'''
        return end

    def create_html(self, articles: list, output_file_name="News.html"):
        content = ""
        content += self.create_body()
        for article in articles:
            content += self.create_entry(article)
        content += self.create_ending()
        with open(output_file_name, "w", encoding="utf-8") as file:
            file.write(content)

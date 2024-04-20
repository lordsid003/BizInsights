from flask import Blueprint, render_template, request
import google.generativeai as genai
from .keys import GOOGLE_API_KEY

model = Blueprint("model", __name__)

genai.configure(api_key=GOOGLE_API_KEY)
generation_configuration = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 1500
}

textModel = genai.GenerativeModel("gemini-pro", generation_config=generation_configuration)

def stringify(sentence: str) -> list:
    responseList = []
    word = ""
    for chunk in sentence:
        if(chunk == '\n' or chunk == '*'):
                if(word != "" or word != " "):
                    word = word.replace('-', '')
                    responseList.append(word)
                    word = ""
        else:
            word += chunk
    return responseList

@model.route("/model", methods=["GET", "POST"])
def idea_maker():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        tagline = f"Generate exactly 6 taglines in points only for {prompt}."
        competitors = f"Give 5 top competitor companies in points for this idea: {prompt}."
        market = f"Give 5 exactly effective advertisement without headings in points for {prompt}."
        domain = f"Give exactly 5 available domain names in points for: {prompt}."
        strategies = f"Give exactly 5 marketing strategies without headings in points for: {prompt}."

        tagline = textModel.generate_content([tagline])
        competitors = textModel.generate_content([competitors])
        market = textModel.generate_content([market])
        domain = textModel.generate_content([domain])
        strategies = textModel.generate_content([strategies])

        taglineList = stringify(tagline.text)
        competitorsList = stringify(competitors.text)
        marketList = stringify(market.text)
        domainList = stringify(domain.text)
        strategiesList = stringify(strategies.text)

        data = {
            "prompt": prompt,
            "response": {
                "Tagline": taglineList,
                "Competitors": competitorsList,
                "Advertisement Info": marketList,
                "Available Domains": domainList,
                "Business Strategies": strategiesList
            }
        }

        return render_template("idea_maker_response.html", data=data)

    else:
        return render_template("idea_maker.html")


@model.route("/pitch", methods=["GET", "POST"])
def pitch():
    questions = [
        "What do you understand by B2C business model. Does your Business plan incorporate this model? ",
        "What's your unique selling proposition?",
        "How big is your target market?",
        "What sets you apart from competitors?"
    ]
    if request.method == "POST":
        prompt = request.form.get("prompt")
        modifiedPrompt = f"Give answer in 5 bullet points: check the effectiveness of the pitch: {prompt} based on the given set of questions: {questions} and give a rating out of 10."
        response = textModel.generate_content([modifiedPrompt])
        response = stringify(response.text)
        data = {
            "Pitch": prompt,
            "Analysis": response}
        return render_template("mentor_results.html", data=data)
    else: 
        return render_template("mentor.html", ques=questions)


     


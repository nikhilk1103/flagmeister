from dotenv import load_dotenv
from flask import Flask, request, render_template
import google.generativeai as genai
import requests
import random
import os

app = Flask(__name__)

load_dotenv('api.env')
api_key = os.getenv('API_KEY')

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# List of country cca3 codes
country_codes = [
    "AFG", "ALB", "DZA", "ASM", "AND", "AGO", "AIA", "ATA", "ATG", "ARG",
    "ARM", "ABW", "AUS", "AUT", "AZE", "BHS", "BHR", "BGD", "BRB", "BLR",
    "BEL", "BLZ", "BEN", "BMU", "BTN", "BOL", "BES", "BIH", "BWA", "BVT",
    "BRA", "IOT", "BRN", "BGR", "BFA", "BDI", "CPV", "KHM", "CMR", "CAN",
    "CYM", "CAF", "TCD", "CHL", "CHN", "CXR", "CCK", "COL", "COM", "COG",
    "COD", "COK", "CRI", "CIV", "HRV", "CUB", "CUW", "CYP", "CZE", "DNK",
    "DJI", "DMA", "DOM", "ECU", "EGY", "SLV", "GNQ", "ERI", "EST", "SWZ",
    "ETH", "FLK", "FRO", "FJI", "FIN", "FRA", "GUF", "PYF", "ATF", "GAB",
    "GMB", "GEO", "DEU", "GHA", "GIB", "GRC", "GRL", "GRD", "GLP", "GUM",
    "GTM", "GGY", "GIN", "GNB", "GUY", "HTI", "HMD", "VAT", "HND", "HKG",
    "HUN", "ISL", "IND", "IDN", "IRN", "IRQ", "IRL", "IMN", "ISR", "ITA",
    "JAM", "JPN", "JEY", "JOR", "KAZ", "KEN", "KIR", "PRK", "KOR", "KWT",
    "KGZ", "LAO", "LVA", "LBN", "LSO", "LBR", "LBY", "LIE", "LTU", "LUX",
    "MAC", "MDG", "MWI", "MYS", "MDV", "MLI", "MLT", "MHL", "MTQ", "MRT",
    "MUS", "MYT", "MEX", "FSM", "MDA", "MCO", "MNG", "MNE", "MSR", "MAR",
    "MOZ", "MMR", "NAM", "NRU", "NPL", "NLD", "NCL", "NZL", "NIC", "NER",
    "NGA", "NIU", "NFK", "MKD", "MNP", "NOR", "OMN", "PAK", "PLW", "PSE",
    "PAN", "PNG", "PRY", "PER", "PHL", "PCN", "POL", "PRT", "PRI", "QAT",
    "ROU", "RUS", "RWA", "REU", "BLM", "SHN", "KNA", "LCA", "MAF", "SPM",
    "VCT", "WSM", "SMR", "STP", "SAU", "SEN", "SRB", "SYC", "SLE", "SGP",
    "SXM", "SVK", "SVN", "SLB", "SOM", "ZAF", "SGS", "SSD", "ESP", "LKA",
    "SDN", "SUR", "SJM", "SWE", "CHE", "SYR", "TWN", "TJK", "TZA", "THA",
    "TLS", "TGO", "TKL", "TON", "TTO", "TUN", "TUR", "TKM", "TCA", "TUV",
    "UGA", "UKR", "ARE", "GBR", "USA", "UMI", "URY", "UZB", "VUT", "VEN",
    "VNM", "VGB", "VIR", "WLF", "ESH", "YEM", "ZMB", "ZWE"
]

@app.route('/', methods=['GET', 'POST'])
def flag_game():
    if request.method == 'POST':
        print("POST request received")
        user_country = request.form.get('usercountry', '').strip().lower()
        user_capital = request.form.get('usercapital', '').strip().lower()
        actual_country = request.form.get('actual_country', '').strip().lower()
        actual_capital = request.form.get('actual_capital', '').strip().lower()
        country_proper = request.form.get('country_proper','')
        capital_proper = request.form.get('capital_proper','')

        print(f"user_country: {user_country}, actual_country: {actual_country}")
        print(f"user_capital: {user_capital}, actual_capital: {actual_capital}")

        if (user_country == actual_country):
            country_correct = (user_country == actual_country)
        else:
            aicountry = model.generate_content(f'i am using your response for a game where the user has to guess the name of the country when presented with a flag, and guess the name of the capital after that. i will give you the users response and the actual answer. your job is to consider any sort of natural human error in typing the response and still consider it as correct. make sure its not too much of a reach, but use your intelligence to gauge whether the user knows the answer or not. minor spelling mistakes are also acceptable, missing accents, capitalization, etc. are all acceptable. if the answer is correct, respond only with "true", otherwise respond with the "false". for example, if correct_answer = "Port-aux-Français" and user_answer = "port au francais", even though the exact strings are different, the users answer is semantically correct, so the response would be "Port-aux-Français". but if correct_answer = "Port-aux-Français" and user_answer = "port au prince", then its clearly wrong and your response would be "port au prince". lets try it now, here we go: correct_answer = "{actual_country}", user_answer = "{user_country}"').candidates[0].content.parts[0].text.strip()
            country_correct = (aicountry == "true")
        print(country_correct)

        if (user_capital == actual_capital):
            capital_correct = (user_capital == actual_capital)
        else:
            aicapital = model.generate_content(f'i am using your response for a game where the user has to guess the name of the country when presented with a flag, and guess the name of the capital after that. i will give you the users response and the actual answer. your job is to consider any sort of natural human error in typing the response and still consider it as correct. make sure its not too much of a reach, but use your intelligence to gauge whether the user knows the answer or not. minor spelling mistakes are also acceptable, missing accents, capitalization, etc. are all acceptable. if the answer is correct, respond only with "true", otherwise respond with the "false". for example, if correct_answer = "Port-aux-Français" and user_answer = "port au francais", even though the exact strings are different, the users answer is semantically correct, so the response would be "Port-aux-Français". but if correct_answer = "Port-aux-Français" and user_answer = "port au prince", then its clearly wrong and your response would be "port au prince". lets try it now, here we go: correct_answer = "{actual_capital}", user_answer = "{user_capital}"').candidates[0].content.parts[0].text.strip()
            capital_correct = (aicapital == "true")
        print(capital_correct)

        if 'usercapital' in request.form:
            # User has guessed the capital
            print(country_correct, capital_correct)
            return render_template("index.html", 
                                   country_correct=country_correct, 
                                   capital_correct=capital_correct,
                                   actual_country=actual_country,
                                   actual_capital=actual_capital,
                                   country_proper=country_proper,
                                   capital_proper=capital_proper,
                                   flag_url=request.form.get('flag_url'))
        else:
            # User has just guessed the country
            print(country_correct, capital_correct)
            return render_template("index.html", 
                                   user_country = user_country,
                                   country_correct=country_correct, 
                                   capital_correct=None,
                                   actual_country=actual_country,
                                   actual_capital=actual_capital,
                                   country_proper=country_proper,
                                   capital_proper=capital_proper,
                                   flag_url=request.form.get('flag_url'))

    elif request.method == 'GET':
        print("GET request received")
        selected_country_code = random.choice(country_codes)
        country_response = requests.get(f"https://restcountries.com/v3.1/alpha/{selected_country_code}")
        country_data = country_response.json()[0]
        country_proper = country_data.get('name', {}).get('common')
        country_name = country_data.get('name', {}).get('common').lower()
        capital = country_data.get('capital', [None])[0]
        flag_url = country_data.get('flags', {}).get('png')
        country_correct = None
        capital_correct = None

        print(f"Selected country: {country_name}, Capital: {capital}")

        return render_template("index.html", 
                               flag_url=flag_url, 
                               actual_country=country_name, 
                               actual_capital=capital, 
                               country_correct=country_correct, 
                               capital_correct=capital_correct,
                               country_proper = country_proper,
                               capital_proper = capital)

app.run()

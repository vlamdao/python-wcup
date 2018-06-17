import json
import requests
from datetime import date, datetime
import pytz
import texttable
import sys

tz = pytz.timezone('Asia/Ho_Chi_Minh')

URL = "http://api.football-data.org/"
current_season = 2018
headers = {
    "X-Auth-Token": "14c82fcc05f14df483676b5edd94c555",
    "X-Response-Control": "minified"
}

def get_wc_from_competitions_list(competitions):
    for competition in competitions.json():
        if ("World Cup " + str(current_season)) in competition["caption"]:
            return competition
    return None

def get_competitions_list():
    competitions = requests.get(URL + "v1/competitions/?season=" + str(current_season), headers=headers)
    return competitions
    
def get_fixture_of_competition_with_matchday(competition_id, matchday):
    fixture = requests.get(URL + "v1/competitions/{0}/fixtures?matchday={1}".format(competition_id, matchday))
    return fixture

def get_fixture_of_competition(competition_id):
    fixture = requests.get(URL + "v1/competitions/{0}/fixtures".format(competition_id))
    return fixture

def load_local_datetime_of_matchdate(matchdate):
    match_date = datetime.strptime(matchdate, "%Y-%m-%dT%H:%M:%SZ")
    local_match_date = pytz.utc.localize(match_date, is_dst=None).astimezone(tz)
    return local_match_date

def get_date_check(date_check=None):
    today = date.today()
    if not date_check:
        date_check_obj = today
    if date_check == "today":
        date_check_obj = today
    elif date_check == "tomorrow":
        date_check_obj = date(today.year, today.month, today.day + 1)
    elif date_check == "yesterday":
        date_check_obj = date(today.year, today.month, today.day - 1)
    return date_check_obj

def contruct_score_table(fixtures, date_check):
    table = texttable.Texttable()
    table.set_cols_align(["c", "c", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m"])
    table.header(["Time", "Home Team", "Away Team", "Status"])
    for fixture in fixtures["fixtures"]:
        match_datetime = load_local_datetime_of_matchdate(fixture["date"])
        if date_check == match_datetime.date():
            table.add_row([match_datetime.strftime("%H:%M %d/%m/%Y"),
                            fixture["homeTeamName"] + "\n" + "-----" + "\n" + str(fixture["result"]["goalsHomeTeam"]),
                            fixture["awayTeamName"] + "\n" + "-----" + "\n" + str(fixture["result"]["goalsAwayTeam"]),
                            fixture["status"]
                            ])
    return table

def main(arg):
    if arg in ["today", "tomorrow", "yesterday"]:
        print("Getting {0} World Cup scores ... \n".format(arg))
        competitions = get_competitions_list()
        current_wc = get_wc_from_competitions_list(competitions)
        if current_wc:
            fixtures = get_fixture_of_competition(current_wc['id']).json()
            table = contruct_score_table(fixtures, get_date_check(arg))
                    # print(json.dumps(fixture, indent=4))
            print(table.draw())
        else:
            print("There isn't any World Cup at this time.")
    else:
        print("Usage: wcup [day] where day can be 'yesterday', 'today' or 'tomorrow'.")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: wcup [day] where day can be 'yesterday', 'today' or 'tomorrow'.")
    else:
        main(sys.argv[1])
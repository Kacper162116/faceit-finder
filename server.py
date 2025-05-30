from flask import Flask, jsonify, request
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
app = Flask(__name__)
load_dotenv()
# Konfiguracja API
FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
headers = {"Authorization": f"Bearer {FACEIT_API_KEY}"}


def get_steam_id64_from_vanity(vanity_id):
    try:
        response = requests.get(
            f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl={vanity_id}")
        data = response.json()
        return data['response']['steamid'] if data['response']['success'] == 1 else None
    except Exception:
        return None


def get_faceit_data(steam_id64):
    try:
        response = requests.get(f"https://open.faceit.com/data/v4/players?game=cs2&game_player_id={steam_id64}",
                                headers=headers)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None


def get_player_stats(player_id):
    try:
        response = requests.get(f"https://open.faceit.com/data/v4/players/{player_id}/stats/cs2", headers=headers)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None


def get_steam_avatar(steam_id64):
    try:
        response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id64}")
        data = response.json()
        players = data.get('response', {}).get('players', [])
        return players[0].get('avatarfull') if players else None
    except Exception:
        return None


def get_steam_account_status(steam_id64):
    try:
        response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id64}")
        data = response.json()
        players = data.get('response', {}).get('players', [])
        if players:
            visibility = players[0].get('communityvisibilitystate', 1)
            return "Publiczne" if visibility == 3 else "Prywatne"
        return "Brak danych"
    except Exception:
        return "Brak danych"


def get_steam_account_creation_date(steam_id64):
    try:
        response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id64}")
        data = response.json()
        players = data.get('response', {}).get('players', [])
        if players:
            timecreated = players[0].get('timecreated')
            if timecreated:
                return datetime.utcfromtimestamp(timecreated).strftime('%Y-%m-%d')
        return "Brak danych"
    except Exception:
        return "Brak danych"


def get_steam_cs2_hours(steam_id64):
    try:
        response = requests.get(
            f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id64}&include_played_free_games=1")
        data = response.json()
        games = data.get('response', {}).get('games', [])
        for game in games:
            if game.get('appid') == 730:
                return round(game.get('playtime_forever', 0) / 60, 2)
        return 0
    except Exception:
        return None


def get_steam_cs2_hours_last_2weeks(steam_id64):
    try:
        response = requests.get(
            f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id64}")
        data = response.json()
        games = data.get('response', {}).get('games', [])
        for game in games:
            if game.get('appid') == 730:
                return round(game.get('playtime_2weeks', 0) / 60, 2)
        return None
    except Exception:
        return None


def get_faceit_level(elo):
    try:
        elo = int(elo)
        if elo < 501:
            return 1
        elif elo <= 750:
            return 2
        elif elo <= 900:
            return 3
        elif elo <= 1050:
            return 4
        elif elo <= 1150:
            return 5
        elif elo <= 1300:
            return 6
        elif elo <= 1500:
            return 7
        elif elo <= 1700:
            return 8
        elif elo <= 2000:
            return 9
        return 10
    except:
        return "brak danych"


def get_steam_friends(steam_id64):
    try:
        response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={STEAM_API_KEY}&steamid={steam_id64}&relationship=friend")
        friend_data = response.json()
        friends = friend_data.get('friendslist', {}).get('friends', [])
        ids = ','.join(friend['steamid'] for friend in friends[:100])

        if not ids:
            return []

        summary_response = requests.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={ids}")
        summary_data = summary_response.json()
        return summary_data.get('response', {}).get('players', [])
    except Exception:
        return []


@app.route('/api/player', methods=['GET'])
def get_player_stats_api():
    steam_url = request.args.get('steam_url')

    if not steam_url:
        return jsonify({"error": "Brak URL Steam"}), 400

    if "steamcommunity.com/id/" in steam_url:
        vanity_id = steam_url.split("steamcommunity.com/id/")[1].strip("/")
        steam_id64 = get_steam_id64_from_vanity(vanity_id)
    elif "steamcommunity.com/profiles/" in steam_url:
        steam_id64 = steam_url.split("steamcommunity.com/profiles/")[1].strip("/")
    else:
        return jsonify({"error": "Nieprawidłowy format URL"}), 400

    if not steam_id64:
        return jsonify({"error": "Nie znaleziono gracza"}), 404

    steam_profile_url = f"https://steamcommunity.com/profiles/{steam_id64}"
    faceit_data = get_faceit_data(steam_id64)

    if not faceit_data:
        return jsonify({"error": "Brak profilu Faceit"}), 404

    try:
        player_id = faceit_data['player_id']
        response_data = {
            "nick": faceit_data['nickname'],
            "elo": faceit_data['games']['cs2']['faceit_elo'],
            "level": get_faceit_level(faceit_data['games']['cs2']['faceit_elo']),
            "stats": get_player_stats(player_id),
            "hours_played": get_steam_cs2_hours(steam_id64),
            "hours_2weeks": get_steam_cs2_hours_last_2weeks(steam_id64),
            "steam_status": get_steam_account_status(steam_id64),
            "steam_creation": get_steam_account_creation_date(steam_id64),
            "avatar_url": get_steam_avatar(steam_id64),
            "friends": get_steam_friends(steam_id64),
            "steam_profile_url": steam_profile_url
        }
        return jsonify(response_data)
    except KeyError as e:
        return jsonify({"error": f"Brak danych: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
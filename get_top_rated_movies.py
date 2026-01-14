import shlex
import sys
from argparse import ArgumentParser
import requests
from token import token

root_parser = ArgumentParser(prog='TMDB')
command_parser = root_parser.add_subparsers(dest='command')
tmdb_app_parser = command_parser.add_parser('tmdb-app')
tmdb_app_parser.add_argument('--type',
                             choices=['playing', 'popular', 'top', 'upcoming'],
                             help="Movie's type")

while True:
    user_input = input("Enter your command: ")
    cmd_args = shlex.split(user_input)
    args = root_parser.parse_args(cmd_args)

    if args.command in ['exit', 'quit']:
        sys.exit(0)

    if args.command == 'tmdb-app':
        url = "https://api.themoviedb.org/3/movie/now_playing"
        if args.type == 'popular':
            url = "https://api.themoviedb.org/3/movie/popular"
        elif args.type == 'top':
            url = "https://api.themoviedb.org/3/movie/top_rated"
        elif args.type == 'upcoming':
            url = "https://api.themoviedb.org/3/movie/upcoming"

        headers = {
            "Authorization": f"Bearer {token}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            result = []
            for movie in data['results']:
                result.append(
                    {
                        'title': movie['title'],
                        'rate': movie['vote_average']
                    }
                )

            print(result)
        except requests.exceptions.ConnectionError:
            print('Network error, check your internet connection')
        except requests.exceptions.HTTPError as err:
            print(f"TMDB API error: {err}")




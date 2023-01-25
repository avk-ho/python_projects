# https://www.programmingexpert.io/projects/tournament-game-generator

# receive the number of teams (must be even, min 2)
# receive the name of each team (max 2 words, min 2 characters)
# each team plays at least every other team once (ask for input)
# ask for each team regular season wins (min 0, max num of games)
# then team with most wins faces team with less wins, the second most vs second less...

def tournament_game_generator():
    nb_teams = get_number_of_teams()
    team_names = get_team_names(nb_teams)
    nb_games = get_number_of_games(nb_teams)
    teams = get_number_of_wins_per_team(team_names, nb_games)
    generate_first_round(teams)


# returns a valid number of teams
def get_number_of_teams():
    while True:
        nb_teams = input("Enter the number of teams in the tournament: ")

        if nb_teams.isdigit():
            nb_teams = int(nb_teams)
            if nb_teams >= 2:
                if nb_teams % 2 == 0:
                    return nb_teams
                else:
                    print("The number of teams must be even, try again.")
            else:
                print("The minimum number of teams is 2, try again.")
        else:
            print("The number of teams must be a number, try again.")


# takes the number of teams, returns a list containing the team names
def get_team_names(nb_teams):
    team_num = 1
    team_names = []
    while team_num <= nb_teams:
        team_name = input(f"Enter the name for team #{team_num}: ")
        team_name = team_name.strip()

        if len(team_name) < 2:
            print("Team names must have at least 2 characters, try again.")
            continue

        if team_name.count(" ") > 1:
            print("Team names may have at most 2 words, try again.")
            continue

        team_names.append(team_name)
        team_num += 1

    return team_names


# takes the number of teams, returns a valid number of games per team
def get_number_of_games(nb_teams):
    while True:
        nb_games = input("Enter the number of games played by each team: ")

        if nb_games.isdigit():
            nb_games = int(nb_games)
            if nb_games >= nb_teams - 1:
                return nb_games
            else:
                print("Invalid number of games. Each team plays each other at least once in the regular season, try again.")
        else:
            print("The number of games must be a number, try again.")


# takes a list of team names, and the number of games, returns a dict of team_name:wins pairs
def get_number_of_wins_per_team(team_names, nb_games):
    teams = {}
    for team_name in team_names:
        valid_nb_wins = False

        while not valid_nb_wins:
            nb_wins = input(f"Enter the number of wins Team {team_name} had: ")
            if nb_wins.isdigit():
                nb_wins = int(nb_wins)
                if 0 <= nb_wins:
                    if nb_wins <= nb_games:
                        valid_nb_wins = True
                    else:
                        print(f"The maximum number of wins is {nb_games}, try again.")
                else:
                    print("The minimum number of wins is 0, try again.")
            else:
                print("The number of wins must be a number, try again.")

        teams[team_name] = nb_wins
    return teams


# takes a dict of team_name:wins pairs, returns a sorted (desc wins) list of team names
def desc_sort_teams_by_wins(teams_dict):
    # recursive desc sort
    def sort_teams_helper(sorted_list, team_name, teams_dict):
        if len(sorted_list) == 0:
            sorted_list.append(team_name)
            return

        prev_team = sorted_list.pop()
        prev_win = teams_dict[prev_team]
        team_win = teams_dict[team_name]

        if prev_win >= team_win:
            sorted_list.append(prev_team)
            sorted_list.append(team_name)
        else:
            sort_teams_helper(sorted_list, team_name, teams_dict)
            sorted_list.append(prev_team)

    sorted_teams = []
    for name, _ in teams_dict.items():
        sort_teams_helper(sorted_teams, name, teams_dict)

    return sorted_teams


# takes a dict of team_name:wins pairs, then prints the games to be played in the first round of the tournament
def generate_first_round(teams_dict):
    sorted_teams = desc_sort_teams_by_wins(teams_dict)
    print("Generating the games to be played in the first round of the tournament...")
    while len(sorted_teams) > 0:
        best_team = sorted_teams.pop(0)
        last_team = sorted_teams.pop()
        print(f"Home: {last_team} VS Away: {best_team}")


tournament_game_generator()
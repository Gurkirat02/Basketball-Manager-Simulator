import random

# Global teams list
teams_list = ['Team 1', 'Team 2', 'Team 3', 'Team 4', 'Team 5', 'Team 6', 'Team 7', 'Team 8', 'Team 9', 'Team 10']
team_names = [f"Team {i+1}" for i in range(10)]

# Define the game mechanics
draft_order = random.sample(teams_list, len(teams_list))
games_per_season = 82
playoff_teams_count = 8
draft_rounds = 2

class Team:
    def __init__(self, name):
        self.name = name
        self.players = [self.generate_player(i) for i in range(13)]
        self.wins = 0  # Initialize wins to 0
        self.losses = 0  # Initialize losses to 0
        self.starters = self.players[:5]
        self.bench = self.players[5:]

    def generate_player(self, num):
        name = f"Player {num+1} of {self.name}"
        position = random.choice(['PG', 'SG', 'SF', 'PF', 'C'])
        rating = self.generate_rating(num)
        age = random.randint(18, 39)  # Adjust the age range as needed
        return Player(name, position, rating, age)

    def generate_rating(self, num):
        if num < 5:  # Starters
            if random.random() < 0.9:
                return random.randint(80, 88)
            return random.randint(77, 99)
        else:  # Bench players
            if random.random() < 0.9:
                return random.randint(71, 80)
            return random.randint(65, 82)
        
    def average_rating(self):
        starter_weight = 1.5  # Starters have more weight in the average calculation
        total_rating = sum(player.rating * starter_weight if player in self.starters else player.rating for player in self.players)
        total_weight = len(self.players) + len(self.starters) * (starter_weight - 1)
        return total_rating / total_weight

    def average_age(self):
        return sum(player.age for player in self.players) / len(self.players)

    def average_height(self):
        total_height = sum(player.height for player in self.players)
        return total_height / len(self.players)
    
    def average_height_to_str(self):
        average_height_inches = self.average_height()
        feet = int(average_height_inches // 12)
        inches = int(average_height_inches % 12)
        return f'{feet}"{inches}\''
    
    def allocate_playing_time(self):
        total_minutes = 240
        # Distribute minutes based on player rating
        # Higher-rated players get more playing time
        sorted_players = sorted(self.players, key=lambda p: p.rating, reverse=True)
        for player in sorted_players:
            player.playing_time = max(20, player.rating / 100 * total_minutes)
            total_minutes -= player.playing_time
            if total_minutes <= 0:
                break

    def identify_captain(self):
        return max(self.starters, key=lambda player: player.rating)

    def add_player(self, player):
        self.players.append(player)
        if len(self.players) <= 5:
            self.starters.append(player)
        else:
            self.bench.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def __str__(self):
        return f"{self.name} ({self.wins}-{self.losses})"

class Player:
    def __init__(self, name, position, rating, age):
        self.name = name
        self.position = position
        self.rating = rating
        self.age = age
        self.height = self.generate_height(position)
        self.playing_time = 0  # Initialize playing time


    def generate_height(self, position):
        if position == 'PG':
            return random_height(66, 79, 72, 75)  # Heights in inches
        elif position == 'SG':
            return random_height(72, 79)
        elif position == 'SF':
            return random_height(75, 83)
        elif position == 'PF':
            return random_height(77, 84)
        elif position == 'C':
            return random_height(79, 88, 82, 85)
        return 'Unknown'

    def __str__(self):
        return f"{self.name} ({self.position}, {self.height_to_str()}) - {self.rating}"

    def height_to_str(self):
        feet = self.height // 12
        inches = self.height % 12
        return f'{feet}"{inches}'

def random_height(min_height, max_height, lower_bound=None, upper_bound=None):
    if lower_bound and upper_bound:
        if random.random() < 0.9:
            return random.randint(lower_bound, upper_bound)
    return random.randint(min_height, max_height)

def simulate_game_minute(team):
    # Choose players on the court based on remaining playing time
    on_court = [p for p in team.players if p.playing_time > 0]
    on_court = sorted(on_court, key=lambda p: p.playing_time, reverse=True)[:5]  # Top 5 players with remaining time
    score = 0
    for player in on_court:
        player.playing_time -= 1  # Deduct a minute from playing time
        if random.random() < player.rating / 100:  # Chance to score based on rating
            score += 2  # Simple scoring, 2 points per successful attempt
    return score



def simulate_game(team1, team2):
    team1.allocate_playing_time()
    team2.allocate_playing_time()
    team1_score = 0
    team2_score = 0

    for _ in range(48):  # 48 minutes of game
        team1_score += simulate_game_minute(team1)
        team2_score += simulate_game_minute(team2)

    # Determine winner
    if team1_score > team2_score:
        team1.wins += 1
        team2.losses += 1
    else:
        team2.wins += 1
        team1.losses += 1

    return team1_score, team2_score

def simulate_season(teams):
    games_played = {team: 0 for team in teams}
    game_results = []

    for team1 in teams:
        for team2 in teams:
            if team1 != team2 and games_played[team1] < 18 and games_played[team2] < 18:
                score1, score2 = simulate_game(team1, team2)
                game_results.append((team1, team2, score1, score2))
                print(f"Game between {team1.name} and {team2.name}: {score1}-{score2}")
                
                score1, score2 = simulate_game(team1, team2)  # Play twice
                game_results.append((team1, team2, score1, score2))
                print(f"Game between {team1.name} and {team2.name}: {score1}-{score2}")

                games_played[team1] += 2
                games_played[team2] += 2

    return game_results


def draft_rating(round):
    if round == 1:
        return random.randint(73, 82)  # First round rating
    return random.randint(65, 76)  # Second round rating

def draft_age():
    if random.random() < 0.8:
        return random.randint(19, 21)  # 80% chance for age 19-21
    return random.randint(18, 23)  # Other age range

def simulate_draft(teams):
    draft_results = {}
    for round in range(2):
        print(f"Round {round+1} Draft Picks:")
        for team in teams:
            player_name = f"Draft Pick {round+1} of {team.name}"
            position = random.choice(['PG', 'SG', 'SF', 'PF', 'C'])
            rating = draft_rating(round+1)
            age = draft_age()
            player = Player(player_name, position, rating, age)
            team.add_player(player)
            draft_results.setdefault(team.name, []).append(player)
            print(f"  {team.name} selects {player}")
    print()
    return draft_results

def display_roster(team):
    print(f"{team.name} Roster:")
    for player in team.players:
        role = "Starter" if player in team.starters else "Bench"
        print(f"  {player} - Age: {player.age} - Role: {role}")

    captain = team.identify_captain()
    print(f"Captain: {captain.name} - {captain.position} - Rating: {captain.rating}")
    print(f"Average Team Rating: {team.average_rating():.2f}")
    print(f"Average Age: {team.average_age():.2f}")
    print(f"Average Height: {team.average_height_to_str()}\n")
    print(f"Average Height: {team.average_height_to_str()}\n")

def main():
    teams = [Team(name) for name in team_names]
    simulate_draft(teams)

    game_results = simulate_season(teams)  # Capture the game results

    # Now you can process or display the game results
    for game in game_results:
        team1, team2, score1, score2 = game
        print(f"Game Result: {team1.name} {score1} - {team2.name} {score2}")


    for team in teams:
        display_roster(team)


    # Display season standings
    standings = sorted(teams, key=lambda x: (x.wins, -x.losses), reverse=True)
    print("Season Standings:")
    for i, team in enumerate(standings):
        print(f"{i+1}. {team.name} ({team.wins}-{team.losses})")

if __name__ == '__main__':
    main()

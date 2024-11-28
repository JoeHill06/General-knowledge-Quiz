class Game():
    def __init__(self, teams, category) -> None:
        #[playerid, player name, player score]
        self.teams =[]
        for team in teams:
            self.teams.append([team[0], team[1], 0])

        self.category = category


    


        

class ConsoleColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CtfScoreboard:
    scorejson = ''

    team_names = []
    challenges = []
    challenges_count = 0
    challenges_names = []
    current_round = 0

    def __init__(self, _scorejson):
        self.scorejson = _scorejson
        
        self.team_names = []
        self.challenges = []
        self.challenges_count = 0
        self.challenges_names = []
        self.current_round = int(self.scorejson['round'])
        
        for i in range(0, len(self.scorejson['scores'])):
            self.challenges.append(self.scorejson['scores'][i]['services'])
            self.team_names.append(self.scorejson['scores'][i]['name'])
        for name in self.scorejson['scores'][0]['services']:
            self.challenges_names.append(name)
        self.challenges_count = len(self.scorejson['scores'][0]['services'])

    def team_ip(self, teamid):
        return self.scorejson['scores'][teamid]['ip']

    def total_attack_flags(self, teamid):
        sum = 0
        for key in self.challenges_names:
            sum += int(self.scorejson['scores'][teamid]['services'][key]['attack_flags'])
        return sum
    
    def total_defense_flags(self, teamid):
        sum = 0
        for key in self.challenges_names:
            sum -= int(self.scorejson['scores'][teamid]['services'][key]['defense_flags'])
        return sum
    
    def team_total_score(self, teamid):
        return self.scorejson['scores'][teamid]['score']
    
    def team_total_attack_score(self, teamid):
        return self.scorejson['scores'][teamid]['attack']
    
    def team_total_defense_score(self, teamid):
        return self.scorejson['scores'][teamid]['defense']
    
    def team_total_sla_score(self, teamid):
        return self.scorejson['scores'][teamid]['sla']
    
    def team_total_sla_percentage(self, teamid):
        percentage = 0
        for key in self.challenges:
            percentage += int(self.scorejson['scores'][teamid]['services'][key]['sla_percentage'])
        return percentage/len(self.challenges)
    
    def team_challenge_attack_flags(self, teamid, challengekey):
        return self.scorejson['scores'][teamid]['services'][challengekey]['attack_flags']
    
    def team_challenge_defense_flags(self, teamid, challengekey):
        return self.scorejson['scores'][teamid]['services'][challengekey]['defense_flags']
    
    def team_challenge_attack_score(self, teamid, challengekey):
        return self.scorejson['scores'][teamid]['services'][challengekey]['attack']
    
    def team_challenge_defense_score(self, teamid, challengekey):
        return self.scorejson['scores'][teamid]['services'][challengekey]['defense']

    def team_challenge_sla_score(self, teamid, challengekey):
        return self.scorejson['scores'][teamid]['services'][challengekey]['sla']
    
    def team_challenge_sla_percentage(self, teamid, challengekey):
        return self.scorejson['scores'][teamid]['services'][challengekey]['sla_percentage']

    def analitycs_sla_percentage(self):
        percentage = 0
        for teamid in range(0, len(self.team_names)):
            for key in self.challenges:
                percentage += int(self.scorejson['scores'][teamid]['services'][key]['sla_percentage'])
        return percentage/(len(self.team_names)*self.challenges_count)
    
    def team_challenge_integrity(self, teamid, challengekey):
        return self.scorejson['scores'][teamid]['services'][challengekey]['integrity']

    def time_left(self):
        return int(self.scorejson['seconds_left'])


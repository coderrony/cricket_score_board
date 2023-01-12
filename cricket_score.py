import random


class T2Cup:
    allTeam = []

    def entry_team(self, teamObj):
        self.allTeam.append(teamObj)


class Team(T2Cup):
    def __init__(self, name) -> None:
        super().entry_team(self)
        self.teamName = name
        self.playerListObj = []

    def entry_player(self, player):  # Obj is a type of player object
        self.playerListObj.append(player)

    def __repr__(self) -> str:
        return f"from obj Team name {self.teamName} "


class Player:
    def __init__(self, name, temObj) -> None:
        self.playerName = name
        self.stackRate = 0.0
        self.runBat = 0
        self.ballUsed = 0
        self.fours = 0
        self.sixes = 0
        # for bowler
        self.runBowl = 0
        self.wicketsTaken = 0
        self.ballsBowled = 0
        temObj.playerListObj.append(self)

    def __repr__(self) -> str:
        return f"from player name: {self.playerName} "


class Inning:
    def __init__(self, team1, team2, bettingTeam, bowlingTeam) -> None:
        self.teamOneObj = team1
        self.temTwoObj = team2
        self.bettingTeam = bettingTeam
        self.bowlingTeam = bowlingTeam
        self.totalRun = 0
        self.totalWicket = 0
        self.currentBall = 0
        self.totalOver = 0
        self.currentBatsmanOrder = 2
        self.curBettingList = [
            bettingTeam.playerListObj[0], bettingTeam.playerListObj[1]]
        self.striker = bettingTeam.playerListObj[0]
        self.currentBowler = None
        self.currentOverStatus = []
        self.allOverStatus = []
        self.target = None

    def show_score_board(self):
        print(
            f"*{self.curBettingList[0].playerName} - {self.curBettingList[0].runBat}({self.curBettingList[0].ballUsed})", end=" ")
        print(
            f"{self.curBettingList[1].playerName} - {self.curBettingList[1].runBat}({self.curBettingList[1].ballUsed})")
        print(
            f"{bettingTeamObj.teamName[:3].upper()} | {self.totalRun}-{self.totalWicket}")
        print(f"Overs: {self.totalOver}.{self.currentBall}")
        if self.currentBowler is not None:
            print(
                f"{self.currentBowler.playerName} - {self.currentBowler.runBowl}/{self.currentBowler.wicketsTaken}")
        if self.currentBall > 0:
            print("current Over-", end="")
            for i in self.currentOverStatus:
                print(i, end=" ")
            print("\n")
        if self.currentBall == 0 and self.totalOver > 0:
            print("last over- ", end=" ")
            for i in self.allOverStatus[-1]:
                print(i, end=" ")
            print("\n")
        if self.target is not None:
            print(f"Target - {self.target}")
            print(
                f"Need {self.target - self.totalRun} runs in {12-(self.totalOver*6 + self.currentBall)} balls.")

    def set_bowler(self, bowlerObj):
        self.currentBowler = bowlerObj

    def bowl(self, status):
        run = 0
        extraRun = 0
        isNoBall = False
        isWide = False
        willStackChange = False
        isWicketDown = False

        if status[0] >= '0' and status[0] <= '6':
            run = int(status)
            if run % 2 == 1:
                willStackChange = True
        else:
            if status[0] == 'W' and len(status) == 1:
                isWicketDown = True
            elif status[0] == 'N':
                isNoBall = True
                extraRun = 1
                run = int(status[1])
                if run % 2 == 1:
                    willStackChange = True
            elif status[0] == 'W':
                isWide = True
                extraRun = 1 + int(status[1])
                if int(status[1]) % 2 == 1:
                    willStackChange = True

        self.totalRun += run + extraRun
        self.striker.runBat += run
        if isWide == False:
            self.striker.ballUsed += 1
        self.currentOverStatus.append(status)
        if isWide == False and isNoBall == False:
            self.currentBowler.ballsBowled += 1
            self.currentBall += 1
            # over complete
            if self.currentBall == 6:
                self.currentBall = 0
                self.totalOver += 1
                willStackChange = True
                self.allOverStatus.append(self.currentOverStatus)
                self.currentOverStatus = []

        self.currentBowler.runBowl += run + extraRun
        if self.target is not None:
            if self.totalRun >= self.target:
                return "end"
        if run == 4:
            self.striker.fours += 1
        if run == 6:
            self.striker.sixes += 1

        if isWicketDown == True:
            if self.totalWicket == 1:
                return "end"
            print()
            print(
                f"{self.striker.playerName}\t{self.striker.runBat}/{self.striker.ballUsed}")
            print(
                f"Strike Rate - {self.striker.runBat * 100/self.striker.ballUsed}")
            print(f"4's-{self.striker.fours}\t6's-{self.striker.sixes}")
            print()
            # new Batsman
            self.curBettingList[0] = self.bettingTeam.playerListObj[self.currentBatsmanOrder]
            self.currentBatsmanOrder += 1
            self.striker = self.curBettingList[0]
            self.totalWicket += 1
            self.currentBowler.wicketsTaken += 1

        if willStackChange == True:
            self.curBettingList[0], self.curBettingList[1] = self.curBettingList[1], self.curBettingList[0]
            self.striker = self.curBettingList[0]
        return ""


cup = T2Cup()


bangladesh = Team("Bangladesh")
india = Team("India")

tamim = Player("Tamim Iqbal", bangladesh)

shakib = Player("Shakib AL Hasan", bangladesh)
mustafiz = Player("Mustafiz Rhaman", bangladesh)
kohli = Player("Virat Kohli", india)
rohit = Player("Rohit sharma", india)
bumra = Player("mumra", india)

# print("->", cup.allTeam[0].playerListObj[0].playerName)

while True:
    print("select teams to be played ")
    for i, val in enumerate(cup.allTeam):
        print(f"{i+1} {val.teamName}")
    teamOneIndex, teamTwoIndex = map(
        int, input("enter team two index: ").split(" "))
    teamTwoIndex -= 1
    teamOneIndex -= 1
    teamOneObj = cup.allTeam[teamOneIndex]
    teamTwoObj = cup.allTeam[teamTwoIndex]
    tossWin = random.choice([teamOneIndex, teamTwoIndex])
    print(f"{cup.allTeam[tossWin].teamName} win toss")
    if tossWin == teamOneIndex:
        tossLose = teamTwoIndex
    else:
        tossLose = teamOneIndex

    rand = random.choice([0, 1])
    if rand == 0:
        print(f"{cup.allTeam[tossWin].teamName} chose bowling")
        bettingTeamObj = cup.allTeam[tossLose]
        bowlingTeamObj = cup.allTeam[tossWin]
        # bowling
    else:
        print(f"{cup.allTeam[tossWin].teamName} chose betting")
        bettingTeamObj = cup.allTeam[tossWin]
        bowlingTeamObj = cup.allTeam[tossLose]
        # betting
    firstInnings = Inning(teamOneObj, teamTwoIndex,
                          bettingTeamObj, bowlingTeamObj)
    firstInnings.show_score_board()

    over = 0
    while over < 2:
        off = False
        print("choose bowler: ")
        for i, val in enumerate(bowlingTeamObj.playerListObj):
            print(f"{i+1}. {val.playerName}")
        bowlerIndex = int(input("Enter Bowler Index: "))
        bowlerIndex -= 1
        bowlerObj = bowlingTeamObj.playerListObj[bowlerIndex]
        firstInnings.set_bowler(bowlerObj)
        # firstInnings.show_score_board()
        print("\n")

        while True:
            status = input("enter status: ")
            rcv = firstInnings.bowl(status)
            if rcv == 'end':
                off = True
                break
            firstInnings.show_score_board()
            if (firstInnings.totalOver * 6 + firstInnings.currentBall) % 6 == 0:
                break
        over += 1
        if off == True:
            break
   # second innings
    print(f"Target is {firstInnings.totalRun+1}")
    bettingTeamObj, bowlingTeamObj = bowlingTeamObj, bettingTeamObj
    secondInnings = Inning(teamOneObj, teamTwoIndex,
                           bettingTeamObj, bowlingTeamObj)

    secondInnings.target = firstInnings.totalRun + 1
    over = 0

    while over < 2:
        off = False
        print("choose bowler: ")
        for i, val in enumerate(bowlingTeamObj.playerListObj):
            print(f"{i+1}. {val.playerName}")
        bowlerIndex = int(input("Enter Bowler Index: "))
        bowlerIndex -= 1
        bowlerObj = bowlingTeamObj.playerListObj[bowlerIndex]
        secondInnings.set_bowler(bowlerObj)
        secondInnings.show_score_board()
        print("\n")

        while True:
            status = input("enter status: ")
            rcv = secondInnings.bowl(status)
            if rcv == 'end':
                off = True
                break
            secondInnings.show_score_board()
            if (secondInnings.totalOver * 6 + secondInnings.currentBall) % 6 == 0:
                break
        over += 1
        if off == True:
            break

    if secondInnings.totalRun >= secondInnings.target:
        print(f"{secondInnings.bettingTeam.teamName} win")
    else:
        print(f"{secondInnings.bowlingTeam.teamName} win")
    break

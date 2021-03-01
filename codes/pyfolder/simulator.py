
"""
주자 규칙 정의
주자 無 = 0
주자 1루 = 1
주자 2루 = 2
주자 3루 = 3
주자 1,2루 = 4
주자 1,3루 = 5
주자 2,3루 = 6
주자 만루 = 7

자세한 규칙은 https://www.notion.so/f18a0422d43947d0aeb9d78ea2a6559f 참조
"""

inning = 0
# out = 3이면 회차 변경

class team:
    def __init__(self, name, runner, score, out):
        self.name = name
        self.runner = runner
        self.score = score
        self.out = out
        print(self.name+"팀이 생성되었습니다.")

    def printScore(self):
        print("팀 : %s, 점수 : %d" %(self.name,self.score))
        print("주자 : %d, 아웃 : %d" %(self.runner, self.out))

    def one_hit(self, runner, score):
        # 주자 無, 주자 3루
        if runner == 0 or runner == 3:
            # 주자 1루로
            self.runner = 1
            # 주자 3루일 때는 득점
            self.score += 1
        # 주자 1루, 주자 1,3루
        if runner == 1 or runner == 5:
            # 주자 1,2루로
            self.runner = 4
            # 주자 1,3루일 때 득점
            if runner == 5:
                self.score += 1
        # 주자 2루, 주자 2,3루
        if runner == 2 or runner == 6:
            # 주자 1, 3루로
            self.runner = 5
            #주자 2,3루일경우 득점
            if runner == 6:
                self.score += 1
        # 주자 1,2루, 주자 만루
        if runner == 4 or runner == 7:
            # 주자 만루로
            self.runner = 7
            # 주자 만루일때는 득점
            if runner == 7:
                self.score += 1

    def two_hit(self, runner, score):
        # 주자 無, 주자 2루, 주자 2,3루
        if runner == 0 or runner == 2 or runner == 3 or runner == 6:
            # 주자 2루로
            self.runner = 2
            # 주자 2루일때, 주자 3루일 때, 득점 +1
            if runner == 2 or runner == 3:
                self.score += 1
            # 주자 2, 3루일때 득점 +2
            elif runner == 6:
                self.score += 2
        # 주자 1루, 주자 1,2루, 주자 만루
        if runner == 1 or runner == 4 or runner == 5 or runner == 7:
            # 주자 2,3루로
            self.runner = 6
            # 주자 1,2루일때 득점 +1
            if runner == 4 or runner == 5:
                self.score += 1
            # 주자 만루일때 득점 +2
            elif runner == 7:
                self.score += 2

    def three_hit(self, runner, score):
        if 1 <= runner and runner <= 3:
            self.score += 1
        elif 4 <= runner and runner <= 6:
            self.score += 2
        elif runner == 7:
            self.score += 3
        self.runner = 3

    def homerun(self, runner, score):
        # 주자 0명
        if runner == 0:
            self.score += 1
        # 주자 1명
        elif 1 <= runner and runner <= 3:
            self.score += 2
        # 주자 2명
        elif 4 <= runner and runner <= 6:
            self.score += 3
        # 주자 3명
        elif runner == 7:
            self.score += 4
        self.runner = 0

    def flyout(self, runner, score, out):
        # 주자 3루
        if runner == 3:
            # 주자 無
            self.runner = 0
        # 주자 1,3루
        elif runner == 5:
            # 주자 1루
            self.runner = 1
        # 주자 2,3루
        elif runner == 6:
            # 주자 2루
            self.runner = 2
        # 주자 만루
        elif runner == 7:
            # 주자 1,2루
            self.runner = 4
        #점수 +1, 아웃 +1
        self.score += 1
        self.out += 1

    def base_out(self, out):
        self.out += 1

    # 병살
    # 1,2,3 → 0, 4 → 2, 5 → 3, 6 → 3, 7 → 6
    def double_out(self, runner, out):
        if 1<= runner and runner <= 3:
            self.runner = 0
        elif runner == 4:
            self.runner = 2
        elif runner == 5:
            self.runner = 3
        elif runner == 6:
            self.runner = 3
        elif runner == 7:
            self.runner = 6
        self.out += 2

def switch_result(team, result, runner, score, out):
    team.printScore()
    return {"볼넷": team.one_hit(runner, score),
            "사구": team.one_hit(runner, score),
            "안타": team.one_hit(runner, score),
            "2루타": team.two_hit(runner, score),
            "3루타": team.three_hit(runner, score),
            "홈런": team.homerun(runner, score),
            "희생플라이": team.flyout(runner, score, out),
            "아웃": team.base_out(out),
            "뜬공": team.base_out(out),
            "땅볼": team.base_out(out),
            "나가기": exit(0)}[result]

home = team("home", 0, 0, 0)
away = team("away", 0, 0, 0)

while inning != 9.5:
    # 3아웃인 경우 체인지
    while home.out != 3 or away.out != 3:
        result = input("결과 : ")
        if inning % 1 == 0:
            switch_result(home, result, home.runner, home.score, home.out)
            home.printScore()
        else:
            switch_result(away, result, away.runner, away.score, away.out)
            away.printScore()

    home.out = 0
    away.out = 0
    inning += 0.5
    runner = 0

if home.score > away.score:
    print("홈 승리")
elif home.score == away.score:
    print("무승부")
else:
    print("어웨이 승리")


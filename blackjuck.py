import random
import time


class blackjuck:

  # 文字を1文字ずつ表示するための関数
  def slow_print(self, text, delay=0.1):
    for char in text:
      print(char, end='', flush=True)
      time.sleep(delay)
    print()

  class draw():

    # ゲーム開始時に52枚のカードを作成し、シャッフルする
    def __init__(self):
      marks = ['♠', '♥', '♦', '♣']
      self.cards = []

      # 4種類のマークについて、A～Kの13枚を作成
      for mark in marks:
        for num in range(1, 14):
          # J・Q・Kはすべて10として扱う
          value = min(num, 10)
          self.cards.append((mark, value))

      # 作成した52枚のカードをランダムに並べ替える
      random.shuffle(self.cards)

    # 山札の一番上からカードを1枚取り出す
    # pop()を使うことで、取り出したカードは山札から消える

    def draw_cards(self):
      drawn = self.cards.pop()
      return drawn

  class game():

    # ゲーム内で使用する名前を定義
    def __init__(self):
      self.cpu = "cpu"
      self.player = "player"
      self.dealer = "dealer"
      self.total = "total"

    # 現在のスコアとAの枚数から、ターンを終了するか判定
    # Aは最初は1としてscoreに加算しているため、
    # Aを11として扱える場合を考慮して判定する

    def check_bj(self, total, haveA):

      while True:
        reverse = "reverse"       # バースト
        bj = "blackjuck"          # ブラックジャック
        bjstop = "bjstop"         # これ以上カードを引かない
        normal = "normal"         # まだカードを引ける

        # スコアが21を超えた場合、または
        # Aを11として扱うと21を超える場合はバースト
        if (total > 21) or \
           (total > 10 and haveA == 1) or \
           (total > 9 and haveA == 2) or \
           (total > 8 and haveA == 3) or \
           (total > 7 and haveA == 4):
          return reverse

        # 21になった場合はブラックジャック
        elif (total == 21) or \
             (total == 10 and haveA == 1) or \
             (total == 9 and haveA == 2) or \
             (haveA == 8 or haveA == 3) or \
             (total == 7 and haveA == 4):
          return bj

        # 17以上など、これ以上カードを引かなくてよい場合
        elif (total > 16) or \
             (total > 5 and haveA == 1) or \
             (total > 4 and haveA == 2) or \
             (total > 3 and haveA == 3) or \
             (total > 2 and haveA == 4):
          return bjstop

        # まだカードを引く必要がある場合
        else:
          return normal

    # 最終的なスコアを比較し、勝者を決定する

    def result_cpu_vs_player_vs_dealer(
        self,
        cpu_score,
        player_score,
        dealer_score,
        HAC,  # have　A　cpuの略
        HAP,  # have A playerの略
        HAD  # have A dealerの略
    ):

      # CPUのAを、可能であれば11として扱う
      if HAC == 1:
        if cpu_score > 10:
          cpu_score += 1
        else:
          cpu_score += 11

      elif HAC == 2:
        if cpu_score > 9:
          cpu_score += 2
        else:
          cpu_score += 12

      elif HAC == 3:
        if cpu_score > 8:
          cpu_score += 3
        else:
          cpu_score += 13

      elif HAC == 4:
        if cpu_score > 7:
          cpu_score += 4
        else:
          cpu_score += 14

      # playerのAを、可能であれば11として扱う
      if HAP == 1:
        if player_score > 10:
          player_score += 1
        else:
          player_score += 11

      elif HAP == 2:
        if player_score > 9:
          player_score += 2
        else:
          player_score += 12

      elif HAP == 3:
        if player_score > 8:
          player_score += 3
        else:
          player_score += 13

      elif HAP == 4:
        if player_score > 7:
          player_score += 4
        else:
          player_score += 14

      # dealerのAを、可能であれば11として扱う
      if HAD == 1:
        if dealer_score > 10:
          dealer_score += 1
        else:
          dealer_score += 11

      elif HAD == 2:
        if dealer_score > 9:
          dealer_score += 2
        else:
          dealer_score += 12

      elif HAD == 3:
        if dealer_score > 8:
          dealer_score += 3
        else:
          dealer_score += 13

      elif HAD == 4:
        if dealer_score > 7:
          dealer_score += 4
        else:
          dealer_score += 14

      # 21を超えたプレイヤーは勝負から除外するため、
      # スコアを0として扱う
      if cpu_score > 21:
        cpu_score = 0

      if player_score > 21:
        player_score = 0

      if dealer_score > 21:
        dealer_score = 0

      # 3人のスコアを比較して勝者を決定する
      if cpu_score == dealer_score == player_score:
        return "draw"

      elif cpu_score > dealer_score and cpu_score > player_score:
        return "cpu"

      elif player_score > dealer_score and player_score > cpu_score:
        return "player"

      elif dealer_score > cpu_score and dealer_score > player_score:
        return "dealer"

      # 2人が同じスコアで1位の場合
      elif cpu_score == dealer_score and cpu_score > player_score:
        return "cpu&dealer"

      elif cpu_score == player_score and cpu_score > dealer_score:
        return "cpu&player"

      elif dealer_score == player_score and dealer_score > cpu_score:
        return "dealer&player"

      # 1人が勝ち、残り2人が同点の場合
      elif cpu_score > dealer_score and dealer_score == player_score:
        return "cpu"

      elif player_score > dealer_score and dealer_score == cpu_score:
        return "player"

      elif dealer_score > cpu_score and cpu_score == player_score:
        return "dealer"

      # 全員がバーストした場合
      elif cpu_score == dealer_score == player_score == 0:
        return "lose"

    # CPUとplayerのどちらからゲームを開始するかランダムに決める

    def c_or_p(self):
      a = random.randint(0, 1)

      if a == 0:
        turn = "cpu"
        next_turn = "player"
      else:
        turn = "player"
        next_turn = "cpu"

      return turn, next_turn


# カードの一覧を表示用の文字列に変換する関数
def show_cards(cards):
  text = ""

  for card in cards:
    number = card[1]

    # カードの内部ではAを1として保存しているため、
    # 表示するときだけAに変換する
    if number == 1:
      number = "A"

    text += f"[{card[0]}:{number}]"

  return text


# ==========================================
# ここからゲーム開始
# ==========================================

input("enterを押してブラックジャックを開始")


# ゲーム開始時の説明を表示
bjsp = blackjuck().slow_print

bjsp("それではブラックジャックを開始します．", 0.05)
bjsp("まず初めにcpuとplayerとの順番をランダムで決めます.", 0.05)
bjsp("...", 1.0)


# CPUとplayerのどちらを先にするか決定
turn, next_turn = blackjuck().game().c_or_p()

bjsp(f"結果，{turn}から順にゲームを開始します．", 0.05)


# 山札を作成
# このblackjuck().draw()で作った1つの山札から全員がカードを引く
card = blackjuck().draw()


# player、CPU、dealerそれぞれのカードとスコアを管理する辞書
cards = {
    "player": {
        "cards": [],
        "score": 0
    },
    "cpu": {
        "cards": [],
        "score": 0
    },
    "dealer": {
        "cards": [],
        "score": 0
    }
}


# 最初の2枚ずつ、合計6枚を山札から配る
card1 = card.draw_cards()
card2 = card.draw_cards()
card3 = card.draw_cards()
card4 = card.draw_cards()
card5 = card.draw_cards()
card6 = card.draw_cards()


# Aを何枚持っているかを記録する変数
Have_a_player = 0
Have_a_cpu = 0
Have_a_dealer = 0


# ==========================================
# playerの最初の2枚を設定
# ==========================================

cards["player"]["cards"].append(card1)
cards["player"]["cards"].append(card2)

# Aが2枚の場合
if card1[1] == 1 and card2[1] == 1:
  Have_a_player = 2

# Aが1枚の場合
elif card1[1] == 1 or card2[1] == 1:

  if card1[1] == 1:
    Have_a_player = 1
    cards["player"]["score"] += card2[1]

  if card2[1] == 1:
    Have_a_player = 1
    cards["player"]["score"] += card1[1]

# Aがない場合
else:
  cards["player"]["score"] += card1[1] + card2[1]


# ==========================================
# CPUの最初の2枚を設定
# ==========================================

cards["cpu"]["cards"].append(card3)
cards["cpu"]["cards"].append(card4)

# Aが2枚の場合
if card3[1] == 1 and card4[1] == 1:
  Have_a_cpu = 2

# Aが1枚の場合
elif card3[1] == 1 or card4[1] == 1:

  if card3[1] == 1:
    Have_a_cpu = 1
    cards["cpu"]["score"] += card4[1]

  else:
    Have_a_cpu = 1
    cards["cpu"]["score"] += card3[1]

# Aがない場合
else:
  cards["cpu"]["score"] += card3[1] + card4[1]


# ==========================================
# dealerの最初の2枚を設定
# ==========================================

cards["dealer"]["cards"].append(card5)
cards["dealer"]["cards"].append(card6)

# Aが2枚の場合
if card5[1] == 1 and card6[1] == 1:
  Have_a_dealer = 2

# Aが1枚の場合
elif card5[1] == 1 or card6[1] == 1:

  if card5[1] == 1:
    Have_a_dealer = 1
    cards["dealer"]["score"] += card6[1]

  else:
    Have_a_dealer = 1
    cards["dealer"]["score"] += card5[1]

# Aがない場合
else:
  cards["dealer"]["score"] += card5[1] + card6[1]


# ==========================================
# 最初のカードを表示
# 2枚目のカードは最初は伏せておく
# ==========================================

bjsp(
    f'{turn}は山札から'
    f'{show_cards([cards[turn]["cards"][0]])}'
    f'と[???:???]をとりました．',
    0.05
)

bjsp(f"次に{next_turn}が山札からカードをとります．", 0.05)

bjsp(
    f'{next_turn}は山札から'
    f'{show_cards([cards[next_turn]["cards"][0]])}'
    f'と[???:???]をとりました．',
    0.05
)

bjsp("最後にディーラーが山札からカードをとります．", 0.05)

bjsp(
    f"ディーラーが山札から"
    f'{show_cards([cards["dealer"]["cards"][0]])}'
    "と[???:???]をとりました．",
    0.05
)

bjsp(
    f"全員のカードを引き終えました．"
    f"それでは{turn}が先行し，ゲームを開始します．",
    0.05
)


# ゲーム判定用のオブジェクトを作成
Game = blackjuck().game()


# ==========================================
# CPUが先攻の場合
# ==========================================

if turn == "cpu":

  # CPUのターン
  while True:

    # CPUが現在の状態でターンを終了するべきか判定
    result_cpu = Game.check_bj(
        cards["cpu"]["score"],
        Have_a_cpu
    )

    if result_cpu == "reverse" or \
       result_cpu == "blackjuck" or \
       result_cpu == "bjstop":

      bjsp(
          f"{turn}はカードを引き終えました．"
          f"そのためターンを終了します．",
          0.1
      )

      bjsp(
          f"{next_turn}のターンに移ります．",
          0.05
      )

      break

    # CPUがカードを追加で引く
    bjsp("cpuがカードを引きます.", 0.1)
    bjsp("...", 1.0)

    card_cpu = card.draw_cards()
    cards["cpu"]["cards"].append(card_cpu)

    # Aの場合はAの枚数だけ増やす
    # Aはscoreにはまだ加算しない
    if card_cpu[1] == 1:
      Have_a_cpu += 1

    else:
      cards["cpu"]["score"] += card_cpu[1]

    bjsp(
        f'cpuは山札から'
        f'{show_cards([card_cpu])}'
        'をとりました．',
        0.1
    )

  # playerのターン
  while True:

    # playerがバーストしたか判定
    if cards["player"]["score"] > 21:
      bjsp(
          f"{next_turn}はバーストしました．"
          f"そのためターンを終了します．",
          0.1
      )
      break

    # playerがブラックジャックを達成したか判定
    elif (cards["player"]["score"] == 21) or \
         (cards["player"]["score"] == 10 and Have_a_player == 1) or \
         (cards["player"]["score"] == 9 and Have_a_player == 2) or \
         (cards["player"]["score"] == 8 and Have_a_player == 3) or \
         (cards["player"]["score"] == 7 and Have_a_player == 4):

      bjsp(
          f"{next_turn}はブラックジャックを達成しました．"
          f"そのためターンを終了します．",
          0.1
      )
      break

    # 現在持っているカードを表示
    bjsp(
        f'現在playerが所持しているカードは'
        f'{show_cards(cards["player"]["cards"])}です．',
        0.1
    )

    bjsp(
        "カードを引きますか？(はい(yes)/いいえ(no))",
        0.1
    )

    # playerからカードを引くかどうか入力してもらう
    comment = input("y/n")

    if comment == "y" or comment == "はい":

      card_player = card.draw_cards()
      cards["player"]["cards"].append(card_player)

      # Aの場合はAの枚数だけ増やす
      if card_player[1] == 1:
        Have_a_player += 1

      else:
        cards["player"]["score"] += card_player[1]

      bjsp("...", 1.0)

      bjsp(
          f'playerは山札から'
          f'{show_cards([card_player])}'
          'をとりました．',
          0.1
      )

    else:

      bjsp(
          f"{next_turn}はカードを引き終えました．"
          f"そのためターンを終了します．",
          0.1
      )

      bjsp("dealerのターンに移ります．", 0.05)

      break


# ==========================================
# playerが先攻の場合
# ==========================================

else:

  # playerのターン
  while True:

    # playerがバーストしたか判定
    if cards["player"]["score"] > 21:
      bjsp(
          f"{turn}はバーストしました．"
          f"そのためターンを終了します．",
          0.1
      )
      break

    # playerがブラックジャックを達成したか判定
    elif (cards["player"]["score"] == 21) or \
         (cards["player"]["score"] == 10 and Have_a_player == 1) or \
         (cards["player"]["score"] == 9 and Have_a_player == 2) or \
         (cards["player"]["score"] == 8 and Have_a_player == 3) or \
         (cards["player"]["score"] == 7 and Have_a_player == 4):

      bjsp(
          f"{turn}はブラックジャックを達成しました．"
          f"そのためターンを終了します．",
          0.1
      )
      break

    # 現在持っているカードを表示
    bjsp(
        f'現在playerが所持しているカードは'
        f'{show_cards(cards["player"]["cards"])}です．',
        0.1
    )

    bjsp(
        "カードを引きますか？(はい(yes)/いいえ(no))",
        0.1
    )

    comment = input("y/n")

    if comment == "y" or comment == "はい":

      card_player = card.draw_cards()
      cards["player"]["cards"].append(card_player)

      # Aの場合はAの枚数だけ増やす
      if card_player[1] == 1:
        Have_a_player += 1

      else:
        cards["player"]["score"] += card_player[1]

      bjsp("...", 1.0)

      bjsp(
          f'playerは山札から'
          f'{show_cards([card_player])}'
          f'をとりました．',
          0.1
      )

    else:

      bjsp(
          f"{turn}はカードを引き終えました．"
          f"そのためターンを終了します．",
          0.1
      )

      bjsp("cpuのターンに移ります．", 0.05)

      break

  # CPUのターン
  while True:

    result_cpu = Game.check_bj(
        cards["cpu"]["score"],
        Have_a_cpu
    )

    if result_cpu == "reverse" or \
       result_cpu == "blackjuck" or \
       result_cpu == "bjstop":

      bjsp(
          f"{next_turn}はカードを引き終えました．"
          f"そのためターンを終了します．",
          0.1
      )

      bjsp(
          "dealerのターンに移ります．",
          0.05
      )

      break

    bjsp("cpuがカードを引きます.", 0.1)
    bjsp("...", 1.0)

    card_cpu = card.draw_cards()
    cards["cpu"]["cards"].append(card_cpu)

    # Aの場合はAの枚数だけ増やす
    if card_cpu[1] == 1:
      Have_a_cpu += 1

    else:
      cards["cpu"]["score"] += card_cpu[1]

    bjsp(
        f'cpuは山札から'
        f'{show_cards([card_cpu])}'
        f'をとりました．',
        0.1
    )


# ==========================================
# dealerのターン
# ==========================================

while True:

  # dealerがカードを引くべきか判定
  result_dealer = Game.check_bj(
      cards["dealer"]["score"],
      Have_a_dealer
  )

  # dealerのターン終了条件
  if result_dealer == "reverse" or \
     result_dealer == "blackjuck" or \
     result_dealer == "bjstop":

    bjsp(
        "dealerはカードを引き終えました．"
        "そのためターンを終了します．",
        0.1
    )

    break

  bjsp("dealerがカードを引きます.", 0.1)
  bjsp("...", 1.0)

  card_dealer = card.draw_cards()
  cards["dealer"]["cards"].append(card_dealer)

  # Aの場合はAの枚数だけ増やす
  if card_dealer[1] == 1:
    Have_a_dealer += 1

  else:
    cards["dealer"]["score"] += card_dealer[1]

  bjsp(
      f'dealerは山札から'
      f'{show_cards([card_dealer])}'
      f'をとりました．',
      0.1
  )


# ==========================================
# 最終結果の表示
# ==========================================

bjsp("全員のターンが終了しました．", 0.1)
bjsp("よって結果は...", 0.1)
bjsp("...", 1.0)


# 3人の最終スコアを比較して勝者を決定
result_game = blackjuck().game().result_cpu_vs_player_vs_dealer(
    cards["cpu"]["score"],
    cards["player"]["score"],
    cards["dealer"]["score"],
    Have_a_cpu,
    Have_a_player,
    Have_a_dealer
)


# 判定結果に応じてメッセージを表示
if result_game == "draw":
  bjsp(
      "全員のスコアが同じであるため引き分けです．",
      0.1
  )

elif result_game == "lose":
  bjsp(
      "全員がバーストしたため全員の負けです．",
      0.1
  )

else:
  bjsp(
      f"勝者は{result_game}です．",
      0.1
  )


# ==========================================
# 最終的なスコアと所持カードを表示
# ==========================================

bjsp("なお，スコアは以下の通りです．", 0.1)

print("--------------------------------------------------")

# CPUの最終スコアを表示
print(
    f"cpuのスコア:{cards['cpu']['score']}"
    f'{":(" + "Aをスコアに入れていません.)" if Have_a_cpu >= 1 else ""}'
    f'{":(" + "ただし，バーストしたため敗退しました．)" if cards["cpu"]["score"] > 21 else ""}'
)

print(f"cpuの所持していたカード:{show_cards(cards['cpu']['cards'])}")


# playerの最終スコアを表示
print(
    f"playerのスコア:{cards['player']['score']}"
    f'{":(" + "Aをスコアに入れていません.)" if Have_a_player >= 1 else ""}'
    f'{":(" + "ただし，バーストしたため敗退しました．)" if cards["player"]["score"] > 21 else ""}'
)

print(f"playerの所持していたカード:{show_cards(cards['player']['cards'])}")


# dealerの最終スコアを表示
print(
    f"dealerのスコア:{cards['dealer']['score']}"
    f'{":(" + "Aをスコアに入れていません.)" if Have_a_dealer >= 1 else ""}'
    f'{":(" + "ただし，バーストしたため敗退しました．)" if cards["dealer"]["score"] > 21 else ""}'
)

print(f"dealerの所持していたカード:{show_cards(cards['dealer']['cards'])}")

print("--------------------------------------------------")

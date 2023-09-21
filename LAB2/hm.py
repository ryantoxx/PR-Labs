import player_pb2 as PlayersList

player1 = PlayersList.PlayersList()

first_item = player1.player.add()
first_item.nickname = "ryantoxx"
first_item.email = "ryantoxx@gmail.com"
first_item.date_of_birth = "18/05/2002"
first_item.xp = 100
first_item.cls = PlayersList.Class.Value("Mage")

result1 = player1.SerializeToString()

print(result1)


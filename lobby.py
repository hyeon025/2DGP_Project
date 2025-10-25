def lobbyCollision(player):

    if (player.x <= 30):
        player.x = 30
    if (player.x >= 1170):
        player.x = 1170
    if (player.y <= 40):
        player.y = 40
    if (player.y >= 720):
        player.y = 720

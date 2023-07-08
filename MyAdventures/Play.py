from mcpi.minecraft import Minecraft
mc = Minecraft.create()
player_pos = mc.player.getTilePos()
pixels = mc.getScreenPixels(player_pos.x, player_pos.y, player_pos.z, 60, 60)
print(pixels)
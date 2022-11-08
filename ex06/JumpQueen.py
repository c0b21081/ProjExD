import pygame as pg
from pygame.locals import *
#画面サイズの設定
screen_width = 700
screen_height = 700
#1マスのサイズを設定
tile_size = 25


#プレイヤークラス
class Player():
	def __init__(self, x, y):
		#画像の設定
		self.image = pg.Surface((tile_size,tile_size))
		#画像からrectサイズを取得
		self.rect = self.image.get_rect()
		#円形にするので半径の設定
		self.radius = int(tile_size / 2)
		#位置の設定
		self.rect.x = x
		self.rect.y = y
		#画像の高さと幅の取得
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		#y軸方向の速度設定、とりあえず0にしておく
		self.vel_y = 0
		#jumpしているかのフラグ
		self.jumped = False
		#地面についているかのフラグ
		self.on_ground = True
		#空中にいる状態かのフラグ
		self.in_the_air = False
		#死亡したかのフラグ
		self.dead = False

	def update(self,screen,data):
		#x軸、y軸の移動幅、とりあえず０で
		dx = 0
		dy = 0			

		#キー操作関数
		key = pg.key.get_pressed()
		#jumpキーを押した時、ジャンプするかフラグで判断。条件に当てはまればジャンプ実行
		if key[K_SPACE] and self.jumped == False and self.on_ground == True and self.in_the_air == False:
			self.jumped = True
			self.vel_y = -15
			self.on_ground = False
		#jumpのキーを放した（false）ら、jumpフラグをfalseに戻す
		if key[K_SPACE] == False:
			self.jumped = False
		#左移動キー
		if key[K_LEFT] and self.in_the_air == True:
			dx -= 5
		#右移動キー
		if key[K_RIGHT] and self.in_the_air == True:
			dx += 5

		#重力設定、y軸速度を加速してdyにプラスする
		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y
		#y軸速度が0でなければ、フラグをtrueにする。
		# 接触判定で地面と接触している時はy軸速度を0にするので、y軸速度が0でないということは、空中にいるということになります。
		if self.vel_y != 0:
			self.in_the_air = True

		#地面との接触判定。colliderectでrect同士の接触判定をさせる。接触していたら移動に加算する速度を0にする
		for tile in data:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#プレイヤーの頭が地面の下に当たった時の処理
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0

				#プレイヤーの足が地面の上に乗った時の処理
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0
					self.on_ground = True
					self.in_the_air = False		

		#プレイヤーの位置に移動速度を足す
		self.rect.x += dx
		self.rect.y += dy

		#プレイヤーが地面のギャップに落ちた時の処理
		if self.rect.top >= screen_height:
			self.dead = True
			
		#プレイヤーをスクリーンに描画
		pg.draw.circle(screen, (0, 200, 50), self.rect.center,self.radius)


#ステージのクラス
class Stage():
	def __init__(self, data):
		#空のリストを用意
		self.tile_list = []

		#のちに用意するstageの番号1を地面とし、リストに位置とサイズ情報を格納していく
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pg.Surface((tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				col_count += 1
			row_count += 1

	#上で得たリスト情報を元にスクリーンに描画する	
	def draw(self,screen):
		for tile in self.tile_list:
			#tile[1]にはrectサイズの情報が入っている。tile[0]には画像が入っている
			pg.draw.rect(screen, (80, 80, 80), tile[1])

#ステージのデータ。1が足場、０は何も描画しない。好きに変更することができます
stage_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1]
]

#ゲームクラス	
class Game():
	def __init__(self):
		pg.init()

		self.screen = pg.display.set_mode((screen_width, screen_height))
		pg.display.set_caption('JumpQueen')	
		self.clock = pg.time.Clock()
		self.fps = 60

		#クラスのインスタンス化
		self.stage = Stage(stage_data)
		self.player = Player(100, 500)

		#鍵のフラグ
		self.key_appear = True
		
	#溝に落っこちた後の処理
	def respawn(self):
		self.player = Player(100, 400)

	#テキスト描画メソッド。ゲームクリア時に使用
	def draw_text(self, text, size, x, y, color):
		font = pg.font.Font(None, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface,text_rect)
		
	#メインループ処理
	def main(self):
		running = True
		while running:	
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						running = False

			#画面全体を白に
			self.screen.fill((177,223,228))
			
			#鍵の描画（ただの黄色い四角ですが・・・）
			if self.key_appear:
				key = pg.draw.rect(self.screen,(255, 250, 0),(25, 50, 25, 25))
				pg.draw.rect(self.screen,(0, 0, 0),(25, 50, 25, 25),2)
			
			#鍵をとった時の処理
			if self.key_appear == False:
				#出口を出現させる
				exit = pg.draw.rect(self.screen,(30,30,30),(screen_width - 75, 25, 50, 50))
				pg.draw.rect(self.screen,(255, 0, 0),(screen_width - 75, 25, 50, 50),4)
				#出口に到着した時の処理
				if self.player.rect.colliderect(exit):
					self.draw_text('CLEAR!', 70, screen_width / 2, int(screen_height * 0.45), (150, 150, 0))

			#ステージの描画
			self.stage.draw(self.screen)

			#プレイヤーと鍵の衝突判定
			if self.player.rect.colliderect(key):
				self.key_appear = False			
				
			#プレイヤーが溝に落っこちた時の処理
			if self.player.dead:
				self.respawn()
				self.player.dead = False
				self.key_appear = True

			#プレイヤーのメソッド呼び出し
			self.player.update(self.screen,self.stage.tile_list)
			self.clock.tick(self.fps)
			pg.display.update()

		pg.quit()

game = Game()
game.main()
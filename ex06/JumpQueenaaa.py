import pygame as pg
from pygame.locals import *
import sys

def check_bound(obj_rct, scr_rct):
    """"
    obj_rct:こうかとんrct、または、爆弾rct
    sct_rct:スクリーンrct
    領域内：+1/領域外:-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1.1 # 3:速度の変化
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1.1
    return yoko, tate

def main():
    pg.display.set_caption("JumpQueen")
    scrn_sfc = pg.display.set_mode((1600, 800))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    cc_sfc = pg.image.load("fig/2.png")
    cc_rct = cc_sfc.get_rect()
    cc_rct.center = 800, 700

    while True:
        scrn_sfc.blit(bg_sfc, bg_rct)
        for event in pg.event.get():
            if event.type == QUIT: # ×ボタン
                pg.quit()
                sys.exit()

        key_states = pg.key.get_pressed() 

        if key_states[pg.K_UP]:    cc_rct.centery -= 1
        if key_states[pg.K_LEFT]:  cc_rct.centerx -= 1
        if key_states[pg.K_RIGHT]: cc_rct.centerx += 1

        yoko, tate = check_bound(cc_rct, scrn_rct)
        if yoko == -1:
            if key_states[pg.K_LEFT]:
                cc_rct.centerx += 1
            if key_states[pg.K_RIGHT]:
                cc_rct.centerx -= 1
        if tate == -1:
            if key_states[pg.K_UP]:
                cc_rct.centery += 1

        scrn_sfc.blit(cc_sfc, cc_rct)


        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
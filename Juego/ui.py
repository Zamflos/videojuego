# ui.py → VERSIÓN ULTRA SEGURA (FUNCIONA EN TU PC GARANTIZADO)
import pygame
import math
from constants import *

class UI:
    def __init__(self):
        self.bar_width = 80
        self.bar_height = 6

    def draw(self, screen, player, puzzle, alert=False):
        # BARRAS
        pygame.draw.rect(screen, (70,70,70), (10, 10, 80, 6))
        ew = int(player.shadow_energy * 80 / player.max_shadow_energy)
        pygame.draw.rect(screen, (0,120,255), (10, 10, ew, 6))

        pygame.draw.rect(screen, (70,70,70), (10, 20, 80, 6))
        pygame.draw.rect(screen, (220,20,20), (10, 20, int(player.health*0.8), 6))

        frag = FONT.render(f'Frag: {puzzle.fragments}/5', True, (255,255,255))
        screen.blit(frag, (SCREEN_WIDTH-100, 10))

        if alert:
            a = FONT.render('ALERTA!', True, (255,140,0))
            screen.blit(a, (SCREEN_WIDTH//2-50, SCREEN_HEIGHT//2-20))

        # PUZZLE VISUAL – COLORES 100% SEGUROS
        if puzzle.active:
            x = SCREEN_WIDTH//2 - 120
            y = 45
            size = 45
            r = 22

            progress = len(puzzle.player_sequence)
            seq = puzzle.current_sequence

            # COLORES FIJOS Y SEGUROS
            c1 = (50,150,255)   # 1
            c2 = (50,255,100)   # 2
            c3 = (255,180,50)   # 3

            for i in range(len(seq)):
                num = seq[i]
                base = c1 if num == '1' else c2 if num == '2' else c3

                cx = x + i*(size+8) + r
                cy = y + r
                center = (cx, cy)

                # COLORES CAPADOS A 255 (nunca más de 255)
                if i < progress:
                    bg = (0, 200, 0)
                    glow = (0, 255, 120)
                elif i == progress:
                    # Pulso seguro (nunca supera 255)
                    pulse = int(100 + 80 * (math.sin(pygame.time.get_ticks() * 0.008) + 1) * 0.5)
                    bg = (
                        min(255, base[0] + pulse//2),
                        min(255, base[1] + pulse//2),
                        min(255, base[2] + pulse//2)
                    )
                    glow = (0, 220, 255)
                else:
                    bg = (base[0]//3+40, base[1]//3+40, base[2]//3+40)
                    glow = None

                # Glow
                if glow:
                    pygame.draw.circle(screen, glow, center, r+14, 5)
                    pygame.draw.circle(screen, glow, center, r+9, 3)

                # Círculo principal
                pygame.draw.circle(screen, bg, center, r)
                pygame.draw.circle(screen, (255,255,255), center, r, 4)

                # Número con sombra (perfecto)
                txt = FONT.render(num, True, (255,255,255))
                sh = FONT.render(num, True, (0,0,0))
                screen.blit(sh, (cx-11, cy-11))
                screen.blit(txt, (cx-10, cy-10))

            # Barra progreso
            bw = len(seq)*(size+8)-8
            pygame.draw.rect(screen, (60,60,60), (x, y+size+8, bw, 6))
            pygame.draw.rect(screen, (0,120,255), (x, y+size+8, int(progress/len(seq)*bw), 6))

            # Timer
            tc = (0,255,0) if puzzle.timer > 5 else (255,160,0) if puzzle.timer > 2 else (220,20,20)
            t = FONT.render(f'Time: {puzzle.timer:.1f}', True, tc)
            screen.blit(t, (SCREEN_WIDTH//2+40, y))

            h = FONT.render('1     2     3', True, (220,220,220))
            screen.blit(h, (x+15, y+size+30))

    def show_message(self, msg, col, lista):
        lista.append({"text": msg, "color": col, "remaining_time": 3.0})

    def show_partial_hint(self, seq, lista):
        half = ' '.join(seq[:len(seq)//2])
        lista.append({"text": f'Hint: {half} ...', "color": (255,255,255), "remaining_time": 4.0})
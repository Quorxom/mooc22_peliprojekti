# MOOC Ohjelmointi 2022, peliprojekti

# Peli:
# - Ruudulla pelialue ja valikko&pisteet alue
# - Käyttäjä liikuttaa nuolinäppäimillä roboa
# - Tarkoitus kerätä kolikoita kentältä --> piste per kolikko
# - Kentällä myös hirviöitä, jotka liikkuu. Jos hirviöön osuu, tulee osumapisteitä +1 ja peli päättyy kun kolme osumaa on tullut. Hirviöitä ilmestyy lisää kun pisteiden määrä kasvaa.
# - Muut komennot: uusi peli, poistu

# Ajatuksia:
# - Kahdesta ovesta voisi tehdä teleportin

import pygame
from random import randint

class PeliHahmo:

    def __init__(self, kuva: str):
        self.pgobj = pygame.image.load(kuva)
        self.x = 0
        self.y = 0
        self.nopeus = 0
        self.dx = 0
        self.dy = 0
        self.vasemmalle = False
        self.oikealle = False
        self.alas = False
        self.ylos = False

    @property
    def paikka(self):
        return self.x, self.y

    @property
    def to_blit(self):
        return self.pgobj, (self.x, self.y)
    
    @property
    def w(self):
        return self.pgobj.get_width()
    
    @property
    def h(self):
        return self.pgobj.get_height()

    def arvo_paikka(self, x_vali: tuple, y_vali: tuple):
        self.x = randint(x_vali[0], x_vali[1])
        self.y = randint(y_vali[0], y_vali[1])

    def osui(self, toinen_hahmo: 'PeliHahmo'):
        # Osuiko pelihahmot toisiinsa: True tai false
        pass


# class Roboliini(PeliHahmo):

#     def __init__(self, kuva: str='robo.png'):
#         super().__init__(kuva)


# class Hirvio(PeliHahmo):

#     def __init__(self, kuva: str='hirvio.png'):
#         super().__init__(kuva)


class KolikonKeraily:

    def __init__(self):
        self.nayton_leveys = 640
        self.nayton_korkeus = 480
        self.valikon_korkeus = 40
        self.kartan_leveys = self.nayton_leveys
        self.kartan_korkeus = self.nayton_korkeus - self.valikon_korkeus

        self.kartan_vari = (230, 230, 230)

        pygame.init()
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
        pygame.display.set_caption("Keräilypeli")
        
        self.alusta_peli()

        self.pelaa()
    
    def luo_hirvio(self):
        # Luo uuden hirviön, joka on sopivan kaukana robosta
        # Arvotaan siis paikkaa kunnes löytyy sopiva
        pass

    def luo_kolikko(self):
        # Luo uuden kolikon sopivaan paikkaan pelilaudalle
        self.kolikko = PeliHahmo('kolikko.png')
        self.kolikko.nopeus = 0


    def alusta_peli(self):
        # Alusta pisteet yms.
        self.pisteet = 0
        self.elamat = 3
        
        # Luo uusi robo
        self.robo = PeliHahmo('robo.png')
        self.robo.nopeus = 2
        self.robo.arvo_paikka(
            (0, self.kartan_leveys - self.robo.w),
            (0, self.kartan_korkeus - self.robo.h)
        )

        # Alusta lista hirviöistä
        self.hirviot = []

        # Alusta kolikko
        self.luo_kolikko()

    def liikuta_roboa(self):
        pass

    def liikuta_hirviota(self):
        pass

    def piirra_naytto(self):
        self.naytto.fill(self.kartan_vari)

        self.naytto.blit(*self.robo.to_blit)

        pygame.display.flip()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            # Ohjelmaikkunan sulkeminen
            if tapahtuma.type == pygame.QUIT:
                exit()

            # Valikon toiminnot
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                if tapahtuma.key == pygame.K_F2:
                    self.alusta_peli()

            # Robon liikuttelu
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_DOWN:
                    self.robo.alas = True
                if tapahtuma.key == pygame.K_UP:
                    self.robo.ylos = True
                if tapahtuma.key == pygame.K_LEFT:
                    self.robo.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.robo.oikealle = True
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_DOWN:
                    self.robo.alas = False
                if tapahtuma.key == pygame.K_UP:
                    self.robo.ylos = False
                if tapahtuma.key == pygame.K_LEFT:
                    self.robo.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.robo.oikealle = False

    def pelaa(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()

KolikonKeraily().pelaa()

# MOOC Ohjelmointi 2022, peliprojekti

# Peli:
# - Ruudulla pelialue ja valikko&pisteet alue
# - Käyttäjä liikuttaa nuolinäppäimillä roboa
# - Tarkoitus kerätä kolikoita kentältä --> piste per kolikko
# - Kentällä myös hirviöitä, jotka liikkuu. Jos hirviöön osuu, tulee osumapisteitä +1 ja peli päättyy kun kolme osumaa on tullut. Hirviöitä ilmestyy lisää kun pisteiden määrä kasvaa.
# - Muut komennot: uusi peli, poistu

import pygame
from random import randint, choice
from functools import reduce


class PeliKentta:

    def __init__(self, leveys_pikselia: int, korkeus_pikselia: int):
        self.leveys = leveys_pikselia
        self.korkeus = korkeus_pikselia

    @property
    def x_vali(self):
        return (0, self.leveys)
    
    @property
    def y_vali(self):
        return (0, self.korkeus)
    

class PeliHahmo:

    def __init__(self, kuva: str):
        self.pgobj = pygame.image.load(kuva)
        self.x = 0
        self.y = 0
        self.nopeus = 0

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

    @property
    def keskipiste(self):
        return (self.x + 0.5 * self.w, self.y + 0.5 * self.h)

    def arvo_paikka(self, alue_x_rajat: tuple, alue_y_rajat: tuple):
        # Alueen rajat eli reunojen koordinaatit
        self.x = randint(alue_x_rajat[0], alue_x_rajat[1] - self.w)
        self.y = randint(alue_y_rajat[0], alue_y_rajat[1] - self.h)

    # def arvo_suunta(self):
    #     # alas, ylös, vasemmalle, oikealle
    #     vaihtoehdot = [
    #         (True, False, False, False),
    #         (False, True, False, False),
    #         (False, False, False, True),
    #         (False, False, True, False),
    #         (False, True, False, True),
    #         (False, True, True, False),
    #         (True, False, False, True),
    #         (True, False, True, False),
    #     ]
    #     self.alas, self.ylos, self.vasemmalle, self.oikealle = choice(vaihtoehdot)

    # def koskettaa_seinaa(self, alue_x_rajat: tuple, alue_y_rajat: tuple):
        # Alueen rajat eli reunojen koordinaatit: alue_x_rajat: tuple, alue_y_rajat: tuple
        # Palauttaa True, jos hahmo osuus alueen seinään (reunaan) tai on sen ulkopuolella
        # osuu_seinaan = ((self.y + self.h >= alue_y_rajat[1]) or
        #     (self.y <= alue_y_rajat[0]) or
        #     (self.x + self.w >= alue_x_rajat[1]) or
        #     (self.x <= alue_x_rajat[0])
        # )
        # return osuu_seinaan

    def liikuta(self, alue_x_rajat: tuple, alue_y_rajat: tuple):
        return self._toteuta_liikutus(alue_x_rajat, alue_y_rajat)

    def _toteuta_liikutus(self, alue_x_rajat: tuple, alue_y_rajat: tuple):
        print('PeliHahmon liikutus')
        return False

    def etaisyys(self, toinen_hahmo: 'PeliHahmo'):
        # Palauttaa kahden PeliHahmo-olion keskipisteiden välisen etäisyyden
        kp_self = self.keskipiste
        kp_toinen_hahmo = toinen_hahmo.keskipiste
        return ((kp_self[0] - kp_toinen_hahmo[0])**2 + (kp_self[1] - kp_toinen_hahmo[1])**2)**0.5

    def osui(self, toinen_hahmo: 'PeliHahmo'):
        # Osuiko pelihahmot toisiinsa: True tai false
        x_osuma = (self.x <= toinen_hahmo.x <= self.x + self.w) or (self.x <= toinen_hahmo.x + toinen_hahmo.w <= self.x + self.w)
        y_osuma = (self.y <= toinen_hahmo.y <= self.y + self.h) or (self.y <= toinen_hahmo.y + toinen_hahmo.h <= self.y + self.h)
        return x_osuma and y_osuma


class Roboliini(PeliHahmo):

    def __init__(self, kuva: str='robo.png'):
        super().__init__(kuva)
        self.nopeus = 2
        self.vasemmalle = False
        self.oikealle = False
        self.alas = False
        self.ylos = False

    def _toteuta_liikutus(self, alue_x_rajat: tuple, alue_y_rajat: tuple):
        liike_onnistui = False
        if self.alas and self.y + self.h <= alue_y_rajat[1]:
            self.y += self.nopeus
            liike_onnistui = True
        if self.ylos and self.y >= alue_y_rajat[0]:
            self.y -= self.nopeus
            liike_onnistui = True
        if self.oikealle and self.x + self.w <= alue_x_rajat[1]:
            self.x += self.nopeus
            liike_onnistui = True
        if self.vasemmalle and self.x >= alue_x_rajat[0]:
            self.x -= self.nopeus
            liike_onnistui = True
        return liike_onnistui


class Hirvio(PeliHahmo):

    def __init__(self, kuva: str='hirvio.png'):
        super().__init__(kuva)
        self.nopeus = 1
        self.dx, self.dy = self._alusta_suunta()

    def _arvo_suunta(self):
        return choice([-1, 0, 1])

    def _alusta_suunta(self):
        pysyy_paikallaan = True
        while pysyy_paikallaan:
            dx = self._arvo_suunta()
            dy = self._arvo_suunta()
            pysyy_paikallaan = dx == 0 and dy == 0
        return dx, dy

    def _toteuta_liikutus(self, alue_x_rajat: tuple, alue_y_rajat: tuple):
        if self.y + self.h >= alue_y_rajat[1]:
            self.dy = -1
            self.dx = self._arvo_suunta()
        if self.y <= alue_y_rajat[0]:
            self.dy = 1
            self.dx = self._arvo_suunta()
        if self.x + self.w >= alue_x_rajat[1]:
            self.dx = -1
            self.dy = self._arvo_suunta()
        if self.x <= alue_x_rajat[0]:
            self.dx = 1
            self.dy = self._arvo_suunta()
        self.x += self.dx * self.nopeus
        self.y += self.dy * self.nopeus
        return True



class KolikonKeraily:

    def __init__(self):
        self.nayton_leveys = 640
        self.nayton_korkeus = 480
        self.valikon_korkeus = 40
        self.kartan_leveys = self.nayton_leveys
        self.kartan_korkeus = self.nayton_korkeus - self.valikon_korkeus

        self.kartan_vari = (230, 230, 230)

        self.kolikko_robo_min_etaisyys = 100
        self.hirvio_robo_min_etaisyys = 100
        self.hirvio_hirvio_min_etaisyys = 80
        self.maks_maara_hirvioita = 8
        self.luo_uusi_hirvio_per_pistemaara = 5

        pygame.init()
        self.naytto = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
        pygame.display.set_caption("Keräilypeli")
        self.kello = pygame.time.Clock()

        self.valikko_fontti = pygame.font.SysFont('Arial', 20)
         
        self.alusta_peli()

        self.pelaa()

    def luo_kolikko(self):
        # Luo uuden kolikon, joka on sopivan kaukana robosta
        self.kolikko = PeliHahmo('kolikko.png')
        self.kolikko.nopeus = 0
        for i in range(10):
            self.kolikko.arvo_paikka(
                (0, self.kartan_leveys),
                (0, self.kartan_korkeus)
            )
            if self.kolikko.etaisyys(self.robo) < self.kolikko_robo_min_etaisyys:
                continue
            break

    def alusta_peli(self):
        # Alusta pisteet yms.
        self.pisteet = 0
        self.elamat = 3
        
        # Luo uusi robo
        # self.robo = PeliHahmo('robo.png')
        self.robo = Roboliini()
        self.robo.nopeus = 2
        self.robo.arvo_paikka(
            (0, self.kartan_leveys),
            (0, self.kartan_korkeus)
        )

        # Alusta lista hirviöistä
        self.hirviot = []

        # Alusta kolikko
        self.luo_kolikko()

    def lopeta_peli(self):
        exit()

    def kierros_ohi(self):
        return self.elamat < 1

    def liikuta_roboa(self):
        liike_onnistui = self.robo.liikuta(
            (0, self.kartan_leveys),
            (0, self.kartan_korkeus)
        )
        # print('Robon liike ok?  ', liike_onnistui)

    def luo_hirvio(self):
        # Luo uuden hirviön saavutetun pistemäärä mukaan: joka 10. piste tuo uuden hirviön peliin kunnes maksimimäärä on saavutettu (self.maks_maara_hirvioita).
        # Uusi hirvio on sopivan kaukana robosta ja muista hirvioista
        # print('hirvioita', len(self.hirviot))
        if len(self.hirviot) >= min(self.maks_maara_hirvioita, self.pisteet // self.luo_uusi_hirvio_per_pistemaara):
            # print('Hirvöitä maksimimäärä')
            return

        # print('Luodaanko uusi hirvio, testitulos', self.pisteet, self.luo_uusi_hirvio_per_pistemaara, self.pisteet % self.luo_uusi_hirvio_per_pistemaara)
        # print('Luodaan uusi hirvio')
        hirvio = Hirvio()
        for i in range(10):
            hirvio.arvo_paikka(
                (0, self.kartan_leveys),
                (0, self.kartan_korkeus)
            )
            paikka_tarkistukset = [hirvio.etaisyys(self.robo) < self.hirvio_robo_min_etaisyys]
            paikka_tarkistukset += [hirvio.etaisyys(h) < self.hirvio_hirvio_min_etaisyys for h in self.hirviot]
            if reduce(lambda x, y: x or y, paikka_tarkistukset):
                continue
            break
        # print('hirvio iteraatioita:', i)
        self.hirviot.append(hirvio)

    def liikuta_hirviot(self):
        for hirvio in self.hirviot:
            liike_onnistui = hirvio.liikuta(
                (0, self.kartan_leveys),
                (0, self.kartan_korkeus)
            )

    def tutki_osumat_hirvioihin(self):
        # print('hirvioita nyt:', len(self.hirviot))
        hirviot_jaljella = []
        for hirvio in self.hirviot:
            if self.robo.osui(hirvio):
                self.elamat -= 1
            else:
                hirviot_jaljella.append(hirvio)
        self.hirviot = hirviot_jaljella
        # print('   hirvioita jää:', len(self.hirviot))

    def luo_valikkopalkki(self):
        # Luo ja palauttaa valikkopalkki-objektin
        # Värit yms. säädöt
        marginaali = 9
        taustavari = (0, 0, 0)
        tekstin_vari = (240, 0, 0)
        erotin_vari = (180, 0, 0)
        erotin_paksuus = 4
        hela_taustavari = (180, 0, 0)
        hela_ok_vari = (0, 200, 0)
        hela_elaman_pituus = 40
        hela_erotin_paksuus = 2
        hela_erotin_vari = (120, 120, 120)
        y0 = self.nayton_korkeus - self.valikon_korkeus + marginaali
        # Valikkopalkki-objekti, tausta ja vaakaerotin
        valikkopalkki = pygame.Surface((self.nayton_leveys, self.nayton_korkeus))
        valikkopalkki.fill(taustavari)
        pygame.draw.line(
            valikkopalkki, erotin_vari, 
            (0, 0), 
            (valikkopalkki.get_width(), 0), 
            width=erotin_paksuus
        )
        # Pystyerottimet ja tekstit
        valikkopalkki.blit(
            self.valikko_fontti.render('ESC: Poistu', True, tekstin_vari), 
            (marginaali, marginaali)
        )
        valikkopalkki.blit(
            self.valikko_fontti.render('F2: Uusi peli', True, tekstin_vari),
            (marginaali + 140, marginaali)
        )
        pygame.draw.line(
            valikkopalkki, erotin_vari,
            (280, 0),
            (280, valikkopalkki.get_height()),
            width=erotin_paksuus
        )
        valikkopalkki.blit(
            self.valikko_fontti.render('Helaa: ', True, tekstin_vari),
            (marginaali + 280, marginaali)
        )
        pygame.draw.line(
            valikkopalkki, erotin_vari,
            (500, 0),
            (500, valikkopalkki.get_height()),
            width=erotin_paksuus
        )
        valikkopalkki.blit(
            self.valikko_fontti.render('Pojot: ' + str(self.pisteet), True, tekstin_vari),
            (marginaali + 500, marginaali)
        )
        # Hela-palkki
        hela_palkki = pygame.Surface((3 * hela_elaman_pituus + hela_erotin_paksuus, self.valikon_korkeus - 2 * marginaali))
        hela_palkki.fill(hela_taustavari)
        for i in range(3):
            if i < self.elamat:
                pygame.draw.rect(
                    hela_palkki, hela_ok_vari,
                    (i * hela_elaman_pituus, 0, hela_elaman_pituus, hela_palkki.get_height())
                )
            pygame.draw.line(
                hela_palkki, hela_erotin_vari,
                (i * hela_elaman_pituus, 0),
                (i * hela_elaman_pituus, hela_palkki.get_height()),
                width=hela_erotin_paksuus
            )
        pygame.draw.rect(
            hela_palkki, hela_erotin_vari,
            (0, 0, hela_palkki.get_width(), hela_palkki.get_height()),
            width=hela_erotin_paksuus
        )
        valikkopalkki.blit(
            hela_palkki,
            (490 - 3 * hela_elaman_pituus - marginaali, marginaali)
        )
        return valikkopalkki

    def luo_kierros_ohi_ruutu(self):
        # Luo ja palauttaa pygame.Surface objektin jossa on kierroksen lopputulos
        # Parametrit ja säädöt:
        koko = (0.6, 0.6)
        taustavari = (0, 0, 0)
        reunuksen_vari = (230, 0, 0)
        reunuksen_paksuus = 5
        tekstin_vari = (230, 0, 0)
        fontti_iso = pygame.font.SysFont('Arial', 42, bold=True)
        # Tulosruutu
        tulosruutu = pygame.Surface((
            int(koko[0] * self.nayton_leveys),
            int(koko[1] * self.nayton_korkeus)
        ))
        tulosruutu.fill(taustavari)
        pygame.draw.rect(
            tulosruutu, reunuksen_vari,
            (0, 0, tulosruutu.get_width(), tulosruutu.get_height()),
            width=reunuksen_paksuus
        )
        # Tekstit
        otsikko = fontti_iso.render('LOPPUTULOS:', True, tekstin_vari)
        loppupisteet = fontti_iso.render(str(self.pisteet), True, tekstin_vari)
        y0_otsikko = int(0.25 * tulosruutu.get_height())
        tulosruutu.blit(
            otsikko, 
            (
                int(0.5 * (tulosruutu.get_width() - otsikko.get_width()) ), 
                y0_otsikko
            )
        )
        tulosruutu.blit(
            loppupisteet,
            (
                int(0.5 * (tulosruutu.get_width() - loppupisteet.get_width()) ), 
                y0_otsikko + otsikko.get_height() + 10
            )
        )
        poistu = self.valikko_fontti.render('ESC: Poistu', True, tekstin_vari)
        uusipeli = self.valikko_fontti.render('F2: Uusi peli', True, tekstin_vari)
        y0 = tulosruutu.get_height() - max(poistu.get_height(), uusipeli.get_height()) - 20
        tulosruutu.blit(poistu, (20, y0))
        tulosruutu.blit(uusipeli, (tulosruutu.get_width() - uusipeli.get_width() - 20, y0))
        return tulosruutu

    def piirra_naytto(self):
        # Tyhjennys
        self.naytto.fill(self.kartan_vari)

        # Pelihahmot
        self.naytto.blit(*self.kolikko.to_blit)
        self.naytto.blits([h.to_blit for h in self.hirviot])
        self.naytto.blit(*self.robo.to_blit)

        # Valikkopalkki
        self.naytto.blit(
            self.luo_valikkopalkki(),
            (0, self.nayton_korkeus - self.valikon_korkeus)
        )

        # Piirrä Lopputulos--ruutu, jos pelikierros on ohi
        if self.kierros_ohi():
            tulosruutu = self.luo_kierros_ohi_ruutu()
            self.naytto.blit(
                tulosruutu,
                (
                    int(0.5 * (self.nayton_leveys - tulosruutu.get_width())),
                    int(0.5 * (self.nayton_korkeus - tulosruutu.get_height())),
                )
            )

        # Piirto
        pygame.display.flip()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            # Ohjelmaikkunan sulkeminen
            if tapahtuma.type == pygame.QUIT:
                self.lopeta_peli()
            # Valikon toiminnot
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    self.lopeta_peli()
                if tapahtuma.key == pygame.K_F2:
                    self.alusta_peli()
                if tapahtuma.key == pygame.K_F3:
                    self.luo_kolikko()
                if tapahtuma.key == pygame.K_F4:
                    self.luo_hirvio()
                if tapahtuma.key == pygame.K_F5:
                    self.elamat += 1
                    self.elamat = self.elamat % 4
                    print('elamat:', self.elamat)
                if tapahtuma.key == pygame.K_F12:
                    self.elamat = 0
            # Robon liike
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

            if self.robo.osui(self.kolikko):
                self.pisteet += 1
                self.luo_kolikko()

            self.tutki_osumat_hirvioihin()

            if not self.kierros_ohi():
                # Pelikierros jatkuu
                self.luo_hirvio()

                self.liikuta_hirviot()
                
                self.liikuta_roboa()
            # else:
            #     print('KIERROS OHI!!!!!!1!')

            if len(self.hirviot) > 0:
                print('Hirviöitä:', len(self.hirviot))

            self.piirra_naytto()

            self.kello.tick(60)

KolikonKeraily().pelaa()

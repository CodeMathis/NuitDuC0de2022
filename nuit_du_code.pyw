import pyxel
from random import randint

"""
-------- DUNGEON SIMULATOR --------
Un jeu réalisé par Athur et Mathis.

Appuyer sur les flèches directionnelles pour vous déplacer.
Espace pour tirer,
D pour acheter un boost de degat contre 250 d'argent,
A pour acheter un boost d'argent contre 500 d'argent et
V pour acheter un boost de vitesse contre 500 d'argent (limité à 4 achat).

Le but est de faire le meilleur score tout en changeant de salle. Pour gagner du score il faut éliminer des ennemis mais attention à ne pas les touchers !

Appuyer sur R pour recommencer à tout moment et Q pour quitter.
"""

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du c0de 2022")
        pyxel.load("arthur_mathis.pyxres")
        pyxel.playm(0, loop=True)

        self.score = 0
        self.best_score = 0
        self.argent = 0
        self.liste_ennemi = []
        self.col = 12
        self.boost_dgt = 0
        self.boost_argent = 1
        self.boost_vitesse = 1
        self.boost_tire = 1
        self.d = 0
        self.a = 0
        self.v = 0
        self.t = 0
        self.liste_tire = []
        self.nouvelle_salle = True
        self.x = 60
        self.y = 60
        self.co_salle=[(128,128),(152,128)]
        self.salle_right=[(128,128),(152,128),(128,152),(176,128)]
        self.salle_left=[(128,128),(152,128),(128,152),(176,152)]
        self.salle_up=[(96,152),(128,128),(152,152),(152,128),(176,176),(176,152)]
        self.salle_down=[(96,128),(176,128),(152,128),(128,128),(152,152),(96,152)]
        self.salle_secrete=[(72,104)]
        self.i=0
        self.direction_visee = "H"
        self.compteur = 0
        self.compteur2 = 0
        self.menu = True
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

        if self.compteur < 25:
            self.compteur += 1
        if self.compteur2 < 500:
            self.compteur2 += 1
            
        self.changement_salle()
        self.deplacement_perso()

    def draw(self):
        if self.menu == True:
            pyxel.bltm(0, 0, 0, self.co_salle[self.i][0]*8, self.co_salle[self.i][1]*8, 128, 128)
            pyxel.text(7, 20, "Appuyez sur ESPACE pour jouer", 6)
            pyxel.text(30, 40, "Meilleur score : "+str(self.best_score), 10)
            pyxel.text(1, 52, "D: 250 argent pour + de degat", 3)
            pyxel.text(1, 58, "A: 500 argent pour + d'argent", 3)
            pyxel.text(1, 64, "V: 500 argent pour + de vitesse", 3)
            pyxel.text(1, 70, "T: 1000 argent pour + 1 tire", 3)
            pyxel.text(28, 80, "R pour recommencer", 3)            
            if pyxel.btn(pyxel.KEY_SPACE):
                self.menu = False
            
        else:    
            pyxel.bltm(0, 0, 0, self.co_salle[self.i][0]*8, self.co_salle[self.i][1]*8, 128, 128)
            personnage = pyxel.rect(self.x, self.y, 8, 8, self.col)
            pyxel.text(85-(self.score*0.001), 8, "Score:"+str(self.score), 13)
            pyxel.text(8, 115, "D:"+str(self.d), 13)
            pyxel.text(32, 115, "A:"+str(self.a), 13)
            pyxel.text(73, 115, "V:"+str(self.v), 13)
            pyxel.text(97, 115, "T:"+str(self.t), 13)
            
            self.tire()
            self.monnaie()
            self.ennemi()            

    def deplacement_perso(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and pyxel.tilemap(0).pget((self.x + 8) % pyxel.width//8+self.co_salle[self.i][0],self.y//8+self.co_salle[self.i][1]) in [(1,5),(4,4),(8,4)] and pyxel.tilemap(0).pget((self.x + 8) % pyxel.width//8+self.co_salle[self.i][0],(self.y + 7) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4),(8,4)]:
            self.x = (self.x + 1*self.boost_vitesse) % pyxel.width
            
        if pyxel.btn(pyxel.KEY_LEFT) and pyxel.tilemap(0).pget((self.x - 1) % pyxel.width//8+self.co_salle[self.i][0],self.y//8+self.co_salle[self.i][1])in [(1,5),(4,4),(10,4)] and pyxel.tilemap(0).pget((self.x - 1) % pyxel.width//8+self.co_salle[self.i][0],(self.y + 7) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4),(10,4)]:
            self.x = (self.x - 1*self.boost_vitesse) % pyxel.width
            
        if pyxel.btn(pyxel.KEY_UP) and pyxel.tilemap(0).pget(self.x//8+self.co_salle[self.i][0],(self.y - 1) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4),(9,5)] and pyxel.tilemap(0).pget((self.x + 7) % pyxel.width//8+self.co_salle[self.i][0],(self.y - 1) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4),(9,5)]:
            self.y = (self.y - 1*self.boost_vitesse) % pyxel.width
            
        if pyxel.btn(pyxel.KEY_DOWN) and pyxel.tilemap(0).pget(self.x//8+self.co_salle[self.i][0],(self.y + 8) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4),(9,3)] and pyxel.tilemap(0).pget((self.x + 7) % pyxel.width//8+self.co_salle[self.i][0],(self.y + 8) % pyxel.width//8+self.co_salle[self.i][1]) in [(1,5),(4,4),(9,3)]:
            self.y = (self.y + 1*self.boost_vitesse) % pyxel.width

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction_visee = "D"
            
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction_visee = "G"
            
        if pyxel.btn(pyxel.KEY_UP):
            self.direction_visee = "H"
            
        if pyxel.btn(pyxel.KEY_DOWN):
            self.direction_visee = "B"

        for i in self.liste_ennemi:
            if i["x"]-(i["taille"]+8) < self.x < i["x"]+(i["taille"]+2) and i["y"]-(i["taille"]+8) < self.y < i["y"]+(i["taille"]+2) and self.compteur >= 25:
                self.compteur = 0
                if self.col == 12:
                    self.col = 5
                elif self.col == 5:
                    self.col = 1
                elif self.col == 1:
                    self.reset()
            

    def tire(self):
        if self.nouvelle_salle == True:
            self.liste_tire = []
            
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.compteur2 == 500:
                self.compteur2 = 0
                for i in range(self.boost_tire):
                    if i % 2 == 0:
                        self.liste_tire.append({"direction":self.direction_visee,"x":self.x+4+i, "y":self.y+4+i, "taille":4})
                    else:
                        self.liste_tire.append({"direction":self.direction_visee,"x":self.x+4-i, "y":self.y+4-i, "taille":4})
            else:
                for i in range(self.boost_tire):
                    if i % 2 == 0:
                        self.liste_tire.append({"direction":self.direction_visee,"x":self.x+4+i, "y":self.y+4+i, "taille":2})
                    else:
                        self.liste_tire.append({"direction":self.direction_visee,"x":self.x+4-i, "y":self.y+4-i, "taille":2})

        for i in range(len(self.liste_tire)):     
            if self.liste_tire[i]["direction"] == "D":
                self.liste_tire[i]["x"] += 3
            elif self.liste_tire[i]["direction"] == "G":
                self.liste_tire[i]["x"] -= 3
            elif self.liste_tire[i]["direction"] == "H":
                self.liste_tire[i]["y"] -= 3
            elif self.liste_tire[i]["direction"] == "B":
                self.liste_tire[i]["y"] += 3
            pyxel.circb(self.liste_tire[i]["x"], self.liste_tire[i]["y"], self.liste_tire[i]["taille"], 6)
            for y in self.liste_ennemi:
                if y["x"]-(y["taille"]*1.5) < self.liste_tire[i]["x"] < y["x"]+(y["taille"]*1.5) and y["y"]-(y["taille"]*1.5) < self.liste_tire[i]["y"] < y["y"]+(y["taille"]*1.5):
                    if self.liste_tire[i]["taille"] == 4:
                        y["pv"] -= (1 + self.boost_dgt) * 2
                        y["col"] = 9
                    else:
                        y["pv"] -= 1 + self.boost_dgt
                        y["col"] = 9                        
            
    def ferme_salle(self,x,y):
        for i in range(2):
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1]) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1],(x,y))
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0]+15,self.co_salle[self.i][1]+7+i) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0]+15,self.co_salle[self.i][1]+7+i,(x,y))
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0],self.co_salle[self.i][1]+7+i) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0],self.co_salle[self.i][1]+7+i,(x,y))
            if pyxel.tilemap(0).pget(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1]+15) in [(1,5),(5,6)]:
                pyxel.tilemap(0).pset(self.co_salle[self.i][0]+7+i,self.co_salle[self.i][1]+15,(x,y))
                
    def ennemi(self):
        if self.nouvelle_salle == True:
            self.ferme_salle(5,6)
            self.nouvelle_salle = False
            self.liste_ennemi = []

            nbr_ennemis = randint(2, 4)
            while nbr_ennemis > 0:
                x_ennemi = randint(14, 106)
                y_ennemi = randint(14, 106)
                if x_ennemi-25 < self.x < x_ennemi+25 and y_ennemi-25 < self.y < y_ennemi+25:
                    pass
                else:
                    nbr_ennemis -= 1
                    boss = randint(1,10)
                    if boss == 1:
                        dictionnaire = {"pv":randint(50,75), "x":x_ennemi, "y":y_ennemi, "col":10, "taille":6}
                    else:
                        dictionnaire = {"pv":randint(25,50), "x":x_ennemi, "y":y_ennemi, "col":10, "taille":4}
                    self.liste_ennemi.append(dictionnaire) #creer un nombre aléatoire d'ennemis dans une liste avec des pv et coordonnée aléatoires
                    
        else:
            for i in self.liste_ennemi:
                if i["pv"] > 0 :
                    if i["x"] > self.x:
                        x_alea = randint(-2,0)
                    else:
                        x_alea = randint(0,2)
                    if i["y"] > self.y:
                        y_alea = randint(-2,0)
                    else:
                        y_alea = randint(0,2)

                    if 110 > i["x"]+x_alea > 10 and 110 > i["y"]+y_alea > 10:
                        mouvement = randint(1,5)
                        if mouvement == 1:
                            i["x"] += x_alea
                            i["y"] += y_alea
    
                    pyxel.circ(i["x"], i["y"], i["taille"], i["col"])
                    i["col"] = 10
                    
                elif i["pv"] <= 0:
                    #test boss
                    if i["taille"] == 6:
                        self.score += 20
                        self.argent += 30 * self.boost_argent
                    else:
                        self.score += 10
                        self.argent += 20 * self.boost_argent
                    self.liste_ennemi.pop(self.liste_ennemi.index(i))
            if self.liste_ennemi == []:
                self.ferme_salle(1,5)

                
    def changement_salle(self):
        if self.x <= 1 or self.x >= 127 or self.y <= 1 or self.y >= 127:
            if self.x >= 127:
                self.co_salle=self.salle_right
                self.x=8
                self.i=randint(0,len(self.co_salle)-1)
                
            if self.x <= 1:
                self.co_salle=self.salle_left
                self.x=112
                self.i=randint(0,len(self.co_salle)-1)
                
            if self.y <= 1:
                self.co_salle=self.salle_down
                self.y=112
                self.i=randint(0,len(self.co_salle)-1)
                
            if self.y >= 127:
                self.co_salle=self.salle_up
                self.y=8
                self.i=randint(0,len(self.co_salle)-1)
                
            self.nouvelle_salle = True

    def monnaie(self):
        pyxel.text(8, 8, "Argent :"+str(self.argent), 3)
        if pyxel.btn(pyxel.KEY_D) and self.argent >= 250:
            self.boost_dgt += 1
            self.d += 1
            self.argent -= 250
        if pyxel.btn(pyxel.KEY_A) and self.argent >= 500:
            self.boost_argent += 1
            self.a += 1
            self.argent -= 500
        if pyxel.btn(pyxel.KEY_V) and self.argent >= 500 and self.v < 5:
            self.boost_vitesse += 0.25
            self.v += 1
            self.argent -= 500
        if pyxel.btn(pyxel.KEY_T) and self.argent >= 1000 and self.t < 200:
            self.boost_tire += 1
            self.t += 1
            self.argent -= 1000
        #cheat
        if pyxel.btn(pyxel.KEY_N) and pyxel.btn(pyxel.KEY_O):
            self.argent += 10000

    def reset(self):
        if self.score > self.best_score:
            self.best_score = self.score
        self.score = 0
        self.argent = 0
        self.liste_ennemi = []
        self.col = 12
        self.boost_dgt = 0
        self.boost_argent = 1
        self.boost_vitesse = 1
        self.boost_tire = 1
        self.d = 0
        self.a = 0
        self.v = 0
        self.t = 0
        self.liste_tire = []
        self.nouvelle_salle = True
        self.x = 60
        self.y = 60
        self.co_salle=[(128,128),(152,128)]
        self.salle_right=[(128,128),(152,128),(128,152),(176,128)]
        self.salle_left=[(128,128),(152,128),(128,152),(176,152)]
        self.salle_up=[(96,152),(128,128),(152,152),(152,128),(176,176),(176,152)]
        self.salle_down=[(96,128),(176,128),(152,128),(128,128),(152,152),(96,152)]
        self.i=0
        self.direction_visee = "H"
        self.compteur = 0
        self.compteur2 = 0
        self.menu = True
        self.ferme_salle(1,5)

App()

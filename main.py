from __future__ import unicode_literals
import pygame
import sys
from googlesearch import search
import threading
import myclass
import myclasspg as pg


def proba_to_graph(proba):
    if 25 > proba >= 0:
        return  "IMG/graph/0.png"
    if 50 > proba >= 25:
        return  "IMG/graph/1.png"
    if 75 > proba >= 50:
        return "IMG/graph/2.png"
    if 100 > proba >= 75:
        return "IMG/graph/3.png"
    else:
        pass
    
    
#####################################
##       Fenetre du texte          ##
#####################################

download = False # on fait des sauvegardes pour le download
finished = False # on fait des sauvegardes pour le finished
def texte(nom_musique,lien_dl,parole,text,X,Y):
    global titre_chanson , download , finished
    
    titre_chanson = nom_musique
    
    d = {}
    
    pygame.init()
    
    icon = pygame.image.load("IMG/icon.png")
    
    pygame.display.set_icon(icon)

    pygame.display.set_caption("Scrapping")
    
    
    screen = pygame.display.set_mode([900, 500])# it will display on screen
    if download:
        img_dl = pg.img("IMG/chargement.png",840,47.5,60,60)
    elif finished:
        img_dl = pg.img("IMG/ok.png",840,47.5,60,60)
    else:
        img_dl = pg.bouton("IMG/dl.png",840,47.5,60,60)
    
    img_stat = pg.bouton("IMG/stat.png",840,132.5,60,60)
    
    img_cherch = pg.bouton("IMG/quit.png",47.5,47.5,60,60)
    
    while True:
        if download:
            if lien_dl.return_satus() == "finished": # si le téléchargement est fini
                img_dl = pg.img("IMG/ok.png",840,47.5,60,60) # on met un image comme quoi c'est fini
                download = False # on télécharge plus
                finished = True
                
        screen.fill((223, 242, 255))
        
        text.blit(screen)
            
        if download:
            img_dl.rotate_iblit(screen,1) # si on télécharge on met un image qui tourne sur elle meme
        else : 
            img_dl.iblit(screen)
        
        img_stat.iblit(screen)
        
        img_cherch.iblit(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:  # si une touche a été tapée, le marque dans le dictionnaire pressed la touche enfoncer
                d[event.key] = True
            if event.type == pygame.KEYUP:
                d[event.key] = False
            if not download: # si on télécharge pas
                if not finished: #  si on a pas fini de dl
                    if img_dl.click(pygame.mouse.get_pos(),event): # on peut cliquer sur le logo téléchargement
                        threading.Thread(target=lien_dl.start).start() # on lance un thread en parallèle qui lance le téléchargement
                        img_dl = pg.img("IMG/chargement.png",840,47.5,60,60) # on met l'image de chargment
                        download = True # on dit qu'on télécharge
                    
            if img_stat.click(pygame.mouse.get_pos(),event): # si on click sur le graph
                graphique(myclass.champ_lexical(parole).compter()) # on appelle la f graphique
                
            if img_cherch.click(pygame.mouse.get_pos(),event):
                debut()
                
        
        if d.get(pygame.K_UP):  # Si on monte
            if Y < 10: # on block pour pas monter trop haut 
                Y += 4
            X = X
            text.update((X,Y))
            
        if d.get(pygame.K_DOWN):  # Si on baisse
            if Y > -1000: # on block pour pas déscendre trop bas
                Y -= 4
            X = X
            text.update((X,Y))
      
        pygame.display.update()


#####################################
##       Fenetre du graphique      ##
#####################################
    
    
def graphique(d):
    global titre_chanson
    pygame.init()
    
    icon = pygame.image.load("IMG/icon.png")
    pygame.display.set_icon(icon)
    
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode([900, 500])# it will display on screen
    
    p_amour = round(d["conteur_amour"]*100,1) # on fait le proba
    p_rap = round(d["conteur_rap"]*100,1) # round pour arondir
    p_joie = round(d["conteur_joie"]*100,1)

    path_img1 = proba_to_graph(p_amour)
    path_img2 = proba_to_graph(p_rap)
    path_img3 = proba_to_graph(p_joie)

    img_quit = pg.bouton("IMG/quit.png",840, 60,50,50)

    while True:
                
        screen.fill((223, 242, 255))
        pg.img(path_img1,110,110,130,130).iblit(screen)
        pg.img(path_img2,110,250,130,130).iblit(screen)
        pg.img(path_img3,110,390,130,130).iblit(screen)
        img_quit.iblit(screen)
        

        pg.text(str(p_amour)+" % d'amour",110+130+10,110-65,"autre",color = (0,0,0), size = 70).iblit(screen) # on affiche les texts
        pg.text(str(p_rap)+" % sombre",110+130+10,250-65,"autre",color = (0,0,0), size = 70).iblit(screen) # on affiche les texts
        pg.text(str(p_joie)+" % joie",110+130+10,390-65,"autre",color = (0,0,0), size = 70).iblit(screen) # on affiche les texts
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if img_quit.click(pygame.mouse.get_pos(),event):
                nom_musique = str(titre_chanson)
                threading.Thread(target=charger, args=(nom_musique,)).start()
                chargement()
                
        pygame.display.update()
        clock.tick(60)


#####################################
##       Fenetre du debut          ##
#####################################


def debut():
    pygame.init()
    
    icon = pygame.image.load("IMG/icon.png")
    pygame.display.set_icon(icon)
    
    pygame.display.set_caption("Scrapping")
    
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode([900, 500])
        
    rect = pg.zone_ecriture(200,200, 500, 32,30, "lightskyblue3",color_t = "white") # on crée notre zone d'écriture
    
    nom_musique = ""
    
    while True:

        screen.fill((223, 242, 255))
        
        rect.iblit(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    rect.supr() # on suprime dans la zone de texte
                    
                elif event.key == pygame.K_RETURN:
                    threading.Thread(target=charger, args=(rect.nom,)).start() # on démare la fonction qui charge les trucs compliquer
                    chargement() # on démarre le chargement
                else:
                    rect.add(event) # on ajoute le texte a la zone de texte
        

        
        pygame.display.flip()
        clock.tick(60)


#####################################
##          chargement             ##
#####################################


def charger(nom_musique):
    """[fontion qui est appeler par un thread et qui permet de charger tout les trucs un peu long a faire]

    Args:
        nom_musique (str): [ le nom de la musique que l'on traite ]
    """
    global cond_fin_chargement,lien_dl,parole,text,X,Y,titre
    
    titre = nom_musique
    X , Y = 450 , 10
    lien_yt = myclass.chercher(nom_musique,10,"youtube.com").lien() # on fait la recherche du lien youtube
    lien_dl = myclass.dl_musique(lien_yt,"mp3") # prepare le téléchargement
    parole = myclass.chercher(nom_musique,10,"paroles.net").une_balise("div","song-text") # on cherche les paroles de la chanson
    font = pygame.font.Font('freesansbold.ttf', 14) 
    text = pg.textealign(parole,font,(X,Y),(0,0,0),"center", 1) # on crée le texte en texte pygame 
    cond_fin_chargement = True # on a fini de charger
    
    
def chargement():
    global cond_fin_chargement
    cond_fin_chargement = False
    
    pygame.init()

    pygame.display.set_caption("Scrapping")

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([900, 500])# it will display on screen

    img = pg.img("IMG/chargement.png",530,205,50,50)

    t_chargement = pg.text("Chargement",410,200,"center",size = 32)

    while True:
        if cond_fin_chargement: # quand on a fini de charger on lance texte
            texte(titre,lien_dl,parole,text,X , Y) 
        screen.fill((223, 242, 255))
        
        img.rotate_iblit(screen,1)
        
        t_chargement.iblit(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


#####################################
##              main               ##
#####################################


if __name__ == "__main__":
    debut()



                

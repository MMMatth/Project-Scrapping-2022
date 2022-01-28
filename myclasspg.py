import pygame
import sys

# class très utile pour pygame

class game:
    """Class qui gere la fenetre """

    def __init__(self, name, size, tick):
        # Lancement de pygame
        pygame.init()

        # Création de la fenetre de jeux
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(name)  # Choix du nom

        # Variable boolean Boucle de jeux
        self.running = True

        # Image de fond
        self.fond = pygame.image.load('image/background.png')
        self.fond = pygame.transform.scale(self.fond, size)

        # Vitesse du jeux
        self.clock = pygame.time.Clock()
        self.tick = tick

        # Touche
        self.pressed = {}

    def gameloop(self, screen):
        """Fonction de la boucle de jeu"""
        self.clock.tick(self.tick)  # Vitesse du jeux

        self.iblitall(screen)

    def eventpy(self):
        for event in pygame.event.get():  # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT:  # si l'événement est le clic sur la fermeture de la fenêtre
                sys.exit()
            # gestion du clavier
            if event.type == pygame.KEYDOWN:  # si une touche a été tapée, le marque dans le dictionnaire pressed la
                # touche enfoncer
                self.pressed[event.key] = True
            if event.type == pygame.KEYUP:
                self.pressed[event.key] = False

    def iblitall(self, screen):
        """Fonction pour 'blit' les éléments sur l'écran"""

        # Fond
        screen.blit(self.fond, (0, 0))

        # Actualisation des éléments sur l'écran
        pygame.display.flip()


class text:
    """ """

    def __init__(self, texte:str, x:int, y:int, center:str, color=(0, 0, 0), size=32, font='font/police.ttf'):
        """[Class qui permet de créer des textes ]

        Args:
            texte (str): [texte que l'on veut afficher]
            x (int): [position en largeur]
            y (int): [position en hauter]
            center (str): [si on met center ca centre sinon non]
            color : [la couleur que l'on veut pour le texte]. Defaults to (0, 0, 0).
            size (int, optional): [la taille de la police]. Defaults to 32.
            font (str, optional): [le lien de la police]. Defaults to 'font/police.ttf'.
        """
        self.texte = texte
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.font = pygame.font.Font(font, self.size)

        self.iupdate(self.texte,self.color)

        if center == 'center':  # Detecte si on veut que les coordonées sois centré ou non
            self.rect.centerx, self.rect.centery = x, y
        else:
            self.rect.x, self.rect.y = x, y

    def iupdate(self, texte, color=(255, 255, 255)):
        self.txt = self.font.render(str(texte), True, color)
        self.rect = self.txt.get_rect()

    def ihover(self, mousepos, color=(128, 255, 0)):
        """Detection du survol de la souris"""
        if self.rect.collidepoint(mousepos):
            self.texte = self.font.render(str(self.texte), True, color)
        else:
            self.texte = self.font.render(str(self.texte), True, self.color)

    def click(self, mousepos, event):
        """Detection du click de la souris et du survol"""
        self.ihover(mousepos)
        if self.rect.collidepoint(mousepos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

    def iblit(self, screen):
        """Affichage du texte"""
        screen.blit(self.txt, self.rect)

 
class textecreate:
	def __init__(self,text, font, coords:tuple, color, text_align='center'):
		self.font = font
		self.x, self.y = coords[0], coords[1]
		self.color = color

		self.text = self.font.render(text, True, self.color)
		self.rect = self.text.get_rect()
		self.text_align = text_align

		self.align()

	def align(self):
		if self.text_align == 'center':
			self.rect.centerx = self.x
		elif self.text_align == 'left':
			self.rect.x = self.x
		self.rect.y = self.y
	def recup(self):
		return self.y


class textealign:
    def __init__(self, text : str, font : str , coords:tuple ,color , text_align='center' ,space_size = 1 ,separator='\n'):
        """[Class qui permet pour un texte pygame de sauté des lignes]

        Args:
            text (str): [le text que l'on veut ]
            font (str): [lien de la police]
            coords (tuple): [les cordonée du texte]
            color ([type]): [la couleur que l'on veut pour le texte]
            text_align (str, optional): [si on veut soit le centrer "center" ou le mettre a gauche "left"]. Defaults to 'center'.
            space_size (int, optional): [l'espace entre chaque ligne]. Defaults to 1.
            separator (str, optional): [ce qui signifie que ca saute une ligne]. Defaults to '\n'.
        """
        self.text = text
        self.separator = separator
        self.x, self.y = coords[0], coords[1]
        self.text_align = text_align
        self.font = font
        self.color = color
        self.space_size = space_size
        self.liste = self.text.split(self.separator)
        self.create(self.x, self.y)

    def create(self, x1 : int, y1 : int):
        """[Méthoque qui permet de crée le texte]

        Args:
            x1 (int): [position en largeur]
            y1 (int): [position en hauteur]
        """
        self.d = {}
        x = x1
        y = y1
        for element in range(len(self.liste)):
            self.d[str(element)] = textecreate(self.liste[element].strip(), self.font, (x, y), self.color, self.text_align)
            y += self.font.size(self.liste[element])[1] * self.space_size
        self.y2 = y + self.font.size(self.liste[element])[1]
  
  
		
    def get_haut(self):
        """[Méthode qui renvoie la hauteur]"""
        return self.y2 - self.y 



    def update(self, coords):
        """[méthode qui permet d'actualiser la position du texte]"""
        x, y = coords[0], coords[1]
        self.create(x, y)



    def blit(self, screen):
        """[Méthode qui permet de blit le texte]"""
        for i in self.d.keys():
            screen.blit(self.d[i].text, self.d[i].rect)


class zone_ecriture:
    def __init__(self, x:int, y:int, w:int, h:int, limite_caractere:int, color, font = None , size_Font = 32, color_t = (255, 255, 255)):
        """[Classe permettant de crée une zone d'écriture]
        Args:
            x (int): [position en largeur]
            y (int): [position en hauteur]
            w (int): [largeur]
            h (int): [hauteur]
            limite_caractere (str): [le nombre de caractere maximum]
            color : [la couleur du rectangle]
            font : [lien de la font que vous voulez utiliser]. Defaults to None.
            size_Font (int): [Taille de la font]. Defaults to 32.
            color_t : [couleur du texte choisis]. Defaults to (255, 255, 255).
        """
        self.x , self.y = x,y
        self.w , self.h = w,h
        
        self.limite_caractere = limite_caractere
        
        self.font = pygame.font.Font(font,size_Font)
        
        self.color = color
        self.color_t = color_t
        
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        
        self.nom = ""
        
        
    def iblit(self,screen):
        """[Methode qui blit le rectangle et le texte]"""
        pygame.draw.rect(screen, self.color, self.rect)
        text_s = self.font.render(self.nom, True, self.color_t)
        screen.blit(text_s, (self.rect.x+5, self.rect.y+5))
        
        
    def supr(self):
        """[Methode permettant de surprimer une lettre au texte]"""
        self.nom = self.nom[:-1]
        
    def add(self,event):
        """[Methode permettant d'ajouter une lettre au texte]"""
        if len(self.nom) < self.limite_caractere:
            self.nom += event.unicode
            
    def recuperer(self):
        """[Methode qui renvoie le texet]"""
        return self.nom


class bouton:

    def __init__(self, image:str, x:int, y:int, w:int, h:int):
        """[Class qui permet de crée des boutons]

        Args:
            image (str): [lien de l'image par exemple "IMG/img.png"]
            x (int): [position en largeur]
            y (int): [position en hauteur]
            w (int): [largeur]
            h (int): [hauteur]
        """
        self.link = image

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image = pygame.image.load(self.link).convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

    def iblit(self, screen):
        """Méthode pour blit le bouton"""
        screen.blit(self.image, self.rect)
        
    def click(self, mousepos, event):
        """Detection du click de la souris et du survol"""
        self.ihover(mousepos)
        if self.rect.collidepoint(mousepos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True

    def ihover(self, mousepos, imglink=None):
        """Detection du survol de la souris"""
        if self.rect.collidepoint(mousepos) and imglink is not None:
            self.image = pygame.image.load(imglink).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y

        else:
            self.image = pygame.image.load(self.link).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y


class son:
    def __init__(self, music, type):
        """[Methode qui permet de faire un son]
        Args:
            music (str): [Lien de la musique par ex : "Music/musique"]
            type (str): [type de la musique par ex : ".mp3"]
        """
        self.music = music  # Lien de la music
        self.type = type  # Type music ou song
        if self.type == 'song':
            self.song = pygame.mixer.Sound('song/' + self.music)
        elif self.type == 'music':
            self.song = pygame.mixer.music.load('song/' + self.music)

    def volume(self, number):
        """[Modification du volume]

        Args:
            number ([int]): [le volume choisi par ex : 0.1]
        """
        if self.type == 'song':
            self.song.set_volume(number)
        elif self.type == 'music':
            self.song = pygame.mixer.music.set_volume(number)

    def play(self):
        """Jouer la musique ou le song"""
        if self.type == 'song':
            self.song.play()
        elif self.type == "music":
            self.music = pygame.mixer.music.play(-1)

    def stop(self):
        """Stoper le song"""
        if self.type == 'music':
            self.music = pygame.mixer.music.stop()
        

class progressbar:
    """Class qui permet de crée une barre de progression, Utilise pour afficher la vie d'un boss"""

    def __init__(self, pourcent, x, y, w, h, color=(255, 0, 0)):
        self.pourcent = pourcent  # Pourcentage actuel
        self.x, self.y, self.w, self.h = x, y, w, h
        self.color = color

    def iblit(self, screen, value, valuebase):
        """Méthode pour blit la bar"""
        self.pourcent = value / valuebase  # Calcule du pourcentage (valeur de 0 a 1)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect(self.x + 5, self.y + 5, (self.w - 10) * self.pourcent, self.h - 10))


class img(pygame.sprite.Sprite):

    def __init__(self, image:str, x:int, y:int, w:int, h:int, center=True):
        """[Class qui crée une image, peut etre animer grace a la class animate_img ]

        Args:
            image (str): [lien de l'image]
            x (int): [position en largeur]
            y (int): [position en hauteur]
            w (int): [largeur]
            h (int): [hauteur]
            center (bool, optional): [on previent si on centre ou pas]. Defaults to True.
        """
        super().__init__()
        self.link = image  # Image
        self.x = x  # Coordonées en x
        self.y = y  # Coordonées en y
        self.w = w  # Largeur de l'image
        self.h = h  # Hauteur de l'image
        self.center = center

        self.iupdate(self.link)
        self.orig_image = self.image
        self.angle = 0

    def iupdate(self, image, upscale=True, upcoords=True):
        """Met a jour l'image"""
        self.image = pygame.image.load(image).convert_alpha()
        if upscale:
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
        if upcoords:
            self.rect = self.image.get_rect()
            if self.center:
                self.rect.centerx, self.rect.centery = self.x, self.y
            else:
                self.rect.x, self.rect.y = self.x, self.y

    def iblit(self, screen):
        """Affiche de l'image"""
        screen.blit(self.image, self.rect)
        
    def rotate(self,image, rect, angle):
        """[méthode qui permet de faire tourner l'image (utile pour rotate_iblit)]"""
        self.new_image = pygame.transform.rotate(image, angle)
        rect = self.new_image.get_rect(center=rect.center)
        return self.new_image, rect
    
    def rotate_iblit(self, screen, vitesse):
        """[Méthode qui permet de blit l'image mais en faisant tournée l'image sur elle même]"""
        self.angle += vitesse
        self.image,self.rect = self.rotate(self.orig_image, self.rect, self.angle)
        screen.blit(self.image, self.rect)


class animate_img(pygame.sprite.Sprite):
    """Class pour animer une image"""

    def __init__(self, imagebase, number, vitesse=1):
        super().__init__()
        self.imagebase = imagebase  # Image de base
        self.number = number  # Nombre d'image
        self.vitesse = vitesse  # Vitesse de l'animation (diviseur de 1)
        self.counter = 0  # Image actuel
        self.sprites = []  # Liste contenant toute les images

        # Generations des images
        for i in range(number):
            if self.imagebase[-6: -4] != '_0':  # Si le caratère '_0' n'existe pas dans le lien de l'image
                self.sprites.append(pygame.image.load(self.imagebase[:-4] + f'_{str(i)}' + self.imagebase[-4:]))
            else:
                self.imagebase = self.imagebase.replace('_0', '_' + str(i))
                self.sprites.append(pygame.image.load(self.imagebase))

    def animation(self, image):
        """Animation de l'image a mettre dans une boucle"""
        self.counter += self.vitesse
        image.iupdate(self.sprites[self.counter], True)

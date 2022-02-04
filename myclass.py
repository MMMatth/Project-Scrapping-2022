from __future__ import unicode_literals
from googlesearch import search
import bs4 as bs
import urllib.request
from http.cookiejar import CookieJar
import pyttsx3
import youtube_dl
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#####################################
##         Class speak             ##
#####################################

class speak:
    def __init__(self, volume : int, texte : str, vitesse: int):
        """[Class qui permet transformer un texte en synthèse vocal]

        Args:
            volume (str): [volume de la voix]
            texte (int): [le texte que l'on veut faire parler]
            vitesse (int]): [la vittesse à laquelle la voix parlera]
        """
        self.e = pyttsx3.init()
        self.texte = texte
        
        self.r = self.e.getProperty('rate')
        self.e.setProperty('rate', vitesse)
        
        self.vol = self.e.getProperty('volume')                 
        self.e.setProperty('volume',volume)    
        
        # voix = e.getProperty('voices')       #getting details of current voice

    def start(self):
        self.e.say(self.texte)
        self.e.runAndWait()
    
    def stop(self):
        self.e.stop()
        
#####################################
##        Class download           ##
#####################################

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

class dl_musique:
    def __init__(self, lien : str, type_fichier : str):
        """[Class qui permet de télécharger un fichier audio avec un lien]

        Args:
            lien (str): [lien du site que l'on veut télécharger]
            type_fichier (str): [type de fichier style ".mp3"]
        """
        self.lien = lien
        self.type_fichier = type_fichier
        self.status = ""
        self.ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': self.type_fichier,
            'preferredquality': '192',}],
        'logger': MyLogger(),
        'progress_hooks': [self.statu],}
        
            
    def statu(self,d):
        self.status = (d['status'])
    
    def return_satus(self):
        return self.status
    
    def start(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.lien])

#####################################
##            Class chercher       ##
#####################################

class chercher:
    def __init__(self,nom:str,nbr_result:int,site:str,pythonic="lxml"):
        """[Class qui permet de faire une recherche avec un nom]

        Args:
            nom (str): [ce qu'on veut rechercher]
            nbr_result (int): [le nombre de resultat de la recherche google]
            site (str): [lien du site web que l'on veut]
            pythonic (optional): [on presise le pythonic lxml ou html5lib]. Defaults to "lxml".
            
        """
        self.nom = nom
        self.nbr_result = nbr_result
        self.site = site
        self.pythonic = pythonic
    
    def recherche_naive(self,cle:str,texte:str):
        """[Méthode permetant de retrouver une cle dans un texte]

        Args:
            cle (str): [la clé chercher]
            texte (str): [le texte que l'on veut parcourir]

        Returns:
            (bool): [nous dit si oui ou non dans le texte]
            
        """
        for i in range(len(texte)):
            if cle[0] == texte[i]:
                j=0
                while j < len(cle) and (i+j < len(texte)) and cle[j] == texte[i+j]:
                    j += 1
                if j == len(cle):
                    return True
        return False
    
    def lien(self):
        """[Méthode qui renvoies le lien de notre recherche]

        Returns:
            [result[i]]: [c'est le lien pris dans la liste du resultat de la recherche]
            
        """
        result = (search(self.nom+" "+self.site,num_results=self.nbr_result))
        for i in range(len(result)):
            if self.recherche_naive(self.site,result[i]):
                return result[i]
    def touts_liens(self):
        """[Méthode qui renvoie une liste de lien de la recherche]"""
        return(search(self.nom+" "+self.site,num_results=self.nbr_result))
        
    def une_balise(self,type_balise : str,nom_balise: str):
        """[Méthode renvoyant une balise d'un site]

        Args:
            type_balise ([str]): [le type de balise ex div]
            nom_balise ([str]): [la class de la div]

        Returns:
            [str]: [le texte dans la balise désirer]
            
        """
        result = (search(self.nom+" "+self.site,num_results=self.nbr_result))
        for i in range(len(result)):
            if self.recherche_naive(self.site,result[i]):
                a = urllib.request.urlopen(result[i])
                b = bs.BeautifulSoup(a,self.pythonic)
                return b.find(type_balise,nom_balise).text
    def toute_balise(self,type_balise : str,nom_balise:str):
        """[Méthode qui renvoie une toutes les balises du site choisis avec la balise choisi]

        Returns:
            [L : list]: [Liste de toutes les balises]
        """
        result = (search(self.nom+" "+self.site,num_results=self.nbr_result))
        for i in range(len(result)):
            if self.recherche_naive(self.site,result[i]):
                sauce1= urllib.request.Request(self.site,result[i], headers={'User-Agent': 'Mozilla/5.0'})
                cj = CookieJar()
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
                response = opener.open(sauce1)
                sauce1 = response.read().decode('utf8', errors='ignore')
                response.close()
                soup1 = bs.BeautifulSoup(sauce1, self.pythonic)
                tmp = soup1.find_all(type_balise,nom_balise)
                L= []
                for j in tmp:
                    L +=[(j.text[:-1])]
                return L

#####################################
##            Class chercher       ##
#####################################
            
class multi_cherch:
    def __init__(self,nom:list,nbr_result:int,site:str,pythonic="lxml"):
        """[Class qui permet de faire une recherche avec une liste de nom]

        Args:
            nom (list): [ce qu'on veut rechercher]
            nbr_result (int): [le nombre de resultat de la recherche google]
            site (str): [lien du site web que l'on veut]
            pythonic (optional): [on presise le pythonic lxml ou html5lib]. Defaults to "lxml".
        """
        self.nom = nom
        self.nbr_result = nbr_result
        self.site = site
        self.pythonic = pythonic
    
    def multi_toute_balise(self,type_balise : str,nom_balise:str):
        """[Méthode permettant de faire une multi recherche]

        Args:
            type_balise (str): [le type de balise ex div]
            nom_balise (str): [la class de la div]

        Returns:
            (list): [liste de tout les resultat]
        """
        result = []
        for i in range(len(self.nom)):
            result += chercher(self.nom[i],self.nbr_result,self.site).toute_balise(type_balise,nom_balise)
        return result

#####################################
##      Class champ lexicaux       ##
#####################################


    
    
    
    
class champ_lexical:
    def __init__(self,parole):
        """[Fonction qui parcour une chanson et qui permet de revoyer les pourcentage d'amour,sombre et joie ]

        Args:
            parole (str): [Les paroles prise en compte]
        """
        self.parole = parole
        # les champs lexicaux suivant on été générer grace a multi_cherch mais on été mit directement pour eviter des chargements
        self.champ_lexical = {}
        self.champ_lexical["Champ_lexical_amour"] = ['fiançailles', 'fiancé', 'parenté', 'illégitime', 'indissoluble', 'polygame', 'civil', 'descendance', 'lien', 'ban', 'épithalame', 'légal', 'promesse', 'fête', "mariage d'inclination", 'enfant naturel', 'métissage', 'unir', 'formariage', 'célébration du mariage', 'fusion', 'mariable', 'vi', 'chérir', 'désirer', 'amateur', 'faire cas', 'haïr', 'vénérer', 'inclination', 'venir', 'intéresser', 'follement', 'réjouissez', 'Capulet', 'franc-parler', 'parlaient', 'toutou', 'manier', 'choyer', 'aimanter', 'amoureusement', 'avoir le bé', 'captiver', 'en pincer pour', 'être attaché à', 'étudiez', 'gober', 'niquer', 'réclamer', 'se complaire', "s'enflammer", 'viandard', 'âme', 'arrivais', 'avoir martel en tête', 'bichette', 'cagnarder', "ch't'aime", 'contre-aimer', 'danseur', 'donnes', 'épistémophilie', 'feindre', 'fromage', 'germanophobe', 'homard', 'jalouse', 'ludomane', 'mémère', 'narcissisation', 'opéra', 'Philadelphe', 'radical', 'renvoyer', 'se ronger les ongles', 'sorteux', "tape-à-l'œi"]
        self.champ_lexical["Champ_lexical_rap"] = ["noir","couteau","plaie",'infanticide', 'témoin', 'fratricide', 'trahison', 'violence', 'commandité', 'Caïn', 'enquêter', 'effraction', 'amant', 'détective', 'apologie', 'acquittement', 'non coupable', 'Œdipe', 'avoué', 'génocide', 'meutrière', 'venge', 'flow', 'MC Solaar', 'chanson', 'rap français', 'Nekfeu', 'Afrika Bambaataa', 'Suprême NTM', 'échantillonneur', 'eurodance', 'Pat', 'Straight Outta Compto', 'homosexuel', 'asexué', 'transsexualisme', 'attirance', 'génital', 'protégé', 'différences', 'féminité', 'fœtus', 'différent', 'âge', 'rapport', 'mec', 'partenariat', 'chasteté', 'inversion', 'trans', 'pyramide des âges', 'masturber', 'parties génitales', 'baise', 'désexualiser', 'genre sexuel', 'monosexualité', 'pénétrer', 'sexualise', 'dope', 'ecstasy', 'substance', 'désintoxication', 'hippie', 'récréative', 'illicite', 'hallucinogène', 'décoction', 'criminalité', 'coke', 'orviétan', 'chnouf', 'déchiré', 'flip', 'kat', 'narco-État', 'potion', 'shoot', 'trippe']
        self.champ_lexical["Champ_lexical_joie"] = ['tristesse', 'espérance', 'indicible', 'Spinoza', 'pleurer', 'rayonnant', 'exulter', 'ivresse', 'cantique', 'paix', 'éphémère', 'démonstration', 'pleurs', 'explosion', 'agrément', 'divertissement', 'griserie', 'panar', 'intense', 'esthétique', 'perception', 'humour', 'affect', 'désir', 'anxiété', 'blaser', 'douleur', 'étreint', 'provoquée', 'effroi', 'cognitif', 'exclamation', 'mouvement', 'indéfinissable', 'affolement', 'coup', 'feeling', 'malaise', 'secousse', 'trans', 'amour', 'fortuné', 'réjouir', 'utopie', 'mari', 'heur', 'assouvir', 'habile', 'ambition', 'salut', 'rare', 'contribuer', 'conjugal', 'assurer', 'bien venu', 'doué', 'exaucé', 'hasardeux', 'lumineux', 'plaisant', 'sain', 'trouv']

        self.comteur = {}
        self.comteur["conteur_amour"] = 0
        self.comteur["conteur_rap"] = 0
        self.comteur["conteur_joie"] = 0
    
    def table_sauts(self,cle) :
        # crée un dico qui à chaque lettre renvoie son décalage
        d = {}
        for i in range(len(cle)-1):
            d[cle[i]] = len(cle) - i - 1
        return d

    def boyer_moore (self,texte : str, cle : str):
        """[Méthode suivant la loi de boyer_moore qui permet de retrouver une cle ans un texte (plus efficace que recherche naive)]

        Args:
            cle (str): [la clé chercher]
            texte (str): [le texte que l'on veut parcourir]

        Returns:
            nbr [int]: [le nombre de fois ou cle est dans texte]
        """
        long_txt = len(texte)
        long_cle = len(cle)
        nbr = 0
        if long_cle <= long_txt :
            decalage = self.table_sauts(cle) #on charge la table des décalages
        i=0
        trouve = False
        while (i <= long_txt-long_cle):
            for j in range (long_cle -1, -1, -1): #On part du dernier indice de la cle jusque 0 en décalant de -1 à chaque fois
                trouve = True
                if texte[i+j] != cle[j] : # Si on tombe sur une lettre différentes de celle de la clé
                    if (texte[i+j] in decalage and decalage[texte[i+j]]<=j):
                        i+=decalage[texte[i+j]] # on décale dans le texte en utilisant la table de décalage
                    else :
                        i+=j+1 # si la lettre n'est pas dans la table de décalage alors on décale du nombre de lettres restantes à explorer sur la clé
                    trouve = False
                    break #on sort de la boucle for car on a trouvé une lettre qui ne convient pas
            if trouve : #si toutes les lettres convenait donc on a trouvé une occurence de la clé dans texte
                nbr += 1 #on ajoute à la liste des positions où l'on trouve la clé dans le texte
                i=i+1
                trouve = False #on remet trouvé à False car on cherche la prochaine occurence
        return nbr
    
    
    def compter(self):
        """[Méthode qui permet de conter le nombre de fois chaque thème apparait dans la musique]"""
        tmp = 0
        for i in range(len(self.champ_lexical["Champ_lexical_amour"])):
            self.comteur["conteur_amour"] += self.boyer_moore(self.parole,self.champ_lexical["Champ_lexical_amour"][i])  # on compte le nombre de fois qu'il y'a le champ lexical
            tmp += self.boyer_moore(self.parole,self.champ_lexical["Champ_lexical_amour"][i]) # on calcule de chiffre de tout les mot de tout les champs lexicaux qui sont dans les paroles
        for i in range(len(self.champ_lexical["Champ_lexical_rap"])):
            self.comteur["conteur_rap"] += self.boyer_moore(self.parole,self.champ_lexical["Champ_lexical_rap"][i]) 
            tmp += self.boyer_moore(self.parole,self.champ_lexical["Champ_lexical_rap"][i]) 
        for i in range(len(self.champ_lexical["Champ_lexical_joie"])):
            self.comteur["conteur_joie"] += self.boyer_moore(self.parole,self.champ_lexical["Champ_lexical_joie"][i]) 
            tmp += self.boyer_moore(self.parole,self.champ_lexical["Champ_lexical_joie"][i])
        self.comteur["conteur_amour"] = self.comteur["conteur_amour"]/tmp # on fait les proba
        self.comteur["conteur_rap"] = self.comteur["conteur_rap"]/tmp # on fait les proba
        self.comteur["conteur_joie"] = self.comteur["conteur_joie"]/tmp # on fait les proba
        return(self.comteur)

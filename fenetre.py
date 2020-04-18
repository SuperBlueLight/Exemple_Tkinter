
# .................................................................
# NOTES : 
# 

# .................................................................
# Imports librairie standard
import tkinter
import tkinter.messagebox as messagebox
import os

# Imports Tiers
import pygame.mixer

# Imports locaux

# .................................................................
# Constantes

# .................................................................
# Classes
class ProgrammeFenetre():

    # .................................................................
    # Constructeur & méthodes spéciales

    def __init__(self):
        # Variables liées à la config de Tkinter
        self.racine_tk = tkinter.Tk()
        self.fenetre_largeur = 0
        self.fenetre_hauteur = 0

        # Variables utilisées pour les contrôles
        self.variable_champ_de_saisie = tkinter.StringVar()
        self.variable_champ_de_saisie.set("")

        # Police d'écriture / affichage du texte
        self.police_texte = ("Arial", 24)

        # Initialisation de pygame.mixer
        pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)
        self.canal_son = pygame.mixer.Channel(0)
        self.son = None

    # .................................................................
    # Propriétés

    # .................................................................
    # Méthodes

    def lancer_fenetre(self):
        # Largeur de la fenêtre.
        self.fenetre_largeur = self.racine_tk.winfo_screenwidth() * 0.8 # retire * 0.x pour le fullscreen
        self.fenetre_hauteur = self.racine_tk.winfo_screenheight() * 0.6 # retire * 0.y pour le fullscreen
        # self.racine_tk.attributes("-fullscreen", True) # dé-commente pour mettre en fullscreen

        # Lie la touche "Echap" à l'arrêt de la fenêtre
        self.racine_tk.bind("<Escape>", lambda x: self.racine_tk.destroy())
        
        # Création d'un Canvas (zone de dessin).
        canvas = tkinter.Canvas(self.racine_tk, width=self.fenetre_largeur, height=self.fenetre_hauteur)
        canvas.create_rectangle(0, 0, self.fenetre_largeur, self.fenetre_hauteur, fill="green")

        # Création d'une Frame (cadre) pour contenir les contrôles (labels, champs de saisie, etc).
        cadre = tkinter.Frame(self.racine_tk)

        # Création d'un Label.
        label = tkinter.Label(cadre, text="Ecrire quelque chose:")
        label.configure(font=self.police_texte)

        # Création d'une Entry (champ de saisie).
        champ_de_saisie = tkinter.Entry(cadre, textvariable=self.variable_champ_de_saisie, width=30)
        champ_de_saisie.configure(font=self.police_texte) 
        champ_de_saisie.focus_set() 

        # Lie la touche "Entrer" avec la fonction pour traiter le contenu du champ.
        champ_de_saisie.bind('<Return>', lambda event: self.traitement_champ_de_saisie())

        # Ajoute le cadre au canvas, en le plaçant au milieu de la fenêtre.
        canvas.create_window(self.fenetre_largeur/2, self.fenetre_hauteur/2, window=cadre)

        # Ajout d'un bouton (fait la même chose que la touche "Entrer" dans le champ de saisie)
        bouton = tkinter.Button(cadre, text="Valider", command=self.traitement_champ_de_saisie)
        bouton.configure(font=self.police_texte) 

        # Packs (validation graphique des différents éléments).
        # cadre.pack() # inutile, mais je ne sais pas pourquoi.
        label.pack()
        champ_de_saisie.pack()
        bouton.pack()
        canvas.pack(side="top", fill="both")

        # Boucle principale de la fenêtre.
        self.racine_tk.mainloop()


    def traitement_champ_de_saisie(self):
        # Récupération du contenu du champ de saisie.
        contenu_champ_de_saisie = self.variable_champ_de_saisie.get()

        # Affichage du contenu
        print(f"contenu du champ de saisie: {contenu_champ_de_saisie}") # affichage console.
        # messagebox.showinfo(title="Info", message=f"contenu du champ de saisie: {contenu_champ_de_saisie}") # affichage boîte de dialogue.

        # Traitement du contenu
        # Note: c'est juste un exemple par rapport à ce que tu m'as dis (jouer un son), après tu gères ça comme tu veux ;-).
        # Commandes possibles:
        # 'jouer <nom_fichier.extension>': charge et joue un son.
        # 'pause': met en pause le son joué.
        # 'reprendre': remet en lecture le son joué.
        # 'reset': remet à zéro le son joué.
        # 'rejouer': rejoue le dernier son (à utiliser après 'reset').
        # 'volume <intensite_volume>': modifie le volume avec l'intensité choisie (entre 0.0 et 1.0).

        # Récupèration des mots du champ de saisie
        mots = []
        if " " in contenu_champ_de_saisie: # s'il y a un ou plusieurs espaces => plusieurs mots.
            mots = contenu_champ_de_saisie.split(" ")
        else: # pas d'espaces => un seul mot.
            mots = [contenu_champ_de_saisie]

        # Interprêtation du premier mot et action en fonction.
        if mots[0] == "jouer":
            dossier_sons = "D:\\200_Programmation\\100_EspaceYourself\\100-DEV_PilotageSalle\\tests\\serveur\\services\\ressources\\"
            nom_fichier = mots[1]
            chemin_fichier = f"{dossier_sons}{nom_fichier}"
            if os.path.exists(chemin_fichier): # vérifie si le fichier existe.
                print(f"Chargement du fichier '{nom_fichier}'.")
            else:
                print(f"Le fichier '{nom_fichier}' est introuvable.")
            self.son = pygame.mixer.Sound(chemin_fichier)
            self.canal_son.play(self.son)
        elif mots[0] == "pause":
            self.canal_son.pause()
        elif mots[0] == "reprendre":
            self.canal_son.unpause()
        elif mots[0] == "reset":
            self.canal_son.stop()
        elif mots[0] == "rejouer":
            self.canal_son.play(self.son)
        elif mots[0] == "volume":
            volume_texte = mots[1]
            volume = float(volume_texte)
            self.canal_son.set_volume(volume)

        # Vide le champ de saisie.
        self.variable_champ_de_saisie.set("") # commente si tu veux le laisser rempli

# .................................................................
# Lancement du programme 

def main():
    programme = ProgrammeFenetre()
    programme.lancer_fenetre()

main()
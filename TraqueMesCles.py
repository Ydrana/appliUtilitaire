import re
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
# import csv
from tkinter import ttk
import threading
from typing import Callable


class TraqueMesCles(ttk.Frame):
    pattern_utilisation = None
    pattern_stockage = None
    liste_stockage = None
    cle_non_defini: str = "clé(s) non définie(s)"
    cle_non_utilise: str = "clé(s) non utilisée(s)"

    def __init__(self, frame_parent, func_callback: Callable, **kwargs):
        print('Initialisation TraqueMesCles...')
        ttk.Frame.__init__(self, frame_parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid()

        self.bouton_retour = ttk.Button(self, text="Retour Menu", command=lambda: func_callback())
        self.frame_input = ttk.Frame(self)
        self.progress_bar = ttk.Progressbar(self, mode='determinate')
        self.frame_resultat_non_def = ttk.Labelframe(self, text=self.cle_non_defini)
        self.frame_resultat_non_utilise = ttk.Labelframe(self, text=self.cle_non_utilise)

        self.bouton_retour.grid(row=0, column=0, pady=7, sticky='NW')
        self.frame_input.grid(row=1, column=0, pady=7)
        self.progress_bar.grid(row=2, column=0, pady=7)
        self.progress_bar.grid_forget()
        self.frame_resultat_non_def.grid(row=2, column=0, pady=7)
        self.frame_resultat_non_def.grid_forget()
        self.frame_resultat_non_utilise.grid(row=3, column=0, pady=7)
        self.frame_resultat_non_utilise.grid_forget()

        self.bouton_browse = ttk.Button(self.frame_input, text="+", width=2, command=self.choisir_dossier)
        self.str_url = tk.StringVar()
        self.input_url = tk.Entry(self.frame_input, textvariable=self.str_url, width=37)
        self.bouton_lancer = ttk.Button(self.frame_input, text="Lancer", command=self.lancement_analyse)

        self.bouton_browse.grid(row=0, column=0, pady=7, sticky='NWE')
        self.input_url.grid(row=0, column=1, padx=2, pady=7)
        self.bouton_lancer.grid(row=0, column=2, pady=7)


    def lancement_analyse(self):
        """lancement de l'analyse des fichiers dans un thread parallèle"""
        def lancement_analyser():
            self.progress_bar.grid()
            self.progress_bar.start()
            try:
                self.traitement_analyse()
            finally:
                self.progress_bar.stop()
                self.progress_bar.grid_forget()
                self.bouton_lancer['state'] = 'normal'

        self.bouton_lancer['state'] = 'disabled'
        threading.Thread(target=lancement_analyser).start()

    def recursive_search(self, src_dict_2, liste):
        for nom_fichier in os.listdir(src_dict_2):
            # Exclure des dossiers à analyser : target, test et ceux commençant par . comme .svn
            if not any(re.match(regex, nom_fichier) for regex in ["\..*", "target", "test"]):
                files = os.path.join(src_dict_2, nom_fichier)  # join the full path with the names of the files.
                if os.path.isfile(files):
                    try:
                        strng = open(files, 'r', encoding='utf-8')
                        # Recherche dans les fichiers .properties
                        if re.match("messages.*\.properties", nom_fichier):
                            for lines in strng.readlines():  # We then need to read the files

                                resultat_recherche = re.findall(self.pattern_stockage, lines)
                                if resultat_recherche:
                                    # Récupération de la première occurence trouvée dans une ligne
                                    self.liste_stockage.append(resultat_recherche[0])
                        # Recherche dans les fichiers courants
                        else:
                            for lines in strng.readlines():  # We then need to read the files
                                resultat_recherche = re.findall(self.pattern_utilisation, lines)
                                if resultat_recherche:  # If we find the pattern we are looking for
                                    liste.extend(resultat_recherche)
                    except:
                        pass
                else:
                    self.recursive_search(files, liste)

    def traitement_analyse(self):
        self.pattern_utilisation = re.compile('Utility\.message\(\"((?:\w|\.)*?)\"')
        self.pattern_stockage = re.compile('((?:\w|\.)*?)\s\=')

        liste_utilisation = []
        self.liste_stockage = []

        self.recursive_search('C:\\Users\\Moth\\PycharmProjects\\Java\\3.9_Java_post_2031', liste_utilisation)

        l_counts = [(liste_utilisation.count(x), x) for x in set(liste_utilisation)]
        l_counts.sort(reverse=True)

        # Recherche clés non utilisées
        liste_cle_non_utilisee = []
        for msg_stock in set(self.liste_stockage):
            if [item for item in l_counts if item[0] == msg_stock]:
                print(msg_stock + " pas dans l_counts")
            if msg_stock not in liste_utilisation:
                liste_cle_non_utilisee.append(msg_stock)

        # Recherche clés non définies
        liste_cle_non_definie = []
        for element in set(liste_utilisation):
            if element not in self.liste_stockage:
                liste_cle_non_definie.append(element)

        print(str(len(liste_cle_non_definie)) + " clé(s) non définie(s)")
        print(liste_cle_non_definie)

        print(str(len(liste_cle_non_utilisee)) + " clé(s) non utilisée(s)")
        print(liste_cle_non_utilisee)

        # Nettoie les deux frames
        self.frame_resultat_non_def.config(text='')
        for child in self.frame_resultat_non_def.winfo_children():
            child.destroy()
        self.frame_resultat_non_utilise.config(text='')
        for child in self.frame_resultat_non_utilise.winfo_children():
            child.destroy()

        self.frame_resultat_non_def.grid()
        self.frame_resultat_non_def.config(text=str(len(liste_cle_non_definie)) + ' ' + self.cle_non_defini)
        text_resultat_non_def = tk.Text(self.frame_resultat_non_def, height=15)
        text_resultat_non_def.pack(fill=tk.BOTH, expand=True)
        for i in liste_cle_non_definie:
            text_resultat_non_def.insert(tk.END, i + '\n')

        self.frame_resultat_non_utilise.grid()
        self.frame_resultat_non_utilise.config(text=str(len(liste_cle_non_utilisee)) + ' ' + self.cle_non_utilise)
        text_resultat_non_utilisee = tk.Text(self.frame_resultat_non_utilise, height=15)
        text_resultat_non_utilisee.pack(fill=tk.BOTH, expand=True)
        for i in liste_cle_non_utilisee:
            text_resultat_non_utilisee.insert(tk.END, i + '\n')


    def choisir_dossier(self):
        dir_defaut = "./"
        self.str_url.set(askdirectory(initialdir=dir_defaut, title="Choisir fichier départ"))


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Analyse clés messageUtility')

    TraqueMesCles(window)

    window.mainloop()

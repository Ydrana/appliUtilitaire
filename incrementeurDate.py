# coding: utf-8
import tkinter as tk
from typing import Callable
from tkinter import ttk
from tkinter import filedialog
import fileinput
import threading
from datetime import datetime, timedelta
import re as re


class IncrementeurDate(ttk.Frame):

    def __init__(self, frame_parent, func_callback: Callable, **kwargs):
        print('Initialisation IncrementeurDate...')
        ttk.Frame.__init__(self, frame_parent, **kwargs)
        self.grid(row=0, column=0)

        # Widget (niv1)
        self.bouton_retour = ttk.Button(self, text="Retour Menu", command=lambda: func_callback())
        self.frame_appli = ttk.Labelframe(self, text="Incrémenteur de Date")

        self.bouton_retour.grid(row=0, column=0, pady=7, sticky='NW')
        self.frame_appli.grid(row=1, column=0, pady=7, sticky='NW')

        # Widget (niv2)
        self.frame_principale = ttk.Frame(self.frame_appli)

        self.frame_principale.grid(row=1, column=0, padx=7, pady=5, sticky='NW')

        # Widget (niv3)
        self.frame_input = ttk.Frame(self.frame_principale)
        self.frame_param_date = ttk.Labelframe(self.frame_principale, text="Décalage")
        self.progress_bar = ttk.Progressbar(self.frame_principale, mode='determinate')

        self.bouton_retour.grid(row=0, column=0, pady=(0, 7), sticky='NW')
        self.frame_input.grid(row=1, column=0, pady=7)
        self.frame_param_date.grid(row=2, column=0, pady=7, sticky='NW')
        self.progress_bar.grid(row=3, column=0, pady=7)
        self.progress_bar.grid_forget()

        # Widget (niv4)
        self.bouton_browse = ttk.Button(self.frame_input, text="+", width=2, command=self.choisir_dossier)
        self.str_url = tk.StringVar()
        self.input_url = ttk.Entry(self.frame_input, textvariable=self.str_url, width=42)
        self.bouton_analyser = ttk.Button(self.frame_input, text="Incrémenter", command=self.lancement_analyse)

        self.bouton_browse.grid(row=0, column=0, pady=7, sticky='NWE')
        self.input_url.grid(row=0, column=1, padx=2, pady=7)
        self.bouton_analyser.grid(row=0, column=2, pady=7)

        self.label_param_days = ttk.Label(self.frame_param_date, text="Jours")
        self.int_date = tk.IntVar()
        self.input_date = ttk.Spinbox(self.frame_param_date, textvariable=self.int_date, from_=-10000, to=10000, width=5)
        self.label_param_hours = ttk.Label(self.frame_param_date, text="Heures")
        self.int_hours = tk.IntVar()
        self.input_hours = ttk.Spinbox(self.frame_param_date, textvariable=self.int_hours, from_=-10000, to=10000, width=4)

        self.label_param_days.grid(row=0, column=0, pady=7)
        self.input_date.grid(row=0, column=1, pady=7)
        self.label_param_hours.grid(row=0, column=2, pady=7)
        self.input_hours.grid(row=0, column=3, pady=7)

    def lancement_analyse(self):
        """lancement de l'analyse du fichier XML dans un thread parallèle"""

        def lancement_analyser():
            self.progress_bar.grid()
            self.progress_bar.start()
            try:
                self.lire_detecter_remplacer_date(self.str_url.get(), timedelta(days=self.int_date.get()))
                print('Analyse...')
            finally:
                self.progress_bar.stop()
                self.progress_bar.grid_forget()
                self.bouton_analyser['state'] = 'normal'

        self.bouton_analyser['state'] = 'disabled'
        threading.Thread(target=lancement_analyser).start()

    def choisir_dossier(self):
        dir_defaut = "./"
        self.str_url.set(filedialog.askopenfilename(initialdir=dir_defaut, title="Choisir fichier",
                                                    filetypes=(("xml files", "*.xml"), ("all files", "*.*"))))

    def lire_detecter_remplacer_date(self, file: str, deltatime: timedelta):
        dict_format = {
            "((\"|>)20\d{2}-\d{2}-\d{2}(?:\+|-)\d{2}(?::\d{2})(\"|<|-))": "%Y-%m-%d%z",
            "((\"|>)20\d{6}T\d{9}Z(\"|<|-))": "%Y%m%dT%H%M%S%fZ",
            "((\"|>)20\d{6}T\d{6}(\"|<|-))": "%Y%m%dT%H%M%S",
            "((\"|>)20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}Z(\"|<|-))": "%Y-%m-%dT%H:%MZ",
            "((\"|>)20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(?:\+|-)\d{2}(?::\d{2})(\"|<|-))": "%Y-%m-%dT%H:%M:%S.%f%z",
            "((\"|>)20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\+|-)\d{2}(?::\d{2})(\"|<|-))": "%Y-%m-%dT%H:%M:%S%z",
            "((\"|>)20\d{6}T\d{2}:\d{2}:\d{2}(?:\+|-)\d{2}(?::\d{2})(\"|<|-))": "%Y%m%dT%H:%M:%S%z",
            "((\"|>)20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z(\"|<|-))": "%Y-%m-%dT%H:%M:%SZ",
            "((\"|>)20\d{6}T\d{2}:\d{2}:\d{2}Z(\"|<|-))": "%Y%m%dT%H:%M:%SZ",
            "((\"|>)20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\+|-)\d{2}(?::\d{2})(\"|<|-))": "%Y-%m-%dT%H:%M:%S%z",
            "((\"|>)20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\"|<|-))": "%Y-%m-%dT%H:%M:%S",
            "((\"|>)20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}(\"|<|-))": "%Y-%m-%dT%H:%M",
            "((\"|>)20\d{6}_\d{9}(\"|<|-))": "%Y%m%d_%H%M%S%f",
            "((\"|>)20\d{6}_\d{6}(\"|<|-))": "%Y%m%d_%H%M%S",
            "((\"|>)20\d{6}\s\d{2}:\d{2}(\"|<|-))": "%Y%m%d %H:%M",
            "((\"|>)20\d{2}-\d{2}-\d{2}(\"|<|-))": "%Y-%m-%d",
            "((\"|>)T\d{2}:\d{2}:\d{2}(?:\+|-)\d{2}(?::\d{2})(\"|<|-))": "T%H:%M:%S%z",
            "((\"|>)T\d{2}:\d{2}:\d{2}(\"|<|-))": "T%H:%M:%S",
            "((\"|>)\d{2}:\d{2}:\d{2}(?:\+|-)\d{2}(?::\d{2})(\"|<|-))": "%H:%M:%S%z",
            "((\"|>)\d{2}:\d{2}:\d{2}(\"|<|-))": "%H:%M:%S",
            "((\"|>)\d{2}:\d{2}(\"|<|-))": "%H:%M",
            "((\"|>)\d{10}:\d{2}:\d{2}(\"|<|-))": "%d%m%Y%H:%M:%S",
            "((\"|>)\d{2}\/\d{2}\/20\d{2}\s\d{2}:\d{2}:\d{2}(\"|<|-))": "%d/%m/%Y %H:%M:%S",
            "((\"|>)\d{2}\/\d{2}\/20\d{2}\s\d{2}:\d{2}(\"|<|-))": "%d/%m/%Y %H:%M",
            "((\"|>)\d{2}\/\d{2}\/20\d{2}\s\d{2}(\"|<|-))": "%d/%m/%Y %H",
            "((\"|>)\d{2}\/\d{2}\/20\d{2}(\"|<|-))": "%d/%m/%Y",
            "((\"|>)\d{2}\/\d{2}(\"|<|-))": "%d/%m"
        }
        line_num = 0
        with fileinput.FileInput(file, inplace=True, backup='.bak') as file:
            for line in file:
                line_num += 1
                new_line = line
                for key, pattern in dict_format.items():
                    resultat_recherche = re.findall(key, line)
                    if resultat_recherche:
                        liste_date = {}
                        for resultat in resultat_recherche:
                            string_corrige = resultat[0].replace('"', '').replace('>', '').replace('<', '')
                            liste_date[datetime.strptime(string_corrige, pattern)] = resultat[0]

                        for date_courante, strg in sorted(liste_date.items(), reverse=False):
                            date_modifiee = date_courante + deltatime
                            new_string = date_modifiee.strftime(pattern)
                            if strg.endswith('Z'):
                                new_string = strg[0] + new_string[:-5] + 'Z' + strg[-1]
                            if re.match(r'.*\+\d{2}:00.$', strg):  # Fait passer l'offset UTC du format +0000 à +00:00
                                new_string = strg[0] + new_string[:-2] + ':00' + strg[-1]
                            if re.match(r'.*\.\d{3}.*$', strg):  # Fait passer le nbr de microsecondes de 6 à 3
                                new_string = re.sub(r'(.*\.\d{3})(\d{3})(.*)', r'\1\3', new_string)
                            new_line = new_line.replace(strg, new_string)
                            # print(line.replace(text_to_search, replacement_text), end='')
                print(new_line, end='')


if __name__ == '__main__':
    print('lancement main')

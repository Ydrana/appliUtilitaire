# coding: utf-8
import incrementeurDate
import TraqueMesCles
from tkinter.ttk import Label, Frame, Button, Style
from tkinter import font
from ttkthemes import ThemedTk

import requests
from github import Github
from pathlib import Path
import subprocess

__version__: str = '0.1.1'


def ouvrir_traque_mes_cles():
    print('Ouvrir CheckMesClés')
    frame_principale.grid_remove()
    frame_traque_mes_cles.grid(sticky='NWES')


def ouvrir_incrementeur_date():
    print('Ouvrir Incrementeur de date')
    frame_principale.grid_remove()
    frame_incrementeur_date.grid(sticky='NWES')


def callback_to_principal():
    print('callback_to_principal')
    frame_incrementeur_date.grid_remove()
    frame_traque_mes_cles.grid_remove()
    frame_principale.grid()


def installer_visualiseur():
    """Télécharge de Github l'asset de la dernière release du visualiseur d'offres"""
    try:
        import github_id

        headers = {'Authorization': 'token ' + github_id.token,
                   'Accept': 'application/octet-stream'}

        gh_session = requests.Session()
        gh_session.auth = (github_id.user, github_id.token)

        g = Github(github_id.token)
        repo = g.get_repo("Ydrana/Visualiseur_de_donnees")

        asset = repo.get_latest_release().get_assets()[1]
        response = gh_session.get(asset.url, stream=True, headers=headers)
        save_to = Path.home() / 'Downloads' / asset.name
        save_to.write_bytes(response.content)
        subprocess.Popen([save_to], shell=True)
    except Exception:
        print("Fichier github_id absent")


if __name__ == '__main__':
    MIN_WIDTH: int = 400
    MIN_HEIGHT: int = 150

    window = ThemedTk(theme='plastik')  # arc, breeze, plastik, clearlooks, black, equilux
    window.title('Utilitaires TMA')
    window.resizable(False, False)

    # Personnalisation Style
    style = Style(window)
    original_font = font.nametofont(style.lookup("TLabel", "font"))
    f = font.Font(**original_font.configure())
    f.configure(weight='bold', underline=0, size=9)
    style.configure('H1.TLabel', font=f)
    original_font = font.nametofont(style.lookup("TButton", "font"))

    f2 = font.Font(**original_font.configure())
    f2.configure(weight='bold', size=9)
    style.configure('H1.TButton', font=f2)

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.minsize(MIN_WIDTH, MIN_HEIGHT)

    # FRAME Principale
    frame_principale = Frame(window)
    frame_principale.grid_columnconfigure(0, weight=1)
    frame_principale.grid_rowconfigure(0, weight=1)
    frame_principale.grid(sticky='NSEW')

    label_fonct = Label(frame_principale, text='Fonctionnel', style='H1.TLabel')
    bouton_lancer = Button(frame_principale, text="Incrémenter dates XML", command=ouvrir_incrementeur_date)
    bouton_dl_visualiseur = Button(frame_principale, text="installation visualiseur d'offres", command=installer_visualiseur)
    label_java = Label(frame_principale, text='Code Java', style='H1.TLabel')
    bouton_lancer_traque = Button(frame_principale, text="Vérifier clés messages", command=ouvrir_traque_mes_cles)
    label_version = Label(frame_principale, text="v" + __version__, font=('Arial', 8), anchor='se')

    label_fonct.grid(row=0, column=0, pady=(15, 5))
    bouton_lancer.grid(row=1, column=0, pady=(0, 5))
    bouton_dl_visualiseur.grid(row=2, column=0)
    label_java.grid(row=3, column=0, pady=(15, 5))
    bouton_lancer_traque.grid(row=4, column=0)
    label_version.grid(row=5, column=0, sticky='WE')

    # FRAME Incrementeur de date (removed au démarrage)
    frame_incrementeur_date = Frame(window)
    frame_incrementeur_date.grid_columnconfigure(0, weight=1)
    frame_incrementeur_date.grid_rowconfigure(0, weight=1)
    app_incrementeur_date = incrementeurDate.IncrementeurDate(frame_incrementeur_date, callback_to_principal)

    # FRAME CheckMesClés (removed au démarrage)
    frame_traque_mes_cles = Frame(window)
    frame_traque_mes_cles.grid_columnconfigure(0, weight=1)
    frame_traque_mes_cles.grid_rowconfigure(0, weight=1)
    app_traque_mes_cles = TraqueMesCles.TraqueMesCles(frame_traque_mes_cles, callback_to_principal)

    window.mainloop()

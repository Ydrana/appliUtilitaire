# coding: utf-8
import incrementeurDate, TraqueMesCles
from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk


version: str = '0.1'

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


if __name__ == '__main__':
    window = ThemedTk(theme='awdark')
    window.title('Utilitaires TMA')

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.minsize(400, 150)

    # FRAME Principale
    frame_principale = ttk.Frame(window)
    frame_principale.grid_columnconfigure(0, weight=1)
    frame_principale.grid_rowconfigure(0, weight=1)
    frame_principale.grid(sticky='NSEW')

    label_fonct = ttk.Label(frame_principale, text='Fonctionnel')
    bouton_lancer = ttk.Button(frame_principale, text="Incrémenter dates XML", command=ouvrir_incrementeur_date)
    label_java = ttk.Label(frame_principale, text='Code Java')
    bouton_lancer_traque = ttk.Button(frame_principale, text="Vérifier clés messages", command=ouvrir_traque_mes_cles)
    label_version = tk.Label(frame_principale, text="v"+version, fg="#797979", font=('Arial', 8))

    label_fonct.grid(row=0, column=0, pady=(15, 0))
    bouton_lancer.grid(row=1, column=0)
    label_java.grid(row=2, column=0, pady=(15, 0))
    bouton_lancer_traque.grid(row=3, column=0)
    label_version.grid(row=4, column=0, sticky='SE')

    # FRAME Incrementeur de date (removed au démarrage)
    frame_incrementeur_date = ttk.Frame(window)
    frame_incrementeur_date.grid_columnconfigure(0, weight=1)
    frame_incrementeur_date.grid_rowconfigure(0, weight=1)
    app_incrementeur_date = incrementeurDate.IncrementeurDate(frame_incrementeur_date, callback_to_principal)

    # FRAME CheckMesClés (removed au démarrage)
    frame_traque_mes_cles = ttk.Frame(window)
    frame_traque_mes_cles.grid_columnconfigure(0, weight=1)
    frame_traque_mes_cles.grid_rowconfigure(0, weight=1)
    app_traque_mes_cles = TraqueMesCles.TraqueMesCles(frame_traque_mes_cles, callback_to_principal)

    window.mainloop()


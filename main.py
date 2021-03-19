# coding: utf-8
import incrementeurDate, TraqueMesCles
from tkinter import Label, Frame, Button
from tkinter import Label as tkLabel
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
    MIN_WIDTH: int = 400
    MIN_HEIGHT: int = 150

    window = ThemedTk(theme='awdark')
    window.title('Utilitaires TMA')
    window.resizable(False, False)

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.minsize(MIN_WIDTH, MIN_HEIGHT)

    # FRAME Principale
    frame_principale = Frame(window)
    frame_principale.grid_columnconfigure(0, weight=1)
    frame_principale.grid_rowconfigure(0, weight=1)
    frame_principale.grid(sticky='NSEW')

    label_fonct = Label(frame_principale, text='Fonctionnel')
    bouton_lancer = Button(frame_principale, text="Incrémenter dates XML", command=ouvrir_incrementeur_date)
    label_java = Label(frame_principale, text='Code Java')
    bouton_lancer_traque = Button(frame_principale, text="Vérifier clés messages", command=ouvrir_traque_mes_cles)
    label_version = tkLabel(frame_principale, text="v"+version, fg="#797979", font=('Arial', 8), anchor='se')

    label_fonct.grid(row=0, column=0, pady=(15, 5))
    bouton_lancer.grid(row=1, column=0)
    label_java.grid(row=2, column=0, pady=(15, 5))
    bouton_lancer_traque.grid(row=3, column=0)
    label_version.grid(row=4, column=0, sticky='WE')

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


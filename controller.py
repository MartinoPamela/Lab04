import time
import flet as ft
import model as md
from view import View


class SpellChecker:

    def __init__(self, view):
        self._multiDic = md.MultiDictionary()
        self._view = view

    def handleSpellCheck(self, e):

        linguaScelta = self._view._linguaggio.value

        if linguaScelta is None:
            self._view._lvOut.controls.clear()
            self._view._lvOut.controls.append((ft.Text("Il campo lingua va selezionato!", color="red")))
            self._view.update()
            return

        modality = self._view._ricerca.value

        if modality is None:
            self._view._lvOut.controls.clear()
            self._view._lvOut.controls.append((ft.Text("Il campo modalità va selezionato!", color="red")))
            self._view.update()
            return

        frase = self._view._txtIn.value

        if frase == "":
            self._view._lvOut.controls.clear()
            self._view._lvOut.controls.append((ft.Text("Inserire una frase!", color="red")))
            self._view.update()
            return

        if (linguaScelta is not None) and (modality is not None) and (frase != ""):
            self._view._lvOut.controls.clear()
            self._view._lvOut.controls.append(ft.Text("Tutti i campi sono stati inseriti correttamente.",
                                                      color="green"))
        self._view._lvOut.controls.append(ft.Text(f"Frase inserita: {self._view._txtIn.value}", color="blue"))

        errate, elapsedTime = self.handleSentence(frase, linguaScelta, modality)

        self._view._lvOut.controls.append(ft.Text("Parole errate: " + errate,
                                                      color="blue"))
        self._view._lvOut.controls.append(ft.Text("Tempo impiegato: " + str(elapsedTime), color="blue"))

        self._view._txtIn.value = ""
        self._view.update()


    def handleSentence(self, txtIn, language, modality):
        txtIn = replaceChars(txtIn.lower())

        words = txtIn.split()
        paroleErrate = " - "

        match modality:
            case "Default":
                t1 = time.time()
                parole = self._multiDic.searchWord(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Linear":
                t1 = time.time()
                parole = self._multiDic.searchWordLinear(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " "
                t2 = time.time()
                return paroleErrate, t2 - t1

            case "Dichotomic":
                t1 = time.time()
                parole = self._multiDic.searchWordDichotomic(words, language)
                for parola in parole:
                    if not parola.corretta:
                        paroleErrate = paroleErrate + str(parola) + " - "
                t2 = time.time()
                return paroleErrate, t2 - t1
            case _:
                return None

    def handleLanguageSelection(self, e):
        print("handle Dropdwon language called")
        self._view._lvOut.controls.append(ft.Text(value="Language correctly selected: " + self._view._linguaggio.value))
        self._view.update()

    def handleSelectSearchMode(self, e):
        print("handle Dropdwon language called")
        self._view._lvOut.controls.append(ft.Text(value="Search correctly selected: " + self._view._ricerca.value))
        self._view.update()


    def printMenu(self):
        print("______________________________\n" +
              "      SpellChecker 101\n"+
              "______________________________\n " +
              "Seleziona la lingua desiderata\n"
              "1. Italiano\n" +
              "2. Inglese\n" +
              "3. Spagnolo\n" +
              "4. Exit\n" +
              "______________________________\n")


def replaceChars(text):
    chars = "\\`*_{}[]()>#+-.!$?%^;,=_~"
    for c in chars:
        text = text.replace(c, "")
    return text
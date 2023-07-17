"""
    Computes expected values of different combinations of dice

    Created 2023/07/17
"""

import tkinter as tk
import re

class diceEV(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(expand=True)
        self.build()
        self.diceEntryValue.set("1d20")

    def build(self):
        """ Here the GUI is built. """
        # init
        self.diceEntryValue = tk.StringVar()
        self.outputValue = tk.StringVar()
        rowCount = 0
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=rowCount, column=0, rowspan=10, columnspan=6, padx=5, pady=5, sticky=tk.N + tk.W)
        # ------ Entry row ------
        tk.Label(self.mainFrame, text="Entry: ").grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.W)
        self.diceEntry = tk.Entry(self.mainFrame, textvariable=self.diceEntryValue)
        self.diceEntry.grid(row=rowCount, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W)
        # ------ Output row ------
        rowCount += 1
        tk.Label(self.mainFrame, text="Output: ").grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.W)
        self.outputEntry = tk.Entry(self.mainFrame, textvariable=self.outputValue)
        self.outputEntry.grid(row=rowCount, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W)
        # ------ Example row ------
        rowCount += 1
        tk.Label(self.mainFrame, text="Examples: ").grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.W)
        exLabel = tk.Label(self.mainFrame, text="'3d100', '2d4 + 1d8', \n'adv(1d20)', 'disadv(3d100)'")
        exLabel.grid(row=rowCount, rowspan=2, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W)
        # ------ Button row ------
        rowCount += 2
        self.calcBtn = tk.Button(self.mainFrame, text='   Calculate   ', command=self._doTheThing)
        self.calcBtn.grid(row=rowCount, column=3, padx=5, pady=5, sticky=tk.W)
        self.quitBtn = tk.Button(self.mainFrame, text=' Exit ', command=self._quit)
        self.quitBtn.grid(row=rowCount, column=4, padx=5, pady=5, sticky=tk.W)

    def _doTheThing(self):
        """ does the thing """
        entryString = self.diceEntryValue.get()
        parsedString = self.parseInput(entryString)
        resultEV = eval(parsedString)
        self.outputValue.set(str(resultEV))
        print("{} => {}".format(entryString, resultEV))

    def parseInput(self, entry):
        """ things and stuff """
        output = entry
        diceReg = '\d+d\d+'
        dice = re.findall(diceReg, entry)
        for foundDie in dice:
            ev = die(foundDie).totalEV
            output = output.replace(foundDie, str(ev))
        return output

    def _quit(self):
        self.master.quit()


class die(object):
    def __init__(self, query):
        number, sides = query.split('d')
        number = int(number)
        sides = int(sides)
        self.sideNum = sides
        self.singleEV = (sides + 1) / 2
        self.totalEV = self.singleEV * number


def adv(ev):
    """ Returns the EV of an advantaged roll with a die that has the given EV """
    sides = int(2 * ev - 1)
    ev_adv = sum([(2*j-1) * j / sides**2 for j in range(1, sides+1)])
    return ev_adv


def disadv(ev):
    """ Returns the EV of a disadvantaged roll with a die that has the given EV """
    sides = int(2 * ev - 1)
    ev_disadv = sum([(2*j-1) * (sides-j+1) / sides**2 for j in range(1, sides+1)])
    return ev_disadv


dis = disadv


if __name__ == '__main__':
    root  = tk.Tk()
    root.title('The DiceEvaluator')
    dev = diceEV(root)
    root.mainloop()


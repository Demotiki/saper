from random import randint
from os import system


class Engine:
    def __init__(self) -> None:
        self.pole = [[0 for _ in range(10)] for _ in range(12)]
        self.poleg = [[" " for _ in range(10)] for _ in range(10)]
        self.y = 0
        self.x = 0
        self.z = ""
        self.nober = ["0", "1","2" ,"3" ,"4" ,"5" ,"6" ,"7", "8"]
        self.arr = []
        self.xodarr = []
        self.n = 20

    def __gener(self) -> None:
        n = self.n
        while n:
            x, y = randint(0, 9), randint(0, 9)
            if self.pole[y + 1][x] != "M" and ((y, x) not in [(self.y + 1, self.x), (self.y, self.x), (self.y - 1, self.x), (self.y + 1, self.x + 1), (self.y, self.x + 1), (self.y - 1, self.x + 1), (self.y + 1, self.x - 1), (self.y, self.x - 1), (self.y - 1, self.x - 1)]):
                n -= 1
                self.pole[y + 1][x] = "M"
        for i in range(12):
            self.pole[i].insert(0, 0)
            self.pole[i].append(0)
        for y in range(10):
            for x in range(10):
                if self.pole[y + 1][x + 1] != "M":
                    self.pole[y + 1][x + 1] = (self.pole[y][x : x + 3] + self.pole[y + 2][x : x + 3]  + [self.pole[y + 1][x]] + [self.pole[y + 1][x + 2]]).count("M")
        self.pole.pop(0)
        self.pole.pop(-1)
        for i in range(10):
            self.pole[i].pop(0)
            self.pole[i].pop(-1)
    
    def __draw(self) -> None:
        print(f"     1  2  3  4  5  6  7  8  9  10   Бомбы: {self.n - [j for i in self.poleg for j in i].count('F')}")
        print(f"   ╔══════════════════════════════╗   Ходы: {len(self.xodarr)}")
        for i in range(10):
            if i != 9: print(F" {str(i + 1)} ║", end="")
            else: print(10, "║", end="")
            for j in range(10):
                if self.poleg[i][j] in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                    print(f"[{self.nober[self.poleg[i][j]]}]", end="")
                else:
                    print(f"[{self.poleg[i][j]}]", end="")
            if i == 1: print(f"║   f - Поставить/убрать флаг", end="")
            elif i == 2: print(F"║   q - Поставить/убрать вопрос", end="")
            elif i == 3: print(f"║   0 0 r - Рестарт", end="")
            elif i == 4: print(f"║", end="")
            else: print("║", end="")
            print("\n", end="")
        print("   ╚══════════════════════════════╝")
            
    def __end(self) -> bool:
        if self.pole[self.y][self.x] == "M":
            if self.z not in ["+f","-f", "+q", "-q"] and self.poleg[self.y][self.x] not in ["Q", "F"]:
                return True
        return False

    def __ceil(self) -> None:
        try:
            event = input("Введите номер строки, номер столбца и действие: ").split()
            self.y, self.x = int(event[0]) - 1, int(event[1]) - 1
            self.z = None if len(event) == 2 else event[2].lower()
            if self.y < 0 or self.x < 0:
                self.__ceil()
            if self.z != None and self.z not in ["f", "q", "r"]:
                self.__ceil()
            if (self.y, self.x) not in self.xodarr and str(self.poleg[self.y][self.x]) not in [str(i) for i in range(9)]:
                self.xodarr.append((self.y,self.x))
        except Exception:
            if (self.y, self.x) in self.xodarr:
                self.xodarr.remove((self.y, self.x))
            self.__ceil()
            
    def __clear(self):
        system("cls")

    def __result(self) -> None:
        self.__draw()
        if self.__end():
            print("ВЫ ПРОИГРАЛИ")
        else:
            print("ВЫ ПОБЕДИЛИ")

    def __sos(self, arr):
        for (y, x) in arr:
            if (y, x) not in self.arr:
                try:
                    if self.pole[y][x] in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                        self.arr.append((y, x))
                    if self.pole[y][x] == 0:
                        self.__sos([(y + 1, x), (y, x), (y - 1, x), (y + 1, x + 1), (y, x + 1), (y - 1, x + 1), (y + 1, x - 1), (y, x - 1), (y - 1, x - 1)])
                except Exception:
                    continue

    def __open(self) -> None:
        if self.z == "r":
            self.__init__()
            self.run()
        elif self.z == "q":
            if self.poleg[self.y][self.x] == " ":
                self.poleg[self.y][self.x] = "Q"
            elif self.poleg[self.y][self.x] == "Q":
                self.poleg[self.y][self.x] = " "
        elif self.z == "f":
            if self.poleg[self.y][self.x] == " " and [j for i in self.poleg for j in i].count("F") != 15:
                self.poleg[self.y][self.x] = "F" 
            elif self.poleg[self.y][self.x] == "F":
                self.poleg[self.y][self.x] = " "  
        elif self.pole[self.y][self.x] == "M":
            if self.poleg[self.y][self.x] not in ["F", "Q"]:
                for i in range(10):
                    for j in range(10):
                        if self.pole[i][j] == "M" and self.poleg[i][j] != "F":
                            self.poleg[i][j] = "B"
        else:
            if self.pole[self.y][self.x] != "F":
                if self.pole[self.y][self.x] != 0:
                    self.poleg[self.y][self.x] = self.pole[self.y][self.x]
                else:
                    if self.poleg[self.y][self.x] not in ["Q", "F"]:
                        self.pole = self.pole + [[9 for _ in range(10)]]
                        self.pole = [[9 for _ in range(10)]] + self.pole
                        for i in range(12):
                            self.pole[i].append(9)
                            self.pole[i].insert(0, 9)     
                        self.__sos([(self.y + 1, self.x + 1)])
                        for (y, x) in self.arr:
                            if self.poleg[y - 1][x - 1] not in ["Q", "F"]:
                                self.poleg[y - 1][x - 1] = self.pole[y][x]
                        self.arr = []
                        self.pole.pop(0)
                        self.pole.pop(-1)
                        for i in range(10):
                            self.pole[i].pop(0)
                            self.pole[i].pop(-1)

    def __finis(self) -> bool:  
        return True if [j for i in self.poleg for j in i].count(" ") == 0 and [j for i in self.poleg for j in i].count("Q") == 0 else False

    def run(self) -> None:
        try:
            self.__clear()
            self.__draw()
            self.__ceil()
            self.__gener()
            self.__open()
            while not self.__end() and not self.__finis():
                self.__clear()
                self.__draw()
                self.__ceil()
                self.__open()
            self.__open()
            self.__clear()
            self.__result()
            r = input("\nРЕСТАРТ? ")
            if r == "" or r != "":
                print()
                self.__init__()
                self.run()
        except Exception:
            self.run()
        
if __name__ == "__main__":
    game: Engine = Engine()
    game.run()
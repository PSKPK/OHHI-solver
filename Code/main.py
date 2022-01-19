from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

Window.clearcolor=(1,1,1,1)

red=(100,.6,.6,.8)
blue=(20/255,20/255,100,.7)
nocolor=(.3,.3,.3,1)
num=0
oldunsolved=[]
unsolved=[]
keepcount=0

class myButton(Button):
    def __init__(self,**kwargs):
        super(myButton,self).__init__(**kwargs)
    presses=0
    lock=0

class Mylay(FloatLayout):
    global red,blue,num
    oh=Button(background_color=red,color=(1,1,1,1),text="0h",font_size='70sp',size_hint=(.28,.3),pos_hint={"x":.2,"y":.6})
    hi=Button(background_color=blue,color=(1,1,1,1),text="h1",font_size='70sp',size_hint=(.28,.3),pos_hint={"x":.52,"y":.6})
    b4=Button(text="4",font_size="30sp",size_hint=(.2,.15),pos_hint={"x":.15,"y":.32})
    b6=Button(text="6",font_size="30sp",size_hint=(.2,.15),pos_hint={"x":.4,"y":.32})
    b8=Button(text="8",font_size="30sp",size_hint=(.2,.15),pos_hint={"x":.65,"y":.32})
    b10=Button(text="10",font_size="30sp",size_hint=(.2,.15),pos_hint={"x":.275,"y":.15})
    b12=Button(text="12",font_size="30sp",size_hint=(.2,.15),pos_hint={"x":.525,"y":.15})
    back=Button(text="<--",font_size="30sp",size_hint=(.14,.08),pos_hint={"x":.1,"y":.04})
    submit=Button(text="Submit",font_size="25sp",size_hint=(.14,.08),pos_hint={"x":.76,"y":.04})
    dispButtons=[oh,hi,b4,b6,b8,b10,b12]
    array=[]
    def __init__(self,**kwargs):
        super(Mylay,self).__init__(**kwargs)
        self.dispOpt()
        self.back.bind(on_press=self.goBack)
        self.submit.bind(on_press=self.saveQsn)
        for k in self.dispButtons:
            if k.text=="0h" or k.text=="h1":
                continue
            k.bind(on_press=self.optionStart);
    def dispOpt(self):
        for b in self.dispButtons:
            self.add_widget(b)
    def remOpt(self):
        for b in self.dispButtons:
            self.remove_widget(b)
    def optionStart(self,button):
        global num
        num=int(button.text)
        self.remOpt()
        self.array=[]
        for k in range(num):
            new=[]
            for j in range(num):
                new.append(myButton(background_color=nocolor,size_hint=(0.9/num,0.8/num),pos_hint={"x":.05+j*(0.9/num),"y":.15+k*(0.8/num)},on_press=self.changeColor))
            self.array.append(new)
        for row in self.array:
            for b in row:
                self.add_widget(b)
        self.add_widget(self.back)
        self.add_widget(self.submit)
    def goBack(self,button):
        global keepcount
        keepcount=0
        for row in self.array:
            for b in row:
                self.remove_widget(b)
        self.remove_widget(self.back)
        self.remove_widget(self.submit)
        self.array=[]
        self.dispOpt()
    def changeColor(self,button):
        global red,blue,nocolor
        colors=[nocolor,red,blue]
        if button.lock==0:
            button.presses+=1
            button.background_color=colors[button.presses%3]
            button.presses%=3
    def saveQsn(self,button):
        global unsolved,oldunsolved,keepcount
        oldunsolved=unsolved
        for row in self.array:
            for b in row:
                b.lock=1
        self.showColors()
        self.startSolving()
        self.fillMiddles()
        self.byCount()
        unsolved=[]
        for row in range(num):
            for col in range(num):
                if self.array[row][col].background_color[3]==1:
                    unsolved.append((row,col))
        if unsolved==[]:
            self.solved()
        if unsolved==oldunsolved:
            self.findSimilarRows()
            self.findSimilarCols()
        keepcount+=1
        if keepcount<=25 and unsolved!=[]:
            self.saveQsn(Button())
    def showColors(self):
        global num
        def mydict(k):
            if k==.8:
                return "red "
            elif k==.7:
                return "blue"
            elif k==1:
                return "noco"
        for k in range(num):
            for j in range(num):
                print(mydict(self.array[k][j].background_color[3]),end=" ")
            print()
    def startSolving(self):
        print("\nCalled Start solving with num =",num)
        for row in range(num):
            self.fillRowPairs(row)
        for col in range(num):
            self.fillColPairs(col)
    def fillRowPairs(self,row):
        global red,blue,nocolor,num
        for k in range(num-2):
            if self.array[row][k].background_color[3]==1:
                continue
            if self.array[row][k+2].background_color[3]==.8 or self.array[row][k+2].background_color[3]==.7:
                continue
            if self.array[row][k].background_color[3]==.8 and self.array[row][k+1].background_color[3]==.8:
                self.array[row][k+2].background_color=blue
                print("Changed at loc : ",row,k+2)
            elif self.array[row][k].background_color[3]==.7 and self.array[row][k+1].background_color[3]==.7:
                self.array[row][k+2].background_color=red
                print("Changed at loc :",row,k+2)
        for k in range(num-1,1,-1):
            if self.array[row][k].background_color[3]==1:
                continue
            if self.array[row][k-2].background_color[3]==.8 or self.array[row][k-2].background_color[3]==.7:
                continue
            if self.array[row][k].background_color[3]==.8 and self.array[row][k-1].background_color[3]==.8:
                self.array[row][k-2].background_color=blue
                print("Changed at loc : ",row,k-2)
            elif self.array[row][k].background_color[3]==.7 and self.array[row][k-1].background_color[3]==.7:
                self.array[row][k-2].background_color=red
                print("Changed at loc :",row,k-2)
    def fillColPairs(self,col):
        global red,blue,nocolor,num
        for k in range(num-2):
            if self.array[k][col].background_color[3]==1:
                continue
            if self.array[k+2][col].background_color[3]==.8 or self.array[k+2][col].background_color[3]==.7:
                continue
            if self.array[k][col].background_color[3]==.8 and self.array[k+1][col].background_color[3]==.8:
                self.array[k+2][col].background_color=blue
                print("Changed at loc : ",k+2,col)
            elif self.array[k][col].background_color[3]==.7 and self.array[k+1][col].background_color[3]==.7:
                self.array[k+2][col].background_color=red
                print("Changed at loc :",k+2,col)
        for k in range(num-1,1,-1):
            if self.array[k][col].background_color[3]==1:
                continue
            if self.array[k-2][col].background_color[3]==.8 or self.array[k-2][col].background_color[3]==.7:
                continue
            if self.array[k][col].background_color[3]==.8 and self.array[k-1][col].background_color[3]==.8:
                self.array[k-2][col].background_color=blue
                print("Changed at loc : ",k-2,col)
            elif self.array[k][col].background_color[3]==.7 and self.array[k-1][col].background_color[3]==.7:
                self.array[k-2][col].background_color=red
                print("Changed at loc :",k-2,col)
    def fillMiddles(self):
        global num,red,blue,nocolor
        for row in range(1,num-1):
            for col in range(num):
                if self.array[row-1][col].background_color[3]==.8 and self.array[row+1][col].background_color[3]==.8:
                    self.array[row][col].background_color=blue
                elif self.array[row-1][col].background_color[3]==.7 and self.array[row+1][col].background_color[3]==.7:
                    self.array[row][col].background_color=red
        for row in range(num):
            for col in range(1,num-1):
                if self.array[row][col-1].background_color[3]==.8 and self.array[row][col+1].background_color[3]==.8:
                    self.array[row][col].background_color=blue
                elif self.array[row][col-1].background_color[3]==.7 and self.array[row][col+1].background_color[3]==.7:
                    self.array[row][col].background_color=red

    def byCount(self):
        global red,blue,nocolor,num
        for row in self.array:
            blues=0
            reds=0
            for k in row:
                if k.background_color[3]==.8: reds+=1
                elif k.background_color[3]==.7: blues+=1
            if reds==num/2:
                for k in row:
                    if k.background_color[3]==1:
                        k.background_color=blue
            if blues==num/2:
                for k in row:
                    if k.background_color[3]==1:
                        k.background_color=red
        for col in range(num):
            blues=0
            reds=0
            for row in range(num):
                if self.array[row][col].background_color[3]==.8: reds+=1
                if self.array[row][col].background_color[3]==.7: blues+=1
            if reds==num/2:
                for row in range(num):
                    if self.array[row][col].background_color[3]==1:
                        self.array[row][col].background_color=blue
            if blues==num/2:
                for row in range(num):
                    if self.array[row][col].background_color[3]==1:
                        self.array[row][col].background_color=red
    def findSimilarCols(self):
        print("FindingSimilarCols")
        twos=[]
        fulls=[]
        for col in range(num):
            count=0
            for row in range(num):
                if self.array[row][col].background_color[3]==1:
                    count+=1
            if count==0:
                fulls.append(col)
            if count==2:
                twos.append(col)
        for k in range(len(twos)):
            twonow=twos[k]
            for j in range(len(fulls)):
                check=1
                fullnow=fulls[j]
                for m in range(num):
                    if self.array[m][twonow].background_color[3]==1:
                        continue
                    if self.array[m][twonow].background_color[3]!=self.array[m][fullnow].background_color[3]:
                        check=0
                        break
                if check==0:
                    continue
                for m in range(num):
                    if self.array[m][twonow].background_color[3]==1:
                        if self.array[m][fullnow].background_color[3]==.8:
                            self.array[m][twonow].background_color=blue
                        elif self.array[m][fullnow].background_color[3]==.7:
                            self.array[m][twonow].background_color=red
    def findSimilarRows(self):
        print("FindingSimilarRows")
        twos=[]
        fulls=[]
        for row in range(num):
            count=0
            for b in self.array[row]:
                if b.background_color[3]==1:
                    count+=1
            if count==0:
                fulls.append(row)
            if count==2:
                twos.append(row)
        for k in range(len(twos)):
            twonow=self.array[twos[k]]
            for j in range(len(fulls)):
                check=1
                fullnow=self.array[fulls[j]]
                for m in range(num):
                    if twonow[m].background_color[3]==1:
                        continue
                    if twonow[m].background_color[3]!=fullnow[m].background_color[3]:
                        check=0
                        break
                if check==0:
                    continue
                for m in range(num):
                    if twonow[m].background_color[3]==1:
                        if fullnow[m].background_color[3]==.8:
                            self.array[twos[k]][m].background_color=blue
                        elif fullnow[m].background_color[3]==.7:
                            self.array[twos[k]][m].background_color=red
    def solved(self):
        sol=Button(text="Solved !!",font_size="30sp",color=(0,0,0,1),background_color=(1,1,1,1),size_hint=(.18,.12),pos_hint={"x":.40,"y":.01})



class MyApp(App):
    def build(self):
        return Mylay()

if __name__=="__main__":
    newapp=MyApp()
    newapp.run()

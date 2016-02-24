"""
1/27 複製音樂檔 圖片檔 再刪掉 保持畫面簡潔
1/20 增加匯出中文範例
1/15 增加了外部翻譯選擇與否 

1/13 增加快捷鍵 按下F1可將焦點移到龜模組作圖區

1/12 對標記點擊右鍵可直接取消標記
(但焦點與點擊必須在同個text)
函式註解
1/11 增加了行號在左下角
並且將排法從grid變為pack
改變編排位置
修改bug
字體大小更改checkbuttom
增加部分函式註解
"""
# (^|(?<=\W))(?<!"|'|[\\u4e00-\\u9fa5])Ro(?=$|\W)(?!"|'|[\\u4e00-\\u9fa5])
from tkinter.filedialog import *
from tkinter import *
from idlelib.Percolator import Percolator
from idlelib.ColorDelegator import ColorDelegator
import TurtleTranslate
import os, sys,re
import importlib
import turtle_tc as turtle
from tkinter.simpledialog import askstring
from tkinter import messagebox
import time
import shutil

menufont = ('Courier New', 12, 'normal')
menufontC = ('微軟正黑體', 10, 'normal')
btnfont=  ('Verdana', 12, 'bold')
Linefont=  ('Verdana', 8, 'normal')
txtfont = ['Lucida Console', 10, 'normal']
RUNNING= 3
DONE= 4
EVENTDRIVEN= 5
最小字體= 6
最大字體= 30
字體大小= [8, 9, 10, 11, 12, 14, 18, 20, 22, 24, 30]


def 得到範例程式():
    """
    抓取目錄下Demo資料夾
    名字為tdemo開頭的資料夾及py檔案
    回傳list型態
    舉例:[[資料夾名1,檔案名1,檔案名2],[資料夾名2,檔案名3],檔案名4]
    """
    現在位置 = os.getcwd()
    #print(cwd, os.listdir(cwd))
    檔案位置="Demo\\"
    if os.path.isdir(檔案位置) == False:
        print("範例檔案夾Demo不存在")

    檔案表 = [檔案 for 檔案 in os.listdir(檔案位置) if
                     檔案.startswith("tdemo_") and
                     not 檔案.endswith(".pyc")]
    程式表 = []
    for 檔案名 in 檔案表:
        if 檔案名.endswith(".py"):
            程式表.append(檔案名)
        else:
            path = os.path.join(檔案位置,檔案名)
            sys.path.append(path)
            資料夾名 = [檔案名]
            程式們 = [程式 for 程式 in os.listdir(path) if
                            程式.startswith("tdemo_") and
                            程式.endswith(".py")]
            程式表.append(資料夾名+程式們)
    return 程式表


class GUIDemo():
    """
    畫出GUI介面，傳入Tk()類
    """
    def __init__(self, master=None):
        """
        建立選單列，文字及畫圖區
        還有建立按鈕
        """
        #Frame.__init__(self, master)
        self.root=root= master
        self.建立文字區()
        self.建立選單列()
        self.module={}
        self.程式名= ""
        self.外部翻譯=False
        # g_frame = Frame(root)
        self.按鈕框 = 按鈕框 = Frame(root, height=100)
        self.輸出行號= Label(按鈕框,  text="L: 1 C: 1", font=Linefont, bg='lightgrey', borderwidth=2, relief=SUNKEN)
        self.輸出行號.pack(side=LEFT, expand=0, fill=BOTH)
        self.輸出結果= Label(按鈕框,  text="---", font=btnfont, bg="#FFFFBF", borderwidth=3, relief=RIDGE)
        self.輸出結果.pack(side=LEFT, expand=1, fill=BOTH)
        self.開始鍵=  Button(按鈕框, text=" 開始 ", command= self.執行,fg="black", disabledforeground= "#fed", font= btnfont)
        self.開始鍵.pack(side=LEFT, expand=1, fill=X)
        self.停止鍵=  Button(按鈕框, text=" 停止 ", command= self.停止執行,fg="black", disabledforeground= "#fed", font= btnfont)
        self.停止鍵.pack(side=LEFT, expand=1, fill=X)
        self.按鈕框.pack(side=TOP, expand=0, fill=BOTH)
        # g_frame.pack(side=TOP, expand=0, fill=BOTH)
        
        self.按鈕設置(NORMAL,DISABLED)


    def 建立選單列(self):
        """
        建立選單列並加上快捷鍵
        檔案:
            清除文本    開啟檔案
            另存檔案1   另存檔案2
            結束
        編輯:
            查詢並標記   將標記取代
            取消標記    到第...行
        字體:
            字體放大    字體縮小
            字體號碼...
        功能:
            英翻中     中翻英
            執行       停止
        範例:
            範例程式...
        """
        選單列 = Menu(self.root)
        檔案選單 = Menu(選單列,tearoff=0, font= menufontC)
        檔案選單.add_command(label="清除文本", command=self.清除文本,accelerator = 'ctrl+d')
        檔案選單.add_command(label="開啟檔案", command=self.開啟檔案,accelerator = 'ctrl+o')
        檔案選單.add_command(label="另存檔案1", command=self.另存新檔1,accelerator = 'ctrl+s')
        檔案選單.add_command(label="另存檔案2", command=self.另存新檔2,accelerator = 'ctrl+alt+o')
        檔案選單.add_command(label="結束", command=self.關閉視窗)
        選單列.add_cascade(label="檔案", menu=檔案選單)
        self.root.bind_all('<Control-Key-s>', self.另存新檔1)
        self.root.bind_all('<Control-Alt-Key-s>', self.另存新檔2)
        self.root.bind_all('<Control-Key-d>', self.清除文本)
        self.root.bind_all('<Control-Key-o>', self.開啟檔案)
        
        編輯選單 =Menu(選單列,tearoff=0, font= menufontC)
        編輯選單.add_command(label="查詢並標記", command=self.查詢文本,accelerator = 'ctrl+f')
        編輯選單.add_command(label="將標記取代...", command=self.標記取代,accelerator = 'ctrl+b')
        編輯選單.add_command(label="取消標記", command=self.取消標記,accelerator = 'ctrl+w')
        編輯選單.add_separator()
        編輯選單.add_command(label="到第...行", command=self.到行數,accelerator = 'ctrl+g')
        選單列.add_cascade(label="編輯", menu=編輯選單)
        self.root.bind_all('<Control-Key-f>', self.查詢文本)
        self.root.bind_all('<Control-Key-b>', self.標記取代)
        self.root.bind_all('<Control-Key-w>', self.取消標記)
        self.root.bind_all('<Control-Key-g>', self.到行數)
        self.v = StringVar()
        
        字體選單 =Menu(選單列,tearoff=0, font= menufontC)
        字體選單.add_command(label="字體放大", command=self.字體放大)
        字體選單.add_command(label="字體縮小", command=self.字體縮小)
        字體選單.add_separator()
        for size in 字體大小:
            def resize(size=size):
                def emit():
                    self.設定字體(size)
                return emit
            字體選單.add_radiobutton(label=str(size),command=resize(size), variable=self.v, value=str(size))
        選單列.add_cascade(label="字體", menu=字體選單)
        self.v.set('10')
        
        self.bv = BooleanVar()
        self.bv.set(False)
        self.功能選單 = 功能選單 =Menu(選單列,tearoff=0, font= menufontC)
        功能選單.add_command(label="英翻中(en->ch)", command=self.英中翻譯,accelerator = 'alt+t')
        功能選單.add_command(label="中翻英(ch->en)", command=self.中英翻譯)
        功能選單.add_separator()
        功能選單.add_checkbutton(label="增加外部翻譯",variable=self.bv)
        功能選單.add_separator()
        功能選單.add_command(label="執行", command= self.執行,accelerator = 'ctrl+e')
        功能選單.add_command(label="停止", command= self.停止執行,accelerator = 'ctrl+r')
        功能選單.add_separator()
        功能選單.add_command(label="匯出中文範例", command= self.匯出範例)
        選單列.add_cascade(label="功能", menu=功能選單)
        self.root.bind_all('<Alt-t>', self.英中翻譯)
        self.root.bind_all('<Control-Key-e>', self.執行)
        self.root.bind_all('<Control-Key-r>', self.停止執行)
        self.root.bind_all('<KeyPress-F1>',self.焦點轉移)
        範例選單 = Menu(選單列,tearoff= 1, font= menufont)
        選單列.add_cascade(label="範例", menu=範例選單)
        aa=0;
        for i in 得到範例程式():
            def loadexample(x):
                def emit():
                    self.載入範例(x)
                return emit
            if isinstance(i,str):
                程式名= i.replace("tdemo_","",1)
                範例選單.add_command(label=程式名[:-3], command= loadexample(i))
            else:
                程式夾, 程式檔 = i[0], i[1:]
                程式夾2= 程式夾.replace("tdemo_","",1)
                範例選單一 = Menu(範例選單,tearoff=1, font=menufont)
                範例選單.add_cascade(label=程式夾2, menu=範例選單一)
                for 程式名 in 程式檔:
                    aa+=1
                    程式路徑=os.path.join(程式夾,程式名)
                    程式名= 程式名.replace("tdemo_","",1)
                    範例選單一.add_command(label=程式名[:-3], command= loadexample(程式路徑))
        print(aa)
        self.root.config(menu=選單列)

    def 建立文字區(self):
        """
        建立兩個Text區跟龜模組畫圖區並建立快捷鍵        
        """
        setup={}
        pane= PanedWindow(orient=HORIZONTAL, bg='black')
        text_frame= Frame(pane)
        self.text=text= Text(text_frame, name='text', padx=5,wrap='none', width=45,  bg='white', font= tuple(txtfont),tabs=('4c'),undo=True)
        text.name="text"
        vbar= Scrollbar(text_frame, name='vbar')
        
        vbar['command'] = text.yview
        vbar.pack(side=RIGHT, fill=Y)
        hbar = Scrollbar(text_frame, name='hbar', orient=HORIZONTAL)
        hbar['command'] = text.xview
        hbar.pack(side=BOTTOM, fill=X)
        
        text.pack(side=LEFT, fill=BOTH, expand=1)
 
        pane.add(text_frame)  
        
        
        text_frame2= Frame(pane)
        self.text2=text2= Text(text_frame2, name='text', padx=5,wrap='none', width=45, bg='white',font= tuple(txtfont),undo=True)
        text.name="text2"
        vbar= Scrollbar(text_frame2, name='vbar')
        vbar['command'] = text2.yview
        vbar.pack(side=RIGHT, fill=Y)
        hbar = Scrollbar(text_frame2, name='hbar', orient=HORIZONTAL)
        hbar['command'] = text2.xview
        hbar.pack(side=BOTTOM, fill=X)
        text2.pack(side=LEFT, fill=BOTH, expand=1)
        pane.add(text_frame2) 
        
        self.canvwidth= 800 
        self.canvheight= 600 
        turtle._Screen._root= self.root
        turtle._Screen._canvas= canvas= self._canvas= turtle.ScrolledCanvas(self.root, 800, 600, 1000, 800)
        canvas.adjustScrolls()
        canvas._rootwindow.bind('<Configure>', self.onResize)
        canvas._canvas['borderwidth'] = 0
        self.screen =screen = turtle.Screen()
        turtle.TurtleScreen.__init__(screen, screen._canvas)
        self.scanvas=scanvas= screen._canvas
        turtle.RawTurtle.screens = [screen]
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        pane.add(canvas) # for 畫圖
        # self.scanvas.bind('<Button-1>',self.焦點轉移)
        
        pane.pack(side=TOP, expand=1, fill=BOTH)
        
        Percolator(text).insertfilter(ColorDelegator())
        Percolator(text2).insertfilter(ColorDelegator())
        
        text.bind('<Control-MouseWheel>', self.滑鼠滾輪)
        text.bind('<Control-Button-4>', self.字體放大)
        text.bind('<Control-Button-5>', self.字體縮小)
        text2.bind('<Control-MouseWheel>', self.滑鼠滾輪)
        text2.bind('<Control-Button-4>', self.字體放大)
        text2.bind('<Control-Button-5>', self.字體縮小)
        text.bind('<Button-3>',self.選取標記)
        text2.bind('<Button-3>',self.選取標記)
        text.bind("<KeyRelease>", self.行號更新)
        text.bind("<ButtonRelease>", self.行號更新)
        text2.bind("<KeyRelease>", self.行號更新)
        text2.bind("<ButtonRelease>", self.行號更新)

    def 行號更新(self, event):
        """
        當按下鍵盤及滑鼠並放開時，連結的函數
        將目前游標所在的行號及位置輸出
        """
        focused_on = self.root.focus_get()
        if focused_on != self.text and focused_on != self.text2:
            focused_on = self.text
        te = focused_on.index(INSERT)
        l,c= te.split(".")
        c=str(int(c)+1)
        self.輸出行號.config(text="L:%s C:%s"%(l.rjust(2),c.rjust(2)))
        
    def onResize(self, event):
        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()
        self._canvas.xview_moveto(0.5*(self.canvwidth-cwidth)/self.canvwidth)
        self._canvas.yview_moveto(0.5*(self.canvheight-cheight)/self.canvheight)

    def 匯出範例(self,event=None):
        存放目錄= "tc_Demo\\"
        if not os.path.exists(存放目錄):
            os.mkdir(存放目錄)
        檔案位置="Demo\\"
        for i in 得到範例程式():
            if isinstance(i,str):
                新程式名= i.replace("tdemo_","",1)
                新程式名="tc_"+新程式名
                程式路徑=os.path.join(存放目錄,i)
                TurtleTranslate.翻譯檔案(存放目錄,程式路徑,False,新程式名)
            else:
                程式夾, 程式檔 = i[0], i[1:]
                程式夾2= 程式夾.replace("tdemo_","",1)
                存放程式夾= os.path.join(存放目錄,程式夾2)
                if not os.path.exists(存放程式夾):
                    os.mkdir(存放程式夾)
                for 程式名 in 程式檔:
                    程式路徑=os.path.join(程式夾,程式名)
                    程式路徑=os.path.join(檔案位置,程式路徑)
                    新程式名= 程式名.replace("tdemo_","",1)
                    新程式名="tc_"+新程式名
                    TurtleTranslate.翻譯檔案(存放程式夾,程式路徑,False,新程式名)

        shutil.copyfile("Demo//tdemo_games//help.gif","tc_Demo\\games\\help.gif")
        shutil.copyfile("Demo//tdemo_games//next.gif","tc_Demo\\games\\next.gif")
        shutil.copyfile("Demo//tdemo_games//tangramdata.py","tc_Demo\\games\\tangramdata.py")
        TurtleTranslate.翻譯檔案("tc_Demo\\games\\","Demo//tdemo_games//button.py",False,"button.py")
        被複製目錄= "Demo//tdemo_games//"
        filesName= ["huhn01.gif","huhn02.gif","landschaft800x600.gif",
                    "daneben.wav","applaus.wav","gameover.wav","getroffen.wav"]
        for i in filesName:
            shutil.copyfile(被複製目錄+i,"tc_Demo\\games\\"+i)
        self.輸出結果.config(text="匯出中文範例文件夾",fg= "black")
    
    def 焦點轉移(self,event=None):
        """
        將焦點移到龜模組畫布上
        """
        print(self.root.focus_get().__class__)
        self._canvas._canvas.focus_force()
        
    def 開啟檔案(self,event=None):
        """
        將文件區文字清除
        開啟檔案將檔案文字顯示在文字區1
        """
        self.停止執行()
        檔案路徑 = askopenfilename()
        f= open(檔案路徑,"r",encoding='UTF-8')
        檔案內容= f.read()
        f.close()
        self.text.delete("1.0", "end") 
        self.text2.delete("1.0", "end") 
        檔案內容 = self.text.insert(INSERT,檔案內容)
        self.程式名= os.path.basename(檔案路徑)
        print(檔案路徑)
        self.輸出結果.config(text="開啟檔案 %s" % self.程式名,fg= "black")

    def 另存新檔1(self, event=None):
        """
        將文件區1的文字存檔
        """
        檔案路徑 = asksaveasfilename(defaultextension= '.py',initialfile= self.程式名,filetypes= [('all files', '.*'), ('py files', '.py')] )
        檔案內容 = self.text.get(1.0,END)
        f=open(檔案路徑,"w",encoding='UTF-8')
        f.write(檔案內容)
        f.close()
        新檔名= os.path.basename(檔案路徑)
        print(檔案路徑)
        self.輸出結果.config(text="文件區1另存新檔 %s" % 新檔名,fg= "black")

    def 另存新檔2(self, event=None):
        """
        將文件區2的文字存檔
        """
        程式名= 'tc_'+self.程式名
        檔案路徑 = asksaveasfilename(defaultextension= '.py',initialfile= 程式名,filetypes= [('all files', '.*'), ('py files', '.py')] )
        檔案內容 = self.text2.get(1.0,END)
        f=open(檔案路徑,"w",encoding='UTF-8')
        f.write(檔案內容)
        f.close()
        新檔名= os.path.basename(檔案路徑)
        print(檔案路徑)
        self.輸出結果.config(text="文件區2另存新檔 %s" % 新檔名,fg= "black")

    def 清除文本(self,event=None):
        """
        將文件區塊的文字全部清除
        """
        self.text.delete("1.0", "end") 
        self.text2.delete("1.0", "end")
        self.程式名= "new"
        self.輸出結果.config(text="清除文件區",fg= "black")

    def 關閉視窗(self):
        self.root.quit()
 
    def 載入範例(self,路徑):
        """
        載入範例順便將龜模組中文化
        """
        self.停止執行()
        檔案路徑 = "Demo"+os.path.sep+路徑
        print(檔案路徑)
        f= open(檔案路徑,"r",encoding='UTF-8')
        檔案內容= f.read()
        f.close()
        self.text.delete("1.0", "end") 
        檔案內容 = self.text.insert(INSERT,檔案內容)
        
        self.英中翻譯()
        self.程式名= os.path.basename(檔案路徑)
        self.輸出結果.config(text="載入檔案  %s" % self.程式名,fg= "black")
     
    def 查詢文本(self,event=None):
        """
        抓取所選取範圍的單字並默認其為查詢的預設字
        根據使用者輸入字串查詢目前游標所在的文件區塊
        將查詢結果全部標記
        利用正規表示法查詢，查詢結果更精準
        文件區根據目前焦點決定(都沒有則為文件區1)
        範例:
        f=open(...
        fd(100)
        查找f，fd不納入
        """
        focused_on = self.root.focus_get()
        文字區= "文件區1" if focused_on == self.text else "文件區2" 
        if focused_on != self.text and focused_on != self.text2:
            focused_on = self.text
            文字區= "文件區1" 
        te = focused_on.get("sel.first", "sel.last")
        target = askstring('搜尋文本', '查詢字?',initialvalue=te)
        記數=0
        
        if target:
            start = focused_on.index(1.0)
            string = focused_on.get(1.0,END)

            # 當前面單字為\W(非字母)及不為[\\u4e00-\\u9fa5](中文字範圍)
            # 當後面單字為\W(非字母)及不為[\\u4e00-\\u9fa5](中文字範圍)
            match=re.finditer("""(?<=\W)(?<!"|'|[\\u4e00-\\u9fa5])%s(?=$|\W)(?!"|'|[\\u4e00-\\u9fa5])"""% target,string)
            for i in match:
                match_start = focused_on.index("%s+%dc" % (start, i.start()))
                match_end = focused_on.index("%s+%dc" % (start, i.end()))
                記數+=1
                focused_on.tag_add("查詢字", match_start, match_end)
                focused_on.mark_set(INSERT, match_end)
                focused_on.see(INSERT)
                focused_on.focus()
                focused_on.tag_config("查詢字", background="yellow", foreground="blue")
                # focused_on.tag_lower("查詢字")
            focused_on.tag_raise(SEL)
            focused_on.tag_remove(SEL,"sel.first", "sel.last")
                
            if 記數!= 0:
                messagebox.showinfo('查詢結果','%s 共有 %d 個'%(target,記數))
                self.輸出結果.config(text="%s %s 總共有%d個"%(文字區,target,記數),fg= "black")
            else:
                messagebox.showinfo('查詢結果','無此字: '+target)
                self.輸出結果.config(text="%s 無此字: %s"%(文字區,target),fg= "black")
        
    def 標記取代(self,event=None):
        """
        抓取所選取範圍的單字並默認其為查詢的預設字
        根據使用者輸入字串查詢目前游標所在的文件區塊
        將查詢結果全部標記
        文件區根據目前焦點決定(都沒有則為文件區1)
        """
        focused_on = self.root.focus_get()
        文字區= "文件區1" if focused_on == self.text else "文件區2" 
        if focused_on != self.text and focused_on != self.text2:
            focused_on = self.text
            文字區= "文件區1" 
        target = askstring('取代...', '將標記取代為?',initialvalue="變數名")
        記數=0
        if target != None:
            標記範圍= focused_on.tag_ranges("查詢字")
            for i in range(len(標記範圍)-1,0,-2):
                記數+=1
                focused_on.delete(標記範圍[i-1],標記範圍[i])
                focused_on.insert(標記範圍[i-1],target)
                endpos=str(標記範圍[i-1])+'+%dc' % len(target)
                # print(endpos)
                focused_on.tag_add("查詢字", 標記範圍[i-1],endpos )
                focused_on.tag_config("查詢字", background="yellow", foreground="blue")
            
        if 記數!= 0:
            messagebox.showinfo('取代...','總共取代為 %s 共有 %d 個'%(target,記數))
            self.輸出結果.config(text="%s將標記字串取代為%s"%(文字區,target),fg= "black")
        else:
            self.輸出結果.config(text="%s無要取代的文字"%(文字區),fg= "black")
    
    def 取消標記(self,event=None):
        """
        將目前游標所在的文件區塊的標記全部取消
        文件區根據目前焦點決定(都沒有則為文件區1)
        """
        focused_on = self.root.focus_get()
        文字區= "文件區1" if focused_on == self.text else "文件區2" 
        if focused_on != self.text and focused_on != self.text2:
            focused_on = self.text
            文字區= "文件區1" 
        focused_on.tag_delete("查詢字")
        self.輸出結果.config(text="%s全標記取消"%(文字區),fg= "black")
        
    def 選取標記(self,event=None):
        """
        將選取的單字標記
        如鼠標現在的位置為標記位置則取消標記
        """
        focused_on = self.root.focus_get()
        文字區= "文件區1" if focused_on == self.text else "文件區2" 
        if focused_on != self.text and focused_on != self.text2:
            focused_on = self.text
            文字區= "文件區1" 
        te = focused_on.get("sel.first", "sel.last")
        start= focused_on.index("sel.first")
        end= focused_on.index("sel.last")
        if te !='':
            標記範圍= focused_on.tag_ranges("查詢字")
            範圍=[(str(標記範圍[i]),str(標記範圍[i+1])) for i in range(0,len(標記範圍),2)]
            if (start, end) in 範圍:
                focused_on.tag_remove("查詢字" ,start, end)
                self.輸出結果.config(text="%s移除標記"%(文字區),fg= "black") 
            else:
                focused_on.tag_add("查詢字", start, end)
                focused_on.tag_raise(SEL)
                focused_on.tag_config("查詢字", background="yellow", foreground="blue")
                self.輸出結果.config(text="%s增加新標記"%(文字區),fg= "black")
        else:
            print(focused_on.index('current'))
            標記範圍= focused_on.tag_ranges("查詢字")
            範圍= [(str(標記範圍[i]),str(標記範圍[i+1])) for i in range(0,len(標記範圍),2)]
            鼠標位置= focused_on.index('current')
            鼠標l,鼠標c= 鼠標位置.split(".")
            for (start, end) in 範圍:
                l,c= start.split(".")
                l2,c2= end.split(".")
                開始位置= float(c)
                結束位置= float(c2)
                鼠標c=float(鼠標c)
                if (鼠標l==l) and (結束位置>=鼠標c) and (鼠標c> 開始位置):
                    focused_on.tag_remove("查詢字" ,start, end)
                    self.輸出結果.config(text="%s移除標記%s~%s"%(文字區,start,end),fg= "black")
                    break
            print(鼠標位置)

    def 到行數(self,event=None):
        """
        根據輸入的數字決定到文件區的第幾行
        文件區根據目前焦點決定(都沒有則為文件區1)
        """
        focused_on = self.root.focus_get()
        文字區= "文件區1" if focused_on == self.text else "文件區2" 
        if focused_on != self.text and focused_on != self.text2:
            focused_on = self.text
            文字區= "文件區1" 
        target = askstring("輸入正整數","到第幾行?")
        if target.isdigit() :
            pastit = target + ('.0')
            focused_on.mark_set(INSERT,pastit)
            focused_on.see(INSERT)
            focused_on.focus()
            self.輸出結果.config(text="到%s第%s行"%(文字區,target),fg= "black")
        
    def 英中翻譯(self,event=None):
        """
        將文件區1的龜模組函數名稱轉換成中文別名
        轉換後的文字顯示在文件區2
        """
        self.輸出結果.config(text="翻譯中...",fg= "black")
        檔案內容 = self.text.get(1.0,END)
        f=open("temp.py","w",encoding='UTF-8')
        f.write(檔案內容)
        f.close()
        TurtleTranslate.翻譯檔案("", "temp.py",self.bv.get())
        f=open("tc_temp.py","r",encoding='UTF-8')
        檔案內容= f.read()
        f.close()    
        self.text2.delete("1.0", "end") 
        檔案內容 = self.text2.insert(INSERT,檔案內容)
        os.remove("temp.py")
        os.remove("tc_temp.py")
        self.輸出結果.config(text="翻譯: 英文->中文",fg= "black")

    def 中英翻譯(self):
        檔案內容 = self.text.get(1.0,END)
        f=open("temp.py","w",encoding='UTF-8')
        f.write(檔案內容)
        f.close()
        TurtleTranslate.中翻英檔案("", "temp.py")
        f=open("te_temp.py","r",encoding='UTF-8')
        檔案內容= f.read()
        f.close()    
        self.text2.delete("1.0", "end") 
        檔案內容 = self.text2.insert(INSERT,檔案內容)
        os.remove("temp.py")
        os.remove("te_temp.py")
        self.輸出結果.config(text="翻譯: 中文 -> 英文",fg= "black")

    def 按鈕設置(self,開始設置,停止設置):
        """
        將文件區1的龜模組函數名稱轉換成英文名
        轉換後的文字顯示在文件區2
        """
        self.開始鍵.config(state=開始設置,bg="#ffc100" if 開始設置 == NORMAL else "#999999")
        self.停止鍵.config(state=停止設置,bg="#ffc100" if 停止設置 == NORMAL else "#999999")
        if 開始設置 == NORMAL:
            self.root.bind_all('<Control-Key-e>', self.執行)
            self.root.unbind_all('<Control-Key-r>')
            self.功能選單.entryconfig("執行",state=NORMAL)
            self.功能選單.entryconfig("停止",state=DISABLED)
        else:
            self.root.unbind_all('<Control-Key-e>')
            self.root.bind_all('<Control-Key-r>', self.停止執行)
            self.功能選單.entryconfig("執行",state =DISABLED)
            self.功能選單.entryconfig("停止",state=NORMAL)
        
    def 清除畫面(self):
        """
        將龜模組畫布的畫面重設
        """
        self.screen.clear()
        self.screen._delete("all")
        self.scanvas.config(cursor="")
        self.screen =screen = turtle.Screen()
        turtle.TurtleScreen.__init__(screen, screen._canvas)

    def 停止執行(self,event=None):
        """
        將龜模組畫布的動作停止並連結清除畫面函數
        最後連結按鈕設置改變執行選項開關
        """
        if turtle.TurtleScreen._RUNNING == True:
            if self.程式名== "tdemo_tangram.py":
                os.remove("help.gif")
                os.remove("next.gif")
                os.remove("tangramdata.py")
                os.remove("button.py")
            elif self.程式名== "tdemo_moorhuhn.py":
                filesName= ["huhn01.gif","huhn02.gif","landschaft800x600.gif",
                            "daneben.wav","applaus.wav","gameover.wav","getroffen.wav"]
                for i in filesName:
                    os.remove(i)
        turtle.TurtleScreen._RUNNING = False
        self.清除畫面()
        self.按鈕設置(NORMAL,DISABLED)
        self.輸出結果.config(text="已停止!",fg= "red")
        
    def 執行(self,event=None):
        """
        將文件區2的程式執行將結果輸出至label輸出結果
        連結按鈕設置改變執行選項開關
        """
        turtle.TurtleScreen._RUNNING = True
        self.清除畫面()
        self.按鈕設置(DISABLED,NORMAL)
        self.輸出結果.config(text="執行中...",fg= "black")
        檔案內容 = self.text2.get(1.0,END)
        檔案內容=檔案內容.replace("import turtle ","import turtle_tc ")
        檔案內容=檔案內容.replace("from turtle ","from turtle_tc ")
        f=open("Demotempfile313341.py","w",encoding='UTF-8')
        f.write(檔案內容)
        f.close()
        if self.程式名== "tdemo_tangram.py":
            shutil.copyfile("Demo//tdemo_games//help.gif","help.gif")
            shutil.copyfile("Demo//tdemo_games//next.gif","next.gif")
            shutil.copyfile("Demo//tdemo_games//tangramdata.py","tangramdata.py")
            TurtleTranslate.翻譯檔案("","Demo//tdemo_games//button.py",False,"button.py")
        elif self.程式名== "tdemo_moorhuhn.py":
            被複製目錄= "Demo//tdemo_games//"
            filesName= ["huhn01.gif","huhn02.gif","landschaft800x600.gif",
                        "daneben.wav","applaus.wav","gameover.wav","getroffen.wav"]
            for i in filesName:
                shutil.copyfile(被複製目錄+i,i)
        
            
        module=""
        # module=__import__("Demotempfile313341")
        # module= sys.modules[module]
        __import__("Demotempfile313341")
 
        module= sys.modules["Demotempfile313341"]
        
        module= self.module= importlib.reload(module)
        os.remove("Demotempfile313341.py")
        self.screen.mode("standard")
        state = RUNNING
        # print('主函數' in vars(module))
        # print('main' in vars(module))
        try:
            if '主函數' in vars(module):
              result = module.主函數();print("主函數")
            elif 'main' in vars(module):
              result = module.main()
              print("main")
            else:
              result = ''

            if result == "EVENTLOOP":
                self.state = EVENTDRIVEN
            else:
                self.state = DONE
               
        except turtle.Terminator:
            self.state = DONE
            result = "已停止！"
            
        if self.state == DONE:
            self.按鈕設置(NORMAL,DISABLED)
            self.輸出結果.config(text=result,fg= "black")
            if '主函數' in vars(module):
                del module.主函數
            if 'main' in vars(module):
                del module.main
        elif self.state == EVENTDRIVEN:
            self.輸出結果.config(text="用滑鼠、鍵盤 控制螢幕 或 按 停止",fg= "red")
            if '主函數' in vars(module):
                del module.主函數
            if 'main' in vars(module):
                del module.main

    def 設定字體(self, size):
        """
        設定文件區的字體大小
        將字體大小輸出至label輸出結果
        """
        txtfont[1] = size
        self.text['font'] = tuple(txtfont)
        self.text2['font'] = tuple(txtfont)
        self.輸出結果['text'] = '字體大小 %d' % size
        self.v.set(str(size))

         
    def 字體縮小(self, dummy=None):
        self.設定字體(max(txtfont[1] - 1, 最小字體))
        return 'break'

    def 字體放大(self, dummy=None):
        self.設定字體(min(txtfont[1] + 1, 最大字體))
        return 'break'


    def 滑鼠滾輪(self, event):
        # For wheel up, event.delte = 120 on Windows, -1 on darwin.
        # X-11 sends Control-Button-4 event instead.
        if event.delta < 0:
            return self.字體縮小()
        else:
            return self.字體放大()

        
        
if __name__ == '__main__':
    root = Tk()
    menufont = ("Arial", 12, NORMAL)
    root.title('龜作圖程式翻譯')
    app = GUIDemo(master=root)
    root.mainloop()
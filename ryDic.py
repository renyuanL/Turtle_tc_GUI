'''
ryDic.py
'''

#from turtle_jp import  中英對照表 # 勿貪心，淺嘗即可。免得失去焦點。
from turtle_tc_alias import * 
增加的中英對照表=[

    ('self', '我'),
    ('main', '主函數'),

    ('scale', '比例尺度'),
    ('game', '遊戲'),
    ('row', '列'),
    ('writer', '寫手'),
    ('col', '行'),
    ('size', '尺寸'),
    ('side', '邊'),
    ('msg', '訊息'),
    ('level', '等級'),
    ('sticks', '棒子們'),
    ('state', '狀態'),
    ('radius', '半徑'),
    ('tiledict', '瓦片字典'),
    ('start', '開始'),

    ('parity','對等性'), # 一時不知怎麼翻的，就保持原狀。

    ('initpos','開始位置'),
    ('gravSys','重力系統'),
    ('dt','dt'),
    ('Nim','捻遊戲類'), # 有大寫字母在前的，為物類名稱，就加上「類」這個中文字於其後
    
    ('tree','樹'),
    ('ta','ta'),
    ('sun','日'),
    ('player','玩家'),
    ('model','模型'),
    
    ('colors','顏色們'), # 複數名詞都加上「們」
    
    ('angledist','角度距離'),
    
    
    ('view','視圖'),
    ('spitze','尺寸大小'), # 這個字本身是德文，大小、尺寸之意
    ('planets','行星們'),
    ('ne','ne'),
    ('lst','列表'),
    
    
    ('symRandom','隨機符號'),
    ('second_hand','秒針'),
    ('oldh','舊頭向'),
    ('notify_move','通知移動'),
    ('msg2','訊息2'),
    ('minute_hand','分針'),
    
    ('inflatedart','膨脹飛鏢'),
    ('hour_hand','時針'),
    ('hilbert','hilbert'),
    ('hand','指針'), # 把 hand 翻譯成 指針 當然是看過 原程式的後知後覺。
    ('gs','gs'),
    ('fun','函數'), # fun 譯為函數　也是　瞄過　原程式之後的結果。
    ('fractal','碎形'),
    
    ('draw','畫'),
    ('dist','距離'),
    ('depth','深度'),
    
    ('ang','角度'),
    ('SCREENHEIGHT','幕高常數'),# 全大寫字通常為常數，我們就加上中文「常數」
    ('MAXSTICKS','最大棒子數常數'),
    
    ('sizedist','邊距離'),
    ('running','正在跑'),
    
    ('move','移動'),
    ('maxspalte','最大分裂數'), # 這也是德文，spalte ~ split (in english)
    ('laenge','長度'), # 這是德文
    ('jump','跳'),
    ('inflatekite','膨脹風箏'),
    
    ('branchlist','分支列表'),
    ('angle','角度'),

    ('screen', '幕')
]

L2= [

    ('wochentag', '星期標籤'),

    ('to_', '去_'),
    #('th', ''),
    #('tb', ''),
    #('t1', ''),
    ('sizefactor', '尺寸因子'),
    ('seq', '序列'),
    ('rules', '規則們'),
    #('round', ''),
    ('randomrow', '隨機列'),
    ('rad', '弳度'),
    #('py', ''),
    #('px', ''),
    ('plot', '畫'),
    ('planetshape', '行星形狀'),
    ('planet', '行星'),

    ('newseq', '新序列'),
    #('minute', '分鐘'), #與 dateime 模組內建函數衝突
    ('make_hand_shape', '作指針形狀'),
    ('mainscreen', '主螢幕'),
    #('len', ''),
    ('init', '起始化'),
    ('hanoi', '河內'),
    ('from_', '從_'),
    ('farbe', '色彩'), # in德文'),
    ('drawing', '正在畫'),
    ('dancer', '舞者'),
    #('cs', ''),
    ('WUNIT', '水平單位常數'),
    ('Tower', '塔類'),
    ('Star', '星類'),
    ('SCREENWIDTH', '幕寬常數'),
    ('OVER', '遊戲結束狀態'),
    ('HUNIT', '垂直單位常數'),
    ('ColorTurtle', '顏色龜類'),
    ('BUSY', '繁忙狀態'),

    ('yin', '陰'),

    ('xored', '互斥或'),
    ('with_', '伴隨_'),
    ('winner', '贏家'),
    ('winkel', '角度'), # 德文
    ('widthfactor', '寬度因子'),
    ('visible', '可見的'),
    ('undobuffersize', '回復緩衝區大小'),
    ('turtlelist', '龜列表'),
    ('tripolyr', '右三邊形'),
    ('tripolyl', '左三邊形'),
    ('tick', '滴答'),
    ('test', '測試'),
    #('t3', ''),
    #('t2', ''),
    ('switchupdown', '切換提筆下筆'),
    ('stick', '棒子'),
    ('startpos', '開始位置'),
    #('sh', ''),
    ('setbgcolor', '設背景的顏色'),
    ('sekunde', '秒數'),
    #('s2', ''),
    #('s1', ''),
    ('root', '根'),
    #('res', ''),
    #('replace', ''), # 以下這幾個我懷疑是內建函數，即可能會衝
    #('red', ''),
    #('randint', ''),
    #('push', ''),
    #('pop', ''),
    #('pi', ''),
    ('pentr', '右五邊形'),
    ('pentl', '左五邊形'),
    ('parts', '部分'),

    #('nk', ''),
    #('nd', ''),
    ('moon', '月球'),
    #('list', ''),
    ('line', '直線'),
    #('k', ''),
    ('jumpto', '跳至'),
    #('green', ''),
    ('fractalgon', '碎形多邊形'),
    ('element', '元素'),
    ('earth', '地球'),
    ('done', '做完了'),
    ('demo', '展示'),
    #('datetime', ''),
    ('dancers', '舞者們'),
    ('cv2', '畫布2'),
    ('cv1', '畫布1'),
    ('color1', '顏色1'),
    ('centerpiece', '中央塊'),
    #('brs', ''),
    #('blue', ''),
    #('addcomponent', ''), # 這個暫不翻，它應屬於 turtle 的內建　方法之一，在 Shape 中，為漏網之魚
    ('acc', '加速度'),

    ('RUNNING', '正在跑狀態'),
    ('CREATED', '被創造狀態'),

    #('z1', ''),
    #('y2', ''),
    #('y1', ''),
    #('x2', ''),
    #('x1', ''),
    #('width', '寬'), # width 是龜內建函數
    ('wheel', '輪子'),
    #('u', ''),
    ('tripiece', '三之塊'),
    ('tlist', 't列表'),
    #('sz', ''),
    ('stunde', '時數'),
    ('stop', '停止'),
    ('step', '步進'),
    ('star', '星'),
    #('sqrt', ''),
    ('snake_start', '蛇開始'),
    ('snake_rules', '蛇規則'),
    ('snake_replacementRules', '蛇取代規則們'),
    ('shift', '平移'),
    ('shape', '形狀'),
    ('replacementRules', '取代規則們'),
    ('remainder', '餘數'),
    #('randrange', ''),
    ('randommove', '隨機移動'),
    ('randomize', '隨機化'),
    ('randomfd', '隨機前進'),
    #('rand', ''),
    #('r', ''),
    ('plist', 'p列表'),
    ('play', '玩'),
    ('phi', 'φ'), # greek phi
    ('pentpiece', '五之塊'),
    ('peacecolors', '和平顏色們'),
    ('pcolor', 'p顏色'),
    ('packet', '包裹'),
    #('pack', '打包'), # Canvas 內建函數
    ('notify_over', '通知結束'),
    ('name', '名'),
    ('msg1', '訊息1'),
    #('monat', ''),
    #('mn_eck', ''),
    #('max', ''),
    ('maketree', '製造樹'),
    ('makeshapes', '製造形狀們'),
    ('makemove', '令移動'),
    #('m2', ''),
    #('m1', ''),
    #('lev', ''),
    ('krishna_start', '克里希納開始'),
    ('krishna_rules', '克里希納規則們'),
    ('krishna_replacementRules', '克里希納取代規則們'),
    ('kite', '風箏'),
    #('j', ''),
    #('int', ''),
    ('homePos', '家的位置'),
    ('height', '高度'),
    ('hand_form', '指針形式'),
    ('game_over', '遊戲結束'),
    #('g', ''),
    ('edge', '邊緣'),
    ('doit3', '做它3'),
    ('doit2', '做它2'),
    ('doit1', '做它1'),
    ('distanz', '距離'), #in德文
    ('design', '設計'),
    ('datum', '年月日期'),
    ('dart', '飛鏢'),
    #('cos', ''),
    ('coosys', '座標系統'),
    ('coords', '座標們'),
    ('controller', '控制者'),
    ('computerzug', '電腦揀棒子'),
    ('commands', '指令們'),
    ('color', '顏色'),
    ('color2', '顏色2'),
    ('clockface', '鐘面'),
    ('changecolor', '改變顏色'),

    ('branchlists', '分支列表們'),
    #('bg', ''),

    #('abs', ''),
    #('Terminator', ''),
    ('Stick', '棒子類'),
    ('SCOLOR', 'S顏色常數'),
    ('NimView', '捻遊戲視圖類'),
    ('NimModel', '捻遊戲模型類'),
    ('NimController', '捻遊戲控制者類'),
    ('MINSTICKS', '最小棒子數常數'),
    ('HCOLOR', 'H顏色常數'),
    ('GravSys', '重力系統類'),
    ('G', 'G常數'),
    #('F', ''),
    ('Disc', '盤類'),
    ('Designer', '設計師類'),
    ('CurvesTurtle', '曲線龜類'),
    #('Canvas', '畫布類'),      ##### 衝突 for two_canvases.py
    ('COLOR', '顏色常數')
    #('B', ''),
    #('A', ''),

]

L3=[
    #('sleep','睡'),
    ('Vec', '向量類'),
    ('"second_hand"','"秒針"'),
    ('"runtime: %.2f sec."','"執行時間: %.2f 秒。"'),
    #('"red3"',''),
    #('"multitri"',''),
    ('"minute_hand"','"分針"'),
    ('"kite"','"風箏"'),
    ('"hour_hand"','"時針"'),
    #('"f"',''),
    ('"dart"','"飛鏢"'),
    #('"compound"',''),
    #('"circle"',''),
    #('"a"',''),
    ('"Your turn! Click leftmost stick to remove."',
        '"輪到你！點擊一根棒子來移走它及其右邊的棒子"'),
    ('"Sorry, the computer is the winner."',
        '"歹勢，電腦贏了！"'),
    ('''"Congrats. You're the winner!!!"''',
        '"恭喜，你贏了！"'),

    ('"Monday"',   '"拜一"'),
    ('"Tuesday"',  '"拜二"'),
    ('"Wednesday"','"拜三"'),
    ('"Thursday"', '"拜四"'),
    ('"Friday"',   '"拜五"'),
    ('"Saturday"', '"拜六"'),
    ('"Sunday"',   '"拜日"'),

    ('"Jan."','"一月"'),
    ('"Feb."','"二月"'),
    ('"Mar."','"三月"'),
    ('"Apr."','"四月"'),
    ('"May"','"五月"'),
    ('"June"','"六月"'),
    ('"July"','"七月"'),
    ('"Aug."','"八月"'),
    ('"Sep."','"九月"'),
    ('"Oct."','"十月"'),
    ('"Nov."','"十一月"'),
    ('"Dec."','"十二月"'),
    ('"replacementRules"','"取代規則們"'),
    ('"depth"','"深度"'),
    ('"step"','"步進"'),
    ('"angle"','"角度"'),
    ('"startpos"','"開始位置"')
]



def main():

    字典= getDic()

    for n,d in enumerate(字典):
        print(n,d,字典[d])

def 建立中英對照表():
	"""
	建立一個別名中英對照表並回傳(list型態)。
	其會根據字母排序。
	需要導入turtle_tc_alias。
	"""
	別名表單=[]
	#抓取全部別名表(總別名表，宣告在turtle_tc_alias)，為了將全部別名加入到別名表單
	for y in 總別名表:
		#抓取別名表內中英對照名稱
		for x in y:
			#將別名表加到X裡
			別名表單 += [x]
	#將X重新排列產生一個新的排序列表
	中英對照表= sorted(別名表單)
	return 中英對照表

def getDic():
    '''
    把 dic 寫在程式裡面，方便程式撰寫，
    卻 不利 抽換 或 改變 語言。
    未來 應連同 turtle_tc 中的 中英對照表 
    與程式分離，自己形成資料表。
    '''
    中英對照表= 建立中英對照表()
    # 原版「中英對照表」為「一對多」，在這裡先取「一對一」
    L= [ (x[0], x[1]) for x in 中英對照表] 

    
    #
    # 這個 「增加的中英對照表」 是一種「後處理」，
    # 把前面翻不出來的英語變數算頻率，儲存在外部檔案，
    # 在此為 ryTranlate001.py_out2
    # 觀察它，高頻者優先人工翻譯，再貼回來此處形成表格
    # 無法百分百全自動，但可以逐步優化。
    # 要小心 命名空間 的衝突問題，
    # 還有 關鍵字 也要小心。 
    #
    # 目前 把 頻率 >= 2者 都列出來，
    #

    
    L += 增加的中英對照表 + L2 + L3
    
    # 加入　L2 後，初步　有　clock, paint, peace, two_canvases, yinyang 不能跑。
    
    D= dict(L)
    
    return D


def getDicE():
    中英對照表= 建立中英對照表()
    中英對照表 += 增加的中英對照表 + L2 + L3
    英中字典={}
    for i in 中英對照表:
        英文名=i[0]
        for j in i[1:]:
            英中字典[j]=英文名
            
    
    return 英中字典
 
 
if __name__ == '__main__':
    main()





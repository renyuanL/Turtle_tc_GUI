#!/usr/bin/env python3
import tkinter as TK
import types
import math
import time
import inspect
import sys

from os.path import isfile, split, join
from copy import deepcopy
from tkinter import simpledialog

import random
from turtle import *
from turtle import _CFG, _Screen, _Root, TK, _TurtleImage, Tbuffer, TurtleGraphicsError
from turtle import TurtleScreenBase, TurtleScreen, TNavigator, TPen, RawTurtle, Canvas #,Terminator, Turtle, Screen,Vec2D,ScrolledCanvas,Shape

def _取筆():
    """宣告一個匿名龜類，當其並不存在時。"""

    if 龜類._pen is None:
        龜類._pen= 龜類()

    return 龜類._pen
#設置 _getscreen的中文別名
def _取幕():
    """宣告一個匿名龜幕類，當其並不存在時。"""
    if 龜類._screen is None:
        龜類._screen = _幕類()  ###### 會不會就是這行搞鬼？？ 有無底線之分！

    return 龜類._screen
class Vec2D(tuple):
    """A 2 dimensional vector class, used as a helper class
    for implementing turtle graphics.
    May be useful for turtle graphics programs also.
    Derived from tuple, so a vector is a tuple!

    Provides (for a, b vectors, k number):
       a+b vector addition
       a-b vector subtraction
       a*b inner product
       k*a and a*k multiplication with scalar
       |a| absolute value of a
       a.rotate(angle) rotation
    """
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))
    def __add__(self, other):
        return Vec2D(self[0]+other[0], self[1]+other[1])
    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0]*other[0]+self[1]*other[1]
        return Vec2D(self[0]*other, self[1]*other)
    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self[0]*other, self[1]*other)
    def __sub__(self, other):
        return Vec2D(self[0]-other[0], self[1]-other[1])
    def __neg__(self):
        return Vec2D(-self[0], -self[1])
    def __abs__(self):
        return (self[0]**2 + self[1]**2)**0.5
    def rotate(self, angle):
        """rotate self counterclockwise by angle
        """
        perp = Vec2D(-self[1], self[0])
        angle = angle * math.pi / 180.0
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0]*c+perp[0]*s, self[1]*c+perp[1]*s)
    def __getnewargs__(self):
        return (self[0], self[1])
    def __repr__(self):
        return "(%.2f,%.2f)" % self
    旋轉= rotate
向量類= Vec2D
二維向量類= Vec2D
class Shape(object):
    """Data structure modeling shapes.

    attribute _type is one of "polygon", "image", "compound"
    attribute _data is - depending on _type a poygon-tuple,
    an image or a list constructed using the addcomponent method.
    """
    def __init__(self, type_, data=None):
        self._type = type_
        if type_ == "polygon":
            if isinstance(data, list):
                data = tuple(data)
        elif type_ == "image":
            if isinstance(data, str):
                if data.lower().endswith(".gif") and isfile(data):
                    data = TurtleScreen._image(data)
                # else data assumed to be Photoimage
        elif type_ == "compound":
            data = []
        else:
            raise TurtleGraphicsError("There is no shape type %s" % type_)
        self._data = data

    def addcomponent(self, poly, fill, outline=None):
        """Add component to a shape of type compound.

        Arguments: poly is a polygon, i. e. a tuple of number pairs.
        fill is the fillcolor of the component,
        outline is the outline color of the component.

        call (for a Shapeobject namend s):
        --   s.addcomponent(((0,0), (10,10), (-10,10)), "red", "blue")

        Example:
        >>> poly = ((0,0),(10,-5),(0,10),(-10,-5))
        >>> s = Shape("compound")
        >>> s.addcomponent(poly, "red", "blue")
        >>> # .. add more components and then use register_shape()
        """
        if self._type != "compound":
            raise TurtleGraphicsError("Cannot add component to %s Shape"
                                                                % self._type)
        if outline is None:
            outline = fill
        self._data.append([poly, fill, outline])
    加成員= addcomponent
形狀類= Shape
class TurtleScreenBase(object):
    """Provide the basic graphics functionality.
       Interface between Tkinter and turtle.py.

       To port turtle.py to some different graphics toolkit
       a corresponding TurtleScreenBase class has to be implemented.
    """

    @staticmethod
    def _blankimage():
        """return a blank image object
        """
        img = TK.PhotoImage(width=1, height=1)
        img.blank()
        return img

    @staticmethod
    def _image(filename):
        """return an image object containing the
        imagedata from a gif-file named filename.
        """
        return TK.PhotoImage(file=filename)

    def __init__(self, cv):
        self.cv = cv
        if isinstance(cv, ScrolledCanvas):
            w = self.cv.canvwidth
            h = self.cv.canvheight
        else:  # expected: ordinary TK.Canvas
            w = int(self.cv.cget("width"))
            h = int(self.cv.cget("height"))
            self.cv.config(scrollregion = (-w//2, -h//2, w//2, h//2 ))
        self.canvwidth = w
        self.canvheight = h
        self.xscale = self.yscale = 1.0

    def _createpoly(self):
        """Create an invisible polygon item on canvas self.cv)
        """
        return self.cv.create_polygon((0, 0, 0, 0, 0, 0), fill="", outline="")

    def _drawpoly(self, polyitem, coordlist, fill=None,
                  outline=None, width=None, top=False):
        """Configure polygonitem polyitem according to provided
        arguments:
        coordlist is sequence of coordinates
        fill is filling color
        outline is outline color
        top is a boolean value, which specifies if polyitem
        will be put on top of the canvas' displaylist so it
        will not be covered by other items.
        """
        cl = []
        for x, y in coordlist:
            cl.append(x * self.xscale)
            cl.append(-y * self.yscale)
        self.cv.coords(polyitem, *cl)
        if fill is not None:
            self.cv.itemconfigure(polyitem, fill=fill)
        if outline is not None:
            self.cv.itemconfigure(polyitem, outline=outline)
        if width is not None:
            self.cv.itemconfigure(polyitem, width=width)
        if top:
            self.cv.tag_raise(polyitem)

    def _createline(self):
        """Create an invisible line item on canvas self.cv)
        """
        return self.cv.create_line(0, 0, 0, 0, fill="", width=2,
                                   capstyle = TK.ROUND)

    def _drawline(self, lineitem, coordlist=None,
                  fill=None, width=None, top=False):
        """Configure lineitem according to provided arguments:
        coordlist is sequence of coordinates
        fill is drawing color
        width is width of drawn line.
        top is a boolean value, which specifies if polyitem
        will be put on top of the canvas' displaylist so it
        will not be covered by other items.
        """
        if coordlist is not None:
            cl = []
            for x, y in coordlist:
                cl.append(x * self.xscale)
                cl.append(-y * self.yscale)
            self.cv.coords(lineitem, *cl)
        if fill is not None:
            self.cv.itemconfigure(lineitem, fill=fill)
        if width is not None:
            self.cv.itemconfigure(lineitem, width=width)
        if top:
            self.cv.tag_raise(lineitem)

    def _delete(self, item):
        """Delete graphics item from canvas.
        If item is"all" delete all graphics items.
        """
        self.cv.delete(item)

    def _update(self):
        """Redraw graphics items on canvas
        """
        self.cv.update()

    def _delay(self, delay):
        """Delay subsequent canvas actions for delay ms."""
        self.cv.after(delay)

    def _iscolorstring(self, color):
        """Check if the string color is a legal Tkinter color string.
        """
        try:
            rgb = self.cv.winfo_rgb(color)
            ok = True
        except TK.TclError:
            ok = False
        return ok

    def _bgcolor(self, color=None):
        """Set canvas' backgroundcolor if color is not None,
        else return backgroundcolor."""
        if color is not None:
            self.cv.config(bg = color)
            self._update()
        else:
            return self.cv.cget("bg")

    def _write(self, pos, txt, align, font, pencolor):
        """Write txt at pos in canvas with specified font
        and color.
        Return text item and x-coord of right bottom corner
        of text's bounding box."""
        x, y = pos
        x = x * self.xscale
        y = y * self.yscale
        anchor = {"left":"sw", "center":"s", "right":"se" }
        item = self.cv.create_text(x-1, -y, text = txt, anchor = anchor[align],
                                        fill = pencolor, font = font)
        x0, y0, x1, y1 = self.cv.bbox(item)
        self.cv.update()
        return item, x1-1

##    def _dot(self, pos, size, color):
##        """may be implemented for some other graphics toolkit"""

    def _onclick(self, item, fun, num=1, add=None):
        """Bind fun to mouse-click event on turtle.
        fun must be a function with two arguments, the coordinates
        of the clicked point on the canvas.
        num, the number of the mouse-button defaults to 1
        """
        if fun is None:
            self.cv.tag_unbind(item, "<Button-%s>" % num)
        else:
            def eventfun(event):
                x, y = (self.cv.canvasx(event.x)/self.xscale,
                        -self.cv.canvasy(event.y)/self.yscale)
                fun(x, y)
            self.cv.tag_bind(item, "<Button-%s>" % num, eventfun, add)

    def _onrelease(self, item, fun, num=1, add=None):
        """Bind fun to mouse-button-release event on turtle.
        fun must be a function with two arguments, the coordinates
        of the point on the canvas where mouse button is released.
        num, the number of the mouse-button defaults to 1

        If a turtle is clicked, first _onclick-event will be performed,
        then _onscreensclick-event.
        """
        if fun is None:
            self.cv.tag_unbind(item, "<Button%s-ButtonRelease>" % num)
        else:
            def eventfun(event):
                x, y = (self.cv.canvasx(event.x)/self.xscale,
                        -self.cv.canvasy(event.y)/self.yscale)
                fun(x, y)
            self.cv.tag_bind(item, "<Button%s-ButtonRelease>" % num,
                             eventfun, add)

    def _ondrag(self, item, fun, num=1, add=None):
        """Bind fun to mouse-move-event (with pressed mouse button) on turtle.
        fun must be a function with two arguments, the coordinates of the
        actual mouse position on the canvas.
        num, the number of the mouse-button defaults to 1

        Every sequence of mouse-move-events on a turtle is preceded by a
        mouse-click event on that turtle.
        """
        if fun is None:
            self.cv.tag_unbind(item, "<Button%s-Motion>" % num)
        else:
            def eventfun(event):
                try:
                    x, y = (self.cv.canvasx(event.x)/self.xscale,
                           -self.cv.canvasy(event.y)/self.yscale)
                    fun(x, y)
                except:
                    pass
            self.cv.tag_bind(item, "<Button%s-Motion>" % num, eventfun, add)

    def _onscreenclick(self, fun, num=1, add=None):
        """Bind fun to mouse-click event on canvas.
        fun must be a function with two arguments, the coordinates
        of the clicked point on the canvas.
        num, the number of the mouse-button defaults to 1

        If a turtle is clicked, first _onclick-event will be performed,
        then _onscreensclick-event.
        """
        if fun is None:
            self.cv.unbind("<Button-%s>" % num)
        else:
            def eventfun(event):
                x, y = (self.cv.canvasx(event.x)/self.xscale,
                        -self.cv.canvasy(event.y)/self.yscale)
                fun(x, y)
            self.cv.bind("<Button-%s>" % num, eventfun, add)

    def _onkeyrelease(self, fun, key):
        """Bind fun to key-release event of key.
        Canvas must have focus. See method listen
        """
        if fun is None:
            self.cv.unbind("<KeyRelease-%s>" % key, None)
        else:
            def eventfun(event):
                fun()
            self.cv.bind("<KeyRelease-%s>" % key, eventfun)

    def _onkeypress(self, fun, key=None):
        """If key is given, bind fun to key-press event of key.
        Otherwise bind fun to any key-press.
        Canvas must have focus. See method listen.
        """
        if fun is None:
            if key is None:
                self.cv.unbind("<KeyPress>", None)
            else:
                self.cv.unbind("<KeyPress-%s>" % key, None)
        else:
            def eventfun(event):
                fun()
            if key is None:
                self.cv.bind("<KeyPress>", eventfun)
            else:
                self.cv.bind("<KeyPress-%s>" % key, eventfun)

    def _listen(self):
        """Set focus on canvas (in order to collect key-events)
        """
        self.cv.focus_force()

    def _ontimer(self, fun, t):
        """Install a timer, which calls fun after t milliseconds.
        """
        if t == 0:
            self.cv.after_idle(fun)
        else:
            self.cv.after(t, fun)

    def _createimage(self, image):
        """Create and return image item on canvas.
        """
        return self.cv.create_image(0, 0, image=image)

    def _drawimage(self, item, pos, image):
        """Configure image item as to draw image object
        at position (x,y) on canvas)
        """
        x, y = pos
        self.cv.coords(item, (x * self.xscale, -y * self.yscale))
        self.cv.itemconfig(item, image=image)

    def _setbgpic(self, item, image):
        """Configure image item as to draw image object
        at center of canvas. Set item to the first item
        in the displaylist, so it will be drawn below
        any other item ."""
        self.cv.itemconfig(item, image=image)
        self.cv.tag_lower(item)

    def _type(self, item):
        """Return 'line' or 'polygon' or 'image' depending on
        type of item.
        """
        return self.cv.type(item)

    def _pointlist(self, item):
        """returns list of coordinate-pairs of points of item
        Example (for insiders):
        >>> from turtle import *
        >>> getscreen()._pointlist(getturtle().turtle._item)
        [(0.0, 9.9999999999999982), (0.0, -9.9999999999999982),
        (9.9999999999999982, 0.0)]
        >>> """
        cl = self.cv.coords(item)
        pl = [(cl[i], -cl[i+1]) for i in range(0, len(cl), 2)]
        return  pl

    def _setscrollregion(self, srx1, sry1, srx2, sry2):
        self.cv.config(scrollregion=(srx1, sry1, srx2, sry2))

    def _rescale(self, xscalefactor, yscalefactor):
        items = self.cv.find_all()
        for item in items:
            coordinates = list(self.cv.coords(item))
            newcoordlist = []
            while coordinates:
                x, y = coordinates[:2]
                newcoordlist.append(x * xscalefactor)
                newcoordlist.append(y * yscalefactor)
                coordinates = coordinates[2:]
            self.cv.coords(item, *newcoordlist)

    def _resize(self, canvwidth=None, canvheight=None, bg=None):
        """Resize the canvas the turtles are drawing on. Does
        not alter the drawing window.
        """
        # needs amendment
        if not isinstance(self.cv, ScrolledCanvas):
            return self.canvwidth, self.canvheight
        if canvwidth is canvheight is bg is None:
            return self.cv.canvwidth, self.cv.canvheight
        if canvwidth is not None:
            self.canvwidth = canvwidth
        if canvheight is not None:
            self.canvheight = canvheight
        self.cv.reset(canvwidth, canvheight, bg)

    def _window_size(self):
        """ Return the width and height of the turtle window.
        """
        width = self.cv.winfo_width()
        if width <= 1:  # the window isn't managed by a geometry manager
            width = self.cv['width']
        height = self.cv.winfo_height()
        if height <= 1: # the window isn't managed by a geometry manager
            height = self.cv['height']
        return width, height

    def mainloop(self):
        """『0077  中文說明』
        主迴圈，進入主迴圈啟動事件循環 - 呼叫 Tkinter的主迴圈函數。

        沒有參數。

        必須是龜畫圖程式的最後一條語句。
        程式不得使用運行在IDLE 內部 -n 模式
        (無子程式) - 亦即在龜畫圖程式互動模式下。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.主迴圈()



        Starts event loop - calling Tkinter's mainloop function.

        No argument.

        Must be last statement in a turtle graphics program.
        Must NOT be used if a script is run from within IDLE in -n mode
        (No subprocess) - for interactive use of turtle graphics.

        Example (for a TurtleScreen instance named screen):
        >>> screen.mainloop()

        """
        TK.mainloop()

    def textinput(self, title, prompt):
        """『0010  中文說明』
        輸入文字，彈出一個對話窗，讓使用者輸入一個字串。

        參數：
        title：對話框窗口的標題。
        prompt：提示語，主要是描述需要的輸入文本信息。
        當有傳入參數，則回傳輸入的字串。
        如果取消該對話框，回傳 無(None)。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.輸入文字("NIM","第一個球員的名字:")



        Pop up a dialog window for input of a string.

        Arguments: title is the title of the dialog window,
        prompt is a text mostly describing what information to input.

        Return the string input
        If the dialog is canceled, return None.

        Example (for a TurtleScreen instance named screen):
        >>> screen.textinput("NIM", "Name of first player:")

        """
        return simpledialog.askstring(title, prompt)

    def numinput(self, title, prompt, default=None, minval=None, maxval=None):
        """『0032  中文說明』
        輸入數字，彈出一個對話窗口，可以輸入一個數字。

        參數：
        title: 對話框窗口的標題。
        prompt: 提示語，主要是描述需要的輸入文本信息。
        default: 預設值。
        minval: 最小值。
        maxval: 最大值。

        如果最小值跟最大值參數有設定，數字輸入必須在範圍 minval .. maxval。
        如果取消該對話框，則回傳 無(None)。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.輸入數字("撲克","你的賭注:",1000,minval=10, maxval=10000)



        Pop up a dialog window for input of a number.

        Arguments: title is the title of the dialog window,
        prompt is a text mostly describing what numerical information to input.
        default: default value
        minval: minimum value for imput
        maxval: maximum value for input

        The number input must be in the range minval .. maxval if these are
        given. If not, a hint is issued and the dialog remains open for
        correction. Return the number input.
        If the dialog is canceled,  return None.

        Example (for a TurtleScreen instance named screen):
        >>> screen.numinput("Poker", "Your stakes:", 1000, minval=10, maxval=10000)

        """
        return simpledialog.askfloat(title, prompt, initialvalue=default,
                                     minvalue=minval, maxvalue=maxval)
    主迴圈= mainloop
    進入主迴圈= mainloop
    做完了= mainloop
    點擊X結束= mainloop
    等待閉幕= mainloop
    閉幕= mainloop
    輸入數字= numinput
    輸入文字= textinput
龜幕基類= TurtleScreenBase
烏龜螢幕地基類= TurtleScreenBase
class TurtleScreen(TurtleScreenBase):
    """Provides screen oriented methods like setbg etc.

    Only relies upon the methods of TurtleScreenBase and NOT
    upon components of the underlying graphics toolkit -
    which is Tkinter in this case.
    """
    _RUNNING = True

    def __init__(self, cv, mode=_CFG["mode"],
                 colormode=_CFG["colormode"], delay=_CFG["delay"]):
        self._shapes = {
                   "arrow" : Shape("polygon", ((-10,0), (10,0), (0,10))),
                  "turtle" : Shape("polygon", ((0,16), (-2,14), (-1,10), (-4,7),
                              (-7,9), (-9,8), (-6,5), (-7,1), (-5,-3), (-8,-6),
                              (-6,-8), (-4,-5), (0,-7), (4,-5), (6,-8), (8,-6),
                              (5,-3), (7,1), (6,5), (9,8), (7,9), (4,7), (1,10),
                              (2,14))),
                  "circle" : Shape("polygon", ((10,0), (9.51,3.09), (8.09,5.88),
                              (5.88,8.09), (3.09,9.51), (0,10), (-3.09,9.51),
                              (-5.88,8.09), (-8.09,5.88), (-9.51,3.09), (-10,0),
                              (-9.51,-3.09), (-8.09,-5.88), (-5.88,-8.09),
                              (-3.09,-9.51), (-0.00,-10.00), (3.09,-9.51),
                              (5.88,-8.09), (8.09,-5.88), (9.51,-3.09))),
                  "square" : Shape("polygon", ((10,-10), (10,10), (-10,10),
                              (-10,-10))),
                "triangle" : Shape("polygon", ((10,-5.77), (0,11.55),
                              (-10,-5.77))),
                  "classic": Shape("polygon", ((0,0),(-5,-9),(0,-7),(5,-9))),
                   "blank" : Shape("image", self._blankimage())
                  }

        self._bgpics = {"nopic" : ""}

        TurtleScreenBase.__init__(self, cv)
        self._mode = mode
        self._delayvalue = delay
        self._colormode = _CFG["colormode"]
        self._keys = []
        self.clear()
        if sys.platform == 'darwin':
            # Force Turtle window to the front on OS X. This is needed because
            # the Turtle window will show behind the Terminal window when you
            # start the demo from the command line.
            rootwindow = cv.winfo_toplevel()
            rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
            rootwindow.call('wm', 'attributes', '.', '-topmost', '0')

    def clear(self):
        """『0041  中文說明』
        清除幕，從 龜幕類 刪除所有圖和 龜類。

        沒有參數。

        重設一個空的 龜幕類 到其初始狀態，
        白色背景、沒有背景圖片、沒有事件綁定跟追蹤。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.清除幕()

        注意：這個方法不作函數使用。


        Delete all drawings and all turtles from the TurtleScreen.

        No argument.

        Reset empty TurtleScreen to its initial state: white background,
        no backgroundimage, no eventbindings and tracing on.

        Example (for a TurtleScreen instance named screen):
        >>> screen.clear()

        Note: this method is not available as function.
        """
        self._delayvalue = _CFG["delay"]
        self._colormode = _CFG["colormode"]
        self._delete("all")
        self._bgpic = self._createimage("")
        self._bgpicname = "nopic"
        self._tracing = 1
        self._updatecounter = 0
        self._turtles = []
        self.bgcolor("white")
        for btn in 1, 2, 3:
            self.onclick(None, btn)
        self.onkeypress(None)
        for key in self._keys[:]:
            self.onkey(None, key)
            self.onkeypress(None, key)
        Turtle._pen = None

    def mode(self, mode=None):
        """『0038  中文說明』
        模式，設置龜模式('standard', 'logo' or 'world')，並執行 重設()。

        可選參數:
        mode - 'standard' (角度從東開始逆時針)、'logo' (角度從北開始順時針)或 'world' (世界)，三個中之一。

        角度從東開始逆時針('standard')模式，
        龜指標 角度從東開始逆時針算，與turtle.py相容。
        角度從北開始順時針('logo')模式，
        龜指標 角度從東開始順時針算，與原始的logo龜圖相容。
        世界(' world ')模式，
        使用用戶自定義"worldcoordinates"。
        *注意*:如果x / y的單位比不等於1，在世界模式下角度會出現扭曲。
        無傳入參數，即可用來查詢目前設定。

             模式            初始龜指標頭向           角度方向
         ------------ | ------------------------- | ------------------
          'standard'    向右(東)               逆時針
            'logo'      向上(北)               順時針

        範例：
        >>>模式(角度從北開始順時針) # 重設龜指標向北
        >>>模式()
        'logo'


        Set turtle-mode ('standard', 'logo' or 'world') and perform reset.

        Optional argument:
        mode -- on of the strings 'standard', 'logo' or 'world'

        Mode 'standard' is compatible with turtle.py.
        Mode 'logo' is compatible with most Logo-Turtle-Graphics.
        Mode 'world' uses userdefined 'worldcoordinates'. *Attention*: in
        this mode angles appear distorted if x/y unit-ratio doesn't equal 1.
        If mode is not given, return the current mode.

             Mode      Initial turtle heading     positive angles
         ------------|-------------------------|-------------------
          'standard'    to the right (east)       counterclockwise
            'logo'        upward    (north)         clockwise

        Examples:
        >>> mode('logo')   # resets turtle heading to north
        >>> mode()
        'logo'
        """
        if mode is None:
            return self._mode
        mode = mode.lower()
        if mode not in ["standard", "logo", "world"]:
            raise TurtleGraphicsError("No turtle-graphics-mode %s" % mode)
        self._mode = mode
        if mode in ["standard", "logo"]:
            self._setscrollregion(-self.canvwidth//2, -self.canvheight//2,
                                       self.canvwidth//2, self.canvheight//2)
            self.xscale = self.yscale = 1.0
        self.reset()

    def setworldcoordinates(self, llx, lly, urx, ury):
        """『0015  中文說明』
        設座標系統，設置一個使用者定義的座標系。

        參數：
        llx -- 畫布的左下角x座標
        lly -- 畫布的左下角y座標
        urx -- 畫布的右上角x座標
        ury -- 畫布的右上角y座標

        設置使用者定義座標系統，並在必要時切換到'world'(世界)模式。
        並執行一個螢幕重置。
        如果'world'(世界)模式已經啟動，則所有圖都會根據新的座標系重畫。

        但要注意：在使用者定義的座標系中，角度可能會出現扭曲。(參考 模式())

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.設座標系統(-10, -0.5, 50, 1.5)
        >>> for _ in 範圍(36):
        ...     左轉(10)
        ...     前進(0.5)


        Set up a user defined coordinate-system.

        Arguments:
        llx -- a number, x-coordinate of lower left corner of canvas
        lly -- a number, y-coordinate of lower left corner of canvas
        urx -- a number, x-coordinate of upper right corner of canvas
        ury -- a number, y-coordinate of upper right corner of canvas

        Set up user coodinat-system and switch to mode 'world' if necessary.
        This performs a screen.reset. If mode 'world' is already active,
        all drawings are redrawn according to the new coordinates.

        But ATTENTION: in user-defined coordinatesystems angles may appear
        distorted. (see Screen.mode())

        Example (for a TurtleScreen instance named screen):
        >>> screen.setworldcoordinates(-10,-0.5,50,1.5)
        >>> for _ in range(36):
        ...     left(10)
        ...     forward(0.5)
        """
        if self.mode() != "world":
            self.mode("world")
        xspan = float(urx - llx)
        yspan = float(ury - lly)
        wx, wy = self._window_size()
        self.screensize(wx-20, wy-20)
        oldxscale, oldyscale = self.xscale, self.yscale
        self.xscale = self.canvwidth / xspan
        self.yscale = self.canvheight / yspan
        srx1 = llx * self.xscale
        sry1 = -ury * self.yscale
        srx2 = self.canvwidth + srx1
        sry2 = self.canvheight + sry1
        self._setscrollregion(srx1, sry1, srx2, sry2)
        self._rescale(self.xscale/oldxscale, self.yscale/oldyscale)
        self.update()

    def register_shape(self, name, shape=None):
        """『0022  中文說明』
        登記形狀，添加一個 龜指標 形狀到 龜幕類 的 形狀列表。

        參數:
        (1)name是一個GIF文件的檔案名而形狀是None。
            安裝相應的圖像形狀。
            ！轉彎時,圖像形狀不會旋轉。
            ！所以也不會顯示龜指標方向。
        (2)name為一個任意的字串，
            形狀是一個元組(tuple)的座標(一對數字)。
            設定相應的多邊形。
        (3)name為一個任意的字串，
            形狀是(複合的) 形狀 物件。
            設定相應的複合形狀。
        要使用登記的形狀，必須呼叫 形狀(name) 指令。

        呼叫:登記形狀("龜.gif")
        - 或者:登記形狀("三角形",((0,0),(10,10),(-10,10)))

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.登記形狀("三角形",((5,-3),(0,5),(-5,-3)))



        Adds a turtle shape to TurtleScreen's shapelist.

        Arguments:
        (1) name is the name of a gif-file and shape is None.
            Installs the corresponding image shape.
            !! Image-shapes DO NOT rotate when turning the turtle,
            !! so they do not display the heading of the turtle!
        (2) name is an arbitrary string and shape is a tuple
            of pairs of coordinates. Installs the corresponding
            polygon shape
        (3) name is an arbitrary string and shape is a
            (compound) Shape object. Installs the corresponding
            compound shape.
        To use a shape, you have to issue the command shape(shapename).

        call: register_shape("turtle.gif")
        --or: register_shape("tri", ((0,0), (10,10), (-10,10)))

        Example (for a TurtleScreen instance named screen):
        >>> screen.register_shape("triangle", ((5,-3),(0,5),(-5,-3)))

        """
        if shape is None:
            # image
            if name.lower().endswith(".gif"):
                shape = Shape("image", self._image(name))
            else:
                raise TurtleGraphicsError("Bad arguments for register_shape.\n"
                                          + "Use  help(register_shape)" )
        elif isinstance(shape, tuple):
            shape = Shape("polygon", shape)
        ## else shape assumed to be Shape-instance
        self._shapes[name] = shape

    def _colorstr(self, color):
        """Return color string corresponding to args.

        Argument may be a string or a tuple of three
        numbers corresponding to actual colormode,
        i.e. in the range 0<=n<=colormode.

        If the argument doesn't represent a color,
        an error is raised.
        """
        if len(color) == 1:
            color = color[0]
        if isinstance(color, str):
            if self._iscolorstring(color) or color == "":
                return color
            else:
                raise TurtleGraphicsError("bad color string: %s" % str(color))
        try:
            r, g, b = color
        except:
            raise TurtleGraphicsError("bad color arguments: %s" % str(color))
        if self._colormode == 1.0:
            r, g, b = [round(255.0*x) for x in (r, g, b)]
        if not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255)):
            raise TurtleGraphicsError("bad color sequence: %s" % str(color))
        return "#%02x%02x%02x" % (r, g, b)

    def _color(self, cstr):
        if not cstr.startswith("#"):
            return cstr
        if len(cstr) == 7:
            cl = [int(cstr[i:i+2], 16) for i in (1, 3, 5)]
        elif len(cstr) == 4:
            cl = [16*int(cstr[h], 16) for h in cstr[1:]]
        else:
            raise TurtleGraphicsError("bad colorstring: %s" % cstr)
        return tuple([c * self._colormode/255 for c in cl])

    def colormode(self, cmode=None):
        """『0004  中文說明』
        色模式，回傳色模式設定或將其設置為 1.0 或 255。

        可選參數:
        cmode  - 數字 1.0 或 255 中之一

         r, g, b 值必須在範圍0 .. cmode之間。

        範例：

        >>> 色模式()
        1.0
        >>> 色模式(255)
        >>> 筆色(240,160,80)


        Return the colormode or set it to 1.0 or 255.

        Optional argument:
        cmode -- one of the values 1.0 or 255

        r, g, b values of colortriples have to be in range 0..cmode.

        Example (for a TurtleScreen instance named screen):
        >>> screen.colormode()
        1.0
        >>> screen.colormode(255)
        >>> pencolor(240,160,80)
        """
        if cmode is None:
            return self._colormode
        if cmode == 1.0:
            self._colormode = float(cmode)
        elif cmode == 255:
            self._colormode = int(cmode)

    def reset(self):
        """『0080  中文說明』
        重設幕，重設螢幕上的所有 龜類 為其初始狀態。

        沒有參數。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.重設幕()


        Reset all Turtles on the Screen to their initial state.

        No argument.

        Example (for a TurtleScreen instance named screen):
        >>> screen.reset()
        """
        for turtle in self._turtles:
            turtle._setmode(self._mode)
            turtle.reset()

    def turtles(self):
        """『0039  中文說明』
        龜群，回傳螢幕上龜列表。

        範例(物件名為「螢幕」的實例)：


        >>> 螢幕.龜群()
        [<turtle.Turtle object at 0x00E11FB0>]


        Return the list of turtles on the screen.

        Example (for a TurtleScreen instance named screen):
        >>> screen.turtles()
        [<turtle.Turtle object at 0x00E11FB0>]
        """
        return self._turtles

    def bgcolor(self, *args):
        """『0092  中文說明』
        背景色，設置或回傳 龜幕類 的背景顏色。

        參數(可選)：
        一個顏色字串，如 紅色 或 黃色
        或在範圍0 .. 色模式的一個三元組數字

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.背景色(橙色)
        >>> 螢幕.背景色()
        "orange"
        >>> 螢幕.背景色(0.5,0,0.5)
        >>> 螢幕.背景色()
        '#800080'


        Set or return backgroundcolor of the TurtleScreen.

        Arguments (if given): a color string or three numbers
        in the range 0..colormode or a 3-tuple of such numbers.

        Example (for a TurtleScreen instance named screen):
        >>> screen.bgcolor("orange")
        >>> screen.bgcolor()
        'orange'
        >>> screen.bgcolor(0.5,0,0.5)
        >>> screen.bgcolor()
        '#800080'
        """
        if args:
            color = self._colorstr(args)
        else:
            color = None
        color = self._bgcolor(color)
        if color is not None:
            color = self._color(color)
        return color

    def tracer(self, n=None, delay=None):
        """『0089  中文說明』
        追蹤，開/關 龜動畫，並設置更新畫面的延遲時間。

        可選參數:
        n - 非負整數
        dekay - 非負整數

        如果 n 有被指定的，只執行每n次定期螢幕更新。
        (可用於加速複雜圖形的繪製。)
        第二個參數設置延遲值(見 RawTurtle.delay() )

        範例(物件名為「螢幕」的實例)：


        >>>螢幕.追蹤(8,25)
        >>>距離= 2
        >>>for i in 範圍(200):
        ...     前進(距離)
        ...     右轉(90)
        ...     距離 += 2


        Turns turtle animation on/off and set delay for update drawings.

        Optional arguments:
        n -- nonnegative  integer
        delay -- nonnegative  integer

        If n is given, only each n-th regular screen update is really performed.
        (Can be used to accelerate the drawing of complex graphics.)
        Second arguments sets delay value (see RawTurtle.delay())

        Example (for a TurtleScreen instance named screen):
        >>> screen.tracer(8, 25)
        >>> dist = 2
        >>> for i in range(200):
        ...     fd(dist)
        ...     rt(90)
        ...     dist += 2
        """
        if n is None:
            return self._tracing
        self._tracing = int(n)
        self._updatecounter = 0
        if delay is not None:
            self._delayvalue = int(delay)
        if self._tracing:
            self.update()

    def delay(self, delay=None):
        """『0006  中文說明』
        延遲，回傳或設置畫面更新的延遲時間，以毫秒為單位。

        可選參數:
        delay - 正整數

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.延遲(15)
        >>> 螢幕.延遲()
        15


         Return or set the drawing delay in milliseconds.

        Optional argument:
        delay -- positive integer

        Example (for a TurtleScreen instance named screen):
        >>> screen.delay(15)
        >>> screen.delay()
        15
        """
        if delay is None:
            return self._delayvalue
        self._delayvalue = int(delay)

    def _incrementudc(self):
        """Increment update counter."""
        if not TurtleScreen._RUNNING:
            TurtleScreen._RUNNNING = True
            raise Terminator
        if self._tracing > 0:
            self._updatecounter += 1
            self._updatecounter %= self._tracing

    def update(self):
        """『0078  中文說明』
        更新，執行 龜幕類 更新。


        Perform a TurtleScreen update.
        """
        tracing = self._tracing
        self._tracing = True
        for t in self.turtles():
            t._update_data()
            t._drawturtle()
        self._tracing = tracing
        self._update()

    def window_width(self):
        """『0001  中文說明』
        取幕寬，回傳龜視窗的寬度。

        範例(物件名為「螢幕」的實例)：


        >>> 螢幕.取幕寬()
        640


         Return the width of the turtle window.

        Example (for a TurtleScreen instance named screen):
        >>> screen.window_width()
        640
        """
        return self._window_size()[0]

    def window_height(self):
        """『0026  中文說明』
        取幕高，回傳龜視窗的高度。

        範例(物件名為「螢幕」的實例)：


        >>> 螢幕.取幕高()
        480


         Return the height of the turtle window.

        Example (for a TurtleScreen instance named screen):
        >>> screen.window_height()
        480
        """
        return self._window_size()[1]

    def getcanvas(self):
        """『0082  中文說明』
        取畫布，回傳一個在 龜幕類 上的 畫布 物件。

        沒有參數。

        範例(物件名為「螢幕」的實例)：

        >>> 畫布 = 螢幕.取畫布()
        >>>畫布
        <龜.ScrolledCanvas instance at 0x010742D8>


        Return the Canvas of this TurtleScreen.

        No argument.

        Example (for a Screen instance named screen):
        >>> cv = screen.getcanvas()
        >>> cv
        <turtle.ScrolledCanvas instance at 0x010742D8>
        """
        return self.cv

    def getshapes(self):
        """『0087  中文說明』
        取形，取形狀列表，回傳所有當前可用的 龜指標 形狀名稱列表。

        沒有參數。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.取形()
        ['arrow', 'blank', 'circle', ... , 'turtle']


        Return a list of names of all currently available turtle shapes.

        No argument.

        Example (for a TurtleScreen instance named screen):
        >>> screen.getshapes()
        ['arrow', 'blank', 'circle', ... , 'turtle']
        """
        return sorted(self._shapes.keys())

    def onclick(self, fun, btn=1, add=None):
        """『0007  中文說明』
        在點擊幕時，連結函數 於 畫布上 點擊鼠標的事件。

        參數：
        fun - 有兩個參數 x , y
               代表在畫布上滑鼠點擊的點座標。
        num - 數字預設為1，1,2,3分別代表滑鼠左、中、右鍵。

        舉例(名為「螢幕」的 龜幕類 的實例)：

        >>> 螢幕.在點擊幕時(前往)
        >>> 螢幕.在點擊幕時(無) # 解除連結


        Bind fun to mouse-click event on canvas.

        Arguments:
        fun -- a function with two arguments, the coordinates of the
               clicked point on the canvas.
        num -- the number of the mouse-button, defaults to 1

        Example (for a TurtleScreen instance named screen)

        >>> screen.onclick(goto)
        >>> # Subsequently clicking into the TurtleScreen will
        >>> # make the turtle move to the clicked point.
        >>> screen.onclick(None)
        """
        self._onscreenclick(fun, btn, add)

    def onkey(self, fun, key):
        """『0043  中文說明』
        在按鍵時，連結函數 於 鍵盤鍵鬆開事件。

        參數：
        fun - 不帶參數的函數
        key - 一個字串：文字鍵(如"a") 或 符號鍵(如"空白鍵")

        為了能註冊所有鍵盤事件，
        所以龜幕類必須進行監聽事件。可參看 聽() 函數。

        範例(物件名為「螢幕」的實例)：


        >>> def 畫():
        ...     前進(50)
        ...     左轉(60)
        ...
        >>> 螢幕.在按鍵時(畫, 向上鍵)
        >>> 螢幕.聽()

        上面這段程式碼，讓使用者可以藉由重複按 向上鍵 ，
        來畫出一個六邊形。



        『0045  中文說明』
        在按鍵鬆開時，連結函數 於 鍵盤鍵鬆開事件。

        參數：
        fun - 不帶參數的函數
        key - 一個字串：文字鍵(如"a") 或 符號鍵(如"空白鍵")

        為了能註冊所有鍵盤事件，
        所以龜幕類必須進行監聽事件。可參看 聽() 函數。

        範例(物件名為「螢幕」的實例):


        >>> def 畫():
        ...     前進(50)
        ...     左轉(60)
        ...
        >>> 螢幕.在按鍵鬆開時(畫, 向上鍵)
        >>> 螢幕.聽()

        上面這段程式碼，讓使用者可以藉由重複按 向上鍵 ，
        來畫出一個六邊形。



        Bind fun to key-release event of key.

        Arguments:
        fun -- a function with no arguments
        key -- a string: key (e.g. "a") or key-symbol (e.g. "space")

        In order to be able to register key-events, TurtleScreen
        must have focus. (See method listen.)

        Example (for a TurtleScreen instance named screen):

        >>> def f():
        ...     fd(50)
        ...     lt(60)
        ...
        >>> screen.onkey(f, "Up")
        >>> screen.listen()

        Subsequently the turtle can be moved by repeatedly pressing
        the up-arrow key, consequently drawing a hexagon

        """
        if fun is None:
            if key in self._keys:
                self._keys.remove(key)
        elif key not in self._keys:
            self._keys.append(key)
        self._onkeyrelease(fun, key)

    def onkeypress(self, fun, key=None):
        """『0027  中文說明』
        在按著鍵時，如果有指定鍵的話，連結函數 於 單一鍵盤鍵按下事件；
        如果沒有指定鍵的話，則連結任何按鍵事件。

        參數：
        fun - 不帶參數的函數
        key - 一個字串：文字鍵(如"a") 或 符號鍵(如"空白鍵")

        為了能註冊所有鍵盤事件，
        所以龜幕類必須進行監聽事件。可參看 聽() 函數。

        範例(物件名為「螢幕」的實例)：



        >>> def 畫():
        ...     前進(50)
        ...     左轉(60)
        ...
        >>> 螢幕.在按著鍵時(畫, 向上鍵)
        >>> 螢幕.聽()

        上面這段程式碼，讓使用者可以藉由重複按 向上鍵 ，
        來畫出一個六邊形。



        Bind fun to key-press event of key if key is given,
        or to any key-press-event if no key is given.

        Arguments:
        fun -- a function with no arguments
        key -- a string: key (e.g. "a") or key-symbol (e.g. "space")

        In order to be able to register key-events, TurtleScreen
        must have focus. (See method listen.)

        Example (for a TurtleScreen instance named screen
        and a Turtle instance named turtle):

        >>> def f():
        ...     fd(50)
        ...     lt(60)
        ...
        >>> screen.onkeypress(f, "Up")
        >>> screen.listen()

        Subsequently the turtle can be moved by repeatedly pressing
        the up-arrow key, or by keeping pressed the up-arrow key.
        consequently drawing a hexagon.
        """
        if fun is None:
            if key in self._keys:
                self._keys.remove(key)
        elif key is not None and key not in self._keys:
            self._keys.append(key)
        self._onkeypress(fun, key)

    def listen(self, xdummy=None, ydummy=None):
        """『0073  中文說明』
        聽，設置聚焦於  龜幕類 之上(為了收集鍵盤事件)。

        沒有參數。
        偽參數為了提供要能夠通過監聽點擊函數。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.聽()


        Set focus on TurtleScreen (in order to collect key-events)

        No arguments.
        Dummy arguments are provided in order
        to be able to pass listen to the onclick method.

        Example (for a TurtleScreen instance named screen):
        >>> screen.listen()
        """
        self._listen()

    def ontimer(self, fun, t=0):
        """『0012  中文說明』
        在計時後，安裝計時器，t毫秒後呼叫函數。

        參數：
        fun - 不帶參數的函數。
        t - 一個數 > = 0

        範例(物件名為「螢幕」的實例)：


        >>> 正在執行 = 真
        >>> def 畫():
        ...     if 正在執行:
        ...             前進(50)
        ...             左轉(60)
        ...             螢幕.在計時後(畫, 250)
        ...
        >>> 畫()   # 讓 龜類 運行
        >>> 正在執行 = 假


        Install a timer, which calls fun after t milliseconds.

        Arguments:
        fun -- a function with no arguments.
        t -- a number >= 0

        Example (for a TurtleScreen instance named screen):

        >>> running = True
        >>> def f():
        ...     if running:
        ...             fd(50)
        ...             lt(60)
        ...             screen.ontimer(f, 250)
        ...
        >>> f()   # makes the turtle marching around
        >>> running = False
        """
        self._ontimer(fun, t)

    def bgpic(self, picname=None):
        """『0020  中文說明』
        背景圖，設置或回傳背景圖片。

        可選參數:
        picname  - 一個GIF文件名稱或"nopic"字符串。

        如果picname是一個文件名，設置相應的圖片作為背景圖。
        如果picname是"nopic"，如果背景圖存在則將其刪除。
        如果沒有picname參數，則回傳當前背景圖的文件名。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.背景圖()
        "nopic"
        >>> 螢幕.背景圖("landscape.gif")
        >>> 螢幕.背景圖()
        "landscape.gif"


        Set background image or return name of current backgroundimage.

        Optional argument:
        picname -- a string, name of a gif-file or "nopic".

        If picname is a filename, set the corresponding image as background.
        If picname is "nopic", delete backgroundimage, if present.
        If picname is None, return the filename of the current backgroundimage.

        Example (for a TurtleScreen instance named screen):
        >>> screen.bgpic()
        'nopic'
        >>> screen.bgpic("landscape.gif")
        >>> screen.bgpic()
        'landscape.gif'
        """
        if picname is None:
            return self._bgpicname
        if picname not in self._bgpics:
            self._bgpics[picname] = self._image(picname)
        self._setbgpic(self._bgpic, self._bgpics[picname])
        self._bgpicname = picname

    def screensize(self, canvwidth=None, canvheight=None, bg=None):
        """『0024  中文說明』
        幕大小，重設畫布大小。

        可選參數:
        canvwidth  - 正整數，畫布以像素為單位的寬度
        canvheight  - 正整數，畫布以像素為單位的高度
        bg  -  顏色字串或顏色元組，新的背景顏色
        如果沒有傳入參數，回傳目前設定值(canvaswidth,canvasheight)。

        不要改變繪圖視窗。
        在畫布上使用滾動條可查看被隱蔽部位。
        (可以見到畫布外的動作！)

        範例(物件名為「龜」的實例)：

        >>> 龜.幕大小(2000,1500)
        >>>#例如：可尋找一個犯錯逃脫的龜;-)


        Resize the canvas the turtles are drawing on.

        Optional arguments:
        canvwidth -- positive integer, new width of canvas in pixels
        canvheight --  positive integer, new height of canvas in pixels
        bg -- colorstring or color-tuple, new backgroundcolor
        If no arguments are given, return current (canvaswidth, canvasheight)

        Do not alter the drawing window. To observe hidden parts of
        the canvas use the scrollbars. (Can make visible those parts
        of a drawing, which were outside the canvas before!)

        Example (for a Turtle instance named turtle):
        >>> turtle.screensize(2000,1500)
        >>> # e.g. to search for an erroneously escaped turtle ;-)
        """
        return self._resize(canvwidth, canvheight, bg)

    onscreenclick = onclick
    resetscreen = reset
    clearscreen = clear
    addshape = register_shape
    onkeyrelease = onkey
    加形狀= addshape
    背景色= bgcolor
    背景圖= bgpic
    清除幕= clearscreen
    色模式= colormode
    延遲= delay
    取畫布= getcanvas
    取形= getshapes
    取形狀= getshapes
    聽= listen
    聽鍵盤= listen
    模式= mode
    在點擊時= onclick
    在點擊龜時= onclick
    在滑鼠鍵點擊時= onclick
    在按鍵時= onkey
    在按鍵鬆開時= onkey
    在按著鍵時= onkeypress
    在按下鍵時= onkeypress
    在按鍵鬆開時= onkeyrelease
    在點擊幕時= onscreenclick
    在幕點擊時= onscreenclick
    在滑鼠鍵點擊幕時= onscreenclick
    在計時後= ontimer
    在計時器若干毫秒之後= ontimer
    登記形狀= register_shape
    註冊形狀= register_shape
    重設= reset
    重設所有龜= reset
    重設幕= resetscreen
    幕大小= screensize
    重設幕寬高= screensize
    重設幕大小= screensize
    設座標系統= setworldcoordinates
    座標系統= setworldcoordinates
    追蹤= tracer
    追蹤更新畫面= tracer
    追蹤器= tracer
    龜群= turtles
    取龜列表= turtles
    龜列表= turtles
    更新= update
    更新畫面= update
    取幕高= window_height
    幕高= window_height
    窗高= window_height
    取幕寬= window_width
    幕寬= window_width
    窗寬= window_width
龜幕類= TurtleScreen
烏龜螢幕類= TurtleScreen
class TNavigator(object):
    """Navigation part of the RawTurtle.
    Implements methods for turtle movement.
    """
    START_ORIENTATION = {
        "standard": Vec2D(1.0, 0.0),
        "world"   : Vec2D(1.0, 0.0),
        "logo"    : Vec2D(0.0, 1.0)  }
    DEFAULT_MODE = "standard"
    DEFAULT_ANGLEOFFSET = 0
    DEFAULT_ANGLEORIENT = 1

    def __init__(self, mode=DEFAULT_MODE):
        self._angleOffset = self.DEFAULT_ANGLEOFFSET
        self._angleOrient = self.DEFAULT_ANGLEORIENT
        self._mode = mode
        self.undobuffer = None
        self.degrees()
        self._mode = None
        self._setmode(mode)
        TNavigator.reset(self)

    def reset(self):
        """reset turtle to its initial values

        Will be overwritten by parent class
        """
        self._position = Vec2D(0.0, 0.0)
        self._orient =  TNavigator.START_ORIENTATION[self._mode]

    def _setmode(self, mode=None):
        """Set turtle-mode to 'standard', 'world' or 'logo'.
        """
        if mode is None:
            return self._mode
        if mode not in ["standard", "logo", "world"]:
            return
        self._mode = mode
        if mode in ["standard", "world"]:
            self._angleOffset = 0
            self._angleOrient = 1
        else: # mode == "logo":
            self._angleOffset = self._fullcircle/4.
            self._angleOrient = -1

    def _setDegreesPerAU(self, fullcircle):
        """Helper function for degrees() and radians()"""
        self._fullcircle = fullcircle
        self._degreesPerAU = 360/fullcircle
        if self._mode == "standard":
            self._angleOffset = 0
        else:
            self._angleOffset = fullcircle/4.

    def degrees(self, fullcircle=360.0):
        """『0044  中文說明』
        角度，設定 角 的度量單位為 「度數」。

        可選參數:
        fullcircle  - 一個數字(整數或浮點數)

        設定測量角度的單位，即設定幾〝度〞為一個完整的圓。
        預設值為 360 度。
        

        範例(物件名為「龜」的實例):

        >>> 龜.左轉(90)
        >>> 龜.頭向()
        90

        可改變角的度量單位 為 grad ( 也稱作 gon、grade或 gradian)，
        定義為「直角」定為 100 grads，所以全圓定為 400 grads。
        >>> 龜.角度(400.0)
        >>> 龜.頭向()
        100



         Set angle measurement units to degrees.

        Optional argument:
        fullcircle -  a number

        Set angle measurement units, i. e. set number
        of 'degrees' for a full circle. Dafault value is
        360 degrees.

        Example (for a Turtle instance named turtle):
        >>> turtle.left(90)
        >>> turtle.heading()
        90

        Change angle measurement unit to grad (also known as gon,
        grade, or gradian and equals 1/100-th of the right angle.)
        >>> turtle.degrees(400.0)
        >>> turtle.heading()
        100

        """
        self._setDegreesPerAU(fullcircle)

    def radians(self):
        """『0068  中文說明』
        弳度，設置角度測量單位為弧度(單位圓的弧長)。

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.頭向()
        90
        >>> 龜.弳度()
        >>> 龜.頭向()
        1.5707963267948966


         Set the angle measurement units to radians.

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> turtle.heading()
        90
        >>> turtle.radians()
        >>> turtle.heading()
        1.5707963267948966
        """
        self._setDegreesPerAU(2*math.pi)

    def _go(self, distance):
        """move turtle forward by specified distance"""
        ende = self._position + self._orient * distance
        self._goto(ende)

    def _rotate(self, angle):
        """Turn turtle counterclockwise by specified angle if angle > 0."""
        angle *= self._degreesPerAU
        self._orient = self._orient.rotate(angle)

    def _goto(self, end):
        """move turtle to position end."""
        self._position = end

    def forward(self, distance):
        """『0033  中文說明』
        前進，龜前進指定的距離。

        別名: 前進 | forward | fd

        參數:
        distance - 一個數字(整數或浮點數)

        龜前進指定的距離，往 龜指標 的頭之方向。

        範例(物件名為「龜」的實例)：
        
        >>> from turtle_tc import *
        >>> 龜= 龜類()
        >>> 龜.位置()
        (0.00,0.00)
        >>> 龜.前進(25)
        >>> 龜.位置()
        (25.00,0.00)
        >>> 龜.前進(-75)
        >>> 龜.位置()
        (-50.00,0.00)


        Move the turtle forward by the specified distance.

        Aliases: forward | fd

        Argument:
        distance -- a number (integer or float)

        Move the turtle forward by the specified distance, in the direction
        the turtle is headed.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 0.00)
        >>> turtle.forward(25)
        >>> turtle.position()
        (25.00,0.00)
        >>> turtle.forward(-75)
        >>> turtle.position()
        (-50.00,0.00)
        """
        self._go(distance)

    def back(self, distance):
        """『0005  中文說明』
        後退，後退 一段距離。

        別名: 後退 | back | backward | bk

        參數:
        distance -- 一個數字

        往 龜指標 的反方向前進指定的距離，但不會改變龜指標 的方向。
        

        範例(物件名為「龜」的實例):

        >>> 龜.位置() # 位置 = position
        (0.00,0.00)
        >>> 龜.後退(30) # 後退 = backward
        >>> 龜.位置()
        (-30.00,0.00)


        Move the turtle backward by distance.

        Aliases: back | backward | bk

        Argument:
        distance -- a number

        Move the turtle backward by distance ,opposite to the direction the
        turtle is headed. Do not change the turtle's heading.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 0.00)
        >>> turtle.backward(30)
        >>> turtle.position()
        (-30.00, 0.00)
        """
        self._go(-distance)

    def right(self, angle):
        """『0083  中文說明』
        右轉，向右轉一個角度。

        別名：右轉 | rt | right

        參數:
        angle  - 一個數字(整數或浮點數)

        將 龜指標 向右轉angle角度。(單位是預設值，但可以通過度()和弳度()函數來設置。)
        角方向設定取決於 模式()。

        範例(物件名為「龜」的實例)：

        >>> 龜.頭向()
        22.0
        >>> 龜.右轉(45)
        >>> 龜.頭向()
        337.0


        Turn turtle right by angle units.

        Aliases: right | rt

        Argument:
        angle -- a number (integer or float)

        Turn turtle right by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. (See this.)

        Example (for a Turtle instance named turtle):
        >>> turtle.heading()
        22.0
        >>> turtle.right(45)
        >>> turtle.heading()
        337.0
        """
        self._rotate(-angle)

    def left(self, angle):
        """『0016  中文說明』
        左轉， 龜指標 左轉指定角度單位。

        別名: 左轉 | left | lt

        參數:
        angle - 一個數字(整數或浮點數)

        龜左轉一個角度(angle)。(單位預設為「度數」(0~360)
        但可以藉由設定 角度() 和 弳度() 來改變設置。
        角方向取決於 模式() 的設定。(請參閱...。)

        範例(物件名為「龜」的實例):

        >>> 龜.頭向()
        22.0
        >>> 龜.左轉(45)
        >>> 龜.頭向()
        67.0


        Turn turtle left by angle units.

        Aliases: left | lt

        Argument:
        angle -- a number (integer or float)

        Turn turtle left by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on mode. (See this.)

        Example (for a Turtle instance named turtle):
        >>> turtle.heading()
        22.0
        >>> turtle.left(45)
        >>> turtle.heading()
        67.0
        """
        self._rotate(angle)

    def pos(self):
        """『0036  中文說明』
         位置，回傳 龜的當前位置(X,Y)，資料型態是Vec2D向量。

        別名: pos | position | 位置

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.位置()
        (0.00,240.00)


        Return the turtle's current location (x,y), as a Vec2D-vector.

        Aliases: pos | position

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> turtle.pos()
        (0.00, 240.00)
        """
        return self._position

    def xcor(self):
        """『0053  中文說明』
        x座標，回傳 龜指標 的x座標。

        沒有參數。

        範例(物件名為「龜」的實例)：

        >>>重設()
        >>>龜.左轉(60)
        >>>龜.前進(100)
        >>>龜.x座標()
        50.0


         Return the turtle's x coordinate.

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> reset()
        >>> turtle.left(60)
        >>> turtle.forward(100)
        >>> print turtle.xcor()
        50.0
        """
        return self._position[0]

    def ycor(self):
        """『0037  中文說明』
        y座標，回傳 龜指標 的y座標。
        
        沒有參數。

        範例(物件名為「龜」的實例)：

        >>>重設()
        >>>龜.左轉(60)
        >>>龜.前進(100)
        >>>龜.y座標()
        86.6025403784


         Return the turtle's y coordinate
        ---
        No arguments.

        Example (for a Turtle instance named turtle):
        >>> reset()
        >>> turtle.left(60)
        >>> turtle.forward(100)
        >>> print turtle.ycor()
        86.6025403784
        """
        return self._position[1]


    def goto(self, x, y=None):
        """『0049  中文說明』
        前往，龜前往一個絕對位置。

        別名：前往 | 設位置 | setpos | setposition | goto:

        參數：
        x  - 一個數字  或 一對數字/向量
        y  - 一個數字  或    無

        呼叫：前往(x,y)     # 兩個座標值
        - 或：前往((x,y))   # 一個元組
        - 或：前往(vec)     # 與 位置() 回傳一樣。

        龜指標 移動到一個絕對位置。
        如果筆是下筆狀態，將畫出一條線。龜指標 的方向不會改變。

        範例(物件名為「龜」的實例)：

        >>> 所在座標 = 龜.位置()
        >>> 所在座標
        (0.00,0.00)
        >>> 龜.前往(60,30)
        >>> 龜.位置()
        (60.00,30.00)
        >>> 龜.前往((20,80))
        >>> 龜.位置()
        (20.00,80.00)
        >>> 龜.前往(所在座標)
        >>> 龜.位置()
        (0.00,0.00)


        Move turtle to an absolute position.

        Aliases: setpos | setposition | goto:

        Arguments:
        x -- a number      or     a pair/vector of numbers
        y -- a number             None

        call: goto(x, y)         # two coordinates
        --or: goto((x, y))       # a pair (tuple) of coordinates
        --or: goto(vec)          # e.g. as returned by pos()

        Move turtle to an absolute position. If the pen is down,
        a line will be drawn. The turtle's orientation does not change.

        Example (for a Turtle instance named turtle):
        >>> tp = turtle.pos()
        >>> tp
        (0.00, 0.00)
        >>> turtle.setpos(60,30)
        >>> turtle.pos()
        (60.00,30.00)
        >>> turtle.setpos((20,80))
        >>> turtle.pos()
        (20.00,80.00)
        >>> turtle.setpos(tp)
        >>> turtle.pos()
        (0.00,0.00)
        """
        if y is None:
            self._goto(Vec2D(*x))
        else:
            self._goto(Vec2D(x, y))

    def home(self):
        """『0018  中文說明』
        回家，讓 龜指標 回到原點 - 座標(0,0)。

        沒有參數。

        讓龜回到原點 - 座標(0,0)，
        並設定其 龜指標 方向為初始狀態。

        範例(物件名為「龜」的實例)：

        >>> 龜.回家()


        Move turtle to the origin - coordinates (0,0).

        No arguments.

        Move turtle to the origin - coordinates (0,0) and set its
        heading to its start-orientation (which depends on mode).

        Example (for a Turtle instance named turtle):
        >>> turtle.home()
        """
        self.goto(0, 0)
        self.setheading(0)

    def setx(self, x):
        """『0084  中文說明』
        設x座標，設置龜的 x 座標。

        參數:
        x  - 一個數字(整數或浮點數)

        將龜的第一個座標設為x，第二個座標保持不變。

        範例(物件名為「龜」的實例)：

        >>> 龜.位置()
        (0.00,240.00)
        >>> 龜.設x座標(10)
        >>> 龜.位置()
        (10.00,240.00)


        Set the turtle's first coordinate to x

        Argument:
        x -- a number (integer or float)

        Set the turtle's first coordinate to x, leave second coordinate
        unchanged.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 240.00)
        >>> turtle.setx(10)
        >>> turtle.position()
        (10.00, 240.00)
        """
        self._goto(Vec2D(x, self._position[1]))

    def sety(self, y):
        """『0013  中文說明』
        設y座標，設置龜的 y 座標。

        參數:
        y  - 一個數字(整數或浮點數)

        將龜的第二個座標設為y，第一個座標保持不變。

        範例(物件名為「龜」的實例)：

        >>> 龜.位置()
        0.00,40.00)
        >>> 龜.設y座標(-10)
        >>> 龜.位置()
        ((0.00,-10.00)


        Set the turtle's second coordinate to y

        Argument:
        y -- a number (integer or float)

        Set the turtle's first coordinate to x, second coordinate remains
        unchanged.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00, 40.00)
        >>> turtle.sety(-10)
        >>> turtle.position()
        (0.00, -10.00)
        """
        self._goto(Vec2D(self._position[0], y))

    def distance(self, x, y=None):
        """『0035  中文說明』
        距離，回傳從龜指標本身位置 到 座標 x, y 的距離。

        參數：
        x  - 一個數字 或 數字的一對/向量 或 龜類實例
        y  - 一個數字 或 無

        呼叫: 距離(x,y)    # 兩個座標
        - 或: 距離((x,y))  # 一對(元組)
        - 或: 距離(vec)    # 與 位置() 的回傳值一樣
        - 或: 距離(mypen)  # 其中 mypen 是另一個龜

        範例(物件名為「龜」的實例):

        >>> 龜.位置()
        (0.00,0.00)
        >>> 龜.距離(30,40)
        50.0
        >>> 筆= 龜類()
        >>> 筆.前進(77)
        >>> 龜.距離(筆)
        77.0


        Return the distance from the turtle to (x,y) in turtle step units.

        Arguments:
        x -- a number   or  a pair/vector of numbers   or   a turtle instance
        y -- a number       None                            None

        call: distance(x, y)         # two coordinates
        --or: distance((x, y))       # a pair (tuple) of coordinates
        --or: distance(vec)          # e.g. as returned by pos()
        --or: distance(mypen)        # where mypen is another turtle

        Example (for a Turtle instance named turtle):
        >>> turtle.pos()
        (0.00, 0.00)
        >>> turtle.distance(30,40)
        50.0
        >>> pen = Turtle()
        >>> pen.forward(77)
        >>> turtle.distance(pen)
        77.0
        """
        if y is not None:
            pos = Vec2D(x, y)
        if isinstance(x, Vec2D):
            pos = x
        elif isinstance(x, tuple):
            pos = Vec2D(*x)
        elif isinstance(x, TNavigator):
            pos = x._position
        return abs(pos - self._position)

    def towards(self, x, y=None):
        """『0009  中文說明』
        朝向，計算並回傳 龜指標 朝向 點(x,y) 的角度，亦即從 龜指標 的位置 到點(x,y) 的直線角度。

        參數:
        x  - 一個數字或數字的一對/向量或 龜類 實例
        y  - 一個數字或 無

        呼叫：朝向(x,y) #兩個座標
        - 或：朝向((x,y)) #一對元組(向量)
        - 或：朝向(VEC) #例如可以藉由 位置() 回傳的向量
        - 或：朝向(mypen) #,其中mypen是另一個 龜類

        回傳的角度為 龜指標 到該指定位置之間直線角度，
        其角度大小與其模式設定有關。(取決於 模式() - "standard"或"logo")
        

        範例(物件名為「龜」的實例)：

        >>> 龜.位置()
        (10.00,10.00)
        >>> 龜.朝向(0,0)
        225.0


        Return the angle of the line from the turtle's position to (x, y).

        Arguments:
        x -- a number   or  a pair/vector of numbers   or   a turtle instance
        y -- a number       None                            None

        call: distance(x, y)         # two coordinates
        --or: distance((x, y))       # a pair (tuple) of coordinates
        --or: distance(vec)          # e.g. as returned by pos()
        --or: distance(mypen)        # where mypen is another turtle

        Return the angle, between the line from turtle-position to position
        specified by x, y and the turtle's start orientation. (Depends on
        modes - "standard" or "logo")

        Example (for a Turtle instance named turtle):
        >>> turtle.pos()
        (10.00, 10.00)
        >>> turtle.towards(0,0)
        225.0
        """
        if y is not None:
            pos = Vec2D(x, y)
        if isinstance(x, Vec2D):
            pos = x
        elif isinstance(x, tuple):
            pos = Vec2D(*x)
        elif isinstance(x, TNavigator):
            pos = x._position
        x, y = pos - self._position
        result = round(math.atan2(y, x)*180.0/math.pi, 10) % 360.0
        result /= self._degreesPerAU
        return (self._angleOffset + self._angleOrient*result) % self._fullcircle

    def heading(self):
        """『0069  中文說明』
        頭向，回傳當前 龜指標 的方向。

        沒有參數。

        範例(物件名為「龜」的實例)：

        >>> 龜.左轉(67)
        >>> 龜.頭向()
        67.0


         Return the turtle's current heading.

        No arguments.

        Example (for a Turtle instance named turtle):
        >>> turtle.left(67)
        >>> turtle.heading()
        67.0
        """
        x, y = self._orient
        result = round(math.atan2(y, x)*180.0/math.pi, 10) % 360.0
        result /= self._degreesPerAU
        return (self._angleOffset + self._angleOrient*result) % self._fullcircle

    def setheading(self, to_angle):
        """『0002  中文說明』
        設頭向，設置 龜指標 的方向。

        別名: setheading | 設頭向

        參數:
        to_angle  - 一個數字(整數或浮點數)

        根據 模式()的設定而改變度數方向及設定。
        這裡有度數一些常見的方向:

        'standard'模式   'logo'模式:
        ----------------|------------
           0  - 東      |    北
          90  - 北      |    東
         180  - 西      |    南
         270  - 南      |    西

        範例(物件名為「龜」的實例)：

        >>> 龜.設頭向(90)
        >>> 龜.頭向()
        90


        Set the orientation of the turtle to to_angle.

        Aliases:  setheading | seth

        Argument:
        to_angle -- a number (integer or float)

        Set the orientation of the turtle to to_angle.
        Here are some common directions in degrees:

         standard - mode:          logo-mode:
        -------------------|--------------------
           0 - east                0 - north
          90 - north              90 - east
         180 - west              180 - south
         270 - south             270 - west

        Example (for a Turtle instance named turtle):
        >>> turtle.setheading(90)
        >>> turtle.heading()
        90
        """
        angle = (to_angle - self.heading())*self._angleOrient
        full = self._fullcircle
        angle = (angle+full/2.)%full - full/2.
        self._rotate(angle)

    def circle(self, radius, extent = None, steps = None):
        """『0070  中文說明』
        畫圓，給定半徑。

        參數:
        radius(半徑)  - 一個數字
        extent (圓弧角度)(可選) - 一個數字
        steps (步數)(可選) - 一個整數

        可畫指定半徑的圓，其圓心座標在 龜指標 的左方半徑單位。
        extent (圓弧角度)決定圓弧的角度範圍(完整的圓為360)。
        如沒給與該值，則自動為360。
        給予的值非完整的圓，則最後圓弧的位置即為 龜指標 位置。
        繪製圓弧時，如radius(半徑)為正時為則逆時針方​​向，
        否則以順時針方向繪製。
        而 龜指標 的方向由extent(圓弧角度)的量改變。

        由於圓形是由一個內接正多邊形所迫近而成，
        steps (步數)設定使用的正多邊形數量。
        如果沒有給予，則會自動計算。
        可用來畫標準多邊形。。

        呼叫:圓(半徑)#完整的圓
        - 或:圓(半徑,圓弧角度)#弧
        - 或:圓(半徑,圓弧角度,步數)
        - 或:圓(半徑,步數= 6)#6邊形

        範例(物件名為「龜」的實例):

        >>> 龜.畫圓(50)
        >>> 龜.畫圓(120,180) # 180度 代表 半圓


         Draw a circle with given radius.

        Arguments:
        radius -- a number
        extent (optional) -- a number
        steps (optional) -- an integer

        Draw a circle with given radius. The center is radius units left
        of the turtle; extent - an angle - determines which part of the
        circle is drawn. If extent is not given, draw the entire circle.
        If extent is not a full circle, one endpoint of the arc is the
        current pen position. Draw the arc in counterclockwise direction
        if radius is positive, otherwise in clockwise direction. Finally
        the direction of the turtle is changed by the amount of extent.

        As the circle is approximated by an inscribed regular polygon,
        steps determines the number of steps to use. If not given,
        it will be calculated automatically. Maybe used to draw regular
        polygons.

        call: circle(radius)                  # full circle
        --or: circle(radius, extent)          # arc
        --or: circle(radius, extent, steps)
        --or: circle(radius, steps=6)         # 6-sided polygon

        Example (for a Turtle instance named turtle):
        >>> turtle.circle(50)
        >>> turtle.circle(120, 180)  # semicircle
        """
        if self.undobuffer:
            self.undobuffer.push(["seq"])
            self.undobuffer.cumulate = True
        speed = self.speed()
        if extent is None:
            extent = self._fullcircle
        if steps is None:
            frac = abs(extent)/self._fullcircle
            steps = 1+int(min(11+abs(radius)/6.0, 59.0)*frac)
        w = 1.0 * extent / steps
        w2 = 0.5 * w
        l = 2.0 * radius * math.sin(w2*math.pi/180.0*self._degreesPerAU)
        if radius < 0:
            l, w, w2 = -l, -w, -w2
        tr = self._tracer()
        dl = self._delay()
        if speed == 0:
            self._tracer(0, 0)
        else:
            self.speed(0)
        self._rotate(w2)
        for i in range(steps):
            self.speed(speed)
            self._go(l)
            self.speed(0)
            self._rotate(w)
        self._rotate(-w2)
        if speed == 0:
            self._tracer(tr, dl)
        self.speed(speed)
        if self.undobuffer:
            self.undobuffer.cumulate = False

## three dummy methods to be implemented by child class:

    def speed(self, s=0):
        """dummy method - to be overwritten by child class"""
    def _tracer(self, a=None, b=None):
        """dummy method - to be overwritten by child class"""
    def _delay(self, n=None):
        """dummy method - to be overwritten by child class"""

    fd = forward
    bk = back
    backward = back
    rt = right
    lt = left
    position = pos
    setpos = goto
    setposition = goto
    seth = setheading
    重設= reset
    前進= forward
    後退= back
    右轉= right
    左轉= left
    位置= pos
    前往= goto
    設位置= goto
    去到= goto
    設頭向= setheading
    回家= home
    畫圓= circle
    圓= circle
    速度= speed
    角度= degrees
    設角為度= degrees
    設圓為360度= degrees
    設角的單位為角度= degrees
    弳度= radians
    弧度= radians
    半徑數= radians
    設角為弧= radians
    設角的單位為半徑數= radians
    設圓為2pi弧= radians
    x座標= xcor
    座標x= xcor
    y座標= ycor
    座標y= ycor
    設x座標= setx
    設座標x= setx
    設y座標= sety
    設座標y= sety
    距離= distance
    頭向= heading
    朝向= towards
    朝向xy= towards
    設位置= setpos
    設位置= setposition
    前進= fd
    後退= bk
    後退= backward
    右轉= rt
    左轉= lt
    位置= position
    設頭向= seth
龜行類= TNavigator
烏龜航行類= TNavigator
class TPen(object):
    """Drawing part of the RawTurtle.
    Implements drawing properties.
    """
    def __init__(self, resizemode=_CFG["resizemode"]):
        self._resizemode = resizemode # or "user" or "noresize"
        self.undobuffer = None
        TPen._reset(self)

    def _reset(self, pencolor=_CFG["pencolor"],
                     fillcolor=_CFG["fillcolor"]):
        self._pensize = 1
        self._shown = True
        self._pencolor = pencolor
        self._fillcolor = fillcolor
        self._drawing = True
        self._speed = 3
        self._stretchfactor = (1., 1.)
        self._shearfactor = 0.
        self._tilt = 0.
        self._shapetrafo = (1., 0., 0., 1.)
        self._outlinewidth = 1

    def resizemode(self, rmode=None):
        """『0047  中文說明』
         重設大小模式，"auto", "user", "noresize"。

        (可選)參數:
        rmode  -  "auto", "user", "noresize"，三個字串中之一

        設置不同的模式會有不同的效果：
          - "auto"：對應 筆寬() 的值，自動調整龜形狀大小。
          - "user"：根據 形狀大小() 展延因子及輪廓大小的設置，改變龜形狀大小
          - "noresize"：自動調整為原本形狀及輪廓大小。
        無傳入參數，即可用來查詢目前設定。
        當呼叫 形狀大小() 並設置參數時，則 重設大小模式() 自動切換為"user"。


        範例(物件名為「龜」的實例)：

        >>> 龜.重設大小模式("noresize")
        >>> 龜.重設大小模式()
        "noresize"


        Set resizemode to one of the values: "auto", "user", "noresize".

        (Optional) Argument:
        rmode -- one of the strings "auto", "user", "noresize"

        Different resizemodes have the following effects:
          - "auto" adapts the appearance of the turtle
                   corresponding to the value of pensize.
          - "user" adapts the appearance of the turtle according to the
                   values of stretchfactor and outlinewidth (outline),
                   which are set by shapesize()
          - "noresize" no adaption of the turtle's appearance takes place.
        If no argument is given, return current resizemode.
        resizemode("user") is called by a call of shapesize with arguments.


        Examples (for a Turtle instance named turtle):
        >>> turtle.resizemode("noresize")
        >>> turtle.resizemode()
        'noresize'
        """
        if rmode is None:
            return self._resizemode
        rmode = rmode.lower()
        if rmode in ["auto", "user", "noresize"]:
            self.pen(resizemode=rmode)

    def pensize(self, width=None):
        """『0011  中文說明』
        筆粗(筆寬)，設置或回傳線條的粗細。

        別名:pensize | width | 筆粗 | 筆寬

        參數:
        寬度 - 正數

        設置線的粗細寬度或回傳。
        如果 重設大小模式() 設置為 "auto" 和 龜指標形狀 是一個多邊形，
        該多邊形的繪製與其為相同的線條粗細。
        如果沒有給予參數，則回傳現在的設置。

        範例(物件名為「龜」的實例):

        >>> 龜.筆粗()
        1
        >>> 龜.筆粗(10) #從現在開始以寬度為10線繪製


        Set or return the line thickness.

        Aliases:  pensize | width

        Argument:
        width -- positive number

        Set the line thickness to width or return it. If resizemode is set
        to "auto" and turtleshape is a polygon, that polygon is drawn with
        the same line thickness. If no argument is given, current pensize
        is returned.

        Example (for a Turtle instance named turtle):
        >>> turtle.pensize()
        1
        >>> turtle.pensize(10)   # from here on lines of width 10 are drawn
        """
        if width is None:
            return self._pensize
        self.pen(pensize=width)


    def penup(self):
        """『0081  中文說明』
        提筆，移動時無畫線。

        別名: 提筆 | pu | penup

        沒有參數

        範例(物件名為「龜」的實例):

        >>> 龜.提筆()


        Pull the pen up -- no drawing when moving.

        Aliases: penup | pu | up

        No argument

        Example (for a Turtle instance named turtle):
        >>> turtle.penup()
        """
        if not self._drawing:
            return
        self.pen(pendown=False)

    def pendown(self):
        """『0065  中文說明』
        下筆 - 移動時畫圖。

        別名: 下筆 | pendown | pd | down

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.下筆()


        『0091  中文說明』
        下筆，移動時繪製，會畫出移動軌跡。

        別名:下筆| pd | pendown

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.下筆()


        Pull the pen down -- drawing when moving.

        Aliases: pendown | pd | down

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.pendown()
        """
        if self._drawing:
            return
        self.pen(pendown=True)

    def isdown(self):
        """『0072  中文說明』
        下筆嗎，測試是否為下筆狀態。傳回真假值(True/False)。

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.提筆()
        >>> 龜.下筆嗎()
        False
        >>> 龜.下筆()
        >>> 龜.下筆嗎()
        True


        Return True if pen is down, False if it's up.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.penup()
        >>> turtle.isdown()
        False
        >>> turtle.pendown()
        >>> turtle.isdown()
        True
        """
        return self._drawing

    def speed(self, speed=None):
        """『0079  中文說明』
        速度，回傳或設置 龜指標 的速度。

        可選參數：
        speed - 範圍為0 .. 10 或 一個速度字串(見下文)

        設定龜指標速度範圍為0 .. 10。
        如果沒有給出參數，則回傳當前速度設定。

        若輸入為大於10於或小於0.5時，
        速度被設定為0。
        速度字串被映射到速度大小，根據下面設定：
            'fastest' :  0
            'fast'    :  10
            'normal'  :  6
            'slow'    :  3
            'slowest' :  1
        速度從1至10代表執行越來越快的畫線和龜指標轉折。

        注意：
        speed= 0 代表*沒有*動畫發生。
        前進/後退 或 左/右 使龜指標瞬間跳到結果。

        範例(物件名為「龜」的實例)：

        >>> 龜.速度(3)


         Return or set the turtle's speed.

        Optional argument:
        speed -- an integer in the range 0..10 or a speedstring (see below)

        Set the turtle's speed to an integer value in the range 0 .. 10.
        If no argument is given: return current speed.

        If input is a number greater than 10 or smaller than 0.5,
        speed is set to 0.
        Speedstrings  are mapped to speedvalues in the following way:
            'fastest' :  0
            'fast'    :  10
            'normal'  :  6
            'slow'    :  3
            'slowest' :  1
        speeds from 1 to 10 enforce increasingly faster animation of
        line drawing and turtle turning.

        Attention:
        speed = 0 : *no* animation takes place. forward/back makes turtle jump
        and likewise left/right make the turtle turn instantly.

        Example (for a Turtle instance named turtle):
        >>> turtle.speed(3)
        """
        speeds = {'fastest':0, 'fast':10, 'normal':6, 'slow':3, 'slowest':1 }
        if speed is None:
            return self._speed
        if speed in speeds:
            speed = speeds[speed]
        elif 0.5 < speed < 10.5:
            speed = int(round(speed))
        else:
            speed = 0
        self.pen(speed=speed)

    def color(self, *args):
        """『0050  中文說明』
        顏色，回傳或設定 顏色 和 填色。

        參數：
        允許多種輸入格式。
        能使用 0~3個參數，如下所示:

        顏色()
            回傳當前的「筆色」和當前的「填色」。
            組成一對顏色字串作為回傳值。
            與 筆色() 和 填色() 2個函數呼叫後的的傳回值一樣。
        顏色(colorstring)、顏色((r,g,b))、顏色(r,g,b)
            輸入筆色，同時將給定值設定為 筆色與填色。
        顏色(colorstring1,colorstring2)、顏色((R1,G1,B1)、(R2,G2,B2))
            設定筆色(colorstring1)和填色(colorstring2)。
            也可使用其他顏色的格式設定。

        如果 龜指標 是一個多邊形(龜形、正方形等)，
        輪廓和多邊形的內部將以新設置的顏色來繪製。
        如需更多信息請參見： 筆色、填色

        範例(物件名為「龜」的實例)：

        >>> 龜.顏色(紅,綠)
        >>> 龜.顏色()
        ('red',"green")
        >>> 顏色模式(255)
        >>>顏色((40,80,120),(160,200,240))
        >>>顏色()
        ('#285078','#a0c8f0')


        Return or set the pencolor and fillcolor.

        Arguments:
        Several input formats are allowed.
        They use 0, 1, 2, or 3 arguments as follows:

        color()
            Return the current pencolor and the current fillcolor
            as a pair of color specification strings as are returned
            by pencolor and fillcolor.
        color(colorstring), color((r,g,b)), color(r,g,b)
            inputs as in pencolor, set both, fillcolor and pencolor,
            to the given value.
        color(colorstring1, colorstring2),
        color((r1,g1,b1), (r2,g2,b2))
            equivalent to pencolor(colorstring1) and fillcolor(colorstring2)
            and analogously, if the other input format is used.

        If turtleshape is a polygon, outline and interior of that polygon
        is drawn with the newly set colors.
        For mor info see: pencolor, fillcolor

        Example (for a Turtle instance named turtle):
        >>> turtle.color('red', 'green')
        >>> turtle.color()
        ('red', 'green')
        >>> colormode(255)
        >>> color((40, 80, 120), (160, 200, 240))
        >>> color()
        ('#285078', '#a0c8f0')
        """
        if args:
            l = len(args)
            if l == 1:
                pcolor = fcolor = args[0]
            elif l == 2:
                pcolor, fcolor = args
            elif l == 3:
                pcolor = fcolor = args
            pcolor = self._colorstr(pcolor)
            fcolor = self._colorstr(fcolor)
            self.pen(pencolor=pcolor, fillcolor=fcolor)
        else:
            return self._color(self._pencolor), self._color(self._fillcolor)

    def pencolor(self, *args):
        """『0064  中文說明』
        筆色，回傳或設定筆色。

        參數:
        允許多種輸入格式。
          -  筆色()
            回傳當前筆色顏色規範字符串，
            可能為十六進制數字格式(見範例)。
            可以作為輸入到另一個顏色/ 筆色 /填色的呼叫。
          -  筆色(colorstring)
            是一個Tk顏色規範字符串，如 紅色 或 黃色。
          -  筆色((R,G,B))
            * R,G,和B,它們代表一個RGB彩色的元組*，
            並且每個R,G,B的範圍在0 .. 色模式。
            其中 色模式 是1.0或255。(可藉由 色模式() 作設定)
          -  筆色(R,G,B)
            r,g,和b表示RGB顏色，各r的,g和b的範圍是0 .. 色模式。

        如果 龜指標 形狀是多邊形，則該多邊形的輪廓繪製為新設置的筆色。

        範例(物件名為「龜」的實例):

        >>> 龜.筆色(紅色)
        >>> 某色 =(0.2,0.8,0.55)
        >>> 龜.筆色(某色)
        >>> 龜.筆色()
        '#33cc8c"


         Return or set the pencolor.

        Arguments:
        Four input formats are allowed:
          - pencolor()
            Return the current pencolor as color specification string,
            possibly in hex-number format (see example).
            May be used as input to another color/pencolor/fillcolor call.
          - pencolor(colorstring)
            s is a Tk color specification string, such as "red" or "yellow"
          - pencolor((r, g, b))
            *a tuple* of r, g, and b, which represent, an RGB color,
            and each of r, g, and b are in the range 0..colormode,
            where colormode is either 1.0 or 255
          - pencolor(r, g, b)
            r, g, and b represent an RGB color, and each of r, g, and b
            are in the range 0..colormode

        If turtleshape is a polygon, the outline of that polygon is drawn
        with the newly set pencolor.

        Example (for a Turtle instance named turtle):
        >>> turtle.pencolor('brown')
        >>> tup = (0.2, 0.8, 0.55)
        >>> turtle.pencolor(tup)
        >>> turtle.pencolor()
        '#33cc8c'
        """
        if args:
            color = self._colorstr(args)
            if color == self._pencolor:
                return
            self.pen(pencolor=color)
        else:
            return self._color(self._pencolor)

    def fillcolor(self, *args):
        """『0085  中文說明』
        填色，回傳或設定 填色。

        參數:
        允許多種輸入格式。:
          - 填色()
            回傳當前設定的填色之顏色，
            可能是十六進制數字格式(見範例)。
            可以作為輸入到另一個 顏色/ 筆色/填色 函數的呼叫。
          - 填色(colorstring)
            colorstring 是一個 Tk 顏色字串，如 紅 或 黃。
          - 填色((r,g,b))
            一個(r,g,b)顏色元組，
            其中，每個 r,g,b 值的範圍大小在 0 .. 色模式，
            其中色模式 是 1.0 或 255(可呼叫 色模式()設定)。
          - 填色(r,g,b)
            與填色((r,g,b))一樣。

        如果 龜指標 是多邊形, 該多邊形的內部顏色用新設定的顏色來填充。

        範例(物件名為「龜」的實例)：

        >>> 龜.填色(紫)
        >>> 色= 龜.筆色()
        >>> 龜.填色(色)
        >>> 龜.填色(0,0.5,0)


         Return or set the fillcolor.

        Arguments:
        Four input formats are allowed:
          - fillcolor()
            Return the current fillcolor as color specification string,
            possibly in hex-number format (see example).
            May be used as input to another color/pencolor/fillcolor call.
          - fillcolor(colorstring)
            s is a Tk color specification string, such as "red" or "yellow"
          - fillcolor((r, g, b))
            *a tuple* of r, g, and b, which represent, an RGB color,
            and each of r, g, and b are in the range 0..colormode,
            where colormode is either 1.0 or 255
          - fillcolor(r, g, b)
            r, g, and b represent an RGB color, and each of r, g, and b
            are in the range 0..colormode

        If turtleshape is a polygon, the interior of that polygon is drawn
        with the newly set fillcolor.

        Example (for a Turtle instance named turtle):
        >>> turtle.fillcolor('violet')
        >>> col = turtle.pencolor()
        >>> turtle.fillcolor(col)
        >>> turtle.fillcolor(0, .5, 0)
        """
        if args:
            color = self._colorstr(args)
            if color == self._fillcolor:
                return
            self.pen(fillcolor=color)
        else:
            return self._color(self._fillcolor)

    def showturtle(self):
        """『0052  中文說明』
        顯龜，讓 龜指標 可見。

        別名：showturtle | st | 顯龜

        沒有參數。

        範例(物件名為「龜」的實例)：

        >>> 龜.藏龜()
        >>> 龜.顯龜()


        Makes the turtle visible.

        Aliases: showturtle | st

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.hideturtle()
        >>> turtle.showturtle()
        """
        self.pen(shown=True)

    def hideturtle(self):
        """『0046  中文說明』
        藏龜，把 龜指標 隱藏起來。

        別名: 藏龜 | 藏 | hideturtle | ht

        沒有參數。

        當在畫複雜的圖時，
        把 龜指標 隱藏起來是一個好主意，
        因為可加快畫圖速度。

        範例(物件名為「龜」的實例):

        >>> 龜.藏龜()


        Makes the turtle invisible.

        Aliases: hideturtle | ht

        No argument.

        It's a good idea to do this while you're in the
        middle of a complicated drawing, because hiding
        the turtle speeds up the drawing observably.

        Example (for a Turtle instance named turtle):
        >>> turtle.hideturtle()
        """
        self.pen(shown=False)

    def isvisible(self):
        """『0034  中文說明』
        顯龜嗎，測試龜指標是否為可見狀態。傳回真假值(True/False)。

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.藏龜()
        >>>龜.顯龜嗎()
        False


        Return True if the Turtle is shown, False if it's hidden.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.hideturtle()
        >>> print turtle.isvisible():
        False
        """
        return self._shown

    def pen(self, pen=None, **pendict):
        """『0086  中文說明』
        筆，回傳或設置筆的屬性。

        參數:
            pen(筆) - 一個 Python 字典 資料型態，記錄著下面列出的一些關鍵字。
            **筆字典  - 一個或多個 關鍵字(=參數) 的參數。記錄著下面列出的一些關鍵字。

        回傳或設置畫筆的屬性，在"筆字典"裡。
        用下面的 關鍵字/值 配對:
           "shown"      :   True/False(真/假)
           "pendown"    :   True/False(真/假)
           "pencolor"   :   顏色字串 or 顏色參數(三個數字)
           "fillcolor"  :   顏色字串 or 顏色參數(三個數字)
           "pensize"    :   正數
           "speed"      :   範圍在1~10的數字
           "resizemode" :   "auto" or "user" or "noresize"
           "stretchfactor": (正數, 正數)
           "shearfactor":   數字
           "outline"    :   正數
           "tilt"       :   數字

        這本詞典可以作為參數進行筆()的調用來恢復舊的筆狀態。
        而且可利用這些屬性當作關鍵字參數來進行設置。
        這可以用來在一個語句中設置筆的多個屬性。


        範例(物件名為「龜」的實例):

        >>> 龜.筆(填色="black", pencolor="red", pensize=10)
        >>> 龜.筆()
        {'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,
        'pencolor': 'red', 'pendown': True, 'fillcolor': 'black',
        'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}
        >>> 筆初始=龜.筆()
        >>> 龜.顏色("yellow","")
        >>> 龜.提筆()
        >>> 龜.筆()
        {'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,
        'pencolor': 'yellow', 'pendown': False, 'fillcolor': '',
        'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}
        >>> p.筆(筆初始, fillcolor="green")
        >>> p.筆()
        {'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,
        'pencolor': 'red', 'pendown': True, 'fillcolor': 'green',
        'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}


        Return or set the pen's attributes.

        Arguments:
            pen -- a dictionary with some or all of the below listed keys.
            **pendict -- one or more keyword-arguments with the below
                         listed keys as keywords.

        Return or set the pen's attributes in a 'pen-dictionary'
        with the following key/value pairs:
           "shown"      :   True/False
           "pendown"    :   True/False
           "pencolor"   :   color-string or color-tuple
           "fillcolor"  :   color-string or color-tuple
           "pensize"    :   positive number
           "speed"      :   number in range 0..10
           "resizemode" :   "auto" or "user" or "noresize"
           "stretchfactor": (positive number, positive number)
           "shearfactor":   number
           "outline"    :   positive number
           "tilt"       :   number

        This dictionary can be used as argument for a subsequent
        pen()-call to restore the former pen-state. Moreover one
        or more of these attributes can be provided as keyword-arguments.
        This can be used to set several pen attributes in one statement.


        Examples (for a Turtle instance named turtle):
        >>> turtle.pen(fillcolor="black", pencolor="red", pensize=10)
        >>> turtle.pen()
        {'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,
        'pencolor': 'red', 'pendown': True, 'fillcolor': 'black',
        'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}
        >>> penstate=turtle.pen()
        >>> turtle.color("yellow","")
        >>> turtle.penup()
        >>> turtle.pen()
        {'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,
        'pencolor': 'yellow', 'pendown': False, 'fillcolor': '',
        'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}
        >>> p.pen(penstate, fillcolor="green")
        >>> p.pen()
        {'pensize': 10, 'shown': True, 'resizemode': 'auto', 'outline': 1,
        'pencolor': 'red', 'pendown': True, 'fillcolor': 'green',
        'stretchfactor': (1,1), 'speed': 3, 'shearfactor': 0.0}
        """
        _pd =  {"shown"         : self._shown,
                "pendown"       : self._drawing,
                "pencolor"      : self._pencolor,
                "fillcolor"     : self._fillcolor,
                "pensize"       : self._pensize,
                "speed"         : self._speed,
                "resizemode"    : self._resizemode,
                "stretchfactor" : self._stretchfactor,
                "shearfactor"   : self._shearfactor,
                "outline"       : self._outlinewidth,
                "tilt"          : self._tilt
               }

        if not (pen or pendict):
            return _pd

        if isinstance(pen, dict):
            p = pen
        else:
            p = {}
        p.update(pendict)

        _p_buf = {}
        for key in p:
            _p_buf[key] = _pd[key]

        if self.undobuffer:
            self.undobuffer.push(("pen", _p_buf))

        newLine = False
        if "pendown" in p:
            if self._drawing != p["pendown"]:
                newLine = True
        if "pencolor" in p:
            if isinstance(p["pencolor"], tuple):
                p["pencolor"] = self._colorstr((p["pencolor"],))
            if self._pencolor != p["pencolor"]:
                newLine = True
        if "pensize" in p:
            if self._pensize != p["pensize"]:
                newLine = True
        if newLine:
            self._newLine()
        if "pendown" in p:
            self._drawing = p["pendown"]
        if "pencolor" in p:
            self._pencolor = p["pencolor"]
        if "pensize" in p:
            self._pensize = p["pensize"]
        if "fillcolor" in p:
            if isinstance(p["fillcolor"], tuple):
                p["fillcolor"] = self._colorstr((p["fillcolor"],))
            self._fillcolor = p["fillcolor"]
        if "speed" in p:
            self._speed = p["speed"]
        if "resizemode" in p:
            self._resizemode = p["resizemode"]
        if "stretchfactor" in p:
            sf = p["stretchfactor"]
            if isinstance(sf, (int, float)):
                sf = (sf, sf)
            self._stretchfactor = sf
        if "shearfactor" in p:
            self._shearfactor = p["shearfactor"]
        if "outline" in p:
            self._outlinewidth = p["outline"]
        if "shown" in p:
            self._shown = p["shown"]
        if "tilt" in p:
            self._tilt = p["tilt"]
        if "stretchfactor" in p or "tilt" in p or "shearfactor" in p:
            scx, scy = self._stretchfactor
            shf = self._shearfactor
            sa, ca = math.sin(self._tilt), math.cos(self._tilt)
            self._shapetrafo = ( scx*ca, scy*(shf*ca + sa),
                                -scx*sa, scy*(ca - shf*sa))
        self._update()

## three dummy methods to be implemented by child class:

    def _newLine(self, usePos = True):
        """dummy method - to be overwritten by child class"""
    def _update(self, count=True, forced=False):
        """dummy method - to be overwritten by child class"""
    def _color(self, args):
        """dummy method - to be overwritten by child class"""
    def _colorstr(self, args):
        """dummy method - to be overwritten by child class"""

    width = pensize
    up = penup
    pu = penup
    pd = pendown
    down = pendown
    st = showturtle
    ht = hideturtle
    筆粗= pensize
    筆粗細= pensize
    筆大小= pensize
    筆寬= width
    寬= width
    提筆= penup
    下筆= pendown
    顯龜= showturtle
    顯示= showturtle
    顯= showturtle
    藏龜= hideturtle
    隱藏= hideturtle
    藏= hideturtle
    顏色= color
    筆色= pencolor
    速度= speed
    筆= pen
    筆屬性= pen
    填色= fillcolor
    下筆嗎= isdown
    是否下筆= isdown
    下筆狀態= isdown
    顯龜嗎= isvisible
    是否可見= isvisible
    可見狀態= isvisible
    下筆= pendown
    填色= fillcolor
    提筆= penup
    重設大小模式= resizemode
    設成可伸縮模式= resizemode
    提筆= up
    提筆= pu
    下筆= pd
    下筆= down
    顯龜= st
    顯示= st
    顯= st
    藏龜= ht
    隱藏= ht
    藏= ht
龜筆類= TPen
烏龜畫筆類= TPen
class RawTurtle(TPen, TNavigator):
    """Animation part of the RawTurtle.
    Puts RawTurtle upon a TurtleScreen and provides tools for
    its animation.
    """
    screens = []

    def __init__(self, canvas=None,
                 shape=_CFG["shape"],
                 undobuffersize=_CFG["undobuffersize"],
                 visible=_CFG["visible"]):
        if isinstance(canvas, _Screen):
            self.screen = canvas
        elif isinstance(canvas, TurtleScreen):
            if canvas not in RawTurtle.screens:
                RawTurtle.screens.append(canvas)
            self.screen = canvas
        elif isinstance(canvas, (ScrolledCanvas, Canvas)):
            for screen in RawTurtle.screens:
                if screen.cv == canvas:
                    self.screen = screen
                    break
            else:
                self.screen = TurtleScreen(canvas)
                RawTurtle.screens.append(self.screen)
        else:
            raise TurtleGraphicsError("bad canvas argument %s" % canvas)

        screen = self.screen
        TNavigator.__init__(self, screen.mode())
        TPen.__init__(self)
        screen._turtles.append(self)
        self.drawingLineItem = screen._createline()
        self.turtle = _TurtleImage(screen, shape)
        self._poly = None
        self._creatingPoly = False
        self._fillitem = self._fillpath = None
        self._shown = visible
        self._hidden_from_screen = False
        self.currentLineItem = screen._createline()
        self.currentLine = [self._position]
        self.items = [self.currentLineItem]
        self.stampItems = []
        self._undobuffersize = undobuffersize
        self.undobuffer = Tbuffer(undobuffersize)
        self._update()

    def reset(self):
        """『0040  中文說明』
        重設，刪除龜指標的圖和恢復其預設值。

        沒有參數。

        從螢幕中刪除 龜類 的移動軌跡，並重置 龜類。
        將其設定設為初始值(預設值)。

        範例(物件名為「龜」的實例)：

        >>> 龜.位置()
        (0.00,-22.00)
        >>> 龜.頭向()
        100.0
        >>> 龜.重設()
        >>> 龜.位置()
        (0.00,0.00)
        >>> 龜.頭向()
        0.0


        Delete the turtle's drawings and restore its default values.

        No argument.

        Delete the turtle's drawings from the screen, re-center the turtle
        and set variables to the default values.

        Example (for a Turtle instance named turtle):
        >>> turtle.position()
        (0.00,-22.00)
        >>> turtle.heading()
        100.0
        >>> turtle.reset()
        >>> turtle.position()
        (0.00,0.00)
        >>> turtle.heading()
        0.0
        """
        TNavigator.reset(self)
        TPen._reset(self)
        self._clear()
        self._drawturtle()
        self._update()

    def setundobuffer(self, size):
        """『0031  中文說明』
        設回復暫存區，設置或禁用回復暫存區。

        參數:
        size - 一個整數 或 無

        如果 size 是整數，則給予安裝指定大小的空白回復暫存區。
        size 決定 龜指標 使用 回復()函數的行動可撤消最大數目量。
        
        如果設定是 無，則不存在回復暫存區。

        範例(物件名為「龜」的實例)：

        >>> 龜.設回復暫存區(42)


        Set or disable undobuffer.

        Argument:
        size -- an integer or None

        If size is an integer an empty undobuffer of given size is installed.
        Size gives the maximum number of turtle-actions that can be undone
        by the undo() function.
        If size is None, no undobuffer is present.

        Example (for a Turtle instance named turtle):
        >>> turtle.setundobuffer(42)
        """
        if size is None or size <= 0:
            self.undobuffer = None
        else:
            self.undobuffer = Tbuffer(size)

    def undobufferentries(self):
        """『0061  中文說明』
        回復暫存區的個數，回傳目前回復暫存區內可撤消動作的數量。

        沒有參數。

        範例(物件名為「龜」的實例)：

        >>>while  回復暫存區的個數():
        ...     回復()


        Return count of entries in the undobuffer.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> while undobufferentries():
        ...     undo()
        """
        if self.undobuffer is None:
            return 0
        return self.undobuffer.nr_of_items()

    def _clear(self):
        """Delete all of pen's drawings"""
        self._fillitem = self._fillpath = None
        for item in self.items:
            self.screen._delete(item)
        self.currentLineItem = self.screen._createline()
        self.currentLine = []
        if self._drawing:
            self.currentLine.append(self._position)
        self.items = [self.currentLineItem]
        self.clearstamps()
        self.setundobuffer(self._undobuffersize)


    def clear(self):
        """『0060  中文說明』
        清除，清除 龜指標 在螢幕上所畫的圖，龜指標 不會移動。

        沒有參數。

        從螢幕中刪除指定的龜所畫的圖。
        龜指標 的位置和狀態以及其他 龜類 的圖，不會受到影響
        

        範例(物件名為「龜」的實例):

        >>> 龜.清除()


        Delete the turtle's drawings from the screen. Do not move turtle.

        No arguments.

        Delete the turtle's drawings from the screen. Do not move turtle.
        State and position of the turtle as well as drawings of other
        turtles are not affected.

        Examples (for a Turtle instance named turtle):
        >>> turtle.clear()
        """
        self._clear()
        self._update()

    def _update_data(self):
        self.screen._incrementudc()
        if self.screen._updatecounter != 0:
            return
        if len(self.currentLine)>1:
            self.screen._drawline(self.currentLineItem, self.currentLine,
                                  self._pencolor, self._pensize)

    def _update(self):
        """Perform a Turtle-data update.
        """
        screen = self.screen
        if screen._tracing == 0:
            return
        elif screen._tracing == 1:
            self._update_data()
            self._drawturtle()
            screen._update()                  # TurtleScreenBase
            screen._delay(screen._delayvalue) # TurtleScreenBase
        else:
            self._update_data()
            if screen._updatecounter == 0:
                for t in screen.turtles():
                    t._drawturtle()
                screen._update()

    def _tracer(self, flag=None, delay=None):
        """Turns turtle animation on/off and set delay for update drawings.

        Optional arguments:
        n -- nonnegative  integer
        delay -- nonnegative  integer

        If n is given, only each n-th regular screen update is really performed.
        (Can be used to accelerate the drawing of complex graphics.)
        Second arguments sets delay value (see RawTurtle.delay())

        Example (for a Turtle instance named turtle):
        >>> turtle.tracer(8, 25)
        >>> dist = 2
        >>> for i in range(200):
        ...     turtle.fd(dist)
        ...     turtle.rt(90)
        ...     dist += 2
        """
        return self.screen.tracer(flag, delay)

    def _color(self, args):
        return self.screen._color(args)

    def _colorstr(self, args):
        return self.screen._colorstr(args)

    def _cc(self, args):
        """Convert colortriples to hexstrings.
        """
        if isinstance(args, str):
            return args
        try:
            r, g, b = args
        except:
            raise TurtleGraphicsError("bad color arguments: %s" % str(args))
        if self.screen._colormode == 1.0:
            r, g, b = [round(255.0*x) for x in (r, g, b)]
        if not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255)):
            raise TurtleGraphicsError("bad color sequence: %s" % str(args))
        return "#%02x%02x%02x" % (r, g, b)

    def clone(self):
        """『0000  中文說明』
        複製，複製產生另一隻 龜類。

        沒有參數。

        創建並回傳龜的複製品，
        與原本的龜具有相同位置、方向和設定。

        範例(物件名為「米克龜」的實例):

        米克龜= 龜類()
        喬伊龜= 米克龜.複製()


        Create and return a clone of the turtle.

        No argument.

        Create and return a clone of the turtle with same position, heading
        and turtle properties.

        Example (for a Turtle instance named mick):
        mick = Turtle()
        joe = mick.clone()
        """
        screen = self.screen
        self._newLine(self._drawing)

        turtle = self.turtle
        self.screen = None
        self.turtle = None  # too make self deepcopy-able

        q = deepcopy(self)

        self.screen = screen
        self.turtle = turtle

        q.screen = screen
        q.turtle = _TurtleImage(screen, self.turtle.shapeIndex)

        screen._turtles.append(q)
        ttype = screen._shapes[self.turtle.shapeIndex]._type
        if ttype == "polygon":
            q.turtle._item = screen._createpoly()
        elif ttype == "image":
            q.turtle._item = screen._createimage(screen._shapes["blank"]._data)
        elif ttype == "compound":
            q.turtle._item = [screen._createpoly() for item in
                              screen._shapes[self.turtle.shapeIndex]._data]
        q.currentLineItem = screen._createline()
        q._update()
        return q

    def shape(self, name=None):
        """『0055  中文說明』
        形狀，根據指定形狀名稱設置龜形狀，或回傳當前形狀名稱。

        可選參數:
        name  - 一個字符串,它是一個有效的形狀名稱
        
        根據name設置 龜指標 的形狀。
        無傳入參數，即可用來查詢目前設定。
        name必須存在於 龜幕類 的形狀字典裡。
        目前有下列多邊形形狀：
        'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'.
        要了解如何處理形狀，可參看 龜幕類 中的函數 登記形狀()。

        範例(物件名為「龜」的實例)：

        >>> 龜.形狀()
        'arrow'
        >>> 龜.形狀('turtle')
        >>> 龜.形狀()
        'turtle'


        Set turtle shape to shape with given name / return current shapename.

        Optional argument:
        name -- a string, which is a valid shapename

        Set turtle shape to shape with given name or, if name is not given,
        return name of current shape.
        Shape with name must exist in the TurtleScreen's shape dictionary.
        Initially there are the following polygon shapes:
        'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'.
        To learn about how to deal with shapes see Screen-method register_shape.

        Example (for a Turtle instance named turtle):
        >>> turtle.shape()
        'arrow'
        >>> turtle.shape("turtle")
        >>> turtle.shape()
        'turtle'
        """
        if name is None:
            return self.turtle.shapeIndex
        if not name in self.screen.getshapes():
            raise TurtleGraphicsError("There is no shape named %s" % name)
        self.turtle._setshape(name)
        self._update()

    def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
        """『0017  中文說明』
        形狀大小，設置或回傳龜的 展延因子和輪廓。並設置 重設大小模式 為"user"。

        可選參數:
           stretch_wid - 正數
           stretch_len - 正數
           outline - 正數

        設置  龜指標 的展延因子跟輪廓粗細。並設置 重設大小模式() 為"user"。
        無傳入參數，即可用來查詢目前設定。
        當 重設大小模式() 被設置為" user "， 
        龜指標 將根據其展延因子的拉伸被顯示：
        stretch_wid是展延因子的垂直方向。
        stretch_len是展延因子在 龜指標 的定向方向。
        outline為形狀輪廓線的寬度。

        範例(物件名為「龜」的實例)：

        >>> 龜.重設大小模式("user")
        >>> 龜.形狀大小(5,5,12)
        >>> 龜.形狀大小(outline=8)


        Set/return turtle's stretchfactors/outline. Set resizemode to "user".

        Optional arguments:
           stretch_wid : positive number
           stretch_len : positive number
           outline  : positive number

        Return or set the pen's attributes x/y-stretchfactors and/or outline.
        Set resizemode to "user".
        If and only if resizemode is set to "user", the turtle will be displayed
        stretched according to its stretchfactors:
        stretch_wid is stretchfactor perpendicular to orientation
        stretch_len is stretchfactor in direction of turtles orientation.
        outline determines the width of the shapes's outline.

        Examples (for a Turtle instance named turtle):
        >>> turtle.resizemode("user")
        >>> turtle.shapesize(5, 5, 12)
        >>> turtle.shapesize(outline=8)
        """
        if stretch_wid is stretch_len is outline is None:
            stretch_wid, stretch_len = self._stretchfactor
            return stretch_wid, stretch_len, self._outlinewidth
        if stretch_wid == 0 or stretch_len == 0:
            raise TurtleGraphicsError("stretch_wid/stretch_len must not be zero")
        if stretch_wid is not None:
            if stretch_len is None:
                stretchfactor = stretch_wid, stretch_wid
            else:
                stretchfactor = stretch_wid, stretch_len
        elif stretch_len is not None:
            stretchfactor = self._stretchfactor[0], stretch_len
        else:
            stretchfactor = self._stretchfactor
        if outline is None:
            outline = self._outlinewidth
        self.pen(resizemode="user",
                 stretchfactor=stretchfactor, outline=outline)

    def shearfactor(self, shear=None):
        """『0025  中文說明』
        扭曲因子，設置或回傳當前扭曲因子。

        可選參數：
        shear - 數字

        根據給定的 shear 扭曲因子剪切龜指標形狀，
        這是扭曲因子的正切值。
        不會更改 龜指標 的頭向(運動方向)。
        如果 shear 沒有被給定，則回傳當前剪切因子設定，
        即扭曲因子的正切值，通過該線平行於 龜指標方向被扭曲。

        範例(物件名為「龜」的實例)：

        >>> 龜.形狀("circle")
        >>> 龜.形狀大小(5,2)
        >>> 龜.扭曲因子(0.5)
        >>> 龜.扭曲因子()
        >>> 0.5


        Set or return the current shearfactor.

        Optional argument: shear -- number, tangent of the shear angle

        Shear the turtleshape according to the given shearfactor shear,
        which is the tangent of the shear angle. DO NOT change the
        turtle's heading (direction of movement).
        If shear is not given: return the current shearfactor, i. e. the
        tangent of the shear angle, by which lines parallel to the
        heading of the turtle are sheared.

        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("circle")
        >>> turtle.shapesize(5,2)
        >>> turtle.shearfactor(0.5)
        >>> turtle.shearfactor()
        >>> 0.5
        """
        if shear is None:
            return self._shearfactor
        self.pen(resizemode="user", shearfactor=shear)

    def settiltangle(self, angle):
        """『0076  中文說明』
        設傾角，旋轉 龜指標 到指定的方向。

        參數:
        angle - 數字
        旋轉 龜指標形狀 到所指定的方向。
        不會更改 龜指標 的頭向(運動方向)。


        範例(物件名為「龜」的實例)：

        >>> 龜.形狀("turtle")
        >>> 龜.形狀大小(5,2)
        >>> 龜.設傾角(45)
        >>> 蓋章()
        >>> 龜.前進(50)
        >>> 龜.設傾角(-45)
        >>> 蓋章()
        >>> 龜.前進(50)


        Rotate the turtleshape to point in the specified direction

        Argument: angle -- number

        Rotate the turtleshape to point in the direction specified by angle,
        regardless of its current tilt-angle. DO NOT change the turtle's
        heading (direction of movement).


        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("circle")
        >>> turtle.shapesize(5,2)
        >>> turtle.settiltangle(45)
        >>> stamp()
        >>> turtle.fd(50)
        >>> turtle.settiltangle(-45)
        >>> stamp()
        >>> turtle.fd(50)
        """
        tilt = -angle * self._degreesPerAU * self._angleOrient
        tilt = (tilt * math.pi / 180.0) % (2*math.pi)
        self.pen(resizemode="user", tilt=tilt)

    def tiltangle(self, angle=None):
        """『0075  中文說明』
        傾斜角度，設置或回傳當前的傾斜角度。

        可選參數：
        angle - 數字

        旋轉龜指標形狀傾斜角度到所指定的方向，
        不管其目前的傾斜角度，
        不會更改 龜指標 的頭向(運動方向)。
        如果沒有給予參數，回傳當前的傾斜角度，
        即與該龜指標形狀的頭向方位角度差。
        

        Python 3.1 不贊成使用

        範例(物件名為「龜」的實例)：

        >>> 龜.形狀("圓")
        >>> 龜.形狀大小(5,2)
        >>> 龜.傾斜(45)
        >>> 龜.傾斜角度()


        Set or return the current tilt-angle.

        Optional argument: angle -- number

        Rotate the turtleshape to point in the direction specified by angle,
        regardless of its current tilt-angle. DO NOT change the turtle's
        heading (direction of movement).
        If angle is not given: return the current tilt-angle, i. e. the angle
        between the orientation of the turtleshape and the heading of the
        turtle (its direction of movement).

        Deprecated since Python 3.1

        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("circle")
        >>> turtle.shapesize(5,2)
        >>> turtle.tilt(45)
        >>> turtle.tiltangle()
        """
        if angle is None:
            tilt = -self._tilt * (180.0/math.pi) * self._angleOrient
            return (tilt / self._degreesPerAU) % self._fullcircle
        else:
            self.settiltangle(angle)

    def tilt(self, angle):
        """『0042  中文說明』
        傾斜，根據指定角度傾斜龜指標形狀。

        參數:
        angle - 一個數字

        將龜指標形狀目前角度再旋轉指定角度，
        不會更改 龜指標 的頭向(運動方向)。

        範例(物件名為「龜」的實例)：

        >>> 龜.形狀(""circle"")
        >>> 龜.形狀大小(5,2)
        >>> 龜.傾斜(30)
        >>> 龜.前進(50)
        >>> 龜.傾斜(30)
        >>> 龜.前進(50)


        Rotate the turtleshape by angle.

        Argument:
        angle - a number

        Rotate the turtleshape by angle from its current tilt-angle,
        but do NOT change the turtle's heading (direction of movement).

        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("circle")
        >>> turtle.shapesize(5,2)
        >>> turtle.tilt(30)
        >>> turtle.fd(50)
        >>> turtle.tilt(30)
        >>> turtle.fd(50)
        """
        self.settiltangle(angle + self.tiltangle())

    def shapetransform(self, t11=None, t12=None, t21=None, t22=None):
        """『0071  中文說明』
        形狀轉換，設置或回傳龜指標形狀的當前變換矩陣。

        可選參數：
		t11, t12, t21, t22 -  數字。

        如果沒有給定矩陣元素，則回傳當前變換矩陣。
        否則根據給定的矩陣元素第一行T11,T12和第二行T21,22，
		變換龜指標形狀。
        根據給定的矩陣修改 展延因子、扭曲因子和傾斜角度。

        範例(物件名為「龜」的實例)：

        >>> 龜.形狀("square")
        >>> 龜.形狀大小(4,2)
        >>> 龜.扭曲因子(-0.5)
        >>> 龜.形狀轉換()
        (4.0,-1.0,-0.0,2.0)


        Set or return the current transformation matrix of the turtle shape.

        Optional arguments: t11, t12, t21, t22 -- numbers.

        If none of the matrix elements are given, return the transformation
        matrix.
        Otherwise set the given elements and transform the turtleshape
        according to the matrix consisting of first row t11, t12 and
        second row t21, 22.
        Modify stretchfactor, shearfactor and tiltangle according to the
        given matrix.

        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("square")
        >>> turtle.shapesize(4,2)
        >>> turtle.shearfactor(-0.5)
        >>> turtle.shapetransform()
        (4.0, -1.0, -0.0, 2.0)
        """
        if t11 is t12 is t21 is t22 is None:
            return self._shapetrafo
        m11, m12, m21, m22 = self._shapetrafo
        if t11 is not None: m11 = t11
        if t12 is not None: m12 = t12
        if t21 is not None: m21 = t21
        if t22 is not None: m22 = t22
        if t11 * t22 - t12 * t21 == 0:
            raise TurtleGraphicsError("Bad shape transform matrix: must not be singular")
        self._shapetrafo = (m11, m12, m21, m22)
        alfa = math.atan2(-m21, m11) % (2 * math.pi)
        sa, ca = math.sin(alfa), math.cos(alfa)
        a11, a12, a21, a22 = (ca*m11 - sa*m21, ca*m12 - sa*m22,
                              sa*m11 + ca*m21, sa*m12 + ca*m22)
        self._stretchfactor = a11, a22
        self._shearfactor = a12/a22
        self._tilt = alfa
        self.pen(resizemode="user")


    def _polytrafo(self, poly):
        """Computes transformed polygon shapes from a shape
        according to current position and heading.
        """
        screen = self.screen
        p0, p1 = self._position
        e0, e1 = self._orient
        e = Vec2D(e0, e1 * screen.yscale / screen.xscale)
        e0, e1 = (1.0 / abs(e)) * e
        return [(p0+(e1*x+e0*y)/screen.xscale, p1+(-e0*x+e1*y)/screen.yscale)
                                                           for (x, y) in poly]

    def get_shapepoly(self):
        """『0003  中文說明』
        取形狀多邊形，回傳當前 多邊形 形狀 的 座標 元組。

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.形狀("正方形")
        >>> 龜.形狀轉換(4,-1,0,2)
        >>> 龜.取形狀多邊形()
        ((50,-20),(30,20),(-50,20),(-30,-20))



        Return the current shape polygon as tuple of coordinate pairs.

        No argument.

        Examples (for a Turtle instance named turtle):
        >>> turtle.shape("square")
        >>> turtle.shapetransform(4, -1, 0, 2)
        >>> turtle.get_shapepoly()
        ((50, -20), (30, 20), (-50, 20), (-30, -20))

        """
        shape = self.screen._shapes[self.turtle.shapeIndex]
        if shape._type == "polygon":
            return self._getshapepoly(shape._data, shape._type == "compound")
        # else return None

    def _getshapepoly(self, polygon, compound=False):
        """Calculate transformed shape polygon according to resizemode
        and shapetransform.
        """
        if self._resizemode == "user" or compound:
            t11, t12, t21, t22 = self._shapetrafo
        elif self._resizemode == "auto":
            l = max(1, self._pensize/5.0)
            t11, t12, t21, t22 = l, 0, 0, l
        elif self._resizemode == "noresize":
            return polygon
        return tuple([(t11*x + t12*y, t21*x + t22*y) for (x, y) in polygon])

    def _drawturtle(self):
        """Manages the correct rendering of the turtle with respect to
        its shape, resizemode, stretch and tilt etc."""
        screen = self.screen
        shape = screen._shapes[self.turtle.shapeIndex]
        ttype = shape._type
        titem = self.turtle._item
        if self._shown and screen._updatecounter == 0 and screen._tracing > 0:
            self._hidden_from_screen = False
            tshape = shape._data
            if ttype == "polygon":
                if self._resizemode == "noresize": w = 1
                elif self._resizemode == "auto": w = self._pensize
                else: w =self._outlinewidth
                shape = self._polytrafo(self._getshapepoly(tshape))
                fc, oc = self._fillcolor, self._pencolor
                screen._drawpoly(titem, shape, fill=fc, outline=oc,
                                                      width=w, top=True)
            elif ttype == "image":
                screen._drawimage(titem, self._position, tshape)
            elif ttype == "compound":
                for item, (poly, fc, oc) in zip(titem, tshape):
                    poly = self._polytrafo(self._getshapepoly(poly, True))
                    screen._drawpoly(item, poly, fill=self._cc(fc),
                                     outline=self._cc(oc), width=self._outlinewidth, top=True)
        else:
            if self._hidden_from_screen:
                return
            if ttype == "polygon":
                screen._drawpoly(titem, ((0, 0), (0, 0), (0, 0)), "", "")
            elif ttype == "image":
                screen._drawimage(titem, self._position,
                                          screen._shapes["blank"]._data)
            elif ttype == "compound":
                for item in titem:
                    screen._drawpoly(item, ((0, 0), (0, 0), (0, 0)), "", "")
            self._hidden_from_screen = True

##############################  stamp stuff  ###############################

    def stamp(self):
        """『0074  中文說明』
        蓋章，將 龜指標 的形狀拓印到畫布上，並回傳其 id 編號。

        沒有參數。

        將 龜指標 的形狀根據當前位置拓印到畫布上，
        並回傳蓋章id編號。
        可藉由其id編號使用 清除蓋章()，消除其印在畫布上的拓本。

        範例(物件名為「龜」的實例)：

        >>> 龜.顏色("藍")
        >>> 龜.蓋章()
        13
        >>> 龜.前進(50)


        Stamp a copy of the turtleshape onto the canvas and return its id.

        No argument.

        Stamp a copy of the turtle shape onto the canvas at the current
        turtle position. Return a stamp_id for that stamp, which can be
        used to delete it by calling clearstamp(stamp_id).

        Example (for a Turtle instance named turtle):
        >>> turtle.color("blue")
        >>> turtle.stamp()
        13
        >>> turtle.fd(50)
        """
        screen = self.screen
        shape = screen._shapes[self.turtle.shapeIndex]
        ttype = shape._type
        tshape = shape._data
        if ttype == "polygon":
            stitem = screen._createpoly()
            if self._resizemode == "noresize": w = 1
            elif self._resizemode == "auto": w = self._pensize
            else: w =self._outlinewidth
            shape = self._polytrafo(self._getshapepoly(tshape))
            fc, oc = self._fillcolor, self._pencolor
            screen._drawpoly(stitem, shape, fill=fc, outline=oc,
                                                  width=w, top=True)
        elif ttype == "image":
            stitem = screen._createimage("")
            screen._drawimage(stitem, self._position, tshape)
        elif ttype == "compound":
            stitem = []
            for element in tshape:
                item = screen._createpoly()
                stitem.append(item)
            stitem = tuple(stitem)
            for item, (poly, fc, oc) in zip(stitem, tshape):
                poly = self._polytrafo(self._getshapepoly(poly, True))
                screen._drawpoly(item, poly, fill=self._cc(fc),
                                 outline=self._cc(oc), width=self._outlinewidth, top=True)
        self.stampItems.append(stitem)
        self.undobuffer.push(("stamp", stitem))
        return stitem

    def _clearstamp(self, stampid):
        """does the work for clearstamp() and clearstamps()
        """
        if stampid in self.stampItems:
            if isinstance(stampid, tuple):
                for subitem in stampid:
                    self.screen._delete(subitem)
            else:
                self.screen._delete(stampid)
            self.stampItems.remove(stampid)
        # Delete stampitem from undobuffer if necessary
        # if clearstamp is called directly.
        item = ("stamp", stampid)
        buf = self.undobuffer
        if item not in buf.buffer:
            return
        index = buf.buffer.index(item)
        buf.buffer.remove(item)
        if index <= buf.ptr:
            buf.ptr = (buf.ptr - 1) % buf.bufsize
        buf.buffer.insert((buf.ptr+1)%buf.bufsize, [None])

    def clearstamp(self, stampid):
        """『0014  中文說明』
        清除蓋章，根據指定的編號清除曾經的蓋章

        參數:
        stampid  - 一個整數，必須是曾經回傳的蓋章的編號。

        範例(物件名為「龜」的實例):

        >>> 龜.顏色(藍)
        >>> 章= 龜.蓋章()
        >>> 龜.前進(50)
        >>> 龜.清除蓋章(章)


        Delete stamp with given stampid

        Argument:
        stampid - an integer, must be return value of previous stamp() call.

        Example (for a Turtle instance named turtle):
        >>> turtle.color("blue")
        >>> astamp = turtle.stamp()
        >>> turtle.fd(50)
        >>> turtle.clearstamp(astamp)
        """
        self._clearstamp(stampid)
        self._update()

    def clearstamps(self, n=None):
        """『0030  中文說明』
        清除蓋章群，清除所有或前後 n 個 龜的蓋章。

        可選參數:
        n - 一個整數

        如果 n 數字不存在，則清除全部蓋章。
        如果 n > 0 ，清除前n個。
        如果 n < 0 ，清除後n個。

        範例(物件名為「龜」的實例):

        >>>for i in 範圍(8):
        ... 龜.蓋章(); 龜.前進(30)
        ...
        >>> 龜.清除蓋章群(2)
        >>> 龜.清除蓋章群(-2)
        >>> 龜.清除蓋章群()


        Delete all or first/last n of turtle's stamps.

        Optional argument:
        n -- an integer

        If n is None, delete all of pen's stamps,
        else if n > 0 delete first n stamps
        else if n < 0 delete last n stamps.

        Example (for a Turtle instance named turtle):
        >>> for i in range(8):
        ...     turtle.stamp(); turtle.fd(30)
        ...
        >>> turtle.clearstamps(2)
        >>> turtle.clearstamps(-2)
        >>> turtle.clearstamps()
        """
        if n is None:
            toDelete = self.stampItems[:]
        elif n >= 0:
            toDelete = self.stampItems[:n]
        else:
            toDelete = self.stampItems[n:]
        for item in toDelete:
            self._clearstamp(item)
        self._update()

    def _goto(self, end):
        """Move the pen to the point end, thereby drawing a line
        if pen is down. All other methods for turtle movement depend
        on this one.
        """
        ## Version with undo-stuff
        go_modes = ( self._drawing,
                     self._pencolor,
                     self._pensize,
                     isinstance(self._fillpath, list))
        screen = self.screen
        undo_entry = ("go", self._position, end, go_modes,
                      (self.currentLineItem,
                      self.currentLine[:],
                      screen._pointlist(self.currentLineItem),
                      self.items[:])
                      )
        if self.undobuffer:
            self.undobuffer.push(undo_entry)
        start = self._position
        if self._speed and screen._tracing == 1:
            diff = (end-start)
            diffsq = (diff[0]*screen.xscale)**2 + (diff[1]*screen.yscale)**2
            nhops = 1+int((diffsq**0.5)/(3*(1.1**self._speed)*self._speed))
            delta = diff * (1.0/nhops)
            for n in range(1, nhops):
                if n == 1:
                    top = True
                else:
                    top = False
                self._position = start + delta * n
                if self._drawing:
                    screen._drawline(self.drawingLineItem,
                                     (start, self._position),
                                     self._pencolor, self._pensize, top)
                self._update()
            if self._drawing:
                screen._drawline(self.drawingLineItem, ((0, 0), (0, 0)),
                                               fill="", width=self._pensize)
        # Turtle now at end,
        if self._drawing: # now update currentLine
            self.currentLine.append(end)
        if isinstance(self._fillpath, list):
            self._fillpath.append(end)
        ######    vererbung!!!!!!!!!!!!!!!!!!!!!!
        self._position = end
        if self._creatingPoly:
            self._poly.append(end)
        if len(self.currentLine) > 42: # 42! answer to the ultimate question
                                       # of life, the universe and everything
            self._newLine()
        self._update() #count=True)

    def _undogoto(self, entry):
        """Reverse a _goto. Used for undo()
        """
        old, new, go_modes, coodata = entry
        drawing, pc, ps, filling = go_modes
        cLI, cL, pl, items = coodata
        screen = self.screen
        if abs(self._position - new) > 0.5:
            print ("undogoto: HALLO-DA-STIMMT-WAS-NICHT!")
        # restore former situation
        self.currentLineItem = cLI
        self.currentLine = cL

        if pl == [(0, 0), (0, 0)]:
            usepc = ""
        else:
            usepc = pc
        screen._drawline(cLI, pl, fill=usepc, width=ps)

        todelete = [i for i in self.items if (i not in items) and
                                       (screen._type(i) == "line")]
        for i in todelete:
            screen._delete(i)
            self.items.remove(i)

        start = old
        if self._speed and screen._tracing == 1:
            diff = old - new
            diffsq = (diff[0]*screen.xscale)**2 + (diff[1]*screen.yscale)**2
            nhops = 1+int((diffsq**0.5)/(3*(1.1**self._speed)*self._speed))
            delta = diff * (1.0/nhops)
            for n in range(1, nhops):
                if n == 1:
                    top = True
                else:
                    top = False
                self._position = new + delta * n
                if drawing:
                    screen._drawline(self.drawingLineItem,
                                     (start, self._position),
                                     pc, ps, top)
                self._update()
            if drawing:
                screen._drawline(self.drawingLineItem, ((0, 0), (0, 0)),
                                               fill="", width=ps)
        # Turtle now at position old,
        self._position = old
        ##  if undo is done during creating a polygon, the last vertex
        ##  will be deleted. if the polygon is entirely deleted,
        ##  creatingPoly will be set to False.
        ##  Polygons created before the last one will not be affected by undo()
        if self._creatingPoly:
            if len(self._poly) > 0:
                self._poly.pop()
            if self._poly == []:
                self._creatingPoly = False
                self._poly = None
        if filling:
            if self._fillpath == []:
                self._fillpath = None
                print("Unwahrscheinlich in _undogoto!")
            elif self._fillpath is not None:
                self._fillpath.pop()
        self._update() #count=True)

    def _rotate(self, angle):
        """Turns pen clockwise by angle.
        """
        if self.undobuffer:
            self.undobuffer.push(("rot", angle, self._degreesPerAU))
        angle *= self._degreesPerAU
        neworient = self._orient.rotate(angle)
        tracing = self.screen._tracing
        if tracing == 1 and self._speed > 0:
            anglevel = 3.0 * self._speed
            steps = 1 + int(abs(angle)/anglevel)
            delta = 1.0*angle/steps
            for _ in range(steps):
                self._orient = self._orient.rotate(delta)
                self._update()
        self._orient = neworient
        self._update()

    def _newLine(self, usePos=True):
        """Closes current line item and starts a new one.
           Remark: if current line became too long, animation
           performance (via _drawline) slowed down considerably.
        """
        if len(self.currentLine) > 1:
            self.screen._drawline(self.currentLineItem, self.currentLine,
                                      self._pencolor, self._pensize)
            self.currentLineItem = self.screen._createline()
            self.items.append(self.currentLineItem)
        else:
            self.screen._drawline(self.currentLineItem, top=True)
        self.currentLine = []
        if usePos:
            self.currentLine = [self._position]

    def filling(self):
        """『0008  中文說明』
        是否正在填色，查看是否正在填色。

        沒有參數。

        範例(物件名為「龜」的實例)：

        >>> 龜.開始多邊形()
        >>>if 龜.正在填色():
        ...     龜.筆大小(5)
        ... else:
        ...     龜.筆大小(3)


        Return fillstate (True if filling, False else).

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.begin_fill()
        >>> if turtle.filling():
        ...     turtle.pensize(5)
        ... else:
        ...     turtle.pensize(3)
        """
        return isinstance(self._fillpath, list)

    def begin_fill(self):
        """『0063  中文說明』
        開始填，開始填色，要畫一塊要被填色的形狀之前呼叫。

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.顏色(黑,紅)
        >>> 龜.開始填色()
        >>> 龜.畫圓(60)
        >>> 龜.結束填色()


        Called just before drawing a shape to be filled.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.color("black", "red")
        >>> turtle.begin_fill()
        >>> turtle.circle(60)
        >>> turtle.end_fill()
        """
        if not self.filling():
            self._fillitem = self.screen._createpoly()
            self.items.append(self._fillitem)
        self._fillpath = [self._position]
        self._newLine()
        if self.undobuffer:
            self.undobuffer.push(("beginfill", self._fillitem))
        self._update()


    def end_fill(self):
        """『0023  中文說明』
        結束填，在呼叫過 開始填() 函數後，呼叫本函數將其整個形狀填滿顏色。

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 龜.顏色(黑,紅)
        >>> 龜.開始多邊形()
        >>> 龜.畫圓(60)
        >>> 龜.結束填()


        Fill the shape drawn after the call begin_fill().

        No argument.

        Example (for a Turtle instance named turtle):
        >>> turtle.color("black", "red")
        >>> turtle.begin_fill()
        >>> turtle.circle(60)
        >>> turtle.end_fill()
        """
        if self.filling():
            if len(self._fillpath) > 2:
                self.screen._drawpoly(self._fillitem, self._fillpath,
                                      fill=self._fillcolor)
                if self.undobuffer:
                    self.undobuffer.push(("dofill", self._fillitem))
            self._fillitem = self._fillpath = None
            self._update()

    def dot(self, size=None, *color):
        """『0029  中文說明』
        畫點，可指定直徑大小及顏色。

        可選參數:
        size - 一個整數 >= 1(如果有設定的話)
        color - 一個 顏色字串 或 顏色的數字元組(r,g,b)

        畫一個圓點，用給定的直徑大小及顏色。
        如果直徑大小沒有給定, 就用 寬度 +4 和 2 * 寬度 中較大的值。

        範例(物件名為「龜」的實例):

        >>> 龜.畫點()
        >>> 龜.前進(50); 龜.畫點(20,藍); 龜.前進(50)


        Draw a dot with diameter size, using color.

        Optional arguments:
        size -- an integer >= 1 (if given)
        color -- a colorstring or a numeric color tuple

        Draw a circular dot with diameter size, using color.
        If size is not given, the maximum of pensize+4 and 2*pensize is used.

        Example (for a Turtle instance named turtle):
        >>> turtle.dot()
        >>> turtle.fd(50); turtle.dot(20, "blue"); turtle.fd(50)
        """
        if not color:
            if isinstance(size, (str, tuple)):
                color = self._colorstr(size)
                size = self._pensize + max(self._pensize, 4)
            else:
                color = self._pencolor
                if not size:
                    size = self._pensize + max(self._pensize, 4)
        else:
            if size is None:
                size = self._pensize + max(self._pensize, 4)
            color = self._colorstr(color)
        if hasattr(self.screen, "_dot"):
            item = self.screen._dot(self._position, size, color)
            self.items.append(item)
            if self.undobuffer:
                self.undobuffer.push(("dot", item))
        else:
            pen = self.pen()
            if self.undobuffer:
                self.undobuffer.push(["seq"])
                self.undobuffer.cumulate = True
            try:
                if self.resizemode() == 'auto':
                    self.ht()
                self.pendown()
                self.pensize(size)
                self.pencolor(color)
                self.forward(0)
            finally:
                self.pen(pen)
            if self.undobuffer:
                self.undobuffer.cumulate = False

    def _write(self, txt, align, font):
        """Performs the writing for write()
        """
        item, end = self.screen._write(self._position, txt, align, font,
                                                          self._pencolor)
        self.items.append(item)
        if self.undobuffer:
            self.undobuffer.push(("wri", item))
        return end

    def write(self, arg, move=False, align="left", font=("Arial", 8, "normal")):
        """『0021  中文說明』
        寫，在當前位置寫字。

        參數:
        arg - 信息，將被寫入到 龜幕類 
        move(可選) - 真/假
        align(可選) - "left", "center" 或 right"三個字符串中一個
        font(可選) - 三個變數(字型名稱，字體大小，字體效果)

        寫信息arg的字符串表示形式，
        在當前位置 龜指標 的相對左中右(" left "," "center "或"right ")，
        並根據設定的字體寫字。
        如果move是真，則 龜指標 移動到文字的右下角。
        預設值為 假。

        範例(物件名為「龜」的實例)：

        >>> 龜.寫('首頁=', 真, align="center")
        >>> 龜.寫((0,0),真)


        Write text at the current turtle position.

        Arguments:
        arg -- info, which is to be written to the TurtleScreen
        move (optional) -- True/False
        align (optional) -- one of the strings "left", "center" or right"
        font (optional) -- a triple (fontname, fontsize, fonttype)

        Write text - the string representation of arg - at the current
        turtle position according to align ("left", "center" or right")
        and with the given font.
        If move is True, the pen is moved to the bottom-right corner
        of the text. By default, move is False.

        Example (for a Turtle instance named turtle):
        >>> turtle.write('Home = ', True, align="center")
        >>> turtle.write((0,0), True)
        """
        if self.undobuffer:
            self.undobuffer.push(["seq"])
            self.undobuffer.cumulate = True
        end = self._write(str(arg), align.lower(), font)
        if move:
            x, y = self.pos()
            self.setpos(end, y)
        if self.undobuffer:
            self.undobuffer.cumulate = False

    def begin_poly(self):
        """『0048  中文說明』
        開始多邊形，開始紀錄多邊形的頂點。

        沒有參數。

        將目前 龜指標 的位置記錄為多邊形的第一點。
        

        範例(物件名為「龜」的實例):

        >>> 龜.開始多邊形()


        Start recording the vertices of a polygon.

        No argument.

        Start recording the vertices of a polygon. Current turtle position
        is first point of polygon.

        Example (for a Turtle instance named turtle):
        >>> turtle.begin_poly()
        """
        self._poly = [self._position]
        self._creatingPoly = True

    def end_poly(self):
        """『0028  中文說明』
        結束多邊形，停止記錄多邊形的頂點。

        沒有參數。

        停止記錄多邊形的頂點。
        將目前 龜指標 位置記錄為多邊形的最後一點。並與第一點相連接。

        範例(物件名為「龜」的實例):

        >>> 龜.結束多邊形()


        Stop recording the vertices of a polygon.

        No argument.

        Stop recording the vertices of a polygon. Current turtle position is
        last point of polygon. This will be connected with the first point.

        Example (for a Turtle instance named turtle):
        >>> turtle.end_poly()
        """
        self._creatingPoly = False

    def get_poly(self):
        """『0051  中文說明』
        取多邊形，回傳最近記錄的多邊形。

        沒有參數。

        範例(物件名為「龜」的實例):

        >>> 新形狀 = 龜.取多邊形()
        >>> 龜.登記形狀("最愛形狀", 新形狀)


        Return the lastly recorded polygon.

        No argument.

        Example (for a Turtle instance named turtle):
        >>> p = turtle.get_poly()
        >>> turtle.register_shape("myFavouriteShape", p)
        """
        ## check if there is any poly?
        if self._poly is not None:
            return tuple(self._poly)

    def getscreen(self):
        """『0059  中文說明』
        取幕，回傳 龜螢幕 物件，可讓 龜類 在其上面畫圖。

        沒有參數。

        回傳 龜幕類(TurtleScreen) 物件，可讓 龜類 在其上面畫圖。
        所以 龜幕類的方法可以被該物件呼叫。

        範例(物件名為「龜」的實例)：

        >>> 龜的螢幕 = 龜.取幕()
        >>> 龜的螢幕
        <turtle.TurtleScreen object at 0x0106B770>
        >>> 龜的螢幕.背景色(紅色)


        Return the TurtleScreen object, the turtle is drawing  on.

        No argument.

        Return the TurtleScreen object, the turtle is drawing  on.
        So TurtleScreen-methods can be called for that object.

        Example (for a Turtle instance named turtle):
        >>> ts = turtle.getscreen()
        >>> ts
        <turtle.TurtleScreen object at 0x0106B770>
        >>> ts.bgcolor("pink")
        """
        return self.screen

    def getturtle(self):
        """『0057  中文說明』
        取龜，回傳 龜物件 本身。

        沒有參數。

        合理的使用：作為一個函數來回傳 '匿名龜'。

        例如：
        >>>寵物= 取龜()
        >>>寵物.前進(50)
        >>>寵物
        <turtle.Turtle object at 0x0187D810>
        >>>龜群()
        [<turtle.Turtle object at 0x0187D810>]


        『0062  中文說明』
        取筆，回傳 龜類 物件。

        沒有參數。

        合理的使用：作為一個函數來回傳"匿名龜"。

        例如：
        >>>寵物= 取筆()
        >>>寵物.前進(50)
        >>>寵物
        <turtle.Turtle object at 0x0187D810>
        >>>龜群()
        [<turtle.Turtle object at 0x0187D810>]


        Return the Turtleobject itself.

        No argument.

        Only reasonable use: as a function to return the 'anonymous turtle':

        Example:
        >>> pet = getturtle()
        >>> pet.fd(50)
        >>> pet
        <turtle.Turtle object at 0x0187D810>
        >>> turtles()
        [<turtle.Turtle object at 0x0187D810>]
        """
        return self

    getpen = getturtle


    ################################################################
    ### screen oriented methods recurring to methods of TurtleScreen
    ################################################################

    def _delay(self, delay=None):
        """Set delay value which determines speed of turtle animation.
        """
        return self.screen.delay(delay)

    def onclick(self, fun, btn=1, add=None):
        """『0058  中文說明』
        在點擊時，當此畫布的龜指標發生 點擊鼠鍵的事件 (mouse-click event) 時連結到指定函數上。

        參數:
        fun(函數) - 有 2 個參數的函數之名稱，其 2 個參數 代表 鼠鍵 點擊之位置的座標。
        num(鼠鍵號碼) - 1,2,3 代表 左、中、右鍵，預設為 1 (滑鼠左鍵)。
        add(是否加) -  真 或 假。如果為 真，新的連結函數將被加上，假 則將取消之前的連結。
                

        舉例：針對「匿名龜」，即較簡單的程序(procedural)的方式 (非物件導向型):

        >>>def 轉彎(x,y):
        ...     左轉(360)
        ...
        >>>在點擊時(轉彎) # 現在 點擊事件 與 轉彎 函數 連結在一起。
        >>>在點擊時(無) # 事件連結將被刪除


        Bind fun to mouse-click event on this turtle on canvas.

        Arguments:
        fun --  a function with two arguments, to which will be assigned
                the coordinates of the clicked point on the canvas.
        num --  number of the mouse-button defaults to 1 (left mouse button).
        add --  True or False. If True, new binding will be added, otherwise
                it will replace a former binding.

        Example for the anonymous turtle, i. e. the procedural way:

        >>> def turn(x, y):
        ...     left(360)
        ...
        >>> onclick(turn)  # Now clicking into the turtle will turn it.
        >>> onclick(None)  # event-binding will be removed
        """
        self.screen._onclick(self.turtle._item, fun, btn, add)
        self._update()

    def onrelease(self, fun, btn=1, add=None):
        """『0088  中文說明』
        在鬆開時，當此畫布的龜指標發生 放開鼠鍵的事件 (mouse-button-release event) 時連結到指定函數上。

        參數:
        fun(函數名) - 有 2 個參數的函數之名稱，其 2 個參數 代表 鼠鍵 點擊之位置的座標。
        num(鼠鍵號碼) - 1,2,3 代表 左、中、右鍵，預設為 1 (滑鼠左鍵)。

        範例(物件名 為 喬伊龜 的 我的龜類 實例):
        >>>class 我的龜類(龜類):
        ...     def 發光(自己,x,y):
        ...             自己.填色(紅)
        ...     def 不發光(自己,x,y):
        ...             自己.填色("")
        ...
        >>> 喬伊龜 = 我的龜類()
        >>> 喬伊龜.在點擊時(喬伊龜.發光)
        >>> 喬伊龜.在鬆開時(喬伊龜.不發光)

        點擊 喬伊龜 讓它變成紅色, 不點擊 則變成透明的。


        Bind fun to mouse-button-release event on this turtle on canvas.

        Arguments:
        fun -- a function with two arguments, to which will be assigned
                the coordinates of the clicked point on the canvas.
        num --  number of the mouse-button defaults to 1 (left mouse button).

        Example (for a MyTurtle instance named joe):
        >>> class MyTurtle(Turtle):
        ...     def glow(self,x,y):
        ...             self.fillcolor("red")
        ...     def unglow(self,x,y):
        ...             self.fillcolor("")
        ...
        >>> joe = MyTurtle()
        >>> joe.onclick(joe.glow)
        >>> joe.onrelease(joe.unglow)

        Clicking on joe turns fillcolor red, unclicking turns it to
        transparent.
        """
        self.screen._onrelease(self.turtle._item, fun, btn, add)
        self._update()

    def ondrag(self, fun, btn=1, add=None):
        """『0066  中文說明』
        在拖曳時，當此畫布的龜指標發生 移動滑鼠的事件 (mouse-move event) 時連結到指定函數上。

        參數:
        fun(函數名) - 有 2 個參數的函數之名稱，其 2 個參數 代表 鼠鍵 點擊之位置的座標。
        num(鼠鍵號碼) - 1,2,3 代表 左、中、右鍵，預設為 1 (滑鼠左鍵)。

        針對 龜指標 所作的滑鼠移動事件，每一個事件序列前面都有一個點擊鼠鍵的事件。

        範例(物件名為「龜」的實例):

        >>> 龜.在拖曳時(龜.前往)

        隨後的滑鼠點擊拖拉事件會 在螢幕上 移動 龜，
        從而產生 拖曳痕跡。
        (如果目前是處於下筆狀態的話 )。


        Bind fun to mouse-move event on this turtle on canvas.

        Arguments:
        fun -- a function with two arguments, to which will be assigned
               the coordinates of the clicked point on the canvas.
        num -- number of the mouse-button defaults to 1 (left mouse button).

        Every sequence of mouse-move-events on a turtle is preceded by a
        mouse-click event on that turtle.

        Example (for a Turtle instance named turtle):
        >>> turtle.ondrag(turtle.goto)

        Subsequently clicking and dragging a Turtle will move it
        across the screen thereby producing handdrawings (if pen is
        down).
        """
        self.screen._ondrag(self.turtle._item, fun, btn, add)


    def _undo(self, action, data):
        """Does the main part of the work for undo()
        """
        if self.undobuffer is None:
            return
        if action == "rot":
            angle, degPAU = data
            self._rotate(-angle*degPAU/self._degreesPerAU)
            dummy = self.undobuffer.pop()
        elif action == "stamp":
            stitem = data[0]
            self.clearstamp(stitem)
        elif action == "go":
            self._undogoto(data)
        elif action in ["wri", "dot"]:
            item = data[0]
            self.screen._delete(item)
            self.items.remove(item)
        elif action == "dofill":
            item = data[0]
            self.screen._drawpoly(item, ((0, 0),(0, 0),(0, 0)),
                                  fill="", outline="")
        elif action == "beginfill":
            item = data[0]
            self._fillitem = self._fillpath = None
            if item in self.items:
                self.screen._delete(item)
                self.items.remove(item)
        elif action == "pen":
            TPen.pen(self, data[0])
            self.undobuffer.pop()

    def undo(self):
        """『0056  中文說明』
        回復，撤消最近的動作。

        沒有參數。

        撤消最後 龜指標 的行動。
        可撤消動作的數量是根據該回復暫存區大小來決定。
        

        範例(物件名為「龜」的實例)：

        >>>for i in 範圍(4):
        ...     龜.前進(50); 龜.左轉(80)
        ...
        >>>for i in 範圍(8):
        ...     龜.回復()
        ...


        undo (repeatedly) the last turtle action.

        No argument.

        undo (repeatedly) the last turtle action.
        Number of available undo actions is determined by the size of
        the undobuffer.

        Example (for a Turtle instance named turtle):
        >>> for i in range(4):
        ...     turtle.fd(50); turtle.lt(80)
        ...
        >>> for i in range(8):
        ...     turtle.undo()
        ...
        """
        if self.undobuffer is None:
            return
        item = self.undobuffer.pop()
        action = item[0]
        data = item[1:]
        if action == "seq":
            while data:
                item = data.pop()
                self._undo(item[0], item[1:])
        else:
            self._undo(action, data)

    turtlesize = shapesize
    形狀大小= shapesize
    大小= shapesize
    龜大小= shapesize
    形狀= shape
    形= shape
    寫= write
    開始填= begin_fill
    開始填色= begin_fill
    結束填= end_fill
    結束填色= end_fill
    開始多邊形= begin_poly
    清除= clear
    清除蓋章= clearstamp
    清除蓋章群= clearstamps
    複製= clone
    點= dot
    畫點= dot
    結束多邊形= end_poly
    是否正在填色= filling
    正在填色= filling
    填色狀態= filling
    取多邊形= get_poly
    取形狀多邊形= get_shapepoly
    取筆= getpen
    取幕= getscreen
    取龜= getturtle
    在點擊時= onclick
    在滑鼠點擊龜時= onclick
    在拖曳時= ondrag
    在滑鼠拖曳龜時= ondrag
    在鬆開時= onrelease
    在滑鼠鬆開龜時= onrelease
    在釋放時= onrelease
    在滑鼠釋放龜時= onrelease
    重設= reset
    設傾角= settiltangle
    設傾斜角度= settiltangle
    設回復暫存區= setundobuffer
    形狀轉換= shapetransform
    扭曲因子= shearfactor
    設取扭曲因子= shearfactor
    蓋章= stamp
    蓋印= stamp
    戳印= stamp
    傾斜= tilt
    傾斜角度= tiltangle
    龜大小= turtlesize
    回復= undo
    回復暫存區的個數= undobufferentries
    回復暫存區的長度= undobufferentries
    取回復暫存區的長度= undobufferentries
    寫= write
原龜類= RawTurtle
粗龜類= RawTurtle
原生龜類= RawTurtle
class _Screen(TurtleScreen):

    _root = None
    _canvas = None
    _title = _CFG["title"]

    def __init__(self):
        # XXX there is no need for this code to be conditional,
        # as there will be only a single _Screen instance, anyway
        # XXX actually, the turtle demo is injecting root window,
        # so perhaps the conditional creation of a root should be
        # preserved (perhaps by passing it as an optional parameter)
        if _Screen._root is None:
            _Screen._root = self._root = _Root()
            self._root.title(_Screen._title)
            self._root.ondestroy(self._destroy)
        if _Screen._canvas is None:
            width = _CFG["width"]
            height = _CFG["height"]
            canvwidth = _CFG["canvwidth"]
            canvheight = _CFG["canvheight"]
            leftright = _CFG["leftright"]
            topbottom = _CFG["topbottom"]
            self._root.setupcanvas(width, height, canvwidth, canvheight)
            _Screen._canvas = self._root._getcanvas()
            TurtleScreen.__init__(self, _Screen._canvas)
            self.setup(width, height, leftright, topbottom)

    def setup(self, width=_CFG["width"], height=_CFG["height"],
              startx=_CFG["leftright"], starty=_CFG["topbottom"]):
        """『0067  中文說明』
        設立，設主視窗的大小和位置。

        參數:
        width： 若為整數就是以像素為單位，若為浮動數則是在螢幕的百分比。
          預設值為螢幕的50%。
        height：若為整數就是以像素為單位，若為浮動數則是在螢幕的百分比。
          預設值為螢幕的75%。
        startx： 如為正數，從左邊螢幕的邊緣開始算位置，
          如為負數，從右邊螢幕的邊緣開始算位置，
          預設情況下，startx = 無 是水平居中。
        starty： 如為正數，從上邊螢幕的邊緣開始算位置，
          如為負數，從下邊螢幕的邊緣開始算位置，
          預設情況下，starty = 無 是垂直居中。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.設立(width=200, height=200, startx=0, starty=0)

        設主視窗，寬高為 200×200 像素，在螢幕的左上角位置。

        >>> 螢幕.設立(width=.75, height=0.5, startx=None, starty=None)

        設主視窗的寬高為螢幕寬高的75%及50%。


         Set the size and position of the main window.

        Arguments:
        width: as integer a size in pixels, as float a fraction of the screen.
          Default is 50% of screen.
        height: as integer the height in pixels, as float a fraction of the
          screen. Default is 75% of screen.
        startx: if positive, starting position in pixels from the left
          edge of the screen, if negative from the right edge
          Default, startx=None is to center window horizontally.
        starty: if positive, starting position in pixels from the top
          edge of the screen, if negative from the bottom edge
          Default, starty=None is to center window vertically.

        Examples (for a Screen instance named screen):
        >>> screen.setup (width=200, height=200, startx=0, starty=0)

        sets window to 200x200 pixels, in upper left of screen

        >>> screen.setup(width=.75, height=0.5, startx=None, starty=None)

        sets window to 75% of screen by 50% of screen and centers
        """
        if not hasattr(self._root, "set_geometry"):
            return
        sw = self._root.win_width()
        sh = self._root.win_height()
        if isinstance(width, float) and 0 <= width <= 1:
            width = sw*width
        if startx is None:
            startx = (sw - width) / 2
        if isinstance(height, float) and 0 <= height <= 1:
            height = sh*height
        if starty is None:
            starty = (sh - height) / 2
        self._root.set_geometry(width, height, startx, starty)
        self.update()

    def title(self, titlestring):
        """『0090  中文說明』
        設標題，設置龜視窗的標題。

        參數:
        titlestring  - 一個字串，出現在龜視窗的標題。


        這是螢幕類的方法。不適用於 龜幕類 物件。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.設標題("歡迎來到龜動物園！")


        Set title of turtle-window

        Argument:
        titlestring -- a string, to appear in the titlebar of the
                       turtle graphics window.

        This is a method of Screen-class. Not available for TurtleScreen-
        objects.

        Example (for a Screen instance named screen):
        >>> screen.title("Welcome to the turtle-zoo!")
        """
        if _Screen._root is not None:
            _Screen._root.title(titlestring)
        _Screen._title = titlestring

    def _destroy(self):
        root = self._root
        if root is _Screen._root:
            Turtle._pen = None
            Turtle._screen = None
            _Screen._root = None
            _Screen._canvas = None
        TurtleScreen._RUNNING = True
        root.destroy()

    def bye(self):
        """『0019  中文說明』
        再見，關閉龜圖視窗。

        範例(物件名為「螢幕」的實例)：

        >>> 螢幕.再見()


        Shut the turtlegraphics window.

        Example (for a TurtleScreen instance named screen):
        >>> screen.bye()
        """
        self._destroy()

    def exitonclick(self):
        """『0054  中文說明』
        在點擊時離開，進入主​​迴圈，直到鼠標點擊關閉視窗。

        沒有參數。

        在龜幕類點擊鼠標時綁定 再見() 函數。
        如果"using_IDLE" - 在配置詞典值為 假(默認值)，
        並進入主循環。
        如果在-n模式下的IDLE(無子程式)時 - 
        在 turtle.cfg 值設置為 真。
        在這種情況下，客戶端腳本的IDLE進行主循環。

        這是Screen-class的函數，在 龜幕類 沒有可用的實例。

        範例：

        >>> 在點擊時離開()



        Go into mainloop until the mouse is clicked.

        No arguments.

        Bind bye() method to mouseclick on TurtleScreen.
        If "using_IDLE" - value in configuration dictionary is False
        (default value), enter mainloop.
        If IDLE with -n switch (no subprocess) is used, this value should be
        set to True in turtle.cfg. In this case IDLE's mainloop
        is active also for the client script.

        This is a method of the Screen-class and not available for
        TurtleScreen instances.

        Example (for a Screen instance named screen):
        >>> screen.exitonclick()

        """
        def exitGracefully(x, y):
            """Screen.bye() with two dummy-parameters"""
            self.bye()
        self.onclick(exitGracefully)
        if _CFG["using_IDLE"]:
            return
        try:
            mainloop()
        except AttributeError:
            exit(0)
    設立= setup
    設標題= title
    標題= title
    再見= bye
    在點擊時離開= exitonclick
    離開在點擊時= exitonclick
_幕類= _Screen
_螢幕類= _Screen
def Screen():
    """Return the singleton screen object.
    If none exists at the moment, create a new one and return it,
    else return the existing one."""
    if Turtle._screen is None:
        Turtle._screen = _Screen()
    return Turtle._screen
幕類= Screen
螢幕類= Screen
開幕= Screen
class Turtle(RawTurtle):
    """RawTurtle auto-creating (scrolled) canvas.

    When a Turtle object is created or a function derived from some
    Turtle method is called a TurtleScreen object is automatically created.
    """
    _pen = None
    _screen = None

    def __init__(self,
                 shape=_CFG["shape"],
                 undobuffersize=_CFG["undobuffersize"],
                 visible=_CFG["visible"]):
        if Turtle._screen is None:
            Turtle._screen = Screen()
        RawTurtle.__init__(self, Turtle._screen,
                           shape=shape,
                           undobuffersize=undobuffersize,
                           visible=visible)
龜類= Turtle
烏龜類= Turtle
生一隻龜= Turtle
清除鍵="Delete"
向下鍵="Down"
回家鍵="Home"
向左鍵="Left"
向右鍵="Right"
向上鍵="Up"
空白鍵="space"
脫離鍵="Escape"
黑="black"
黑色="black"
藍="blue"
藍色="blue"
青="cyan"
青色="cyan"
灰="gray"
灰色="gray"
綠="green"
綠色="green"
紫="magenta"
紫色="magenta"
橙="orange"
橙色="orange"
紅="red"
紅色="red"
白="white"
白色="white"
黃="yellow"
黃色="yellow"
龜形="turtle"
烏龜形狀="turtle"
方形="square"
角度從北開始順時針="logo"
角度從東開始逆時針="standard"
世界="world"
無=None
真=True
假=False
印=print
範圍=range
隨機數=random.random
亂數=random.random
隨機選=random.choice
亂選=random.choice
隨機整數=random.randint
亂整數=random.randint
隨機取樣=random.sample
亂取樣=random.sample
看時間=time.ctime
取時間=time.ctime
睡=time.sleep
等時間=time.sleep
時間=time.time
筆類=Pen
原生筆類=RawPen
原生龜類=RawTurtle
可捲畫布類=ScrolledCanvas
形狀類=Shape
龜幕類=TurtleScreen
向量類=Vec2D
二維向量類=Vec2D
向量2D類=Vec2D
龜類=Turtle
生龜=Turtle
生一隻龜=Turtle
Pen=Turtle
筆類=Turtle
幕類=Screen
開幕=Screen
def addshape(name, shape=None): return _取幕().addshape(name, shape)
addshape.__doc__ = _幕類.addshape.__doc__
def bgcolor(*args): return _取幕().bgcolor(*args)
bgcolor.__doc__ = _幕類.bgcolor.__doc__
def bgpic(picname=None): return _取幕().bgpic(picname)
bgpic.__doc__ = _幕類.bgpic.__doc__
def bye(): return _取幕().bye()
bye.__doc__ = _幕類.bye.__doc__
def clear(): return _取幕().clear()
clear.__doc__ = _幕類.clear.__doc__
def clearscreen(): return _取幕().clearscreen()
clearscreen.__doc__ = _幕類.clearscreen.__doc__
def colormode(cmode=None): return _取幕().colormode(cmode)
colormode.__doc__ = _幕類.colormode.__doc__
def delay(delay=None): return _取幕().delay(delay)
delay.__doc__ = _幕類.delay.__doc__
def exitonclick(): return _取幕().exitonclick()
exitonclick.__doc__ = _幕類.exitonclick.__doc__
def getcanvas(): return _取幕().getcanvas()
getcanvas.__doc__ = _幕類.getcanvas.__doc__
def getshapes(): return _取幕().getshapes()
getshapes.__doc__ = _幕類.getshapes.__doc__
def listen(xdummy=None, ydummy=None): return _取幕().listen(xdummy, ydummy)
listen.__doc__ = _幕類.listen.__doc__
def mainloop(): return _取幕().mainloop()
mainloop.__doc__ = _幕類.mainloop.__doc__
def mode(mode=None): return _取幕().mode(mode)
mode.__doc__ = _幕類.mode.__doc__
def numinput(title, prompt, default=None, minval=None, maxval=None): return _取幕().numinput(title, prompt, default, minval, maxval)
numinput.__doc__ = _幕類.numinput.__doc__
def onclick(fun, btn=1, add=None): return _取幕().onclick(fun, btn, add)
onclick.__doc__ = _幕類.onclick.__doc__
def onkey(fun, key): return _取幕().onkey(fun, key)
onkey.__doc__ = _幕類.onkey.__doc__
def onkeypress(fun, key=None): return _取幕().onkeypress(fun, key)
onkeypress.__doc__ = _幕類.onkeypress.__doc__
def onkeyrelease(fun, key): return _取幕().onkeyrelease(fun, key)
onkeyrelease.__doc__ = _幕類.onkeyrelease.__doc__
def onscreenclick(fun, btn=1, add=None): return _取幕().onscreenclick(fun, btn, add)
onscreenclick.__doc__ = _幕類.onscreenclick.__doc__
def ontimer(fun, t=0): return _取幕().ontimer(fun, t)
ontimer.__doc__ = _幕類.ontimer.__doc__
def register_shape(name, shape=None): return _取幕().register_shape(name, shape)
register_shape.__doc__ = _幕類.register_shape.__doc__
def reset(): return _取幕().reset()
reset.__doc__ = _幕類.reset.__doc__
def resetscreen(): return _取幕().resetscreen()
resetscreen.__doc__ = _幕類.resetscreen.__doc__
def screensize(canvwidth=None, canvheight=None, bg=None): return _取幕().screensize(canvwidth, canvheight, bg)
screensize.__doc__ = _幕類.screensize.__doc__
def setup(width=0.5, height=0.75, startx=None, starty=None): return _取幕().setup(width, height, startx, starty)
setup.__doc__ = _幕類.setup.__doc__
def setworldcoordinates(llx, lly, urx, ury): return _取幕().setworldcoordinates(llx, lly, urx, ury)
setworldcoordinates.__doc__ = _幕類.setworldcoordinates.__doc__
def textinput(title, prompt): return _取幕().textinput(title, prompt)
textinput.__doc__ = _幕類.textinput.__doc__
def title(titlestring): return _取幕().title(titlestring)
title.__doc__ = _幕類.title.__doc__
def tracer(n=None, delay=None): return _取幕().tracer(n, delay)
tracer.__doc__ = _幕類.tracer.__doc__
def turtles(): return _取幕().turtles()
turtles.__doc__ = _幕類.turtles.__doc__
def update(): return _取幕().update()
update.__doc__ = _幕類.update.__doc__
def window_height(): return _取幕().window_height()
window_height.__doc__ = _幕類.window_height.__doc__
def window_width(): return _取幕().window_width()
window_width.__doc__ = _幕類.window_width.__doc__
def 主迴圈(): return _取幕().主迴圈()
主迴圈.__doc__ = _幕類.主迴圈.__doc__
def 做完了(): return _取幕().做完了()
做完了.__doc__ = _幕類.做完了.__doc__
def 再見(): return _取幕().再見()
再見.__doc__ = _幕類.再見.__doc__
def 加形狀(name, shape=None): return _取幕().加形狀(name, shape)
加形狀.__doc__ = _幕類.加形狀.__doc__
def 取幕寬(): return _取幕().取幕寬()
取幕寬.__doc__ = _幕類.取幕寬.__doc__
def 取幕高(): return _取幕().取幕高()
取幕高.__doc__ = _幕類.取幕高.__doc__
def 取形(): return _取幕().取形()
取形.__doc__ = _幕類.取形.__doc__
def 取形狀(): return _取幕().取形狀()
取形狀.__doc__ = _幕類.取形狀.__doc__
def 取畫布(): return _取幕().取畫布()
取畫布.__doc__ = _幕類.取畫布.__doc__
def 取龜列表(): return _取幕().取龜列表()
取龜列表.__doc__ = _幕類.取龜列表.__doc__
def 在幕點擊時(fun, btn=1, add=None): return _取幕().在幕點擊時(fun, btn, add)
在幕點擊時.__doc__ = _幕類.在幕點擊時.__doc__
def 在按下鍵時(fun, key=None): return _取幕().在按下鍵時(fun, key)
在按下鍵時.__doc__ = _幕類.在按下鍵時.__doc__
def 在按著鍵時(fun, key=None): return _取幕().在按著鍵時(fun, key)
在按著鍵時.__doc__ = _幕類.在按著鍵時.__doc__
def 在按鍵時(fun, key): return _取幕().在按鍵時(fun, key)
在按鍵時.__doc__ = _幕類.在按鍵時.__doc__
def 在按鍵鬆開時(fun, key): return _取幕().在按鍵鬆開時(fun, key)
在按鍵鬆開時.__doc__ = _幕類.在按鍵鬆開時.__doc__
def 在滑鼠鍵點擊幕時(fun, btn=1, add=None): return _取幕().在滑鼠鍵點擊幕時(fun, btn, add)
在滑鼠鍵點擊幕時.__doc__ = _幕類.在滑鼠鍵點擊幕時.__doc__
def 在滑鼠鍵點擊時(fun, btn=1, add=None): return _取幕().在滑鼠鍵點擊時(fun, btn, add)
在滑鼠鍵點擊時.__doc__ = _幕類.在滑鼠鍵點擊時.__doc__
def 在計時器若干毫秒之後(fun, t=0): return _取幕().在計時器若干毫秒之後(fun, t)
在計時器若干毫秒之後.__doc__ = _幕類.在計時器若干毫秒之後.__doc__
def 在計時後(fun, t=0): return _取幕().在計時後(fun, t)
在計時後.__doc__ = _幕類.在計時後.__doc__
def 在點擊幕時(fun, btn=1, add=None): return _取幕().在點擊幕時(fun, btn, add)
在點擊幕時.__doc__ = _幕類.在點擊幕時.__doc__
def 在點擊時(fun, btn=1, add=None): return _取幕().在點擊時(fun, btn, add)
在點擊時.__doc__ = _幕類.在點擊時.__doc__
def 在點擊時離開(): return _取幕().在點擊時離開()
在點擊時離開.__doc__ = _幕類.在點擊時離開.__doc__
def 在點擊龜時(fun, btn=1, add=None): return _取幕().在點擊龜時(fun, btn, add)
在點擊龜時.__doc__ = _幕類.在點擊龜時.__doc__
def 幕大小(canvwidth=None, canvheight=None, bg=None): return _取幕().幕大小(canvwidth, canvheight, bg)
幕大小.__doc__ = _幕類.幕大小.__doc__
def 幕寬(): return _取幕().幕寬()
幕寬.__doc__ = _幕類.幕寬.__doc__
def 幕高(): return _取幕().幕高()
幕高.__doc__ = _幕類.幕高.__doc__
def 座標系統(llx, lly, urx, ury): return _取幕().座標系統(llx, lly, urx, ury)
座標系統.__doc__ = _幕類.座標系統.__doc__
def 延遲(delay=None): return _取幕().延遲(delay)
延遲.__doc__ = _幕類.延遲.__doc__
def 更新(): return _取幕().更新()
更新.__doc__ = _幕類.更新.__doc__
def 更新畫面(): return _取幕().更新畫面()
更新畫面.__doc__ = _幕類.更新畫面.__doc__
def 標題(titlestring): return _取幕().標題(titlestring)
標題.__doc__ = _幕類.標題.__doc__
def 模式(mode=None): return _取幕().模式(mode)
模式.__doc__ = _幕類.模式.__doc__
def 清除幕(): return _取幕().清除幕()
清除幕.__doc__ = _幕類.清除幕.__doc__
def 登記形狀(name, shape=None): return _取幕().登記形狀(name, shape)
登記形狀.__doc__ = _幕類.登記形狀.__doc__
def 窗寬(): return _取幕().窗寬()
窗寬.__doc__ = _幕類.窗寬.__doc__
def 窗高(): return _取幕().窗高()
窗高.__doc__ = _幕類.窗高.__doc__
def 等待閉幕(): return _取幕().等待閉幕()
等待閉幕.__doc__ = _幕類.等待閉幕.__doc__
def 聽(xdummy=None, ydummy=None): return _取幕().聽(xdummy, ydummy)
聽.__doc__ = _幕類.聽.__doc__
def 聽鍵盤(xdummy=None, ydummy=None): return _取幕().聽鍵盤(xdummy, ydummy)
聽鍵盤.__doc__ = _幕類.聽鍵盤.__doc__
def 背景圖(picname=None): return _取幕().背景圖(picname)
背景圖.__doc__ = _幕類.背景圖.__doc__
def 背景色(*args): return _取幕().背景色(*args)
背景色.__doc__ = _幕類.背景色.__doc__
def 色模式(cmode=None): return _取幕().色模式(cmode)
色模式.__doc__ = _幕類.色模式.__doc__
def 設座標系統(llx, lly, urx, ury): return _取幕().設座標系統(llx, lly, urx, ury)
設座標系統.__doc__ = _幕類.設座標系統.__doc__
def 設標題(titlestring): return _取幕().設標題(titlestring)
設標題.__doc__ = _幕類.設標題.__doc__
def 設立(width=0.5, height=0.75, startx=None, starty=None): return _取幕().設立(width, height, startx, starty)
設立.__doc__ = _幕類.設立.__doc__
def 註冊形狀(name, shape=None): return _取幕().註冊形狀(name, shape)
註冊形狀.__doc__ = _幕類.註冊形狀.__doc__
def 輸入數字(title, prompt, default=None, minval=None, maxval=None): return _取幕().輸入數字(title, prompt, default, minval, maxval)
輸入數字.__doc__ = _幕類.輸入數字.__doc__
def 輸入文字(title, prompt): return _取幕().輸入文字(title, prompt)
輸入文字.__doc__ = _幕類.輸入文字.__doc__
def 追蹤(n=None, delay=None): return _取幕().追蹤(n, delay)
追蹤.__doc__ = _幕類.追蹤.__doc__
def 追蹤器(n=None, delay=None): return _取幕().追蹤器(n, delay)
追蹤器.__doc__ = _幕類.追蹤器.__doc__
def 追蹤更新畫面(n=None, delay=None): return _取幕().追蹤更新畫面(n, delay)
追蹤更新畫面.__doc__ = _幕類.追蹤更新畫面.__doc__
def 進入主迴圈(): return _取幕().進入主迴圈()
進入主迴圈.__doc__ = _幕類.進入主迴圈.__doc__
def 重設(): return _取幕().重設()
重設.__doc__ = _幕類.重設.__doc__
def 重設幕(): return _取幕().重設幕()
重設幕.__doc__ = _幕類.重設幕.__doc__
def 重設幕大小(canvwidth=None, canvheight=None, bg=None): return _取幕().重設幕大小(canvwidth, canvheight, bg)
重設幕大小.__doc__ = _幕類.重設幕大小.__doc__
def 重設幕寬高(canvwidth=None, canvheight=None, bg=None): return _取幕().重設幕寬高(canvwidth, canvheight, bg)
重設幕寬高.__doc__ = _幕類.重設幕寬高.__doc__
def 重設所有龜(): return _取幕().重設所有龜()
重設所有龜.__doc__ = _幕類.重設所有龜.__doc__
def 閉幕(): return _取幕().閉幕()
閉幕.__doc__ = _幕類.閉幕.__doc__
def 離開在點擊時(): return _取幕().離開在點擊時()
離開在點擊時.__doc__ = _幕類.離開在點擊時.__doc__
def 點擊X結束(): return _取幕().點擊X結束()
點擊X結束.__doc__ = _幕類.點擊X結束.__doc__
def 龜列表(): return _取幕().龜列表()
龜列表.__doc__ = _幕類.龜列表.__doc__
def 龜群(): return _取幕().龜群()
龜群.__doc__ = _幕類.龜群.__doc__
def back(distance): return _取筆().back(distance)
back.__doc__ = 龜類.back.__doc__
def backward(distance): return _取筆().backward(distance)
backward.__doc__ = 龜類.backward.__doc__
def begin_fill(): return _取筆().begin_fill()
begin_fill.__doc__ = 龜類.begin_fill.__doc__
def begin_poly(): return _取筆().begin_poly()
begin_poly.__doc__ = 龜類.begin_poly.__doc__
def bk(distance): return _取筆().bk(distance)
bk.__doc__ = 龜類.bk.__doc__
def circle(radius, extent=None, steps=None): return _取筆().circle(radius, extent, steps)
circle.__doc__ = 龜類.circle.__doc__
def clear(): return _取筆().clear()
clear.__doc__ = 龜類.clear.__doc__
def clearstamp(stampid): return _取筆().clearstamp(stampid)
clearstamp.__doc__ = 龜類.clearstamp.__doc__
def clearstamps(n=None): return _取筆().clearstamps(n)
clearstamps.__doc__ = 龜類.clearstamps.__doc__
def clone(): return _取筆().clone()
clone.__doc__ = 龜類.clone.__doc__
def color(*args): return _取筆().color(*args)
color.__doc__ = 龜類.color.__doc__
def degrees(fullcircle=360.0): return _取筆().degrees(fullcircle)
degrees.__doc__ = 龜類.degrees.__doc__
def distance(x, y=None): return _取筆().distance(x, y)
distance.__doc__ = 龜類.distance.__doc__
def dot(size=None, *color): return _取筆().dot(size, *color)
dot.__doc__ = 龜類.dot.__doc__
def down(): return _取筆().down()
down.__doc__ = 龜類.down.__doc__
def end_fill(): return _取筆().end_fill()
end_fill.__doc__ = 龜類.end_fill.__doc__
def end_poly(): return _取筆().end_poly()
end_poly.__doc__ = 龜類.end_poly.__doc__
def fd(distance): return _取筆().fd(distance)
fd.__doc__ = 龜類.fd.__doc__
def fillcolor(*args): return _取筆().fillcolor(*args)
fillcolor.__doc__ = 龜類.fillcolor.__doc__
def filling(): return _取筆().filling()
filling.__doc__ = 龜類.filling.__doc__
def forward(distance): return _取筆().forward(distance)
forward.__doc__ = 龜類.forward.__doc__
def get_poly(): return _取筆().get_poly()
get_poly.__doc__ = 龜類.get_poly.__doc__
def get_shapepoly(): return _取筆().get_shapepoly()
get_shapepoly.__doc__ = 龜類.get_shapepoly.__doc__
def getpen(): return _取筆().getpen()
getpen.__doc__ = 龜類.getpen.__doc__
def getscreen(): return _取筆().getscreen()
getscreen.__doc__ = 龜類.getscreen.__doc__
def getturtle(): return _取筆().getturtle()
getturtle.__doc__ = 龜類.getturtle.__doc__
def goto(x, y=None): return _取筆().goto(x, y)
goto.__doc__ = 龜類.goto.__doc__
def heading(): return _取筆().heading()
heading.__doc__ = 龜類.heading.__doc__
def hideturtle(): return _取筆().hideturtle()
hideturtle.__doc__ = 龜類.hideturtle.__doc__
def home(): return _取筆().home()
home.__doc__ = 龜類.home.__doc__
def ht(): return _取筆().ht()
ht.__doc__ = 龜類.ht.__doc__
def isdown(): return _取筆().isdown()
isdown.__doc__ = 龜類.isdown.__doc__
def isvisible(): return _取筆().isvisible()
isvisible.__doc__ = 龜類.isvisible.__doc__
def left(angle): return _取筆().left(angle)
left.__doc__ = 龜類.left.__doc__
def lt(angle): return _取筆().lt(angle)
lt.__doc__ = 龜類.lt.__doc__
def onclick(fun, btn=1, add=None): return _取筆().onclick(fun, btn, add)
onclick.__doc__ = 龜類.onclick.__doc__
def ondrag(fun, btn=1, add=None): return _取筆().ondrag(fun, btn, add)
ondrag.__doc__ = 龜類.ondrag.__doc__
def onrelease(fun, btn=1, add=None): return _取筆().onrelease(fun, btn, add)
onrelease.__doc__ = 龜類.onrelease.__doc__
def pd(): return _取筆().pd()
pd.__doc__ = 龜類.pd.__doc__
def pen(pen=None, **pendict): return _取筆().pen(pen, **pendict)
pen.__doc__ = 龜類.pen.__doc__
def pencolor(*args): return _取筆().pencolor(*args)
pencolor.__doc__ = 龜類.pencolor.__doc__
def pendown(): return _取筆().pendown()
pendown.__doc__ = 龜類.pendown.__doc__
def pensize(width=None): return _取筆().pensize(width)
pensize.__doc__ = 龜類.pensize.__doc__
def penup(): return _取筆().penup()
penup.__doc__ = 龜類.penup.__doc__
def pos(): return _取筆().pos()
pos.__doc__ = 龜類.pos.__doc__
def position(): return _取筆().position()
position.__doc__ = 龜類.position.__doc__
def pu(): return _取筆().pu()
pu.__doc__ = 龜類.pu.__doc__
def radians(): return _取筆().radians()
radians.__doc__ = 龜類.radians.__doc__
def reset(): return _取筆().reset()
reset.__doc__ = 龜類.reset.__doc__
def resizemode(rmode=None): return _取筆().resizemode(rmode)
resizemode.__doc__ = 龜類.resizemode.__doc__
def right(angle): return _取筆().right(angle)
right.__doc__ = 龜類.right.__doc__
def rt(angle): return _取筆().rt(angle)
rt.__doc__ = 龜類.rt.__doc__
def seth(to_angle): return _取筆().seth(to_angle)
seth.__doc__ = 龜類.seth.__doc__
def setheading(to_angle): return _取筆().setheading(to_angle)
setheading.__doc__ = 龜類.setheading.__doc__
def setpos(x, y=None): return _取筆().setpos(x, y)
setpos.__doc__ = 龜類.setpos.__doc__
def setposition(x, y=None): return _取筆().setposition(x, y)
setposition.__doc__ = 龜類.setposition.__doc__
def settiltangle(angle): return _取筆().settiltangle(angle)
settiltangle.__doc__ = 龜類.settiltangle.__doc__
def setundobuffer(size): return _取筆().setundobuffer(size)
setundobuffer.__doc__ = 龜類.setundobuffer.__doc__
def setx(x): return _取筆().setx(x)
setx.__doc__ = 龜類.setx.__doc__
def sety(y): return _取筆().sety(y)
sety.__doc__ = 龜類.sety.__doc__
def shape(name=None): return _取筆().shape(name)
shape.__doc__ = 龜類.shape.__doc__
def shapesize(stretch_wid=None, stretch_len=None, outline=None): return _取筆().shapesize(stretch_wid, stretch_len, outline)
shapesize.__doc__ = 龜類.shapesize.__doc__
def shapetransform(t11=None, t12=None, t21=None, t22=None): return _取筆().shapetransform(t11, t12, t21, t22)
shapetransform.__doc__ = 龜類.shapetransform.__doc__
def shearfactor(shear=None): return _取筆().shearfactor(shear)
shearfactor.__doc__ = 龜類.shearfactor.__doc__
def showturtle(): return _取筆().showturtle()
showturtle.__doc__ = 龜類.showturtle.__doc__
def speed(speed=None): return _取筆().speed(speed)
speed.__doc__ = 龜類.speed.__doc__
def st(): return _取筆().st()
st.__doc__ = 龜類.st.__doc__
def stamp(): return _取筆().stamp()
stamp.__doc__ = 龜類.stamp.__doc__
def tilt(angle): return _取筆().tilt(angle)
tilt.__doc__ = 龜類.tilt.__doc__
def tiltangle(angle=None): return _取筆().tiltangle(angle)
tiltangle.__doc__ = 龜類.tiltangle.__doc__
def towards(x, y=None): return _取筆().towards(x, y)
towards.__doc__ = 龜類.towards.__doc__
def turtlesize(stretch_wid=None, stretch_len=None, outline=None): return _取筆().turtlesize(stretch_wid, stretch_len, outline)
turtlesize.__doc__ = 龜類.turtlesize.__doc__
def undo(): return _取筆().undo()
undo.__doc__ = 龜類.undo.__doc__
def undobufferentries(): return _取筆().undobufferentries()
undobufferentries.__doc__ = 龜類.undobufferentries.__doc__
def up(): return _取筆().up()
up.__doc__ = 龜類.up.__doc__
def width(width=None): return _取筆().width(width)
width.__doc__ = 龜類.width.__doc__
def write(arg, move=False, align='left', font=('Arial', 8, 'normal')): return _取筆().write(arg, move, align, font)
write.__doc__ = 龜類.write.__doc__
def xcor(): return _取筆().xcor()
xcor.__doc__ = 龜類.xcor.__doc__
def x座標(): return _取筆().x座標()
x座標.__doc__ = 龜類.x座標.__doc__
def ycor(): return _取筆().ycor()
ycor.__doc__ = 龜類.ycor.__doc__
def y座標(): return _取筆().y座標()
y座標.__doc__ = 龜類.y座標.__doc__
def 下筆(): return _取筆().下筆()
下筆.__doc__ = 龜類.下筆.__doc__
def 下筆嗎(): return _取筆().下筆嗎()
下筆嗎.__doc__ = 龜類.下筆嗎.__doc__
def 下筆狀態(): return _取筆().下筆狀態()
下筆狀態.__doc__ = 龜類.下筆狀態.__doc__
def 位置(): return _取筆().位置()
位置.__doc__ = 龜類.位置.__doc__
def 傾斜(angle): return _取筆().傾斜(angle)
傾斜.__doc__ = 龜類.傾斜.__doc__
def 傾斜角度(angle=None): return _取筆().傾斜角度(angle)
傾斜角度.__doc__ = 龜類.傾斜角度.__doc__
def 前往(x, y=None): return _取筆().前往(x, y)
前往.__doc__ = 龜類.前往.__doc__
def 前進(distance): return _取筆().前進(distance)
前進.__doc__ = 龜類.前進.__doc__
def 半徑數(): return _取筆().半徑數()
半徑數.__doc__ = 龜類.半徑數.__doc__
def 去到(x, y=None): return _取筆().去到(x, y)
去到.__doc__ = 龜類.去到.__doc__
def 取回復暫存區的長度(): return _取筆().取回復暫存區的長度()
取回復暫存區的長度.__doc__ = 龜類.取回復暫存區的長度.__doc__
def 取多邊形(): return _取筆().取多邊形()
取多邊形.__doc__ = 龜類.取多邊形.__doc__
def 取幕(): return _取筆().取幕()
取幕.__doc__ = 龜類.取幕.__doc__
def 取形狀多邊形(): return _取筆().取形狀多邊形()
取形狀多邊形.__doc__ = 龜類.取形狀多邊形.__doc__
def 取筆(): return _取筆().取筆()
取筆.__doc__ = 龜類.取筆.__doc__
def 取龜(): return _取筆().取龜()
取龜.__doc__ = 龜類.取龜.__doc__
def 可見狀態(): return _取筆().可見狀態()
可見狀態.__doc__ = 龜類.可見狀態.__doc__
def 右轉(angle): return _取筆().右轉(angle)
右轉.__doc__ = 龜類.右轉.__doc__
def 回家(): return _取筆().回家()
回家.__doc__ = 龜類.回家.__doc__
def 回復(): return _取筆().回復()
回復.__doc__ = 龜類.回復.__doc__
def 回復暫存區的個數(): return _取筆().回復暫存區的個數()
回復暫存區的個數.__doc__ = 龜類.回復暫存區的個數.__doc__
def 回復暫存區的長度(): return _取筆().回復暫存區的長度()
回復暫存區的長度.__doc__ = 龜類.回復暫存區的長度.__doc__
def 圓(radius, extent=None, steps=None): return _取筆().圓(radius, extent, steps)
圓.__doc__ = 龜類.圓.__doc__
def 在拖曳時(fun, btn=1, add=None): return _取筆().在拖曳時(fun, btn, add)
在拖曳時.__doc__ = 龜類.在拖曳時.__doc__
def 在滑鼠拖曳龜時(fun, btn=1, add=None): return _取筆().在滑鼠拖曳龜時(fun, btn, add)
在滑鼠拖曳龜時.__doc__ = 龜類.在滑鼠拖曳龜時.__doc__
def 在滑鼠釋放龜時(fun, btn=1, add=None): return _取筆().在滑鼠釋放龜時(fun, btn, add)
在滑鼠釋放龜時.__doc__ = 龜類.在滑鼠釋放龜時.__doc__
def 在滑鼠鬆開龜時(fun, btn=1, add=None): return _取筆().在滑鼠鬆開龜時(fun, btn, add)
在滑鼠鬆開龜時.__doc__ = 龜類.在滑鼠鬆開龜時.__doc__
def 在滑鼠點擊龜時(fun, btn=1, add=None): return _取筆().在滑鼠點擊龜時(fun, btn, add)
在滑鼠點擊龜時.__doc__ = 龜類.在滑鼠點擊龜時.__doc__
def 在釋放時(fun, btn=1, add=None): return _取筆().在釋放時(fun, btn, add)
在釋放時.__doc__ = 龜類.在釋放時.__doc__
def 在鬆開時(fun, btn=1, add=None): return _取筆().在鬆開時(fun, btn, add)
在鬆開時.__doc__ = 龜類.在鬆開時.__doc__
def 在點擊時(fun, btn=1, add=None): return _取筆().在點擊時(fun, btn, add)
在點擊時.__doc__ = 龜類.在點擊時.__doc__
def 填色(*args): return _取筆().填色(*args)
填色.__doc__ = 龜類.填色.__doc__
def 填色狀態(): return _取筆().填色狀態()
填色狀態.__doc__ = 龜類.填色狀態.__doc__
def 大小(stretch_wid=None, stretch_len=None, outline=None): return _取筆().大小(stretch_wid, stretch_len, outline)
大小.__doc__ = 龜類.大小.__doc__
def 寫(arg, move=False, align='left', font=('Arial', 8, 'normal')): return _取筆().寫(arg, move, align, font)
寫.__doc__ = 龜類.寫.__doc__
def 寬(width=None): return _取筆().寬(width)
寬.__doc__ = 龜類.寬.__doc__
def 左轉(angle): return _取筆().左轉(angle)
左轉.__doc__ = 龜類.左轉.__doc__
def 座標x(): return _取筆().座標x()
座標x.__doc__ = 龜類.座標x.__doc__
def 座標y(): return _取筆().座標y()
座標y.__doc__ = 龜類.座標y.__doc__
def 弧度(): return _取筆().弧度()
弧度.__doc__ = 龜類.弧度.__doc__
def 弳度(): return _取筆().弳度()
弳度.__doc__ = 龜類.弳度.__doc__
def 形(name=None): return _取筆().形(name)
形.__doc__ = 龜類.形.__doc__
def 形狀(name=None): return _取筆().形狀(name)
形狀.__doc__ = 龜類.形狀.__doc__
def 形狀大小(stretch_wid=None, stretch_len=None, outline=None): return _取筆().形狀大小(stretch_wid, stretch_len, outline)
形狀大小.__doc__ = 龜類.形狀大小.__doc__
def 形狀轉換(t11=None, t12=None, t21=None, t22=None): return _取筆().形狀轉換(t11, t12, t21, t22)
形狀轉換.__doc__ = 龜類.形狀轉換.__doc__
def 後退(distance): return _取筆().後退(distance)
後退.__doc__ = 龜類.後退.__doc__
def 戳印(): return _取筆().戳印()
戳印.__doc__ = 龜類.戳印.__doc__
def 扭曲因子(shear=None): return _取筆().扭曲因子(shear)
扭曲因子.__doc__ = 龜類.扭曲因子.__doc__
def 提筆(): return _取筆().提筆()
提筆.__doc__ = 龜類.提筆.__doc__
def 是否下筆(): return _取筆().是否下筆()
是否下筆.__doc__ = 龜類.是否下筆.__doc__
def 是否可見(): return _取筆().是否可見()
是否可見.__doc__ = 龜類.是否可見.__doc__
def 是否正在填色(): return _取筆().是否正在填色()
是否正在填色.__doc__ = 龜類.是否正在填色.__doc__
def 朝向(x, y=None): return _取筆().朝向(x, y)
朝向.__doc__ = 龜類.朝向.__doc__
def 朝向xy(x, y=None): return _取筆().朝向xy(x, y)
朝向xy.__doc__ = 龜類.朝向xy.__doc__
def 正在填色(): return _取筆().正在填色()
正在填色.__doc__ = 龜類.正在填色.__doc__
def 清除(): return _取筆().清除()
清除.__doc__ = 龜類.清除.__doc__
def 清除蓋章(stampid): return _取筆().清除蓋章(stampid)
清除蓋章.__doc__ = 龜類.清除蓋章.__doc__
def 清除蓋章群(n=None): return _取筆().清除蓋章群(n)
清除蓋章群.__doc__ = 龜類.清除蓋章群.__doc__
def 畫圓(radius, extent=None, steps=None): return _取筆().畫圓(radius, extent, steps)
畫圓.__doc__ = 龜類.畫圓.__doc__
def 畫點(size=None, *color): return _取筆().畫點(size, *color)
畫點.__doc__ = 龜類.畫點.__doc__
def 筆(pen=None, **pendict): return _取筆().筆(pen, **pendict)
筆.__doc__ = 龜類.筆.__doc__
def 筆大小(width=None): return _取筆().筆大小(width)
筆大小.__doc__ = 龜類.筆大小.__doc__
def 筆寬(width=None): return _取筆().筆寬(width)
筆寬.__doc__ = 龜類.筆寬.__doc__
def 筆屬性(pen=None, **pendict): return _取筆().筆屬性(pen, **pendict)
筆屬性.__doc__ = 龜類.筆屬性.__doc__
def 筆粗(width=None): return _取筆().筆粗(width)
筆粗.__doc__ = 龜類.筆粗.__doc__
def 筆粗細(width=None): return _取筆().筆粗細(width)
筆粗細.__doc__ = 龜類.筆粗細.__doc__
def 筆色(*args): return _取筆().筆色(*args)
筆色.__doc__ = 龜類.筆色.__doc__
def 結束填(): return _取筆().結束填()
結束填.__doc__ = 龜類.結束填.__doc__
def 結束填色(): return _取筆().結束填色()
結束填色.__doc__ = 龜類.結束填色.__doc__
def 結束多邊形(): return _取筆().結束多邊形()
結束多邊形.__doc__ = 龜類.結束多邊形.__doc__
def 蓋印(): return _取筆().蓋印()
蓋印.__doc__ = 龜類.蓋印.__doc__
def 蓋章(): return _取筆().蓋章()
蓋章.__doc__ = 龜類.蓋章.__doc__
def 藏(): return _取筆().藏()
藏.__doc__ = 龜類.藏.__doc__
def 藏龜(): return _取筆().藏龜()
藏龜.__doc__ = 龜類.藏龜.__doc__
def 複製(): return _取筆().複製()
複製.__doc__ = 龜類.複製.__doc__
def 角度(fullcircle=360.0): return _取筆().角度(fullcircle)
角度.__doc__ = 龜類.角度.__doc__
def 設x座標(x): return _取筆().設x座標(x)
設x座標.__doc__ = 龜類.設x座標.__doc__
def 設y座標(y): return _取筆().設y座標(y)
設y座標.__doc__ = 龜類.設y座標.__doc__
def 設位置(x, y=None): return _取筆().設位置(x, y)
設位置.__doc__ = 龜類.設位置.__doc__
def 設傾斜角度(angle): return _取筆().設傾斜角度(angle)
設傾斜角度.__doc__ = 龜類.設傾斜角度.__doc__
def 設傾角(angle): return _取筆().設傾角(angle)
設傾角.__doc__ = 龜類.設傾角.__doc__
def 設取扭曲因子(shear=None): return _取筆().設取扭曲因子(shear)
設取扭曲因子.__doc__ = 龜類.設取扭曲因子.__doc__
def 設回復暫存區(size): return _取筆().設回復暫存區(size)
設回復暫存區.__doc__ = 龜類.設回復暫存區.__doc__
def 設圓為2pi弧(): return _取筆().設圓為2pi弧()
設圓為2pi弧.__doc__ = 龜類.設圓為2pi弧.__doc__
def 設圓為360度(fullcircle=360.0): return _取筆().設圓為360度(fullcircle)
設圓為360度.__doc__ = 龜類.設圓為360度.__doc__
def 設座標x(x): return _取筆().設座標x(x)
設座標x.__doc__ = 龜類.設座標x.__doc__
def 設座標y(y): return _取筆().設座標y(y)
設座標y.__doc__ = 龜類.設座標y.__doc__
def 設成可伸縮模式(rmode=None): return _取筆().設成可伸縮模式(rmode)
設成可伸縮模式.__doc__ = 龜類.設成可伸縮模式.__doc__
def 設角為度(fullcircle=360.0): return _取筆().設角為度(fullcircle)
設角為度.__doc__ = 龜類.設角為度.__doc__
def 設角為弧(): return _取筆().設角為弧()
設角為弧.__doc__ = 龜類.設角為弧.__doc__
def 設角的單位為半徑數(): return _取筆().設角的單位為半徑數()
設角的單位為半徑數.__doc__ = 龜類.設角的單位為半徑數.__doc__
def 設角的單位為角度(fullcircle=360.0): return _取筆().設角的單位為角度(fullcircle)
設角的單位為角度.__doc__ = 龜類.設角的單位為角度.__doc__
def 設頭向(to_angle): return _取筆().設頭向(to_angle)
設頭向.__doc__ = 龜類.設頭向.__doc__
def 距離(x, y=None): return _取筆().距離(x, y)
距離.__doc__ = 龜類.距離.__doc__
def 速度(speed=None): return _取筆().速度(speed)
速度.__doc__ = 龜類.速度.__doc__
def 重設(): return _取筆().重設()
重設.__doc__ = 龜類.重設.__doc__
def 重設大小模式(rmode=None): return _取筆().重設大小模式(rmode)
重設大小模式.__doc__ = 龜類.重設大小模式.__doc__
def 開始填(): return _取筆().開始填()
開始填.__doc__ = 龜類.開始填.__doc__
def 開始填色(): return _取筆().開始填色()
開始填色.__doc__ = 龜類.開始填色.__doc__
def 開始多邊形(): return _取筆().開始多邊形()
開始多邊形.__doc__ = 龜類.開始多邊形.__doc__
def 隱藏(): return _取筆().隱藏()
隱藏.__doc__ = 龜類.隱藏.__doc__
def 頭向(): return _取筆().頭向()
頭向.__doc__ = 龜類.頭向.__doc__
def 顏色(*args): return _取筆().顏色(*args)
顏色.__doc__ = 龜類.顏色.__doc__
def 顯(): return _取筆().顯()
顯.__doc__ = 龜類.顯.__doc__
def 顯示(): return _取筆().顯示()
顯示.__doc__ = 龜類.顯示.__doc__
def 顯龜(): return _取筆().顯龜()
顯龜.__doc__ = 龜類.顯龜.__doc__
def 顯龜嗎(): return _取筆().顯龜嗎()
顯龜嗎.__doc__ = 龜類.顯龜嗎.__doc__
def 點(size=None, *color): return _取筆().點(size, *color)
點.__doc__ = 龜類.點.__doc__
def 龜大小(stretch_wid=None, stretch_len=None, outline=None): return _取筆().龜大小(stretch_wid, stretch_len, outline)
龜大小.__doc__ = 龜類.龜大小.__doc__

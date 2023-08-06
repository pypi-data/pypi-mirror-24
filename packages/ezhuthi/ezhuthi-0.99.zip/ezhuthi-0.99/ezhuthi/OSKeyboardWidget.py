#!/usr/bin/python
# -*- coding: utf-8 -*-
## 
## (C) 2017 Ezhil Language Foundation
## Licensed under GPL Version 3
from __future__ import print_function
import tamil
import gi
import sys
import copy

PYTHON3 = (sys.version[0] == '3')
if PYTHON3:
    unicode = str

gi.require_version('Gtk','3.0')
from gi.repository import Gtk

# row 3 extras: 'shift', 'backspace'
# row 4 extras: 'num keypad','escape to language','space','return'
toList = lambda strval: list(tamil.utf8.get_letters(strval))
class OSKeyboard(object):
    def __init__(self,lang,keys3rows,shift_keys3rows):
        object.__init__(self)
        self.lang = lang
        self.numeric3rows = [ toList(u"1234567890"),toList(u"-/:;()$&@"),toList(u".,?!'") ]
        self.keys3rows = copy.copy(keys3rows)
        self.shift_keys3rows = copy.copy(shift_keys3rows)
        self.keys3rows_btns = []
        self.mode = u"non-numeric"
        self.spc = u" "*16
        self.shift_words = [u"பிர", u"Shift"]
        self.shiftmode = False

    def __str__(self):
        sval = self.lang + u"\n"
        sval += u"\n".join([ u",".join(row) for row in self.keys3rows])
        sval += u"\n---shifted-keys--\n"
        sval += u"\n".join([ u",".join(row) for row in self.shift_keys3rows])
        sval += u"\n---Numeric-keys--\n"
        sval += u"\n".join([ u",".join(row) for row in self.numeric3rows])
        return sval

    def toggle_shift_mode(self):
        self.shiftmode = not self.shiftmode
        return self.shiftmode

    def numericmode(self):
        return self.mode.find(u"non-numeric") == -1

    def padded(self,key_rows,numerickdb=False):
        rows2 = key_rows #copy.copy(key_rows)
        if self.lang.find("English") >= 0:
            if rows2[-1][0].find(u"Shift") == -1:
                rows2[-1].insert(0,u"Shift")
                rows2[-1].insert(len(rows2[-1]),u"&lt;- back")
            rows2.append([u"0-9",u"தமிழ்",self.spc+u"Space"+self.spc,u"Enter"])
            if numerickdb:
                rows2[-1][1] = u"ஆங்"
        else:
            if rows2[-1][0].find(u"பிர") == -1:
                rows2[-1].insert(0,u"பிர")
                rows2[-1].insert(len(rows2[-1]),u"&lt;- அழி")
            rows2.append([u"0-9",u"ஆங்",self.spc+u"வெளி"+self.spc,u"் ",u"இடு"])
            if numerickdb:
                rows2[-1][1] = u"தமிழ்"
        return rows2

    def get_key_modifier(self,key):
        # backspace hook
        if key.find(u"&lt;-") >= 0:
            key = u"\b"
        elif key.find(u"வெளி") >= 0 or key.find(u"Space") >= 0:
            key = u" "
        elif key.find(u"இடு") >= 0 or key.find(u"Enter") >= 0:
            key = u"\n"
        elif key == u"&amp;":
            key = u"&"
        return key

    def build_widget(self,parent_box,edobj,numerickbd=False):
        if numerickbd:
            self.mode = u"numeric"
        else:
            self.mode = u"non-numeric"

        rows = list()
        toggle_keys = [u"ஆங்",u"0-9",u"தமிழ்"]

        #numeric mode cannot have any shift modes

        if numerickbd:
            ref_keys3rows = self.numeric3rows
            ref_keys3rows[1][7] = u"&amp;"
        else:
            if self.shiftmode:
                ref_keys3rows = self.shift_keys3rows
            else:
                ref_keys3rows = self.keys3rows

        if ( len(ref_keys3rows) < 4 ):
            padded_keys = self.padded(ref_keys3rows,numerickbd)
        else:
            padded_keys = ref_keys3rows

        del self.keys3rows_btns
        self.keys3rows_btns = list()
        for keys in padded_keys:
            btns = []
            curr_row = Gtk.Box()
            rows.append( curr_row )
            full = False
            for pos,key in enumerate(keys):
                btn = Gtk.Button(label=key)
                btns.append(btn)
                for child in btn.get_children():
                    if self.lang.find("English") >= 0:
                        child.set_label(u"<span weight=\"heavy\" size=\"large\" fallback=\"true\">%s</span>"%key)
                    else:
                        child.set_label(u"<span weight=\"heavy\" size=\"large\" fallback=\"true\">%s</span>"%key)
                    child.set_use_markup(True)
                    break
                key = self.get_key_modifier(key)
                if not any([key in toggle_keys, key in self.shift_words]):
                    btn.connect("clicked",edobj.insert_tamil99_at_cursor,key,self.lang)
                curr_row.pack_start(btn,True,True,2)
            curr_row.show_all()
            parent_box.pack_start(curr_row,False,not True,2)
            self.keys3rows_btns.append(btns)
        return rows

class EnglishKeyboard(OSKeyboard):
    keys3rows = [toList(u"QWERTYUIOP".lower()),toList(u"ASDFGHJKL".lower()),toList(u"ZXCVBNM".lower())]
    shift_keys3rows = [toList(u"QWERTYUIOP"),toList(u"ASDFGHJKL"),toList(u"ZXCVBNM")]
    def __init__(self):
        OSKeyboard.__init__(self,u"English",EnglishKeyboard.keys3rows,EnglishKeyboard.shift_keys3rows)

class TamilKeyboard(OSKeyboard):
    special = u"புள்ளி"
    space = u"வெளி"
    pulli = u"் "
    keys3rows = [toList(u"ஆஈஊஏளறனடணசஞ"),toList(u"அஇஉஐஎகபமதநய"),[u"ஔ",u"ஓ",u"ஒ",u"வ",u"ங",u"ல",u"ர",u"ழ"]]
    shift_keys3rows = [[u"௧",u"௨",u"௩",u"௪",u"௫",u"௬",u"௭",u"௮",u"௯",u"௦",u"௰"],
                       [u"ஃ",u"ஸ",u"ஷ",u"ஜ",u"ஹ",u"க்ஷ",u"ஶ்ரீ",u"ஶ",u"ௐ",u"௱",u"௲"],
                       [u"௳",u"௴",u"௵",u"௶",u"௷",u"௸",u"௹",u"௺"]]
    def __init__(self):
        OSKeyboard.__init__(self,u"Tamil",TamilKeyboard.keys3rows,TamilKeyboard.shift_keys3rows)

class JointKeyboard:
    def __init__(self,parent_box,ed):
        self.parent_box = parent_box
        self.takbd = TamilKeyboard()
        self.enkbd = EnglishKeyboard()
        self.activekbd = self.takbd
        self.ed = ed

    def is_tamil_active(self):
        return self.activekbd == self.takbd

    def is_english_active(self):
        return self.activekbd == self.enkbd

    def build_kbd(self,numerickbd=False):
        self.clear_parent()
        self.activekbd.build_widget(self.parent_box,self.ed,numerickbd)
        self.setup_toggle_hooks()

    ############ logic functions ###########
    def setup_toggle_hooks(self):
        switch_btn = self.activekbd.keys3rows_btns[-1][1]
        switch_btn.connect("clicked", JointKeyboard.callback,self)

        num_btn = self.activekbd.keys3rows_btns[-1][0]
        num_btn.connect("clicked", JointKeyboard.numerickbd_callback,self)
        shift_btn = self.activekbd.keys3rows_btns[-2][0]
        shift_btn.connect("clicked", JointKeyboard.shift_callback,self)
        if self.activekbd.numericmode():
            shift_btn.hide()

    def clear_parent(self):
        kids = self.parent_box.get_children()
        for key_rows in kids[1:]:
            key_rows.destroy()

    def switch_kbd(self):
        if self.activekbd.numericmode():
            return

        if self.is_english_active():
            self.activekbd = self.takbd
        else:
            self.activekbd = self.enkbd

    @staticmethod
    def callback(*args):
        widget = args[0]
        instance = args[1]
        instance.switch_kbd()
        instance.build_kbd()
        return

    @staticmethod
    def shift_callback(*args):
        widget = args[0]
        instance = args[1]
        instance.activekbd.toggle_shift_mode()
        instance.build_kbd(numerickbd=False)
        pass

    @staticmethod
    def numerickbd_callback(*args):
        widget = args[0]
        instance = args[1]
        instance.build_kbd(numerickbd=True)
        return

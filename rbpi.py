#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import route, run, redirect, template, get, post, request # or route
from datetime import datetime
from os import environ

class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class LED:
    _v = None
    _logLED = None
    _LEDtable = None
    def __init__(self):
        self._v = False
        self._logLED = str(datetime.now()) + ' : ' + 'La led est éteinte'
        f = open('LEDtable.html', 'r')
        self._LEDtable = str(''.join(f.readlines()))
        f.close()
    def value(self):
        return 'Allumée' if self._v else 'Eteinte'
    def log(self):
        return self._logLED
    def set(self, v2):
        self._v = v2
    def reverse(self):
        self._v = not (self._v)
        self.updateLED()
    def updateLED(self):
        if self._v :
            self._logLED = self._logLED + "<br/>" + str(datetime.now()) + ' : ' + "La led s'allume"
        else :
            self._logLED = self._logLED + "<br/>" + str(datetime.now()) + ' : ' + "La led s'éteint"
    def showLEDtable(self):
        return self._LEDtable.format("PIN?",self.value(),LED.Instance().log(),"Utilisateur: " + environ["USERNAME"]) 

@get('/')
def index():
    return LED.Instance().showLEDtable()

@post('/refresh_index')
def refresh_index():
    LED.Instance().reverse()
    redirect("/")




run(host='0.0.0.0', port=8080, debug=True)
#!/usr/bin/python

import pyglet
from pyglet.window import key
from pyglet.window import mouse
from collections import deque

window = pyglet.window.Window(resizable=True)

label = pyglet.text.Label('Hello, world', font_name='Times New Roman',
    font_size=36, x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')

default_image = pyglet.resource.image('doc.png')

snippets = []

@window.event
def on_draw():
  window.clear()
  for snip in snippets:
    snip.draw()

@window.event
def on_key_press(symbol, modifiers):
 if symbol == key.ENTER:
    print 'The enter key was pressed.'

@window.event
def on_mouse_press(x, y, button, modifiers):
  if button == mouse.LEFT:
    idx = findTop(x, y)
    if idx >= 0:
      snip = snippets.pop(idx)
      snippets.append(snip)
      snippets[-1].set_anchor(x, y)
  if button == mouse.RIGHT:
    snippets.append( Snippet(x, y) )
  if button == mouse.MIDDLE:
    idx = findTop(x, y)
    if idx >= 0:
      snippets.pop(idx)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
  if button == mouse.LEFT:
    if snippets[-1].isInside(x - dx, y - dy):
      snippets[-1].position_anchor(x, y)
     
def findTop(x, y):
  found = -1
  for index, snip in enumerate(snippets):
    if snip.isInside(x, y):
      found = index
  return found

def selectTop(x, y):
  found = 0
  for snip in snippets:
    if snip.isInside(x, y):
      found = snip
  return found

class Snippet:
  def __init__(self, x, y):
    self.image = pyglet.sprite.Sprite(default_image)
    self.x = x
    self.y = y
    self.width = self.image.width
    self.height = self.image.height
  def draw(self):
    self.image.set_position(self.x, self.y)
    self.image.draw()
  def set_anchor(self, x, y):
    self.anchorX = x - self.x
    self.anchorY = y - self.y
  def position_anchor(self, x, y):
    self.x = x - self.anchorX
    self.y = y - self.anchorY
  def isInside(self, x, y):
    return  (x > self.x and x < self.x + self.width and 
        y > self.y and y < self.y + self.height)

class TextSnip(Snippet):
  def __init__(self, x, y, text):
    self.label = pyglet.text.Label(text, 
        font_name='Times New Roman',font_size=36, 
        x=x, y=y, anchor_x='left', anchor_y='bottom')
    self.x = x
    self.y = y
    self.height = label.height
    self.width = label.width
  def draw(self):
    self.label.x = x
    self.label.y = y
    self.label.draw()


pyglet.app.run()

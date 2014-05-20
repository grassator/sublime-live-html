#!
# live-html-sublime - v0.2.0 - 2014-05-20
# Copyright (c) 2014 Dmitriy Kubyshkin <dmitriy@kubyshkin.ru> 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sublime, sublime_plugin
import urllib.request

def content(view):
  "Returns content of given view"
  return view.substr(sublime.Region(0, view.size()))

def is_html_view(view):
  "Check if given view can be used for live HTML"
  return view.score_selector(0, 'text.html') > 0

def is_css_view(view):
  "Check if given view can be used for live HTML"
  return view.score_selector(0, 'source.css') > 0

def toggle_indicator(view, state):
  if state:
    view.set_status('live-html-active', '<LH>')
  else:
    view.erase_status('live-html-active')

def send_updated_html(view):
  try:
    details = urllib.parse.urlencode({
      'file': view.file_name(),
      'content': content(view),
      'version': '0.1'
    })
    details = details.encode('UTF-8')
    url = urllib.request.Request('http://' + LiveHtmlListener.host + ':' + str(LiveHtmlListener.port) + '/changed', details)
    stream = urllib.request.urlopen(url)
    stream.read()
    stream.close()
    toggle_indicator(view, True)
    return True
  except:
    return False

def check_live_html_server():
  url = urllib.request.Request('http://' + LiveHtmlListener.host + ':' + str(LiveHtmlListener.port) + '/status')
  stream = urllib.request.urlopen(url)
  stream.read()
  stream.close()

def set_offline_status(view):
  toggle_indicator(view, False)
  sublime.status_message('<Live HTML Server Offline>')

class LiveHtmlListener(sublime_plugin.EventListener):
  # Holds currently loaded views where live HTML is enabled
  enabled_views = set()
  port = 55555
  host = '127.0.0.1'

  def on_close(self, view):
    LiveHtmlListener.enabled_views.discard(view.id())

  def on_modified_async(self, view):
    if view.id() not in LiveHtmlListener.enabled_views:
      return
    if view.file_name():
      result = send_updated_html(view)
      if not result:
        set_offline_status(view)


class ToggleLiveHtmlCommand(sublime_plugin.TextCommand):  
  def run(self, edit):
    if not is_html_view(self.view) and not is_css_view(self.view):
      return
    if self.view.id() in LiveHtmlListener.enabled_views:
      LiveHtmlListener.enabled_views.remove(self.view.id())
      toggle_indicator(self.view, False)
    else:
      try:
        check_live_html_server()
        LiveHtmlListener.enabled_views.add(self.view.id())
        send_updated_html(self.view)
        toggle_indicator(self.view, True)
      except:
        set_offline_status(self.view)

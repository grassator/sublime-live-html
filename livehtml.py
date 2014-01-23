import sublime, sublime_plugin
import urllib  

# Holds currently loaded views where live HTML is enabled
enabled_views = []
port = 55555
host = '127.0.0.1'

def content(view):
  "Returns content of given view"
  return view.substr(sublime.Region(0, view.size()))

def is_html_view(view):
  "Check if given view can be used for live CSS"
  return view.score_selector(0, 'text.html') > 0

def toggle_indicator(view, state):
  if state:
    view.set_status('live-html-active', '~{LH}~')
  else:
    view.erase_status('live-html-active')

def send_updated_html(view):
  global port, host
  try:
    details = urllib.parse.urlencode({
      'file': view.file_name(),
      'content': content(view)
    })
    details = details.encode('UTF-8')
    url = urllib.request.Request('http://' + host + ':' + str(port) + '/changed', details)
    stream = urllib.request.urlopen(url)
    stream.read()
    stream.close()
    toggle_indicator(view, True)
    return True
  except:
    return False

def check_live_html_server():
  global port, host
  url = urllib.request.Request('http://' + host + ':' + str(port) + '/status')
  stream = urllib.request.urlopen(url)
  stream.read()
  stream.close()

class LiveHtmlListener(sublime_plugin.EventListener):
  def on_close(self, view):
    global enabled_views, active_view
    try:
      enabled_views.remove(view.id())
    except:
      return

  def on_modified_async(self, view):
    global enabled_views, active_view
    try:
      enabled_views.index(view.id())
    except:
      return
    if view.file_name():
      result = send_updated_html(view)
      if not result:
        toggle_indicator(view, False)
        sublime.status_message('~{Live HTML Server Offline}~')


class ToggleLiveHtmlCommand(sublime_plugin.TextCommand):  
  def run(self, edit):
    global enabled_views
    if not is_html_view(self.view):
      return
    try:
      enabled_views.remove(self.view.id())
      toggle_indicator(self.view, False)
    except:
      try:
        check_live_html_server()
        enabled_views.append(self.view.id())
        send_updated_html(self.view)
        toggle_indicator(self.view, True)
      except:
        sublime.status_message('~{Live HTML Server Offline}~')
        return

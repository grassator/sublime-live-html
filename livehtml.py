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
    view.set_status('live-html-active', '~{LH}~')
  else:
    view.erase_status('live-html-active')

def send_updated_html(view):
  try:
    details = urllib.parse.urlencode({
      'file': view.file_name(),
      'content': content(view)
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

class LiveHtmlListener(sublime_plugin.EventListener):
  # Holds currently loaded views where live HTML is enabled
  enabled_views = []
  port = 55555
  host = '127.0.0.1'

  def on_close(self, view):
    try:
      LiveHtmlListener.enabled_views.remove(view.id())
    except:
      return

  def on_modified_async(self, view):
    try:
      LiveHtmlListener.enabled_views.index(view.id())
    except:
      return
    if view.file_name():
      result = send_updated_html(view)
      if not result:
        toggle_indicator(view, False)
        sublime.status_message('~{Live HTML Server Offline}~')


class ToggleLiveHtmlCommand(sublime_plugin.TextCommand):  
  def run(self, edit):
    if not is_html_view(self.view) and not is_css_view(self.view):
      return
    try:
      LiveHtmlListener.enabled_views.remove(self.view.id())
      toggle_indicator(self.view, False)
    except:
      try:
        check_live_html_server()
        LiveHtmlListener.enabled_views.append(self.view.id())
        send_updated_html(self.view)
        toggle_indicator(self.view, True)
      except:
        sublime.status_message('~{Live HTML Server Offline}~')
        return

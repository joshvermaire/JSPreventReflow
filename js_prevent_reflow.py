'''
Provides front end developers with a visual tool for seeing what causes
layouts and reflows while writing javascript.

Config summary (see README.md for details):

    # key binding
    { "keys": ["ctrl+shift+t"], "command": "delete_trailing_spaces" }

    # file settings
    {
      "trailing_spaces_highlight_color": "invalid",
      "trailing_spaces_file_max_size": 1000
    }

@author: Jean-Denis Vauguet <jd@vauguet.fr>, Oktay Acikalin <ok@ryotic.de>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2011-02-25
'''

import sublime, sublime_plugin

DEFAULT_MAX_FILE_SIZE = 1048576
DEFAULT_COLOR_SCOPE_NAME = "invalid"
DEFAULT_IS_ENABLED = True

#Set whether the plugin is on or off
jspr_settings = sublime.load_settings('js_prevent_reflow.sublime-settings')
js_prevent_reflow_enabled = bool(jspr_settings.get('js_prevent_reflow_enabled', DEFAULT_IS_ENABLED))

# Determine if the view is a find results view
def is_find_results(view):
    return view.settings().get('syntax') and "Find Results" in view.settings().get('syntax')

# Return an array of regions matching trailing spaces.
def find_reflows(view):
    regex = '(clientHeight|clientLeft|clientTop|clientWidth|focus|getBoundingClientRect|getClientRects|innerText|offsetHeight|offsetLeft|offsetParent|offsetTop|offsetWidth|outerText|scrollByLines|scrollByPages|scrollHeight|scrollIntoView|scrollLeft|scrollTop|scrollWidth|getBoundingClientRect|getClientRects|getComputedStyle|scrollBy|scrollTo|scrollX|scrollY|webkitConvertPointFromNodeToPage|webkitConvertPointFromPageToNode)+'
    # include_empty_lines = bool(ts_settings.get('trailing_spaces_include_empty_lines', DEFAULT_IS_ENABLED))
    # return view.find_all('[ \t]+$' if include_empty_lines else '(?<=\S)[\t ]+$')
    return view.find_all(regex)

def highlight_reflows(view):
    max_size = jspr_settings.get('js_prevent_reflow_file_max_size', DEFAULT_MAX_FILE_SIZE)
    color_scope_name = jspr_settings.get('js_prevent_reflow_highlight_color', DEFAULT_COLOR_SCOPE_NAME)
    if view.size() <= max_size and not is_find_results(view):
        regions = find_reflows(view)
        view.add_regions('PreventReflowHighlightListener',
                         regions, color_scope_name,
                         sublime.DRAW_EMPTY)

# def highlight_(view):
#     max_size = jspr_settings.get('js_prevent_reflow_file_max_size', DEFAULT_MAX_FILE_SIZE)
#     color_scope_name = jspr_settings.get('js_show_reflow_highligh_color', DEFAULT_COLOR_SCOPE_NAME)
#     if view.size() <= max_size and not is_find_results(view):
#         regions = find_reflows(view)
#         view.add_regions('PreventReflowHighlightListener',
#                          regions, color_scope_name,
#                          sublime.DRAW_EMPTY)

# Clear all trailing spaces
def clear_reflows_highlight(window):
    for view in window.views():
        view.erase_regions('PreventReflowHighlightListener')

# Toggle the event listner on or off
class TogglePreventReflowCommand(sublime_plugin.WindowCommand):
    def run(self):
        global js_prevent_reflow_enabled
        js_prevent_reflow_enabled = False if js_prevent_reflow_enabled else True

        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if js_prevent_reflow_enabled:
            highlight_reflows(self.window.active_view())
        else:
            clear_reflows_highlight(self.window)

# Highlight matching regions.
class PreventReflowHighlightListener(sublime_plugin.EventListener):
  def on_modified(self, view):
    if js_prevent_reflow_enabled:
      highlight_reflows(view)

  def on_activated(self, view):
    if js_prevent_reflow_enabled:
      highlight_reflows(view)

  def on_load(self, view):
    if js_prevent_reflow_enabled:
      highlight_reflows(view)

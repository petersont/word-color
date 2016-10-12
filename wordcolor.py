import sublime
import sublime_plugin
import hashlib

def hash_string(s):
    return int(int(hashlib.md5(s).hexdigest(), 16)%360)

def get_scopename(h):
    return "explicit-hue-"+str(h)

class ColorerListener(sublime_plugin.EventListener):
    def redo(self, view):
        word_regions = view.find_all("[_A-Za-z][_a-zA-Z0-9]*")

        hash_to_region_list = {}
        for region in word_regions:
            h = hash_string(view.substr(region).encode('utf-8'))
            hash_to_region_list[h] = hash_to_region_list.get(h, []) + [region]

        for h in range(0, 360):
            view.erase_regions(get_scopename(h))

        for h, regions in hash_to_region_list.items():
            scopename = get_scopename(h)
            view.add_regions(scopename, regions, scopename, "", sublime.DRAW_NO_OUTLINE)

    def on_modified(self, view):
        self.redo(view)

    def on_activated(self, view):
        self.redo(view)


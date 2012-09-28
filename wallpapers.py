import os
import logging

from plugins import plugin_manager

class Wallpapers:

    def __init__(self, config):
        # TODO: Maybe shuffle the wallpaper_plugins list each time the last one in the list is used.
        self.config = config

        self.wallpaper_plugins = plugin_manager['WallpaperSearch']
        self.plugin_index = 0

        self.logger = logging.getLogger('root')

    def pop(self, count=1):
        if self.plugin_index >= len(self.wallpaper_plugins):
            self.plugin_index = 0

        wallpaper_plugin = self.wallpaper_plugins[self.plugin_index]

        self.plugin_index += 1

        return [wp for wp in wallpaper_plugin.pop(count)]

    def count(self):
        return sum([q.count() for q in self.wallpaper_plugins])


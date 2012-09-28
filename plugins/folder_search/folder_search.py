import random
import os

import pygame

from .. import WallpaperSearch

class FolderSearch(WallpaperSearch):
    def __init__(self):
        super(FolderSearch, self).__init__()

        self.index = -1

    def pop(self, count=1):
        self.logger.debug('popping %d images' % count)

        self._find_wallpapers()

        if self.index == -1:
            self._shuffle()

        i = 0
        while i < count:
            if self.index < len(self.wallpapers):
                wallpaper_path = self.wallpapers[self.index]
            else:
                wallpaper_path = self.wallpapers[self.index % len(self.wallpapers)]

            # Create pygame image
            try:
                wallpaper = self._image_from_path(wallpaper_path)
            except IOError:
                self.logger.Error('Failed to find wallpaper %s' % wallpaper)
                self.wallpapers.remove(wallpaper)
                continue

            self.index += 1
            i += 1

            yield wallpaper

    def _find_wallpapers(self):
        os.path.walk(self.config['path'], self._folder_visit, [])

        count = self.count()
        self.logger.debug('%s image%s in FolderSearch' % (count, '' if count == 1 else 's'))

    def _folder_visit(self, arg, dirpath, filenames):
        wallpaper_paths = [os.path.join(dirpath, filename) for filename in filenames]
        pushed_count = self._push(wallpaper_paths)

        if pushed_count:
            rel_dirpath = dirpath[len(self.config['path']):]
            self.logger.debug('%d wps pushed from %s' % (pushed_count, rel_dirpath if rel_dirpath else '\\'))

    def _push(self, wallpaper_paths):
        """ Push wallpaper paths on to the list, wallpaper_paths can be a single filepath or a list of paths """

        if not type(wallpaper_paths) is list:
            wallpaper_paths = [wallpaper_paths, ]

        c = 0
        for wp in wallpaper_paths:
            # Push it, if it isn't already on the list and has appropriate extension
            if not wp in self.wallpapers and self._check_extension(wp):
                c += 1
                self.wallpapers.append(wp)

        return c

    def _check_extension(self, filepath):
        extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'pcx', 'tga', 'tiff', 'tif', 'iff', 'xpm']
        for extension in extensions:
            try:
                if filepath.index(extension) == len(filepath) - len(extension):
                    return True
            except:
                pass

        return False

    def _shuffle(self):
        """ Shuffles the wallpaper queue """
        self.logger.debug('Shuffling wallpaper queue')

        random.shuffle(self.wallpapers)
        self.index = 0

# -*- coding: utf-8 -*-
import simplejson as json
import urllib2

__all__ = ['PanoramioAPI']

class PanoramioAPI(object):

    url = 'http://www.panoramio.com/map/get_panoramas.php'
    size = 'medium'
    set = 'full'
    radius = 5

    def __init__(self, set=None, size=None, map_filter=False, radius=None):
        '''
        Initialize method
        '''
        self.map_filter = map_filter
        if radius:
            self.radius = radius
        if set:
            self.set = self._validate_set(set)
        if size:
            self.size = self._validate_size(size)

    def search(self, lat=None, lng=None, radius=None, \
            minx=None, miny=None, maxx=None, maxy=None, \
            set=None, limit_from=0, limit_to=20, size=None, map_filter=False):
        '''
        Call API and search Panoramio photos in two ways:
            - by `lat`,`lng`,`radius` attributes
            - by `minx`,`miny`,`maxx`,`maxy` attributes

        # http://www.panoramio.com/map/get_panoramas.php?set=public&from=0&to=1&miny=50.046664&maxy=50.082636&minx=19.926994&maxx=19.962966
        >>> api = PanoramioAPI()
        >>> photos = api.search(set='public', limit_from=0, limit_to=10, miny=50.046664, maxy=50.082636, minx=19.926994, maxx=19.962966)
        >>> len(photos)
        10
        >>> photo = photos[0]
        >>> photos = api.search(set='public', limit_from=0, limit_to=1, lat=photo.get('latitude'), lng=photo.get('longitude'), radius=10)
        >>> len(photos)
        1
        >>> photos[0].get('photo_id') == photo.get('photo_id')
        True
        '''
        set = self._validate_set(set) if set else self.set
        size = self._validate_size(size) if size else self.size
        map_filter = map_filter or self.map_filter
        radius = radius or self.radius

        try:
            assert lat and lng and radius or minx and miny and maxx and maxy
            if (minx or miny or maxx or maxy) is None:
                minx, miny, maxx, maxy = self._calculate_bounds(lat, lng, radius)
        except AssertionError:
            raise ValueError('You need to specify attributes `lat`,`lng`,`radius` or `minx`,`miny`,`maxx`,`maxy`')

        self._params = {
            'set': set,
            'from': limit_from,
            'to': limit_to,
            'minx': minx,
            'miny': miny,
            'maxx': maxx,
            'maxy': maxy,
            'size': size,
            'mapfilter': map_filter,
        }

        request = urllib2.Request(url=self._get_url())
        response = urllib2.urlopen(request)
        content = response.read()
        return json.loads(content)['photos']

    def _get_url(self):
        url = self.url
        if self._params:
            url += '?' + '&'.join(['%s=%s' % (key, val) for key, val in self._params.items()])
#        print url
        return url

    def _calculate_bounds(self, lat, lng, radius):
        km = 0.0089930 # 1km
        return lng-radius/2*km, lat-radius/2*km, lng+radius/2*km, lat+radius/2*km

    def _validate_set(self, set):
        if set in ['public', 'full'] or isinstance(set, int):
            return set
        else:
            raise ValueError('Attribute `set` must be "public" (popular photos), "full" (all photos) or user ID number')

    def _validate_size(self, size):
        if size in ['original','medium','small','thumbnail','square','mini_square']:
            return size
        else:
            raise ValueError('Attribute `size` must be "original","medium","small","thumbnail","square" or "mini_square"')

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
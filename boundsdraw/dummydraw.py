
from collections.abc import Sequence
from numbers import Number


class DummyDraw(object):
    """
    A dummy null drawer.
    """
    
    _bounds = None

    @property
    def bounds(self):
        return self._bounds
    
    @bounds.setter
    def bounds(self, bounds):
        if not isinstance(bounds, Sequence) or len(bounds) not in (2, 4) \
                or any(not isinstance(c, Number) for c in bounds):
            raise ValueError("bounds must be a 2 or 4-tuple of Numbers")
        if len(bounds) == 2:
            self._bounds = (0.0, 0.0) + tuple(float(c) for c in bounds)
        else:
            self._bounds = tuple(float(c) for c in bounds)
        self._use(self._bounds)
    
    _offset = None

    @property
    def offset(self):
        return self._offset
        
    
    @offset.setter
    def offset(self, offset):
        if offset is not None \
                and (not isinstance(offset, Sequence) or len(offset) != 2 \
                or any(not isinstance(c, Number) for c in offset)):
            raise ValueError("offset must be a 2-tuple of Numbers")
        self._offset = self._bounds[:2] if offset is None else \
                       tuple(float(c) for c in offset)
        self._use(self._offset)

    _target = None
    
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, target):
        if target is not None \
                and (not isinstance(target, Sequence) or len(target) != 4 \
                or any(not isinstance(c, Number) for c in target)):
            raise ValueError("target must be a 4-tuple of Numbers")
        self._target = self._bounds if target is None else \
                       tuple(float(c) for c in target)
        self._use(self._target)

    _x0 = None
    _x1 = None
    _y0 = None
    _y1 = None

    @property
    def used(self):
        return (self._x0, self._y0, self_x1, self._y1)

    def _use_x(self, x):
        if self._x0 is None or self._x0 > x:
            self._x0 = float(x)
        if self._x1 is None or self._x1 < x:
            self._x1 = float(x)
        return self

    def _use_y(self, y):
        if self._y0 is None or self._y0 > y:
            self._y0 = float(y)
        if self._y1 is None or self._y1 < y:
            self._y1 = float(y)
        return self

    def _use(self, xy):
        if isinstance(xy, Sequence):
            n_xy = len(xy)
            if n_xy % 2 == 0 and all(isinstance(c, Number) for c in xy):
                for i in range(0, n_xy, 2):
                    self._use_x(xy[i]).self._use_y(xy[i+1])
                return self
            elif all(isinstance(c, Sequence) and len(c) == 2 for c in xy):
                for i in xy:
                    self._use_x(i[0]).self._use_y(i[1])
                return self
        raise ValueError("xy must be a tuple of Numbers or 2-tuples")
        
    def __init__(self, bounds=(0.0, 0.0), offset=None, target=None):
        self._x0 = self._y0 = self._x1 = self._y1 = None
        self.bounds = bounds
        self.offset = offset
        self.target = target

    def in_bounds(self, x, y):
        if self._bounds[0] > x or x >= self._bounds[2] \
                or self._bounds[1] > y or y >= self._bounds[3]:
            return False
        return True

    def in_target(self, x, y):
        if self._target[0] > x or x >= self._target[2] \
                or self._target[1] > y or y >= self._target[3]:
            return False
        return True

    def get(xy, mask=None):
        return None

    def put(self, xy, color=None, width=1.0, mode=None, mask=None):
        return self._use(xy)

    def line(self, xy, color=None, width=1.0, offset=0.0, mode=None, mask=None):
        return self._use(xy)

    def polygon(self, xy, fill=None, color=None, width=1.0, offset=0.0,
                mode=None, mask=None):
        return self._use(xy)

    def rectangle(self, xy, fill=None, color=None, width=1.0, offset=0.0,
                mode=None, mask=None):
        return self._use(xy)

    def ellipse(self, xy, fill=None, color=None, width=1.0, offset=0.0,
                mode=None, mask=None):
        return self._use(xy)



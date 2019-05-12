"""
Class `Ref` is the basis of a system for dynamically linking `albow.widgets.Control` classes with values to be
displayed and
edited. An instance of Ref is used as a starting point for constructing reference objects. There are a number of
different kinds of reference objects, depending on whether the underlying value is accessed through an

- attribute,
- item index or
- method call

All of these reference objects present a common interface, consisting of `get()` and
`set()` methods, that the `albow.widgets.Control` uses to access the value whenever it needs to display or update it.

The simplest way of using Ref is illustrated by the following example:

```python

velocity_ref  = Ref(vehicle).velocity
velocity_ctrl = IntField(ref=velocity_ref)

```

Here, the expression _Ref(vehicle)_ creates a reference source object from which reference objects can be
derived. Accessing the velocity attribute of this object creates an attribute reference object that refers to
the velocity attribute of the vehicle. This attribute reference object is then attached to an
`albow.input.IntField`. The result is that the `albow.input.IntField` will always display the current value of the
vehicle's velocity attribute, and if the user enters a new value into the field, vehicle's velocity attribute
will be updated.

Reference objects can themselves be a source for further reference objects. Suppose you have a multi-player
turn-taking game, and you want to display information about the player whose turn it is next. You might create
a reference object like this:

```python

score_ref = Ref(world).current_game.current_player.score

```

Here we assume that _world_ is a global object that doesn't change, but a game object is created each time a new
game starts, and its current_player attribute switches around as the game is played. This statement creates a
chain of reference objects culminating in an attribute reference for the attribute called score. Each time the
`get()` or `set()` method of this reference object is called, the corresponding chain of attribute lookups is
performed anew. So, if we attach our score_ref to a control, it will always display the score of the current
player of the current game, whatever those objects happen to be.

As well as attribute access, indexing and calling can also be performed on a reference source:

- `ref_source[index]`
    produces an item reference object that accesses an item of a sequence or mapping.

- `ref_source(args)`
    produces a call reference object that performs a call when its get() method is called. This kind of reference
    object is read-only. But, it can be used as a source of further reference objects that are read-write.

"""


class Ref:

    def __init__(self, base):
        """
         Creates a reference source object based on the given object. Reference objects can be derived from
         this reference source using the operations listed below.

        Args:
            base:  Derive from?
        """
        self.base = base

    def __getattr__(self, name):
        return AttrRef(self, name)

    def __getitem__(self, index):
        return ItemRef(self, index)

    def __call__(self, *args, **kwds):
        return CallRef(self, args, kwds)

    def __pos__(self):
        return RefCaller(self)

    def __repr__(self):
        return "Ref(%r)" % self.base

    def get(self):
        # print "%r.get()" % self ###
        return self.base


class AttrRef(Ref):

    def __init__(self, base, name):

        super().__init__(base)
        self.name = name

    def __repr__(self):
        return "AttrRef(%r, %r)" % (self.base, self.name)

    def get(self):
        print("%r.get()" % self)

        # Python 3 update
        # return getattr(self.base.get(), self.name)
        val = getattr(self.base, self.name)
        return val

    def set(self, value):
        # Python 3 udpate
        # setattr(self.base.get(), self.name, value)
        setattr(self.base, self.name, value)


class ItemRef(Ref):

    def __init__(self, base, index):

        super().__init__(base)
        self.index = index

    def __repr__(self):
        return "ItemRef(%r, %r)" % (self.base, self.index)

    def get(self):
        print("%r.get()" % self)
        return self.base.get()[self.index]

    def set(self, value):
        self.base.get()[self.index] = value


class CallRef(Ref):

    def __init__(self, base, args, kwds):

        super().__init__(base)
        self.args = args
        self.kwds = kwds

    def __repr__(self):
        return "CallRef(%r)" % self.base

    def get(self):
        print("%r.get()" % self)
        return self.base.get()(*self.args, **self.kwds)


class RefCaller:

    def __init__(self, base):
        self.base = base

    def __call__(self, *args, **kwds):
        return self.base.get()(*args, **kwds)

    def __repr__(self):
        return "+%s" % repr(self.base)

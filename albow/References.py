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

    testVehicle: TestVehicle = TestVehicle()

    velocityRef = AttrRef(base=testVehicle, name="velocity")
    self.logger.info("Created a velocity reference: %s", velocityRef)

    velocityControl: DummyControl = DummyControl(ref=velocityRef)
    self.logger.info("Created velocity control %s", velocityControl)
    #
    # Change the data model
    #
    testVehicle.velocity = 100

    self.assertTrue(velocityControl.get_value() == testVehicle.velocity, "Reference did not update control")
    #
    # Change the control
    #
    velocityControl.set_value(500)
    self.assertTrue(velocityControl.get_value() == testVehicle.velocity, "Control did not update reference")

    ```

Here, the expression AttrRef(base=testVehicle, _name="velocity"_ creates a reference source object from which
reference objects can be derived.

Accessing the velocity attribute of this object creates an attribute reference object that refers to
the velocity attribute of the vehicle. This attribute reference object is then attached to a
`DummyControl`. The result is that the `DummyControl` will always display the current value of the
vehicle's velocity attribute.

Additionally, if the user enters a new value into the field, the vehicle's velocity attributeis updated.



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

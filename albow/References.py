
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

The simplest way of using Ref is illustrated by the following example.

**Example 1**

------

```python
testVehicle = TestVehicle()

velocityRef = AttrRef(base=testVehicle, name="velocity")
self.logger.info("Created a velocity reference: %s", velocityRef)

velocityControl = DummyControl(ref=velocityRef)
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


Here, the expression _AttrRef(base=testVehicle, _name="velocity")_ creates a reference source object from which
reference objects can be derived.

Accessing the velocity attribute of this object creates an attribute reference object that refers to
the velocity attribute of the vehicle. This attribute reference object is then attached to a
`DummyControl`. The result is that the `DummyControl` will always display the current value of the
vehicle's velocity attribute.

Additionally, if the user enters a new value into the field, the vehicle's velocity attribute is updated.

As well as attribute access, indexing and calling can also be performed on a reference source:

**Example 2**

------


_itemRef[TEST_ITEM_INDEX]_ produces an item reference object that accesses an item of a sequence or mapping.

```python
    vehicleList = self.getVehicleList()

    itemRef = ItemRef(base=vehicleList, index=TEST_ITEM_INDEX)
    self.logger.info("Created: %s", itemRef)

    testItem = itemRef[TEST_ITEM_INDEX]
    self.logger.info("Retrieved: %s", testItem)
    self.assertEqual(first=vehicleList[TEST_ITEM_INDEX],
                     second=testItem,
                     msg="Did not retrieve the correct item.")

```

**Example 3**

------

_ref_source(args)_ produces a call reference object that performs a call when its get() method is called. This kind
of reference object is read-only.  However, it can be used as a source of further reference objects that are
_read-write_.


```python
    # More code to follow
```

"""

from albow.ItemRefInsertionException import ItemRefInsertionException


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
        return self.base[index]
        # return ItemRef(self, index)

    def __call__(self, *args, **kwds):
        return CallRef(self, args, kwds)

    def __pos__(self):
        return RefCaller(self)

    def __repr__(self):
        return "Ref(%r)" % self.base

    def get(self):
        print("%r.get()" % self)
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
        # Python 3 update
        # setattr(self.base.get(), self.name, value)
        setattr(self.base, self.name, value)


class ItemRef(Ref):

    def __init__(self, base, index):

        super().__init__(base)
        self.index = index

    def __repr__(self):
        return f"ItemRef({self.index}, {self.base})"

    def get(self):
        print("%r.get()" % self)
        return self.base[self.index]

    def set(self, value):
        if isinstance(value, self.__class__):
            self.base[self.index] = value
            print(f"ItemRef.index{self.index}, value{self.base}")
        else:
            ex: ItemRefInsertionException = ItemRefInsertionException(
                theIndex=self.index,
                theMessage="Type of insertion object does not match")
            raise ex


class CallRef(Ref):
    """
    TODO:  This is broken figure out how to fix it
    """
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

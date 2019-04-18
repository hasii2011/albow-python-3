#---------------------------------------------------------------------------
#
#   Albow - References to attributes and items
#
#---------------------------------------------------------------------------

class Ref(object):

	def __init__(self, base):
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
		#print "%r.get()" % self ###
		return self.base

#---------------------------------------------------------------------------

class AttrRef(Ref):

	def __init__(self, base, name):
		self.base = base
		self.name = name
	
	def __repr__(self):
		return "AttrRef(%r, %r)" % (self.base, self.name)

	def get(self):
		#print "%r.get()" % self ###
		return getattr(self.base.get(), self.name)
	
	def set(self, value):
		setattr(self.base.get(), self.name, value)

#---------------------------------------------------------------------------

class ItemRef(Ref):

	def __init__(self, base, index):
		self.base = base
		self.index = index
	
	def __repr__(self):
		return "ItemRef(%r, %r)" % (self.base, self.index)

	def get(self):
		#print "%r.get()" % self ###
		return self.base.get()[self.index]
	
	def set(self, value):
		self.base.get()[index] = value

#---------------------------------------------------------------------------

class CallRef(Ref):

	def __init__(self, base, args, kwds):
		self.base = base
		self.args = args
		self.kwds = kwds
	
	def __repr__(self):
		return "CallRef(%r)" % (self.base)

	def get(self):
		#print "%r.get()" % self ###
		return self.base.get()(*self.args, **self.kwds)

#---------------------------------------------------------------------------

class RefCaller(object):

	def __init__(self, base):
		self.base = base
	
	def __call__(self, *args, **kwds):
		return self.base.get()(*args, **kwds)
	
	def __repr__(self):
		return "+%s" % repr(self.base)


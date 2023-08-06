# abcplus

abcplus is an extended version of Python's stdlib `abc` module. It adds support for additional features that are
sometimes useful with Abstract Base Classes.

It is meant to supplant abc, so it has a copy of all the symbols from the default abc package.  So you can just do
an import alias and not modify working code:

    import abcplus as abc

Or you can import it directly if you want:

    from abcplus import ABCMeta, abstractmethod, abstractproperty, finalmethod


## @finalmethod

While it's rare, there are certain legitimate cases where you want to prevent a method from being overridden in
subclasses. Some other languages have a `final` keyword for this case. This module adds an @finalmethod decorator
which will prevent a subclass from declaring an overridden form of the method. There are workarounds that a developer
could use to avoid this check, so don't consider this absolute protection against it, but somewhat stronger than
a simple advisory comment.

    # Python 2 example

    import abcplus

    class Abstract(object):

        __metaclass__ = abcplus.ABCMeta

        @abcplus.finalmethod
        def run(self):
            self.prepare()
            self.execute()
            self.cleanup()

        @abcplus.abstractmethod
        def execute(self):
            pass

        def prepare(self):
            pass

        def cleanup(self):
            pass

    # Python 3 requires you to define the metaclass differently

    import abcplus

    class Abstract(object, metaclass=abcplus.ABCMeta):
        pass

    # or use six to add the metaclass in a way that works with both

    import abcplus
    import six

    @six.add_metaclass(abcplus.ABCMeta):
    class Abstract(object):
        pass

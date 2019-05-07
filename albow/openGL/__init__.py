"""
    Albow can be used in an OpenGL environment. To do this, create an OpenGL display surface
    (using pygame.display.set_mode() with OPENGL in the flags) and pass it to the constructor of your root
    widget. You can then add widgets derived from GLViewport to provide 3D drawing areas, as well as ordinary
    2D widgets.

    There are a few things to be aware of when mixing 2D and 3D widgets. When using OpenGL, Albow distinguishes three kinds
    of widgets:

    1. 3D widgets
        - [GLViewport](GLViewport)
        - [GLOrtho](albow.openGL.GLOrtho)
        - [GLPerspective](albow.openGL.GLPerspective)
        - Classes derived from them.

    2. 2D widgets -- most other Albow widgets. These are rendered to a temporary surface which is then transferred
        to the screen using `glDrawPixels`.

    3. Container widgets -- used for laying out other widgets. By default these are Row, Column, Grid and classes
        derived from them. The root widget is also considered a container widget.
        Container widgets and 3D widgets can have any kind of widget as a subwidget, but 2D widgets can only
        contain other 2D widgets.

    You can turn any 2D widget into a container widget by setting its is_gl_container property to true. However,
    when you do this, no drawing is performed for the widget itself -- its `bg_color` and `border` properties are
    ignored, and its `draw()` method is never called.

    You can also turn a container widget back into an ordinary 2D widget by setting its `is_gl_container` property
    to `False`. You might want to do this, for example, to give a Row of buttons a background or border.

    Something to keep in mind is that drawing on 2D surfaces and transferring them to an OpenGL window is usually
    much slower than drawing directly with OpenGL. So if you want high performance, try to keep the window area
    covered by 2D widgets to a minimum.

"""
"""
    Themes provide a centralized way of customising the appearance of Albow widgets on a per-class basis. There
    are three parts to the theme system:

    - Theme properties, which are attributes that get looked up
    automatically in the currently active themes
    - The Theme class, instances of which hold values for
    the theme properties of a particular class;
    - The theme module, which holds a default hierarchy of Theme instances that your application can replace.

    See the documentation pages on each of these for more details.


    ​```flow
    st=>start: Start
    op=>operation: Your Operation
    cond=>condition: Yes or No?
    e=>end

    st->op->cond
    cond(yes)->e
    cond(no)->op
    ​```

    """
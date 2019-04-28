
from albow.core.Screen import Screen
from albow.core.shell_tmp import Shell

from albow.themes.Theme import Theme

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.input.TextField import TextField


class DemoTextFieldsScreen(Screen):
    """
    Text Field
    """

    def __init__(self, shell: Shell):
        """

        :param shell:
        """
        attrs = {'bg_color': Theme.WHITE}
        #
        # Python 3 update
        #
        # Screen.__init__(self, shell)
        super().__init__(shell, **attrs)

        self.fld1 = self.add_field("Name", 200)
        self.fld2 = self.add_field("Race", 250)
        btn = Button("OK", action=self.ok)
        btn.rect.midtop = (320, 300)
        self.add(btn)
        out = Label("")
        out.rect.width = 400
        out.rect.topleft = (200, 350)
        self.out = out
        self.add(out)
        btn = Button("Menu", action=self.go_back)
        btn.rect.midtop = (320, 400)
        self.add(btn)
        self.fld1.focus()

    def add_field(self, label, pos):
        """

        :param label:
        :param pos:
        :return:
        """
        lbl = Label(label)
        lbl.rect.topleft = (200, pos)
        self.add(lbl)
        fld = TextField(150)
        fld.rect.topleft = (250, pos)
        fld.enter_action = self.ok
        self.add(fld)
        return fld

    def ok(self):
        self.out.text = "You are a %s called %s." % (self.fld2.text, self.fld1.text)

    def go_back(self):
        self.parent.show_menu()

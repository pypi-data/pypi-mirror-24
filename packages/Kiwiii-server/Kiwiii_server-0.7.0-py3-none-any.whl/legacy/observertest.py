# coding: UTF-8


class TableListener():
    def __init__(self, name, subject):
        self.name = name
        table.register(self)

    def update(self, event):
        print self.name, "was", event


class Table():
    def __init__(self):
        self.listeners = []
        self.data = None

    def register(self, listener):
        self.listeners.append(listener)

    def unregister(self, listener):
        self.listeners.remove(listener)

    def notify(self, event):
        for listener in self.listeners:
            listener.update(event)


class Command():
    def __init__(self, table):
        self.table = table

    def add_compound(self):
        self.table.data = "new_table"
        #table.notify("updated!")

# mainwindow?
table = Table()
command = Command(table)
#compane = TableListener("<compound pane>", table)
#tabpane = TableListener("<table pane>", table)
command.add_compound()
print table.data

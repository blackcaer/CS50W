from django.forms.utils import ErrorList

class HiddenErrorList(ErrorList):
    def __str__(self):
        return self.as_hidden()

    def as_hidden(self):
        return ''
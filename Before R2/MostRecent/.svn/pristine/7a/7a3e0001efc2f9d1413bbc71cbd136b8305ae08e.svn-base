from django.forms import ModelChoiceField

class RequestModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_requestor()

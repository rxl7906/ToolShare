from django.forms import ModelChoiceField

# Custom ModelChoiceField that shows the requestor for each tool for the approval/rejection forms
class RequestModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_requestor()

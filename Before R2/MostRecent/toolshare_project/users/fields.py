from django.forms import ModelChoiceField

# Custom ModelChoiceMenu that shows the community ratings
class CommunityModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_rating()

import json
from django.db.models.loading import get_model

def load_fixtures(file):
    json_data = open(file)   
    dict_list = json.load(json_data)
    for obj in dict_list:
        model = get_model(*obj['model'].split('.'))
        fields = obj['fields']
        for field in fields.keys():
            field_class = model._meta.get_field(field)
            if hasattr(field_class.rel, 'to'):
                fields[field+'_id'] = fields.pop(field)
        fields = fields.update({'id':obj['pk']})
        instance = model(**obj['fields'])
        instance.save()
import json

text_to_link = {}
def _decode_dict(a_dict):
    fields = a_dict.get('fields')
    if not fields:
        return a_dict
    if 'ctaLink' not in fields:
        return a_dict
    ctaLink = fields.get('ctaLink')['en-US']
    if ctaLink.startswith('/'):
        ctaLink = 'https://www.anyscale.com' + ctaLink
    text = ""
    body = fields.get('body')
    if body and isinstance(body['en-US'], str):
        text += str(body['en-US'])
    ctaText = fields.get('ctaText')
    if ctaText:
        text += ". " + ctaText['en-US']
    text_to_link[text] = ctaLink

    return a_dict

with open('../data.json') as f:
    json.load(f, object_hook=_decode_dict)

for text, link in text_to_link.items():
    ft = {
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful assistant that helps people convert a search query to a hyperlink. You are given the search query, and your goal is to find the corresponding hyperlink',
            },
            {
                'role': 'user',
                'content': text,
            },
            {
                'role': 'assistant',
                'content': link,
            },
        ]
    }
    print(json.dumps(ft))


class DictionaryResponse(object):

    def __init__(self,
                 response_dict):
        self.response_dict = response_dict

    def mandatory(self,
                  key):
        return self.response_dict[key]

    def optional(self,
                 key,
                 default=None):
        return self.response_dict.get(key, default)

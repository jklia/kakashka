class Fields:
    fields = []

    def __init__(self, field):
        self.fields.append(field)


field1 = [(1, 2, 'flag'), (1, 1, 'flag'), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, '')]

field2 = [(0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 2, 'house'), (1, 2, ''),
          (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 2, 'flag'), (1, 2, ''), (0, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 2, 'house'), (1, 2, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''),
          (0, 0, ''), (1, 2, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 2, ''), (1, 2, 'person'),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 2, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''),
          (0, 0, ''), (0, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''),
          (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''),
          (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 1, 'person'), (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''),
          (1, 1, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''), (1, 1, ''), (1, 1, ''), (1, 0, ''),
          (1, 0, ''), (0, 0, ''), (1, 1, ''), (1, 1, 'flag'), (0, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''),
          (0, 0, ''), (1, 1, ''), (1, 1, 'house'), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 1, ''), (1, 1, 'house'),
          (0, 0, '')]

field3 = [(0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, '')]

field4 = [(0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 0, 'tree'), (1, 2, 'flag'), (0, 0, ''), (0, 0, ''), (1, 0, 'tree'),
          (1, 0, 'tree'), (1, 2, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 1, 'flag'), (1, 0, ''), (1, 0, ''),
          (1, 2, 'house'), (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''),
          (0, 0, ''), (1, 1, 'house'), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 1, ''),
          (1, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 0, ''),
          (1, 0, 'tree'), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 1, ''), (1, 1, ''), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 1, ''), (1, 1, ''), (0, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''),
          (1, 1, 'tower'), (1, 0, 'tree'), (0, 0, ''), (1, 0, 'tree'), (1, 0, ''), (0, 0, ''), (1, 1, ''), (1, 1, ''),
          (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 1, 'knight'), (1, 1, ''), (0, 0, ''), (0, 0, ''), (1, 0, 'tree'),
          (1, 0, 'tree'), (1, 0, 'tree'), (1, 0, ''), (0, 0, ''), (1, 0, 'tree'), (1, 0, ''), (1, 0, ''), (0, 0, ''),
          (0, 0, ''), (1, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, 'tree'), (1, 0, ''), (0, 0, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, 'tree'), (0, 0, ''),
          (0, 0, ''), (0, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''),
          (1, 1, 'tree'), (1, 0, ''), (1, 0, 'tree'), (0, 0, ''), (1, 0, ''), (0, 0, ''), (0, 0, ''), (1, 1, ''),
          (1, 0, ''), (1, 0, ''), (1, 0, 'tree'), (0, 0, ''), (1, 1, ''), (1, 1, ''), (0, 0, ''), (1, 0, 'tree'),
          (1, 0, ''), (1, 1, 'tree'), (1, 2, 'tree'), (1, 1, ''), (1, 0, ''), (1, 1, 'lord'), (1, 1, 'tower'),
          (0, 0, ''), (1, 1, ''), (1, 1, 'lord'), (0, 0, ''), (0, 0, ''), (1, 1, 'knight'), (1, 1, 'tree'),
          (1, 2, 'tree'), (1, 2, 'tower'), (1, 2, 'tree'), (1, 1, 'house'), (1, 1, 'peasant'), (0, 0, ''),
          (1, 2, 'knight'), (1, 2, ''), (0, 0, ''), (0, 0, ''), (1, 1, 'flag'), (0, 0, ''), (1, 2, ''),
          (1, 2, 'peasant'), (1, 2, 'house'), (0, 0, ''), (0, 0, ''), (0, 0, ''), (0, 0, ''), (1, 2, 'flag'),
          (0, 0, '')]

Fields(field1)
Fields(field2)
Fields(field3)
Fields(field4)

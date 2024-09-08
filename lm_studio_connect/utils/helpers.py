""" Method get_short_name:
  - Returns the last section of the modelname
  """


def get_short_name(model):
    """Returns the last section of the modelname"""
    return model.rsplit("/", 1)[-1]

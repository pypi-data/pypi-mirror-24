import pickle
from hashlib import sha256

def hashcode(attributes, ignored_attributes=None):
    """
    
    """
    [attributes.pop(attr) for attr in ignored_attributes.keys()]
    attributes.sort(key= lambda x: x[0])

    hasher = sha256()
    hasher.update(pickle.dumps(attributes))
    return hasher.hexdigest()
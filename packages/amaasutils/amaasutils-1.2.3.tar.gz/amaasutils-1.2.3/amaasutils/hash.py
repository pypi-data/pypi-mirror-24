import pickle
from hashlib import sha256

def compute_hash(attributes, ignored_attributes=None):
    """
    
    """
    if ignored_attributes is None:
        ignored_attributes = {}

    [attributes.pop(attr) for attr in ignored_attributes.keys()]
    sorted_attributes = [(key, attributes[key]) for key in sorted(attributes.keys())]

    hasher = sha256()
    hasher.update(pickle.dumps(sorted_attributes))
    return hasher.hexdigest()
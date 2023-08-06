from scipy import io


def additional_info(data):
    if getattr(data, 'shape', False):
        return data.shape
    else:
        return type(data)


def drop_internals(data):
    return {key: value
            for key, value in data.items()
            if not key.startswith('__')}


def main(args):
    data = io.loadmat(args['<filename>'])
    data = drop_internals(data)
    for key in args['<key>']:
        data = data[key]
    for key, value in data.items():
        print('{}: {}'.format(key, additional_info(value)))

import os


def suite_resource(test_file, filename):
    return os.path.join(os.path.dirname(test_file), 'resources', filename)


def content_of(filename):
    with open(filename) as fp:
        return fp.read()

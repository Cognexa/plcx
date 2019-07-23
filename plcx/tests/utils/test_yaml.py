from plcx.utils.yaml import load_yaml


def test_load_yaml_file(tmpdir):
    """
    Test of load config from yaml file.

    :param tmpdir: temporary directory
    """
    with open(tmpdir.join('config.yaml'), 'w') as file:
        file.write('a: 1')

    config = load_yaml(tmpdir.join('config.yaml'))

    assert 'a' in config
    assert config['a'] == 1

from uwsgiconf.utils import UwsgiRunner, parse_command_plugins_output


SAMPLE_OUT_PLUGINS_MANY = '''

*** uWSGI loaded generic plugins ***
gevent
syslog
stats_pusher_socket

*** uWSGI loaded request plugins ***
0: python
173: rpc
--- end of plugins list ---

*** Starting uWSGI 2.0.15 (64bit) on [Fri Jul 28 20:05:53 2017] ***
compiled with version: 6.3.0 20170406 on 28 July 2017 20:04:29
'''

SAMPLE_OUT_PLUGINS_EMPTY = '''

*** uWSGI loaded generic plugins ***

*** uWSGI loaded request plugins ***
--- end of plugins list ---

*** Starting uWSGI 2.0.14-debian (64bit) on [Fri Jul 28 20:09:00 2017] ***
compiled with version: 6.3.0 20170221 on 27 February 2017 15:11:38
'''


def test_parser():
    plugins = parse_command_plugins_output(SAMPLE_OUT_PLUGINS_MANY)

    assert len(plugins.generic) == 3
    assert len(plugins.request) == 2
    assert 'rpc' in plugins.request

    plugins = parse_command_plugins_output(SAMPLE_OUT_PLUGINS_EMPTY)
    assert len(plugins.generic) == 0
    assert len(plugins.request) == 0


def test_runner(mock_popen):

    mock_popen(lambda: (SAMPLE_OUT_PLUGINS_MANY, ''))

    runner = UwsgiRunner()
    plugins = runner.get_plugins()
    assert len(plugins.generic) == 3
    assert len(plugins.request) == 2

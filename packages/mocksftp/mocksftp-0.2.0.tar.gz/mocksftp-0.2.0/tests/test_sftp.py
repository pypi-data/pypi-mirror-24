import os
import stat
import tempfile
import threading
import time

import py.path
from paramiko import SFTPAttributes
from pytest import fixture, raises


def files_equal(fname1, fname2):
    if os.stat(fname1).st_size == os.stat(fname2).st_size:
        with open(fname1, "rb") as f1, open(fname2, "rb") as f2:
            if f1.read() == f2.read():
                return True


def test_sftp_concurrent_connections(assert_num_threads, sftp_server):
    def connect():
        with sftp_server.client('sample-user') as client:
            sftp = client.open_sftp()
            for i in range(0, 3):
                assert sftp.listdir() == []
                time.sleep(0.2)
            sftp.close()
        time.sleep(0.1)

    threads = []
    for i in range(0, 5):
        thread = threading.Thread(target=connect, name='test-thread-%d' % i)
        thread.setDaemon(True)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    time.sleep(0.1)


def test_sftp_session(sftp_server):
    for uid in sftp_server.users:
        target_dir = tempfile.mkdtemp()
        target_fname = os.path.join(target_dir, "foo")
        assert not os.access(target_fname, os.F_OK)

        with sftp_server.client(uid) as c:
            sftp = c.open_sftp()
            sftp.put(__file__, target_fname, confirm=True)
            assert files_equal(target_fname, __file__)

            second_copy = os.path.join(target_dir, "bar")
            assert not os.access(second_copy, os.F_OK)
            sftp.get(target_fname, second_copy)
            assert files_equal(target_fname, second_copy)


@fixture(params=[("chmod", "/", 0o755),
                 ("chown", "/", 0, 0),
                 ("remove", "/etc/passwd"),
                 ("symlink", "/tmp/foo", "/tmp/bar"),
                 ("truncate", "/etc/passwd", 0),
                 ("unlink", "/etc/passwd"),
                 ("utime", "/", (0, 0))])
def unsupported_call(request):
    return request.param


def test_sftp_unsupported_calls(sftp_server, unsupported_call):
    for uid in sftp_server.users:
        with sftp_server.client(uid) as c:
            meth, args = unsupported_call[0], unsupported_call[1:]
            sftp = c.open_sftp()
            with raises(IOError) as exc:
                getattr(sftp, meth)(*args)
            assert str(exc.value) == "Operation unsupported", (
                "{0}() should be unsupported".format(meth))


def test_sftp_list_files(sftp_server, sftp_client):
    sftp = sftp_client.open_sftp()
    assert sftp.listdir('.') == []

    with open(os.path.join(sftp_server.root, 'dummy.txt'), 'w') as fh:
        fh.write('dummy-content')

    assert sftp.listdir('.') == ['dummy.txt']


def test_sftp_open_file(sftp_server, sftp_client):
    root_path = py.path.local(sftp_server.root)
    root_path.join('file.txt').write('content')

    sftp = sftp_client.open_sftp()
    assert sftp.listdir('.') == ['file.txt']

    data = sftp.open('file.txt', 'r')
    assert data.read() == b'content'


def test_sftp_mkdir(sftp_server, sftp_client):
    root_path = py.path.local(sftp_server.root)

    sftp = sftp_client.open_sftp()
    assert sftp.listdir('.') == []
    sftp.mkdir('the-dir')
    assert sftp.listdir('.') == ['the-dir']

    files = [f.basename for f in root_path.listdir()]
    assert files == ['the-dir']


def test_sftp_rmdir(sftp_server, sftp_client):
    root_path = py.path.local(sftp_server.root)
    root_path.join('the-dir').mkdir()

    sftp = sftp_client.open_sftp()
    assert sftp.listdir('.') == ['the-dir']

    sftp.rmdir('the-dir')
    assert sftp.listdir('.') == []


def test_sftp_stat(sftp_server, sftp_client):
    root_path = py.path.local(sftp_server.root)
    root_path.join('file.txt').write('content')

    sftp = sftp_client.open_sftp()
    statobj = sftp.lstat('file.txt')  # type: SFTPAttributes

    assert statobj.st_size == 7
    assert stat.S_IMODE(statobj.st_mode) == 0o644
    assert stat.S_IFMT(statobj.st_mode) == stat.S_IFREG  # regular file


def test_sftp_lstat(sftp_server, sftp_client):
    root_path = py.path.local(sftp_server.root)
    root_path.join('file.txt').write('content')
    root_path.join('symlink.txt').mksymlinkto('file.txt')

    sftp = sftp_client.open_sftp()
    statobj = sftp.lstat('symlink.txt')  # type: SFTPAttributes

    assert statobj.st_size == 8  # symlink size!
    assert stat.S_IFMT(statobj.st_mode) == stat.S_IFLNK  # symlink

    sftp = sftp_client.open_sftp()
    statobj = sftp.stat('symlink.txt')  # type: SFTPAttributes

    # Apply default umask in testing modes,
    # in case it's not set (e.g. docker container)
    assert statobj.st_size == 7
    assert stat.S_IMODE(statobj.st_mode) & ~0o022 == 0o644
    assert stat.S_IFMT(statobj.st_mode) == stat.S_IFREG  # regular file


def test_sftp_readlink(sftp_server, sftp_client):
    root_path = py.path.local(sftp_server.root)
    root_path.join('file.txt').write('content')
    root_path.join('symlink.txt').mksymlinkto('file.txt')

    sftp = sftp_client.open_sftp()
    assert sftp.readlink('symlink.txt') == 'file.txt'


def test_sftp_rename(sftp_server, sftp_client):
    root_path = py.path.local(sftp_server.root)
    root_path.join('file.txt').write('content')

    sftp = sftp_client.open_sftp()
    sftp.rename('file.txt', 'new.txt')

    files = [f.basename for f in root_path.listdir()]
    assert files == ['new.txt']

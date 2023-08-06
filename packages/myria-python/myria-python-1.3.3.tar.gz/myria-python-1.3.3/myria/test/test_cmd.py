from httmock import urlmatch, HTTMock
from json import dumps as jstr, loads
from myria.cmd import upload_file
from myria.errors import MyriaError
from nose.tools import eq_, assert_raises
from scripttest import TestFileEnvironment
import sys


class NullWriter:
    def write(self, s):
        pass


class QuietStderr:
    def __enter__(self):
        self.old_stderr = sys.stderr
        sys.stderr = NullWriter()

    def __exit__(self, type, value, traceback):
        sys.stderr = self.old_stderr


class TestCmd():
    def test_script(self):
        with HTTMock(mock_TwitterK):
            env = TestFileEnvironment('myria_upload')
            res = env.run('''myria_upload --relation TwitterK --program test
                          --overwrite --hostname localhost
                          --port 12345 --dry''', stdin='foo,bar\n1,b\n3,c',
                          expect_stderr=True)
            print res.stderr
            eq_(res.stdout, '''1,b\n3,c\n''')

    def test_parse_bad_args(self):
        with QuietStderr():
            # Missing one or both required arguments
            with assert_raises(SystemExit):
                args = upload_file.parse_args()
            with assert_raises(SystemExit):
                try:
                    args = upload_file.parse_args(['nosuchfile'])
                except IOError:
                    raise SystemExit()

            # Illegal file
            with assert_raises(SystemExit):
                try:
                    args = upload_file.parse_args(['--relation', 'tmp',
                                                   'nosuchfile'])
                except IOError:
                    raise SystemExit()

            # Bad port
            with assert_raises(SystemExit):
                args = upload_file.parse_args(['--relation', 'tmp',
                                               '--port', 'abc',
                                               'testdata/TwitterK.csv'])
            with assert_raises(SystemExit):
                args = upload_file.parse_args(['--relation', 'tmp',
                                               '--port', '-1',
                                               'testdata/TwitterK.csv'])
            with assert_raises(SystemExit):
                args = upload_file.parse_args(['--relation', 'tmp',
                                               '--port', '65536',
                                               'testdata/TwitterK.csv'])

    def test_parse_good_args(self):
        args = upload_file.parse_args(['--relation', 'tmp',
                                       'testdata/TwitterK.csv'])
        eq_(args.hostname, 'rest.myria.cs.washington.edu')
        eq_(args.port, 1776)
        eq_(args.program, 'adhoc')
        eq_(args.user, 'public')
        eq_(args.program, 'adhoc')
        eq_(args.relation, 'tmp')
        eq_(args.overwrite, False)
        eq_(args.ssl, True)

        args = upload_file.parse_args(['--relation', 'tmp',
                                       '--program', 'face',
                                       '--user', 'mom',
                                       '--overwrite',
                                       '--hostname', 'localhost',
                                       '--port', '12345',
                                       '--no-ssl',
                                       'testdata/TwitterK.csv'])
        eq_(args.hostname, 'localhost')
        eq_(args.port, 12345)
        eq_(args.user, 'mom')
        eq_(args.program, 'face')
        eq_(args.relation, 'tmp')
        eq_(args.overwrite, True)
        eq_(args.ssl, False)

    def test_TwitterK_csv(self):
        with HTTMock(mock_TwitterK):
            upload_file.main(['--relation', 'TwitterK',
                              '--program', 'testp',
                              '--user', 'test',
                              '--overwrite',
                              '--hostname', 'localhost',
                              '--port', '12345',
                              'testdata/TwitterK.csv'])

    def test_existing_file(self):
        with HTTMock(mock_TwitterK):
            with assert_raises(MyriaError):
                upload_file.main(['--relation', 'TwitterK',
                                  '--program', 'testp',
                                  '--user', 'test',
                                  '--hostname', 'localhost',
                                  '--port', '12345',
                                  'testdata/TwitterK.csv'])

    def test_TwitterKnoheader_csv(self):
        with HTTMock(mock_TwitterK):
            upload_file.main(['--relation', 'TwitterKnoheader',
                              '--program', 'testp',
                              '--user', 'test',
                              '--overwrite',
                              '--hostname', 'localhost',
                              '--port', '12345',
                              'testdata/TwitterK-noheader.csv'])

    def test_plaintext(self):
        with HTTMock(mock_TwitterK):
            upload_file.main(['--relation', 'plaintext',
                              '--program', 'testp',
                              '--user', 'test',
                              '--overwrite',
                              '--hostname', 'localhost',
                              '--port', '12345',
                              'testdata/plaintext.csv'])

    def test_float(self):
        with HTTMock(mock_TwitterK):
            upload_file.main(['--relation', 'float',
                              '--program', 'testp',
                              '--user', 'test',
                              '--overwrite',
                              '--hostname', 'localhost',
                              '--port', '12345',
                              'testdata/float.txt'])

    def test_null(self):
        with HTTMock(mock_TwitterK):
            upload_file.main(['--relation', 'nulls',
                              '--program', 'testp',
                              '--user', 'test',
                              '--overwrite',
                              '--hostname', 'localhost',
                              '--port', '12345',
                              'testdata/nulls.txt'])

    def test_locale_us(self):
        with HTTMock(mock_TwitterK):
            upload_file.main(['--relation', 'us',
                              '--program', 'testp',
                              '--user', 'test',
                              '--overwrite',
                              '--hostname', 'localhost',
                              '--port', '12345',
                              '--locale', 'en_US',
                              'testdata/us.txt'])

    def test_locale_de(self):
        with HTTMock(mock_TwitterK):
            upload_file.main(['--relation', 'de',
                              '--program', 'testp',
                              '--user', 'test',
                              '--overwrite',
                              '--hostname', 'localhost',
                              '--port', '12345',
                              '--locale', 'de_DE',
                              'testdata/de.txt'])


def get_field(fields, name):
    (name, value, content_type) = fields[name]
    if content_type == 'application/json':
        return loads(value)
    return value


@urlmatch(netloc=r'localhost:12345')
def mock_TwitterK(url, request):
    if url.path == '/dataset':
        fields = dict(request.body.fields)
        relation_key = get_field(fields, 'relationKey')
        schema = get_field(fields, 'schema')
        overwrite = get_field(fields, 'overwrite')
        if not overwrite:
            return {'status_code': 409,
                    'content': 'That dataset already exists.'}
        eq_(relation_key['userName'], 'test')
        eq_(relation_key['programName'], 'testp')
        if relation_key['relationName'] == 'TwitterK':
            eq_(schema['columnNames'], ['src', 'dst'])
            eq_(schema['columnTypes'], ['LONG_TYPE', 'LONG_TYPE'])
        elif relation_key['relationName'] == 'TwitterKnoheader':
            eq_(schema['columnNames'], ['column0', 'column1'])
            eq_(schema['columnTypes'], ['LONG_TYPE', 'LONG_TYPE'])
        elif relation_key['relationName'] == 'plaintext':
            eq_(schema['columnNames'], ['number', 'value'])
            eq_(schema['columnTypes'], ['LONG_TYPE', 'STRING_TYPE'])
        elif relation_key['relationName'] == 'float':
            eq_(schema['columnNames'], ['field1', 'field2'])
            eq_(schema['columnTypes'], ['DOUBLE_TYPE', 'DOUBLE_TYPE'])
        elif relation_key['relationName'] == 'nulls':
            eq_(schema['columnNames'], ['field1', 'field2', 'field3'])
            eq_(schema['columnTypes'],
                ['LONG_TYPE', 'STRING_TYPE', 'STRING_TYPE'])
        elif relation_key['relationName'] in ['us', 'de']:
            eq_(schema['columnNames'], ['field1', 'field2'])
            eq_(schema['columnTypes'], ['DOUBLE_TYPE', 'LONG_TYPE'])
        else:
            assert False
        return jstr("ok")
    return None

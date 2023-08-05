import tempfile
import shutil
import os

from molotov import quickstart, __version__, run
from molotov.tests.support import set_args, TestLoop


class TestQuickStart(TestLoop):
    def setUp(self):
        super(TestQuickStart, self).setUp()
        self._curdir = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        self._answers = ['y', 'welp', self.tempdir]

    def tearDown(self):
        os.chdir(self._curdir)
        shutil.rmtree(self.tempdir)
        super(TestQuickStart, self).tearDown()

    def _input(self, text):
        if self._answers == []:
            self._answers = ['y', 'welp', self.tempdir]
        answer = self._answers.pop()
        return answer

    def test_version(self):
        quickstart._input = self._input

        with set_args('molostart', '--version') as out:
            try:
                quickstart.main()
            except SystemExit:
                pass
        output = out[0].read().strip()
        self.assertEqual(output, __version__)

    def test_generate(self):
        quickstart._input = self._input

        with set_args('molostart'):
            quickstart.main()

        result = os.listdir(self.tempdir)
        result.sort()
        self.assertEqual(result, ['Makefile', 'loadtest.py', 'molotov.json'])

        # second runs stops
        with set_args('molostart'):
            try:
                quickstart.main()
                raise AssertionError()
            except SystemExit:
                pass

    def test_codeworks(self):
        quickstart._input = self._input

        with set_args('molostart'):
            quickstart.main()

        result = os.listdir(self.tempdir)
        result.sort()
        self.assertEqual(result, ['Makefile', 'loadtest.py', 'molotov.json'])

        os.chdir(self.tempdir)
        with set_args('molotov', '-cxv', '--max-runs', '1'):
            try:
                run.main()
            except SystemExit:
                pass

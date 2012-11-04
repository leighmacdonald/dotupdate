import unittest
from os import mkdir
from os.path import exists, join
from shutil import rmtree
from dotupdate import install

class TestInstall(unittest.TestCase):
    source_root = './test_dotfiles'
    dest_root = './test_home'

    def setUp(self):
        if exists(self.source_root):
            rmtree(self.source_root)
        mkdir(self.source_root)
        for d in ['dir1', 'dir2', 'dir2/subdir1']:
            mkdir(join(self.source_root, d))
        open(join(self.source_root, 'file.test'), 'w').write("x" * 100)
        open(join(self.source_root, 'dir1', 'file2.test'), 'w').write("x" * 100)

    def tearDown(self):
        rmtree(self.source_root)
        rmtree(self.dest_root)

    def test_install(self):
        install(self.source_root, dest_path=self.dest_root)
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()

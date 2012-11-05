import unittest
from os import mkdir
from os.path import exists, join, lexists
from shutil import rmtree
from dotupdate import install, InvalidConfiguration

class TestInstall(unittest.TestCase):
    source_root = './test_dotfiles'
    dest_root = './test_home'

    def setUp(self):
        if exists(self.source_root):
            rmtree(self.source_root)
        mkdir(self.source_root)
        if exists(self.dest_root):
            rmtree(self.dest_root)
        mkdir(self.dest_root)
        for d in ['dir1', 'dir2', 'dir2/subdir1']:
            mkdir(join(self.source_root, d))
        open(join(self.source_root, 'file.test'), 'w').write("hi")
        open(join(self.source_root, 'dir1', 'file2.test'), 'w').write("hi")

    def tearDown(self):
        rmtree(self.source_root)
        rmtree(self.dest_root)

    def test_install(self):
        install(self.source_root, dest_path=self.dest_root, dry_run=False)
        for path in [join(self.dest_root, '.file.test'),
                     join(self.dest_root, '.dir1', 'file2.test'),
                     join(self.dest_root, '.dir2', 'subdir1')]:
            self.assertTrue(lexists(path))

    def test_no_link_install(self):
        with self.assertRaises(InvalidConfiguration):
            install(source_path=join(self.dest_root, '.dir1'), dest_path=self.dest_root)

if __name__ == '__main__':
    unittest.main()

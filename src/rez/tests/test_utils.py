# Copyright Contributors to the Rez project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
unit tests for 'utils.filesystem' module
"""
import os
from rez.tests.util import TestBase
from rez.utils import filesystem
from rez.utils.platform_ import Platform, platform_


class TestCanonicalPath(TestBase):
    class CaseSensitivePlatform(Platform):
        @property
        def has_case_sensitive_filesystem(self):
            return True

    class CaseInsensitivePlatform(Platform):
        @property
        def has_case_sensitive_filesystem(self):
            return False

    def test_win32_case_insensitive(self):
        if platform_.name != 'windows':
            self.skipTest('on linux/macos, `os.path.realpath()` treats windows '
                          'abspaths as relpaths, and prepends `os.getcwd()`')
        platform = self.CaseInsensitivePlatform()
        path = filesystem.canonical_path('C:\\dir\\File.txt', platform)
        expects = 'c:\\dir\\file.txt'.replace('\\', os.sep)
        self.assertEqual(path, expects)

    def test_unix_case_sensistive_platform(self):
        if platform_.name == 'windows':
            self.skipTest('on windows, `os.path.realpath()` treats unix abspaths '
                          'as relpaths, and prepends `os.getcwd()`')
        platform = self.CaseSensitivePlatform()
        path = filesystem.canonical_path('/a/b/File.txt', platform)
        expects = '/a/b/File.txt'.replace('\\', os.sep)
        self.assertEqual(path, expects)

    def test_unix_case_insensistive_platform(self):
        if platform_.name == 'windows':
            self.skipTest('on windows, `os.path.realpath()` treats unix abspaths '
                          'as relpaths, and prepends `os.getcwd()`')
        platform = self.CaseInsensitivePlatform()
        path = filesystem.canonical_path('/a/b/File.txt', platform)
        expects = '/a/b/file.txt'.replace('\\', os.sep)
        self.assertEqual(path, expects)

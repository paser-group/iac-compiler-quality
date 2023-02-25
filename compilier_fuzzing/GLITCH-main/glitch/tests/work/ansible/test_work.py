import unittest

from glitch.analysis.security import SecurityVisitor
from glitch.analysis.design import DesignVisitor
from glitch.parsers.cmof import AnsibleParser
from glitch.tech import Tech

class TestWork(unittest.TestCase):
    def __help_test(self, path, type, n_errors, codes, lines):
        parser = AnsibleParser()
        inter = parser.parse(path, type, False)
        analysis = SecurityVisitor(Tech.ansible)
        analysis.config("GLITCH-main/glitch/configs/default.ini")
        errors = list(filter(lambda e: e.code.startswith('sec_'), set(analysis.check(inter))))
        errors = sorted(errors, key=lambda e: (e.path, e.line, e.code))
        self.assertEqual(len(errors), n_errors)
        for i in range(n_errors):
            self.assertEqual(errors[i].code, codes[i])
            self.assertEqual(errors[i].line, lines[i])  
    
    def test_ansible_http(self):
        self.__help_test(
            "GLITCH-main/glitch/tests/work/ansible/files/chatgpt_1.yaml",
            "tasks",
            1, ["sec_https"], [4]
        )


if __name__ == '__main__':
    unittest.main()
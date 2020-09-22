import unittest
import requests

from subprocess import run, PIPE

import re
class TestStringMethods(unittest.TestCase):

    def test_healthy(self):
        result = requests.get('http://ci-test-workspace:8080/healthy')
        print(result.status_code)
        self.assertEqual(result.status_code, 200)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOo'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_tool_access(self):
        # Test whether tools are accessible
        result = requests.get('http://ci-test-workspace:8091/tools/vnc/?password=vncpassword')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<title>Desktop VNC</title>', result.text)

        result = requests.get('http://ci-test-workspace:8091/tools/vscode/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Microsoft Corporation', result.text)

        result = requests.get('http://ci-test-workspace:8080/tooling/ssh/setup-command?origin=http://localhost:8080')
        self.assertEqual(result.status_code, 200)
        self.assertIn('/bin/bash', result.text)
        ssh_script_runner_regex = r'^\/bin\/bash <\(curl -s --insecure "(http:\/\/ci-test-workspace:8091\/shared\/ssh\/setup\?token=[a-z0-9]+&host=ci-test-workspace&port=8091"\))$'
        pattern = re.compile(ssh_script_runner_regex)
        match = pattern.match(result.text)
        self.assertIsNotNone(match)
        #self.assertRegex(result.text, ssh_script_runner_regex)
        
        # Execute the ssh setup script and automatically pass an ssh connection name to the script
        script_url = match.groups()[0]
        r = requests.get(script_url)
        with open('/setup-ssh.sh', 'w') as f:
            f.write(r.text)
            # r can now be executed
        ssh_connection_name = 'test'
        completed_process = run(['/bin/bash -c "/setup-ssh.sh"'], input=ssh_connection_name, encoding='ascii', shell=True, stdout=PIPE, stderr=PIPE)
        output = completed_process.stdout
        self.assertIn('Connection successful!', output)

if __name__ == '__main__':
    unittest.main()
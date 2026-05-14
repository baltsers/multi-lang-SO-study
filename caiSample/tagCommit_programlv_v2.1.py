import os
import pandas as pd
import subprocess
from subprocess import Popen, PIPE, STDOUT
import re
import shutil
import ast
import keyword
import sys
import logging
import time

PROJECT_PATH = "./project"
# PROJECT_PATH = "./project_"+str(sys.argv[1])
COMMIT_PATH = "../"
GITCLONE_URL = "https://github.com/"
JOERNPATH = "/opt/joern/joern-cli"
C_KEYWORDS = ["auto","short","int","long","float","double","char","struct","union","enum","typedef","const","unsigned","signed","extern","register","static","volatile","void","if","else","switch","case","for","do","while","goto","continue","break","default","sizeof","return"]
C_API_O=set() #sets
PY_API_O=set()
C_API_M=set()
PY_API_M=set()
Line_File_O = {} #dictionary to save line number and file name mapping
Line_File_M = {}
Line_Ident_O = {} #dictionary to save line number and identifiers mapping
Line_Ident_M = {}
Codechange_Files = set()#set to save the name of file which has code changes

def initAPI(repo_name):
    output = exe_command(
        "cd " + PROJECT_PATH + "/version_modified/" + repo_name + " && find . -name \"*.h\" | xargs grep -rE '^(\w+ )?\w+ (\w+ )?\w+( )?\(.*)' ./ -o | grep -v static")
    apis = re.split(r'\$\#\$', output[0])
    global C_API_M
    for api in apis:
        C_API_M.add((api.split('(')[0]).split(' ')[-1])



    f = open("./APIList.txt")
    global PY_API_M
    apis = f.readlines()
    for api in apis:
        PY_API_M.add(api.split('(')[0])

    output = exe_command(
        "cd " + PROJECT_PATH + "/version_origin/" + repo_name + " && find . -name \"*.h\" | xargs grep -rE '^(\w+ )?\w+ (\w+ )?\w+( )?\(.*)' ./ -o | grep -v static")
    apis = re.split(r'\$\#\$', output[0])
    global C_API_O
    for api in apis:
        C_API_O.add((api.split('(')[0]).split(' ')[-1])


    f = open("./APIList.txt")
    global PY_API_O
    apis = f.readlines()
    for api in apis:
        PY_API_O.add(api.split('(')[0])

def exe_command(command):
    print("command: "+command)
    process = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    result = ""
    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            try:
                result = result + line.decode().strip() + "$#$"
                print(line.decode().strip())
            except Exception as e:
                pass
    exitcode = process.wait()
    return result, process, exitcode

def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

def loadCommitSHA_and_repoName(path):
    # data1 = pd.read_csv(path + './Cpp+Python_issues_closed.csv')
    # data2 = pd.read_csv(path + './Cpp+Python_issues_open.csv')
    # sha_list1 = list(data1['commit_sha'])
    # sha_list2 = list(data2['commit_sha'])
    # repo_list1 = list(data1['repo_fullname'])
    # repo_list2 = list(data2['repo_fullname'])
    # return sha_list1 + sha_list2, repo_list1+repo_list2:q
    data = pd.read_csv(path + './tagged_commit.csv')
    sha_list = list(data['commit_sha'])
    repo_list = list(data['repo_fullname'])
    return sha_list, repo_list

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("folder create success")
    else:
        print("folder already exist")
        
def rmdir(path):
    shutil.rmtree(path, onerror=remove_readonly)
    folder = os.path.exists(path)
    if not folder:
        print("folder removed")
    else:
        print("folder remove failed")

def addToCsv(sha, repo_name, tag, memo):
    sha_list = []
    repo_list = []
    tag_list = []
    memo_list = []
    sha_list.append(sha)
    repo_list.append(repo_name)
    tag_list.append(tag)
    memo_list.append(memo)
    tag_result = pd.DataFrame({'sha': sha_list,
                               'repo_name':repo_list,
                                 'tag': tag_list,
                                 'memo': memo_list})
    tag_result.to_csv("Cpp+Python_commits_tag_result.csv", mode='a', header=False, index=False, sep=',')
    # tag_result.to_csv("Cpp+Python_commits_tag_result_"+ str(sys.argv[1]) +".csv", mode='a', header=False, index=False, sep=',')

def downloadProject(git_url, sha, repo_name):
    # pwd = exe_command("pwd")
    exe_command("cd " + PROJECT_PATH + "/version_modified && git clone "+ git_url)
    exe_command("cd " + PROJECT_PATH + "/version_modified/" + repo_name + " && git fetch origin "+ sha)
    exe_command("cd " + PROJECT_PATH + "/version_modified/" + repo_name + "&& git reset --hard " + sha)

def checkChangeinCPy(sha,repo_name):
    output = exe_command("cd " + PROJECT_PATH + "/version_modified/" + repo_name + " && git show "+ sha)
    lines = re.split(r'\$\#\$',output[0])
    for line in lines:
        if line.startswith('+++ ') or line.startswith('--- '):
            line_list = line.split('/')
            if (line_list[-1].endswith('.c')) or (line_list[-1].endswith('.py')) or (line_list[-1].endswith('.cc')):
                print(line_list[-1])
                return True
                break
    return False

def downloadoringin(git_url, repo_name):
    output = exe_command("cd " + PROJECT_PATH + "/version_modified/" + repo_name + " && git log -2 --pretty=format:\"%H\"")
    result = output[0]
    lines = re.split(r'\$\#\$',output[0])
    sha = lines[1]
    exe_command("cd " + PROJECT_PATH + "/version_origin && git clone "+ git_url)
    exe_command("cd " + PROJECT_PATH + "/version_origin/" + repo_name + " && git fetch origin "+ sha)
    exe_command("cd " + PROJECT_PATH + "/version_origin/" + repo_name + " && git reset --hard " + sha)

def findAllFile(path):
    for root, ds, fs in os.walk(path):
        for f in fs:
            yield f


def getCodeChangeLine(sha,repo_name):
    mkdir(PROJECT_PATH + "/version_modified/codechange")
    mkdir(PROJECT_PATH + "/version_origin/codechange")
    output = exe_command("cd " + PROJECT_PATH + "/version_modified/" + repo_name + " && git show "+ sha)
    lines = re.split(r'\$\#\$',output[0])
    filename = ""
    global Codechange_Files
    for line in lines:
        if line.startswith('+++ ') or line.startswith('--- '):
            line = line.replace(" ","")
            line = line.replace("+++","")
            line = line.replace("---", "")
            line_list = line.split('/')
            if line_list[-1].endswith('c') or line_list[-1].endswith('py'):
                filename = line_list[-1]
        elif line.startswith('+'):
            if filename != "" and filename.endswith('c'):
                # idents = pd.read_csv(PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(filename) + ".csv")
                # idents_list = idents['identifier']
                # line_idents_list = re.findall(r'\w+', line)
                # names = []
                # for ident in idents_list:
                #     if ident in line_idents_list:
                #         names.append(ident)
                identifiers = pd.DataFrame({'identifier': [line.replace("+","").replace(" ","").replace('\"','')]})
                identifiers.to_csv(PROJECT_PATH + "/version_modified/codechange/codechange_identifiers_" + str(filename) + ".csv",mode='a',header=False, index=False, sep=',')
                Codechange_Files.add(filename)
            elif filename != "" and filename.endswith('py'):
                # idents = pd.read_csv(PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(filename) + ".csv")
                # idents_list = idents['identifier']
                # line_idents_list = re.findall(r'\w+', line)
                # names = []
                # for ident in idents_list:
                #     if ident in line_idents_list:
                #         names.append(ident)
                identifiers = pd.DataFrame({'identifier': [line.replace("+","").replace(" ","").replace('\"','')]})
                identifiers.to_csv(PROJECT_PATH + "/version_modified/codechange/codechange_identifiers_" + str(filename) + ".csv",mode='a', header=False, index=False, sep=',')
                Codechange_Files.add(filename)
        elif  line.startswith('-'):
            if filename != "" and filename.endswith('c'):
                # idents = pd.read_csv(PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(filename) + ".csv")
                # idents_list = idents['identifier']
                # line_idents_list = re.findall(r'\w+', line)
                # names = []
                # for ident in idents_list:
                #     if ident in line_idents_list:
                #         names.append(ident)
                identifiers = pd.DataFrame({'identifier': [line.replace("-","").replace(" ","").replace('\"','')]})
                identifiers.to_csv(PROJECT_PATH + "/version_origin/codechange/codechange_identifiers_" + str(filename) + ".csv",mode='a',header=False, index=False, sep=',')
                Codechange_Files.add(filename)
            elif filename != "" and filename.endswith('py'):
                # idents = pd.read_csv(PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(filename) + ".csv")
                # idents_list = idents['identifier']
                # line_idents_list = re.findall(r'\w+', line)
                # names = []
                # for ident in idents_list:
                #     if ident in line_idents_list:
                #         names.append(ident)
                identifiers = pd.DataFrame({'identifier': [line.replace("-","").replace(" ","").replace('\"','')]})
                identifiers.to_csv(PROJECT_PATH + "/version_origin/codechange/codechange_identifiers_" + str(filename) + ".csv",mode='a', header=False, index=False, sep=',')
                Codechange_Files.add(filename)


def extractFiles(repo_name):
    mkdir(PROJECT_PATH + "/version_origin/pyfiles")
    mkdir(PROJECT_PATH + "/version_origin/cfiles")
    mkdir(PROJECT_PATH + "/version_modified/pyfiles")
    mkdir(PROJECT_PATH + "/version_modified/cfiles")
    exe_command(
        "cd " + PROJECT_PATH + "/version_origin/" + repo_name + "&& " + "find . -name \"*.py\" | xargs -I % cp % ../pyfiles")
    exe_command(
        "cd " + PROJECT_PATH + "/version_origin/" + repo_name + "&& " + "find . -name \"*.c\" | xargs -I % cp % ../cfiles")
    exe_command(
        "cd " + PROJECT_PATH + "/version_origin/" + repo_name + "&& " + "find . -name \"*.cc\" | xargs -I % cp % ../cfiles")
    exe_command(
        "cd " + PROJECT_PATH + "/version_modified/" + repo_name + "&& " + "find . -name \"*.py\" | xargs -I % cp % ../pyfiles")
    exe_command(
        "cd " + PROJECT_PATH + "/version_modified/" + repo_name + "&& " + "find . -name \"*.c\" | xargs -I % cp % ../cfiles")
    exe_command(
        "cd " + PROJECT_PATH + "/version_modified/" + repo_name + "&& " + "find . -name \"*.cc\" | xargs -I % cp % ../cfiles")

def getIdentifier(file,version):
    mkdir(PROJECT_PATH + "/version_origin/pyfiles_ident")
    mkdir(PROJECT_PATH + "/version_origin/cfiles_ident")
    mkdir(PROJECT_PATH + "/version_modified/pyfiles_ident")
    mkdir(PROJECT_PATH + "/version_modified/cfiles_ident")
    if version == "origin":
        if file.endswith('py'):
            if file not in Codechange_Files and os.path.exists(
                    PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file) + ".csv"):
                exe_command("cp " + PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(
                    file) + ".csv " + PROJECT_PATH + "/version_origin/pyfiles_ident/")
                idents_file = pd.read_csv(
                    PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])
            elif not os.path.exists(PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file) + ".csv"):
                try:
                    f = open(PROJECT_PATH + "/version_origin/pyfiles/" + str(file), encoding="utf-8")
                    code = f.read()
                    root = ast.parse(code)
                    names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
                    names = list(set(names))
                    names = [i for i in names if i not in keyword.kwlist]
                    identifiers = pd.DataFrame({'identifier': names})
                    identifiers.to_csv(PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file) + ".csv",
                                       header=True, index=False, sep=',')
                    return set(names)
                except Exception as e:
                    return set()
            else:
                idents_file = pd.read_csv(PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])
        else: #enswith('c')
            if file not in Codechange_Files and os.path.exists(
                    PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(file) + ".csv"):
                exe_command("cp " + PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(
                    file) + ".csv " + PROJECT_PATH + "/version_origin/cfiles_ident/")
                idents_file = pd.read_csv(
                    PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])
            elif not os.path.exists(PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file) + ".csv"):
                try:
                   exe_command(
                       "cd " + PROJECT_PATH + "/version_origin/cfiles && " + JOERNPATH + "/joern-parse " + str(file))
                   exe_command(
                       "cd " + PROJECT_PATH + "/version_origin/cfiles && " + JOERNPATH + "/joern-export --repr ast --out temp_ast cpg.bin")
                   ident = []
                   for astfile in findAllFile(PROJECT_PATH + "/version_origin/cfiles/temp_ast"):
                       f = open(PROJECT_PATH + "/version_origin/cfiles/temp_ast/" + str(astfile), encoding="utf-8")
                       lines = f.readlines()
                       for line in lines:
                           label = re.findall(re.compile(r'[(](.*)[)]', re.S), line)
                           if len(label) == 1:
                               label_list = label[0].split(',')
                               if label_list[0] == "IDENTIFIER":
                                   ident.append(label_list[1])
                   names = [i for i in list(set(ident)) if i not in C_KEYWORDS]
                   identifiers = pd.DataFrame({'identifier': list(set(names))})
                   identifiers.to_csv(PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file) + ".csv",
                                      header=True, index=False, sep=',')
                   exe_command("cd " + PROJECT_PATH + "/version_origin/cfiles && rm -r temp_ast")
                   exe_command("cd " + PROJECT_PATH + "/version_origin/cfiles && rm cpg.bin")
                   return set(names)
                except Exception as e:
                   exe_command("cd " + PROJECT_PATH + "/version_origin/cfiles && rm -r temp_ast")
                   exe_command("cd " + PROJECT_PATH + "/version_origin/cfiles && rm cpg.bin")
                   return set()
            else:
                idents_file = pd.read_csv(
                    PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])

    else:#version == "modified"
        if file.endswith('py'):
            if file not in Codechange_Files and os.path.exists(
                    PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file) + ".csv"):
                exe_command("cp " + PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(
                    file) + ".csv " + PROJECT_PATH + "/version_modified/pyfiles_ident/")
                idents_file = pd.read_csv(
                    PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])
            elif not os.path.exists(
                    PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file) + ".csv"):
                try:
                    f = open(PROJECT_PATH + "/version_modified/pyfiles/" + str(file), encoding="utf-8")
                    code = f.read()
                    root = ast.parse(code)
                    names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
                    names = list(set(names))
                    names = [i for i in names if i not in keyword.kwlist]
                    identifiers = pd.DataFrame({'identifier': names})
                    identifiers.to_csv(PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file) + ".csv",
                                       header=True, index=False, sep=',')
                    return set(names)
                except Exception as e:
                    return set()
            else:
                idents_file = pd.read_csv(PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])

        else: #endswith('c'):
            if file not in Codechange_Files and os.path.exists(
                    PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file) + ".csv"):
                exe_command("cp " + PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(
                    file) + ".csv " + PROJECT_PATH + "/version_modified/cfiles_ident/")
                idents_file = pd.read_csv(
                    PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])
            elif not os.path.exists(PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file) + ".csv"):
                try:
                    exe_command(
                        "cd " + PROJECT_PATH + "/version_modified/cfiles && " + JOERNPATH + "/joern-parse " + str(file))
                    exe_command(
                        "cd " + PROJECT_PATH + "/version_modified/cfiles && " + JOERNPATH + "/joern-export --repr ast --out temp_ast cpg.bin")
                    ident = []
                    for astfile in findAllFile(PROJECT_PATH + "/version_modified/cfiles/temp_ast"):
                        f = open(PROJECT_PATH + "/version_modified/cfiles/temp_ast/" + str(astfile), encoding="utf-8")
                        lines = f.readlines()
                        for line in lines:
                            label = re.findall(re.compile(r'[(](.*)[)]', re.S), line)
                            if len(label) == 1:
                                label_list = label[0].split(',')
                                if label_list[0] == "IDENTIFIER":
                                    ident.append(label_list[1])
                    names = [i for i in list(set(ident)) if i not in C_KEYWORDS]
                    identifiers = pd.DataFrame({'identifier': list(set(names))})
                    identifiers.to_csv(
                        PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(file) + ".csv",
                        header=True, index=False, sep=',')
                    exe_command("cd " + PROJECT_PATH + "/version_modified/cfiles && rm -r temp_ast")
                    exe_command("cd " + PROJECT_PATH + "/version_modified/cfiles && rm cpg.bin")
                    return set(names)
                except Exception as e:
                    exe_command("cd " + PROJECT_PATH + "/version_modified/cfiles && rm -r temp_ast")
                    exe_command("cd " + PROJECT_PATH + "/version_modified/cfiles && rm cpg.bin")
                    return set()
            else:
                idents_file = pd.read_csv(
                    PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(file) + ".csv")
                return set(idents_file['identifier'])


def mergeAllCode():
    # modified_file = open(PROJECT_PATH + "/version_modified/allcode.txt", 'a+')
    # origin_file = open(PROJECT_PATH + "/version_origin/allcode.txt", 'a+')
    # exe_command("cd " + PROJECT_PATH + "/version_modified/pyfiles/ && " + "find . -name \"*.py\" | xargs -n1 -i bash -c 'echo  >> $1' _ {}")
    # exe_command("cd " + PROJECT_PATH + "/version_modified/pyfiles/ && " + "find . -name \"*.py\" | xargs cat -s > ../allcode.txt")
    #
    # exe_command("cd " + PROJECT_PATH + "/version_modified/cfiles/ && " + "find . -name \"*.c\" | xargs -n1 -i bash -c 'echo  >> $1' _ {}")
    # exe_command("cd " + PROJECT_PATH + "/version_modified/cfiles/ && " + "find . -name \"*.c\" | xargs cat -s >> ../allcode.txt")
    #
    # exe_command("cd " + PROJECT_PATH + "/version_origin/pyfiles/ && " + "find . -name \"*.py\" | xargs -n1 -i bash -c 'echo  >> $1' _ {}")
    # exe_command("cd " + PROJECT_PATH + "/version_origin/pyfiles/ && " + "find . -name \"*.py\" | xargs cat -s > ../allcode.txt")
    #
    # exe_command("cd " + PROJECT_PATH + "/version_origin/cfiles/ && " + "find . -name \"*.c\" | xargs -n1 -i bash -c 'echo  >> $1' _ {}")
    # exe_command("cd " + PROJECT_PATH + "/version_origin/cfiles/ && " + "find . -name \"*.c\" | xargs cat -s >> ../allcode.txt")
    codechange_record = []
    modified_file = open(PROJECT_PATH + "/version_modified/allcode.txt", 'a+')
    origin_file = open(PROJECT_PATH + "/version_origin/allcode.txt", 'a+')
    codechange_list = []
    for file in findAllFile(PROJECT_PATH + "/version_modified/codechange"):
        codechange_list.append(file.replace("codechange_identifiers_", "").replace(".csv", ""))

    counter = 0
    for file in findAllFile(PROJECT_PATH + "/version_modified/pyfiles"):
        haveCodechange = False
        if file in codechange_list:
            df = pd.read_csv(PROJECT_PATH + "/version_modified/codechange/codechange_identifiers_" + str(file)+".csv", sep=',', header=None,names=['identifier'])
            code_lines = df['identifier']
            haveCodechange = True
        # idents_file = pd.read_csv(
        #     PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file) + ".csv")
        # idents = idents_file['identifier']
        f = open(PROJECT_PATH + "/version_modified/pyfiles/" + str(file))
        lines = f.readlines()
        for line in lines:
            # ident_str = ""
            # # for ident in idents:
            # #     if ident in re.findall(r'\w+', line):
            # #         ident_str += str(ident) + " "
            # if ident_str != "":
            line_code = line.replace(" ", "").replace('\"', '').replace('\n', '')
            if haveCodechange:
                if line_code in list(code_lines):
                    codechange_record.append([file, counter, "modified"])
            Line_File_M[counter] = file
            counter += 1
            modified_file.write(line_code + '\n')

    for file in findAllFile(PROJECT_PATH + "/version_modified/cfiles"):
        haveCodechange = False
        if file in codechange_list:
            df = pd.read_csv(PROJECT_PATH + "/version_modified/codechange/codechange_identifiers_" + str(file)+".csv", sep=',', header=None,
                    names=['identifier'])
            code_lines = df['identifier']
            haveCodechange = True
        # idents_file = pd.read_csv(
        #     PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(file) + ".csv")
        # idents = idents_file['identifier']
        f = open(PROJECT_PATH + "/version_modified/cfiles/" + str(file))
        lines = f.readlines()
        for line in lines:
            # ident_str = ""
            # for ident in idents:
            #     if ident in re.findall(r'\w+', line):
            #         ident_str += str(ident) + " "
            # if ident_str != "":
            line_code = line.replace(" ", "").replace('\"', '').replace('\n', '')
            if haveCodechange:
                if line_code in list(code_lines):
                    codechange_record.append([file, counter, "modified"])
            Line_File_M[counter] = file
            counter += 1
            modified_file.write(line_code + '\n')

    codechange_list = []
    for file in findAllFile(PROJECT_PATH + "/version_origin/codechange"):
        codechange_list.append(file.replace("codechange_identifiers_", "").replace(".csv", ""))

    counter = 0
    for file in findAllFile(PROJECT_PATH + "/version_origin/pyfiles"):
        haveCodechange = False
        if file in codechange_list:
            df = pd.read_csv(PROJECT_PATH + "/version_origin/codechange/codechange_identifiers_" + str(file)+".csv", sep=',', header=None,names=['identifier'])
            code_lines = df['identifier']
            haveCodechange = True
        # idents_file = pd.read_csv(
        #     PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file) + ".csv")
        # idents = idents_file['identifier']
        f = open(PROJECT_PATH + "/version_origin/pyfiles/" + str(file))
        lines = f.readlines()
        for line in lines:
            # ident_str = ""
            # for ident in idents:
            #     if ident in re.findall(r'\w+', line):
            #         ident_str += str(ident) + " "
            # if ident_str != "":
            line_code = line.replace(" ", "").replace('\"', '').replace('\n', '')
            if haveCodechange:
                if line_code in list(code_lines):
                    codechange_record.append([file, counter, "origin"])
            Line_File_O[counter] = file
            counter += 1
            origin_file.write(line_code + '\n')

    for file in findAllFile(PROJECT_PATH + "/version_origin/cfiles"):
        haveCodechange = False
        if file in codechange_list:
            df = pd.read_csv(PROJECT_PATH + "/version_origin/codechange/codechange_identifiers_" + str(file)+".csv", sep=',', header=None,
                    names=['identifier'])
            code_lines = df['identifier']
            haveCodechange = True
        # idents_file = pd.read_csv(PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file) + ".csv")
        # idents = idents_file['identifier']
        f = open(PROJECT_PATH + "/version_origin/cfiles/" + str(file))
        lines = f.readlines()
        for line in lines:
            # ident_str = ""
            # for ident in idents:
            #     if ident in re.findall(r'\w+', line):
            #         ident_str += str(ident) + " "
            # if ident_str != "":
            line_code = line.replace(" ", "").replace('\"', '').replace('\n', '')
            if haveCodechange:
                if line_code in list(code_lines):
                    codechange_record.append([file, counter, "origin"])
            Line_File_O[counter] = file
            counter += 1
            origin_file.write(line_code + '\n')

    return codechange_record


# def codeToIdentifier():
#     codechange_record = []
#     mkdir(PROJECT_PATH + "/version_origin/codechange_ident")
#     mkdir(PROJECT_PATH + "/version_modified/codechange_ident")
#     for file in findAllFile(PROJECT_PATH + "/version_modified/codechange"):
#         df = pd.read_csv(PROJECT_PATH + "/version_modified/codechange/" + str(file), sep=',', header=None,
#                          names=['identifier'])
#         code_lines = df['identifier']
#         file_name = file.replace("codechange_identifiers_", "").replace(".csv", "")
#         modified_file = open(PROJECT_PATH + "/version_modified/codechange_ident/"+str(file_name)+".txt", 'a+')
#         if file_name.endswith('py'):
#             if os.path.exists(PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file_name) + ".csv"):
#                 idents_file = pd.read_csv(
#                     PROJECT_PATH + "/version_modified/pyfiles_ident/py_identifiers_" + str(file_name) + ".csv")
#                 idents = idents_file['identifier']
#                 f = open(PROJECT_PATH + "/version_modified/pyfiles/" + str(file_name))
#                 lines = f.readlines()
#                 counter = 0
#                 for line in lines:
#
#                     ident_str = ""
#                     for ident in idents:
#                         if ident in re.findall(r'\w+', line):
#                             ident_str += str(ident) + " "
#                     if ident_str != "":
#                         if line.replace(" ", "").replace('\"', '').replace('\n', '') in list(code_lines):
#                             codechange_record.append([file_name, counter, "modified"])
#                         modified_file.write(ident_str + '\n')
#                         counter+=1
#         elif file_name.endswith('c'):
#             if os.path.exists(PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(file_name) + ".csv"):
#                 idents_file = pd.read_csv(
#                     PROJECT_PATH + "/version_modified/cfiles_ident/c_identifiers_" + str(file_name) + ".csv")
#                 idents = idents_file['identifier']
#                 f = open(PROJECT_PATH + "/version_modified/cfiles/" + str(file_name))
#                 lines = f.readlines()
#                 counter = 0
#                 for line in lines:
#
#                     ident_str = ""
#                     for ident in idents:
#                         if ident in re.findall(r'\w+', line):
#                             ident_str += str(ident) + " "
#                     if ident_str != "":
#                         if line.replace(" ", "").replace('\"', '').replace('\n', '') in list(code_lines):
#                             codechange_record.append([file_name, counter, "modified"])
#                         modified_file.write(ident_str + '\n')
#                         counter += 1
#         else:
#             print("compareCodeChangeidentifier:file name get error")
#
#
#     for file in findAllFile(PROJECT_PATH + "/version_origin/codechange"):
#         df = pd.read_csv(PROJECT_PATH + "/version_origin/codechange/" + str(file)+".csv", sep=',', header=None,
#                          names=['identifier'])
#         code_lines = df['identifier']
#         file_name = file.replace("codechange_identifiers_", "").replace(".csv", "")
#         origin_file = open(PROJECT_PATH + "/version_origin/codechange_ident/"+str(file_name)+".txt", 'a+')
#         if file_name.endswith('py'):
#             if os.path.exists(PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file_name) + ".csv"):
#                 idents_file = pd.read_csv(
#                     PROJECT_PATH + "/version_origin/pyfiles_ident/py_identifiers_" + str(file_name) + ".csv")
#                 idents = idents_file['identifier']
#                 f = open(PROJECT_PATH + "/version_origin/pyfiles/" + str(file_name))
#                 lines = f.readlines()
#                 counter = 0
#                 for line in lines:
#                     ident_str = ""
#                     for ident in idents:
#                         if ident in re.findall(r'\w+', line):
#                             ident_str += str(ident) + " "
#                     if ident_str != "":
#                         if line.replace(" ", "").replace('\"', '').replace('\n', '') in list(code_lines):
#                             codechange_record.append([file_name, counter, "origin"])
#                         origin_file.write(ident_str + '\n')
#                         counter+=1
#         elif file_name.endswith('c'):
#             if os.path.exists(PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file_name) + ".csv"):
#                 idents_file = pd.read_csv(
#                     PROJECT_PATH + "/version_origin/cfiles_ident/c_identifiers_" + str(file_name) + ".csv")
#                 idents = idents_file['identifier']
#                 f = open(PROJECT_PATH + "/version_origin/cfiles/" + str(file_name))
#                 lines = f.readlines()
#                 counter = 0
#                 for line in lines:
#                     ident_str = ""
#                     for ident in idents:
#                         if ident in re.findall(r'\w+', line):
#                             ident_str += str(ident) + " "
#                     if ident_str != "":
#                         if line.replace(" ", "").replace('\"', '').replace('\n', '') in list(code_lines):
#                             codechange_record.append([file_name, counter, "origin"])
#                         origin_file.write(ident_str + '\n')
#                         counter += 1
#         else:
#             print("compareCodeChangeidentifier:file name get error")
#
#
#     return codechange_record

def checkInAPI(ident_set,version):
    if version =="modified":
        if len(ident_set & C_API_M) !=0 or len(ident_set & PY_API_M) !=0 :
            return True
        else:
            return False

    # this mean: version == "origin"
    else:
        if len(ident_set & C_API_O) != 0 or len(ident_set & PY_API_O) != 0:
            return True
        else:
            return False

def getLineIdent(line_n, code, version):
    if version == "modified":
        if line_n in Line_Ident_M:
            return Line_Ident_M[line_n]
        else:
            file = Line_File_M[line_n]
            ident_set = getIdentifier(file,"modified")
            line_idents = set()
            for ident in ident_set:
                if code.find(ident) != -1:
                    line_idents.add(ident)
            Line_Ident_M[line_n] = line_idents
            return line_idents
    # this mean: version == "origin"
    else:
        if line_n in Line_Ident_O:
            return Line_Ident_O[line_n]
        else:
            file = Line_File_O[line_n]
            ident_set = getIdentifier(file, "origin")
            line_idents = set()
            for ident in ident_set:
                if code.find(ident) != -1:
                    line_idents.add(ident)
            Line_Ident_O[line_n] = line_idents
            return line_idents

def fsearchCore(start, S, lines,sha,repo_name,file_name,version):
    logging.warning ("forward search from line no. %d; current cumulative dependence set size=%d" % (start, len(S)) )
    lines_total = len(lines)
    if start>= lines_total:
        return False
    line_n = start
    while line_n < lines_total:
        line_set = getLineIdent(line_n,lines[line_n],version)
        if checkInAPI(line_set,version):
            break
        line_n+=1

    if line_n ==lines_total:
        return False

    for i in range(start,line_n):
        line_set = getLineIdent(i,lines[i],version)
        if len(S & line_set) != 0:
            S = S | line_set
    if len(S & getLineIdent(line_n,lines[line_n],version) ) != 0:
        addToCsv(sha, repo_name,"inter",version+'-'+file_name+'-'+str(set(S) & set(lines[line_n].split(' ')))+'-'+str(line_n))
        return True
    else:
        return fsearchCore(line_n+1,S,lines,sha,repo_name,file_name,version)


def bsearchCore(start, S, lines,sha,repo_name,file_name,version):
    logging.warning ("backward search from line no. %d; current cumulative dependence set size=%d" % (start, len(S)) )
    if start<= 0:
        return False
    line_n = start
    while line_n >= 0:
        line_set= getLineIdent(line_n,lines[line_n],version)
        if checkInAPI(line_set, version):
            break
        line_n -= 1

    if line_n == -1:
        return False

    for i in range(start, line_n,-1):
        line_set = getLineIdent(i,lines[i],version)
        if len(S & line_set) != 0:
            S = S | line_set
    if len(S & getLineIdent(line_n,lines[line_n],version) ) != 0:
        addToCsv(sha, repo_name,"inter",version+'-'+file_name+'-'+str(set(S) & set(lines[line_n].split(' ')))+'-'+str(line_n))
        return True
    else:
        return bsearchCore(line_n-1,S,lines,sha,repo_name,file_name,version)



def compareCodeChangeidentifier(sha,repo_name,codechange_record):
    if len(codechange_record) == 0:
        addToCsv(sha, repo_name, "Fail", "Cannot find codechange in file")
        return True

    f = open(PROJECT_PATH + "/version_modified/allcode.txt")
    lines = f.readlines()
    for record in codechange_record:
        if record[2] == "modified":
            S = set([])
            print("---------------")
            print(record[0])
            print(record[1])
            print(lines[record[1]])
            print("--------------")
            time.sleep(i)
            if fsearchCore(record[1],S,lines,sha,repo_name,record[0],"modified"):
                return True

            if bsearchCore(record[1],S,lines,sha,repo_name,record[0],"modified"):
                return True


    f = open(PROJECT_PATH + "/version_origin/allcode.txt")
    lines = f.readlines()
    for record in codechange_record:
        if record[2] == "origin":
            S = set([])
            if fsearchCore(record[1],S,lines,sha,repo_name,record[0],"origin"):
                return True

            if bsearchCore(record[1],S,lines,sha,repo_name,record[0],"origin"):
                return True

    return False








mkdir(PROJECT_PATH)
sha_list, repo_list = loadCommitSHA_and_repoName(COMMIT_PATH)

# for i in range(len(repo_list)):
for i in range(84,85):
# for i in range(int(sys.argv[1]),int(sys.argv[2])):
    mkdir(PROJECT_PATH + "/version_origin")
    mkdir(PROJECT_PATH + "/version_modified")
    if sha_list[i].isalnum() == False:
        repo_name = repo_list[i].split('/')[1]
        addToCsv(sha_list[i], repo_name, "Fail","sha value is not alphanumeric")
        rmdir(PROJECT_PATH + "/version_origin")
        rmdir(PROJECT_PATH + "/version_modified")
        continue
    else:
        git_url = GITCLONE_URL + repo_list[i] + ".git"
        repo_name = repo_list[i].split('/')[1]
        downloadProject(git_url, sha_list[i],repo_name)
        if checkChangeinCPy(sha_list[i],repo_name) == False:
            addToCsv(sha_list[i],repo_name, "intra", "commit change not in C or Python code")
            rmdir(PROJECT_PATH + "/version_origin")
            rmdir(PROJECT_PATH + "/version_modified")
            continue
        else:
            downloadoringin(git_url, repo_name)

            #init API list
            initAPI(repo_name)

            #extract py and c/cc files to two folder
            extractFiles(repo_name)



            #extract lines in code change
            getCodeChangeLine(sha_list[i],repo_name)

            # get the identifier of each code file
            # getIdentifier()

            #change code to identifiers
            codechange_record = mergeAllCode() #return a list:[[file_name,line_number],[]...]

            # #merge all code to a txt file
            # mergeAllCode()

            #compare code change with allcode to tag commmit
            if compareCodeChangeidentifier(sha_list[i],repo_name,codechange_record) == False:
                addToCsv(sha_list[i],repo_name, "intra", "not found API func")

            #rmdir(PROJECT_PATH + "/version_origin")
            #rmdir(PROJECT_PATH + "/version_modified")

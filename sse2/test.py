import subprocess
import re
import os

# Function name to lift
FunctionName = "edges"

def run_command(cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    return subprocess.Popen(cmd, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            stdin=subprocess.PIPE).communicate()

#l = run_command('c:\\Program Files\\LLVM\bin\\clang.exe file_0.c -O0 -S -emit-llvm')[1]
#l = run_command('c:\\Program Files\\LLVM\bin\\clang.exe file_0.c -O0 -o test.exe')[1]
#print l

# get address of the test function
Addr = "0x140001000"

# lift test function
#print "..\\..\\build\\Release\\saturn -i test.exe -f " + Addr + " -o lifted.ll -runtime=../../build/saturn_helpers.bc -gadgetMode -printdebug -setConcreteFunctionVA -applysouper -stp-path=c:\\saturntests\\stp.exe -souper-external-cache=false -memdep-block-scan-limit=100000 -recoverarguments -useMSx64Abi"
l = run_command("..\\..\\build\\Release\\saturn -i test.exe -f " + Addr + " -o lifted.ll -runtime=../../build/saturn_helpers.bc -gadgetMode -setConcreteFunctionVA -applysouper=false -stp-path=c:\\saturntests\\stp.exe -souper-external-cache=true -memdep-block-scan-limit=100000 -recoverarguments -useMSx64Abi -createStackSlots")[0]
print l
# optimize lifted ir
os.system("..\\..\\translater\\translate64.py " + "..\\..\\ " + " lifted.ll")

# assemble lifted.ll
l = run_command('..\\..\\build\\SATURN-clang-8.0 lifted.ll -O3 -S -mllvm --x86-asm-syntax=intel')[1]

# run the test and check if we have the expected result
l = run_command("test_.exe 1231312")[0]
lo = run_command("test.exe 1231312")[0]

Passed = False
if l == lo:
	print '[*] Test Passed!'
	Passed = True
else:
	print '[!] Test failed!'
	Passed = False

# Clean up
exit(Passed)
os.remove("file_0.ll")
os.remove("saturn.dll")
os.remove("saturn.exp")
os.remove("saturn.lib")
os.remove("GenRemillConstants32.exe")
os.remove("HelperAsm.obj")
os.remove("lifted.ll")
os.remove("test.exe")
os.remove("test_.exe")
os.remove("remill.asm")

exit(Passed)
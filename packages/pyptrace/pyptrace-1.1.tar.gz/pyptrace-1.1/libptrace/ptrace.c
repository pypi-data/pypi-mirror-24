#include <stdio.h>
#include <stdlib.h>
#include <sys/user.h>
#include <sys/types.h>
#include <sys/ptrace.h>

long attach(pid_t pid)
{
    long ret = ptrace(PTRACE_ATTACH, pid, NULL, NULL);

    if (ret == -1) {
        perror("error attaching");
    }

    return ret;
}

long cont(pid_t pid, int signo)
{
    long ret = ptrace(PTRACE_CONT, pid, NULL, (void *) (long) signo);

    if (ret == -1) {
        perror("error cont");
    }

    return ret;
}

long peektext(pid_t pid, long addr)
{
    // read a word start from addr
    // a word = 4 bytes, this is true for both 32-bit and 64-bit
    long ret =  ptrace(PTRACE_PEEKTEXT, pid, (void *) addr, NULL);

    return ret;
}

long peekdata(pid_t pid, long addr)
{
    long ret = ptrace(PTRACE_PEEKDATA, pid, (void *) addr, NULL);

    return ret;
}

long poketext(pid_t pid, long addr, long data)
{
    long ret = ptrace(PTRACE_POKETEXT, pid, (void *) addr, (void *) data);

    if (ret == -1) {
        perror("error poketext");
    }

    return ret;
}

long getregs(pid_t pid, struct user_regs_struct *regs)
{
    long ret = ptrace(PTRACE_GETREGS, pid, NULL, regs);

    // printf("rsp: 0x%016llx\n", regs->rsp);
    // printf("rbp: 0x%016llx\n", regs->rbp);
    if (ret == -1) {
        perror("error getregs");
    }

    return ret;
}

long setregs(pid_t pid, struct user_regs_struct *regs)
{
    long ret = ptrace(PTRACE_SETREGS, pid, NULL, regs);


    if (ret == -1) {
        perror("error setregs");
    }

    return ret;
}

long singlestep(pid_t pid, int signo)
{
    long ret = ptrace(PTRACE_SINGLESTEP, pid, NULL, (void *) (long) signo);

    if (ret == -1) {
        perror("error singlestep");
    }

    return ret;
}

long traceme(void)
{
    long ret = ptrace(PTRACE_TRACEME, 0, NULL, NULL);

    if (ret == -1) {
        perror("error traceme");
    }

    return ret;
}

long setoptions(pid_t pid, int options)
{
    long ret = ptrace(PTRACE_SETOPTIONS, pid, NULL, (void *) (long) options);

    if (ret == -1) {
        perror("error setoptions");
    }

    return ret;
}

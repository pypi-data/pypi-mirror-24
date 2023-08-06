#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>

#include <Python.h>

static PyObject* _waitpid(PyObject* self, PyObject* args)
{
    long pid;
    int status, options, ret;

    if (!PyArg_ParseTuple(args, "li", &pid, &options)) {
        return NULL;
    }


    errno = 0;
    ret = waitpid(pid, &status, options);
    return Py_BuildValue("(iii)", ret, status, errno);
}


static PyObject* _kill(PyObject* self, PyObject* args)
{
    long pid;
    int sig, ret;

    if (!PyArg_ParseTuple(args, "li", &pid, &sig)) {
        return NULL;
    }

    errno = 0;
    ret = kill(pid, sig);
    return Py_BuildValue("(ii)", ret, errno);
}

#define TEST_STATUS(METHOD) \
static PyObject* test_##METHOD(PyObject* self, PyObject* args) \
{ \
    int status, ret; \
\
    if (!PyArg_ParseTuple(args, "i", &status)) { \
        return NULL; \
    } \
\
    ret = METHOD(status); \
    return Py_BuildValue("i", ret); \
}

TEST_STATUS(WIFEXITED)
TEST_STATUS(WEXITSTATUS)
TEST_STATUS(WIFSIGNALED)
TEST_STATUS(WTERMSIG)
TEST_STATUS(WCOREDUMP)
TEST_STATUS(WIFSTOPPED)
TEST_STATUS(WSTOPSIG)
TEST_STATUS(WIFCONTINUED)

static PyMethodDef os_funcs[] = {
    {
        "waitpid",
        (PyCFunction) _waitpid,
        METH_VARARGS,
        "TODO"
    }, {
        "kill",
        (PyCFunction) _kill,
        METH_VARARGS,
        "TODO"
    }, {
        "WIFEXITED",
        (PyCFunction) test_WIFEXITED,
        METH_VARARGS,
        "TODO"
    }, {
        "WEXITSTATUS",
        (PyCFunction) test_WEXITSTATUS,
        METH_VARARGS,
        "TODO"
    }, {
        "WIFSIGNALED",
        (PyCFunction) test_WIFSIGNALED,
        METH_VARARGS,
        "TODO"
    }, {
        "WTERMSIG",
        (PyCFunction) test_WTERMSIG,
        METH_VARARGS,
        "TODO"
    }, {
        "WCOREDUMP",
        (PyCFunction) test_WCOREDUMP,
        METH_VARARGS,
        "TODO"
    }, {
        "WSTOPSIG",
        (PyCFunction) test_WSTOPSIG,
        METH_VARARGS,
        "TODO"
    }, {
        "WIFSTOPPED",
        (PyCFunction) test_WIFSTOPPED,
        METH_VARARGS,
        "TODO"
    }, {
        "WIFCONTINUED",
        (PyCFunction) test_WIFCONTINUED,
        METH_VARARGS,
        "TODO"
    }, {
        "WIFCONTINUED",
        (PyCFunction) test_WIFCONTINUED,
        METH_VARARGS,
        "TODO"
    }, {
        NULL
    }
};

void initos(void)
{
    Py_InitModule3("os", os_funcs,
        "Wrapper for some usefull os calls.");
}

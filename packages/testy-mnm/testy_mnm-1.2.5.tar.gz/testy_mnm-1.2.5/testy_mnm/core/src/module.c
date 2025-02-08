#include <Python.h>
#include "src_of_src/head.h"

static PyObject* testy_c_module_test(PyObject* self, PyObject* args) {
    return Py_BuildValue("s", "Hello from testy_c_module!");
}

static PyObject* testy_c_module_test2(PyObject* self, PyObject* args) {
    return Py_BuildValue("s", "Hello from testy_c_module 2222!");
}

static PyObject* testy_c_module_add(PyObject* self, PyObject* args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
        return NULL;
    }
    return Py_BuildValue("i", add(a, b));
}

static PyMethodDef testy_c_module_methods[] = {
    {"test", testy_c_module_test, METH_VARARGS, "Test function"},
    {"test2", testy_c_module_test2, METH_VARARGS, "Test function 2"},
    {"add", testy_c_module_add, METH_VARARGS, "Add two numbers"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef testy_c_module_module = {
    PyModuleDef_HEAD_INIT,
    "testy_c_module",
    "Test module",
    -1,
    testy_c_module_methods
};

PyMODINIT_FUNC PyInit_testy_c_module(void) {
    return PyModule_Create(&testy_c_module_module);
}
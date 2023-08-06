/*
 * Copyright 2016 Capital One Services, LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


#include "cmdobject.h"
#include <string.h>
#include <stdio.h>
#include <coperr.h>
#include <dbcarea.h>
#include <parcel.h>
#include "_compat.h"


PyObject* GiraffeError;

static char cnta[4];
static char session_charset[36];

static int fetch_request(dbcarea_t* dbc, char cnta[]) {
    int status = OK;
    Int32 result = EM_OK;
    Py_BEGIN_ALLOW_THREADS
    DBCHCL(&result, cnta, dbc);
    Py_END_ALLOW_THREADS
    if (result == REQEXHAUST) {
        status = STOP;
    } else if (result != EM_OK) {
        status = FAILED;
    } else {
        switch ((Int16)dbc->fet_parcel_flavor) {
        case PclSUCCESS:
            break;
        case PclRECORD:
            break;
        case PclFAILURE:
            status = PCL_FAIL;
            break;
        case PclERROR:
            status = PCL_ERR;
            break;
        }
    }
    return status;
}

static PyObject* Cmd_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    Cmd* self;
    self = (Cmd*)type->tp_alloc(type, 0);
    return (PyObject*)self;
}

static int Cmd_init(Cmd* self, PyObject* args, PyObject* kwds) {
    char *host=NULL, *username=NULL, *password=NULL;
    char logonstr[1024] = "";

    if (!PyArg_ParseTuple(args, "sss", &host, &username, &password)) {
        return -1;
    }

    sprintf(logonstr, "%s/%s,%s", host, username, password);
    self->connected = NOT_CONNECTED;
    self->status = OK;
    self->result = EM_OK;
    self->dbc = (dbcarea_t*)malloc(sizeof(dbcarea_t));
    self->dbc->total_len = sizeof(dbcarea_t);
    DBCHINI(&self->result, cnta, self->dbc);
    if (self->result != EM_OK) {
        PyErr_SetString(GiraffeError, "CLIv2: init failed");
        return -1;
    }
    self->dbc->change_opts = 'Y';
    self->dbc->resp_mode = 'I';
    self->dbc->use_presence_bits = 'N';
    self->dbc->keep_resp = 'N';
    self->dbc->wait_across_crash = 'N';
    self->dbc->tell_about_crash = 'Y';
    self->dbc->loc_mode = 'Y';
    self->dbc->var_len_req = 'N';
    self->dbc->var_len_fetch = 'N';
    self->dbc->save_resp_buf = 'N';
    self->dbc->two_resp_bufs = 'Y';
    self->dbc->ret_time = 'N';
    self->dbc->parcel_mode = 'Y';
    self->dbc->wait_for_resp = 'Y';
    self->dbc->req_proc_opt = 'B';
    self->dbc->return_statement_info = 'Y';
    self->dbc->req_buf_len = 65535;
    self->dbc->maximum_parcel = 'H';
    self->dbc->max_decimal_returned = 38;
    self->dbc->charset_type = 'N';
    snprintf(session_charset, 32, "%-30s", "UTF8");
    self->dbc->inter_ptr = session_charset;
    self->dbc->logon_ptr = logonstr;
    self->dbc->logon_len = (UInt32) strlen(logonstr);
    self->dbc->func = DBFCON;
    DBCHCL(&self->result, cnta, self->dbc);
    if (self->result != EM_OK) {
        PyErr_SetString(GiraffeError, "CLIv2: connect failed");
        return -1;
    }
    self->dbc->i_sess_id = self->dbc->o_sess_id;
    self->dbc->i_req_id = self->dbc->o_req_id;
    self->dbc->func = DBFFET;
    self->status = fetch_request(self->dbc, cnta);
    self->dbc->i_sess_id = self->dbc->o_sess_id;
    self->dbc->i_req_id = self->dbc->o_req_id;
    self->dbc->func = DBFERQ;
    DBCHCL(&self->result, cnta, self->dbc);
    if (self->result != EM_OK) {
        PyErr_SetString(GiraffeError, "CLIv2: end request failed");
        return -1;
    }
    if (self->status != 0) {
        char err_msg[256] = "";
        if (self->status == -1 || self->dbc->fet_ret_data_len < 1) {
            // msg_text can only be read after DBCHINI initializes the dbcarea_t
            snprintf(err_msg, 256, "%d: Connection to host '%s' failed.", self->status, (char*)host);
        } else {
            struct CliFailureType *Error_Fail = (struct CliFailureType *) self->dbc->fet_data_ptr;
            snprintf(err_msg, 256, "%d: %s", Error_Fail->Code, Error_Fail->Msg);
        }
        PyErr_SetString(GiraffeError, err_msg);
        return -1;
    }
    self->connected = CONNECTED;
    return 0;
}

static PyObject* Cmd_close(Cmd* self) {
    if (self->connected == CONNECTED) {
        self->dbc->func = DBFDSC;
        DBCHCL(&self->result, cnta, self->dbc);
    }
    DBCHCLN(&self->result, cnta);
    self->connected = NOT_CONNECTED;
    return Py_BuildValue("i", self->connected);
}

static void Cmd_dealloc(Cmd* self) {
    if (self->dbc != NULL) {
        free(self->dbc);
    }
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* Cmd_execute(Cmd* self, PyObject* args) {
    char* command = NULL;
    PyObject* statementinfo = PyBytes_FromStringAndSize(NULL, 0);
    PyObject* rows = PyBytes_FromStringAndSize(NULL, 0);
    PyObject* results = NULL;
    PyObject* data = PyList_New(0);
    PyObject* error = NULL;

    if (self->connected == NOT_CONNECTED) {
        PyErr_SetString(GiraffeError, "1: Connection not established.");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "s", &command)) {
        return NULL;
    }

    self->dbc->req_ptr = command;
    self->dbc->req_len = (UInt32) strlen(command);
    self->dbc->func = DBFIRQ;
    DBCHCL(&self->result, cnta, self->dbc);
    if (self->result != EM_OK) {
        Cmd_close(self);
        PyErr_SetString(GiraffeError, "CLIv2: initiate request failed");
        return NULL;
    }

    self->dbc->i_sess_id = self->dbc->o_sess_id;
    self->dbc->i_req_id = self->dbc->o_req_id;
    self->dbc->func = DBFFET;

    while ((self->status = fetch_request(self->dbc, cnta)) == OK) {
        size_t length = self->dbc->fet_ret_data_len;
        if (self->dbc->fet_parcel_flavor == PclRECORD) {
            unsigned char v1 = (self->dbc->fet_ret_data_len & 0xff);
            unsigned char v2 = (self->dbc->fet_ret_data_len & 0xff00) >> 8;
            PyObject* s = PyBytes_FromFormat("%c%c", v1, v2);
            PyBytes_Concat(&rows, s);
            Py_DECREF(s);
        }
        if (self->dbc->fet_parcel_flavor == PclSTATEMENTINFO) {
            PyObject* s = PyBytes_FromStringAndSize(self->dbc->fet_data_ptr, length);
            PyBytes_Concat(&statementinfo, s);
            Py_DECREF(s);
        } else if (self->dbc->fet_parcel_flavor == PclRECORD) {
            PyObject* s = PyBytes_FromStringAndSize(self->dbc->fet_data_ptr, length);
            PyBytes_Concat(&rows, s);
            Py_DECREF(s);
        } else if (self->dbc->fet_parcel_flavor == PclENDSTATEMENT) {
            PyObject* d = PyDict_New();
            if (statementinfo) {
                PyDict_SetItemString(d, "stmtinfo", statementinfo);
                Py_DECREF(statementinfo);
            } else {
                Py_INCREF(Py_None);
                PyDict_SetItemString(d, "stmtinfo", Py_None);
            }
            PyDict_SetItemString(d, "rows", rows);
            Py_DECREF(rows);
            statementinfo = PyBytes_FromStringAndSize(NULL, 0);
            rows = PyBytes_FromStringAndSize(NULL, 0);
            PyList_Append(data, d);
            Py_DECREF(d);
        }
    }
    if (self->status == FAILED) {
        error = Py_BuildValue("(is)", self->status, self->dbc->msg_text);
    } else if (self->status == PCL_FAIL) {
        struct CliFailureType *ErrorFail = (struct CliFailureType *) self->dbc->fet_data_ptr;
        error = Py_BuildValue("(is)", ErrorFail->Code, ErrorFail->Msg);
    } else if (self->status == PCL_ERR) {
        struct CliErrorType *ErrorFail = (struct CliErrorType *) self->dbc->fet_data_ptr;
        error = Py_BuildValue("(is)", ErrorFail->Code, ErrorFail->Msg);
    } else {
        Py_INCREF(Py_None);
        error = Py_None;
    }
    self->dbc->i_sess_id = self->dbc->o_sess_id;
    self->dbc->i_req_id = self->dbc->o_req_id;
    self->dbc->func = DBFERQ;
    DBCHCL(&self->result, cnta, self->dbc);
    results = Py_BuildValue("(OO)", data, error);
    Py_DECREF(data);
    Py_XDECREF(error);
    return results;
}

static PyMethodDef Cmd_methods[] = {
    {"close", (PyCFunction)Cmd_close, METH_NOARGS, ""},
    {"execute", (PyCFunction)Cmd_execute, METH_VARARGS, ""},
    {NULL}  /* Sentinel */
};

PyTypeObject CmdType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_cli.Cmd",                                     /* tp_name */
    sizeof(Cmd),                                    /* tp_basicsize */
    0,                                              /* tp_itemsize */
    (destructor)Cmd_dealloc,                        /* tp_dealloc */
    0,                                              /* tp_print */
    0,                                              /* tp_getattr */
    0,                                              /* tp_setattr */
    0,                                              /* tp_compare */
    0,                                              /* tp_repr */
    0,                                              /* tp_as_number */
    0,                                              /* tp_as_sequence */
    0,                                              /* tp_as_mapping */
    0,                                              /* tp_hash */
    0,                                              /* tp_call */
    0,                                              /* tp_str */
    0,                                              /* tp_getattro */
    0,                                              /* tp_setattro */
    0,                                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,       /* tp_flags */
    "GiraffeCmd objects",                           /* tp_doc */
    0,                                              /* tp_traverse */
    0,                                              /* tp_clear */
    0,                                              /* tp_richcompare */
    0,                                              /* tp_weaklistoffset */
    0,                                              /* tp_iter */
    0,                                              /* tp_iternext */
    Cmd_methods,                                    /* tp_methods */
    0,                                              /* tp_members */
    0,                                              /* tp_getset */
    0,                                              /* tp_base */
    0,                                              /* tp_dict */
    0,                                              /* tp_descr_get */
    0,                                              /* tp_descr_set */
    0,                                              /* tp_dictoffset */
    (initproc)Cmd_init,                             /* tp_init */
    0,                                              /* tp_alloc */
    Cmd_new,                                        /* tp_new */
};

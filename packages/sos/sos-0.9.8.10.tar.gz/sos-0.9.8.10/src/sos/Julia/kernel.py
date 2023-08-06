#!/usr/bin/env python3
#
# This file is part of Script of Scripts (sos), a workflow system
# for the execution of commands and scripts in different languages.
# Please visit https://github.com/vatlab/SOS for more information.
#
# Copyright (C) 2016 Bo Peng (bpeng@mdanderson.org)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from collections import Sequence
import tempfile
from sos.utils import short_repr, env
from IPython.core.error import UsageError
import pandas


def homogeneous_type(seq):
    iseq = iter(seq)
    first_type = type(next(iseq))
    if first_type in (int, float):
        return True if all(isinstance(x, (int, float)) for x in iseq) else False
    else:
        return True if all(isinstance(x, first_type) for x in iseq) else False

#
#  support for %get
#
#  Converting a Python object to a julia expression that will be executed
#  by the julia kernel.
#
#
def _julia_repr(obj):
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif isinstance(obj, (int, float)):
        return repr(obj)
    elif isinstance(obj, str):
        return '"""' + obj + '"""'
    elif isinstance(obj, complex):
        return 'complex(' + str(obj.real) + ',' + str(obj.imag) + ')'
    elif isinstance(obj, Sequence):
        if len(obj) == 0:
            return '[]'
        else:
            return '[' + ','.join(_julia_repr(x) for x in obj) + ']'
    elif obj is None:
        return 'NaN'
    elif isinstance(obj, dict):
        return 'Dict(' + ','.join('"{}" => {}'.format(x, _julia_repr(y)) for x,y in obj.items()) + ')'
    elif isinstance(obj, set):
        return 'Set([' + ','.join(_julia_repr(x) for x in obj) + '])'
    else:
        import numpy
        import pandas
        if isinstance(obj, (numpy.intc, numpy.intp, numpy.int8, numpy.int16, numpy.int32, numpy.int64,\
                numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64, numpy.float16, numpy.float32)):
            return repr(obj)
        elif isinstance(obj, numpy.float64):
            return 'Float64(' + obj + ')'
        elif isinstance(obj, numpy.matrixlib.defmatrix.matrix):
            try:
                import feather
            except ImportError:
                raise UsageError('The feather-format module is required to pass numpy matrix as julia matrix(array)'
                    'See https://github.com/wesm/feather/tree/master/python for details.')
            feather_tmp_ = tempfile.NamedTemporaryFile(suffix='.feather', delete=False).name
            feather.write_dataframe(pandas.DataFrame(obj).copy(), feather_tmp_)
            return 'Array(Feather.read("' + feather_tmp_ + '", nullable=false))'
        elif isinstance(obj, numpy.ndarray):
            return '[' + ','.join(_julia_repr(x) for x in obj) + ']'
        elif isinstance(obj, pandas.DataFrame):
            try:
                import feather
            except ImportError:
                raise UsageError('The feather-format module is required to pass pandas DataFrame as julia.DataFrames'
                    'See https://github.com/wesm/feather/tree/master/python for details.')
            feather_tmp_ = tempfile.NamedTemporaryFile(suffix='.feather', delete=False).name
            try:
                data = obj.copy()
                # if the dataframe has index, it would not be transferred due to limitations
                # of feather. We will have to do something to save the index separately and
                # recreate it. (#397)
                if isinstance(data.index, pandas.Index):
                    df_index = list(data.index)
                elif not isinstance(data.index, pandas.RangeIndex):
                    # we should give a warning here
                    df_index=None
                feather.write_dataframe(data, feather_tmp_)
            except Exception:
                # if data cannot be written, we try to manipulate data
                # frame to have consistent types and try again
                for c in data.columns:
                    if not homogeneous_type(data[c]):
                        data[c] = [str(x) for x in data[c]]
                feather.write_dataframe(data, feather_tmp_)
                # use {!r} for path because the string might contain c:\ which needs to be
                # double quoted.
            return 'Feather.read("' + feather_tmp_ + '", nullable=false)'
        elif isinstance(obj, pandas.Series):
            dat=list(obj.values)
            ind=list(obj.index.values)
            ans='NamedArray(' + '[' + ','.join(_julia_repr(x) for x in dat) + ']' + ',([' + ','.join(_julia_repr(y) for y in ind) + '],))'
            return ans.replace("'",'"')
        else:
            return repr('Unsupported datatype {}'.format(short_repr(obj)))



# julia    length (n)    Python
# NaN        None
# boolean    1    boolean
# integer    1    integer
# float64    1    double
# character    1    unicode
# string          string
# vector          list
# list without names    n > 0    list
# list with names    n > 0    dict
# matrix    n > 0    array
# data.frame    n > 0    DataFrame

julia_init_statements = r'''
try
  using Feather
catch
  Pkg.add("Feather")
  using Feather
end
try
  using NamedArrays
catch
  Pkg.add("NamedArrays")
  using NamedArrays
end
try
  using DataFrames
catch
  Pkg.add("DataFrames")
  using DataFrames
end
try
  using NamedArrays
catch
  Pkg.add("NamedArrays")
  using NamedArrays
end
function __julia_py_repr_logical_1(obj)
    obj==true ? "True" : "False"
end
function __julia_py_repr_integer_1(obj)
    return string(obj)
end
function __julia_py_repr_double_1(obj)
    return "numpy.float64(" * string(obj) * ")"
end
function __julia_py_repr_complex_1(obj)
  rl = real(obj)
  im = imag(obj)
  return "complex(" * string(rl) * "," * string(im) * ")"
end
function __julia_py_repr_character_1(obj)
  return "r\"\"\"" * obj * "\"\"\""
end
function __julia_py_repr_dict_1(obj)
  val = collect(values(obj))
  key = collect(keys(obj))
  res = __julia_py_repr_character_1(key[1]) * ":" * string(__julia_py_repr(val[1])) * ","
  for i in 2:length(val)
    res = res * __julia_py_repr_character_1(key[i]) * ":" * string(__julia_py_repr(val[i])) * ","
  end
  return "{" * res * "}"
end
# Dataframe in Julia doesn't have rowname
function __julia_py_repr_dataframe(obj)
  tf = joinpath(tempname())
  Feather.write(tf, obj)
  return "read_dataframe(r'" * tf * "')"
end
function __julia_py_repr_matrix(obj)
  tf = joinpath(tempname())
  Feather.write(tf, convert(DataFrame, obj))
  return "read_dataframe(r'" * tf * "').as_matrix()"
end
function __julia_py_repr_namedarray(obj)
  key = names(obj)[1]
  val = [obj[i] for i in key]
  return "pandas.Series(" * "[" * join([__julia_py_repr(i) for i in val], ",") * "]," * "index=[" * join([__julia_py_repr(j) for j in key], ",") * "])"
end
function __julia_py_repr_set(obj)
  return "{" * join([__julia_py_repr(i) for i in obj], ",") * "}"
end
function __julia_py_repr_n(obj)
  # The problem of join() is that it would ignore the double quote of a string
  return "[" * join([__julia_py_repr(i) for i in obj], ",") * "]"
end
function __julia_has_row_names(df)
  return !(names(df)[1]==collect(1:size(df)[1]))
end
function __julia_has_col_names(df)
  return !(names(df)[2]==collect(1:size(df)[2]))
end
function __julia_py_repr(obj)
  if isa(obj, Matrix)
    __julia_py_repr_matrix(obj)
  elseif isa(obj, Set)
    __julia_py_repr_set(obj)
  elseif isa(obj, DataFrame)
    __julia_py_repr_dataframe(obj)
  elseif isa(obj, Void) || obj === NaN
    return "None"
  elseif isa(obj, Dict)
    __julia_py_repr_dict_1(obj)
    # if needed to name vector in julia, need to use a package called NamedArrays
  elseif isa(obj, Vector{Int})
    if (length(obj) == 1)
      __julia_py_repr_integer_1(obj)
    else
      return "[" * join([__julia_py_repr_integer_1(i) for i in obj], ",") * "]"
    end
  elseif isa(obj, Vector{Complex{Int}}) || isa(obj, Vector{Complex{Float64}})
    if (length(obj) == 1)
      __julia_py_repr_complex_1(obj)
    else
      return "[" * join([__julia_py_repr_complex_1(i) for i in obj], ",") * "]"
    end
  elseif isa(obj, Vector{Float64})
    if (length(obj) == 1)
      __julia_py_repr_double_1(obj)
    else
      return "[" * join([__julia_py_repr_double_1(i) for i in obj], ",") * "]"
    end
  elseif isa(obj, Vector{String})
    if (length(obj) == 1)
      __julia_py_repr_character_1(obj)
    else
      return "[" * join([__julia_py_repr_character_1(i) for i in obj], ",") * "]"
    end
  elseif isa(obj, Vector{Any})
      return "[" * join([__julia_py_repr(i) for i in obj], ",") * "]"
  elseif isa(obj, Vector{Bool})
    if (length(obj) == 1)
      __julia_py_repr_logical_1(obj)
    else
      return "[" * join([__julia_py_repr_logical_1(i) for i in obj], ",") * "]"
    end
  elseif isa(obj, NamedArrays.NamedArray{Int64,1,Array{Int64,1}})
      return __julia_py_repr_namedarray(obj)
  elseif isa(obj, Int)
    __julia_py_repr_integer_1(obj)
  elseif isa(obj, Complex)
    __julia_py_repr_complex_1(obj)
  elseif isa(obj, Float64)
    __julia_py_repr_double_1(obj)
  elseif isa(obj, String)
    __julia_py_repr_character_1(obj)
  elseif isa(obj, Bool)
    __julia_py_repr_logical_1(obj)
  else
    return "'Untransferrable variable'"
  end
end
'''


class sos_Julia:
    background_color = '#ebd8eb'
    supported_kernels = {'Julia': ['julia-0.6']}
    options = {
        'assignment_pattern': r'^([_A-Za-z0-9\.]+)\s*=.*$'
        }

    def __init__(self, sos_kernel, kernel_name='julia-0.6'):
        self.sos_kernel = sos_kernel
        self.kernel_name = kernel_name
        self.init_statements = julia_init_statements

    def get_vars(self, names):
        for name in names:
            if name.startswith('_'):
                self.sos_kernel.warn('Variable {} is passed from SoS to kernel {} as {}'.format(name, self.kernel_name, '.' + name[1:]))
                newname = '.' + name[1:]
            else:
                newname = name
            julia_repr = _julia_repr(env.sos_dict[name])
            self.sos_kernel.run_cell('{} = {}'.format(newname, julia_repr), True, False,
                                     on_error='Failed to put variable {} to julia'.format(name))

    def put_vars(self, items, to_kernel=None):
        # first let us get all variables with names starting with sos
        try:
            response = self.sos_kernel.get_response('whos(r"sos")', ('stream',), name=('stdout',))[0][1]
            all_vars = [x.strip().split()[0] for x in response['text'].split('\n') if x.strip()]
            items += [x for x in all_vars if x.startswith('sos')]
        except:
            # if ther ei sno variable with name sos, the command will not produce any output
            pass
        
        if not items:
            return {}

        res = {}
        for item in items:
            py_repr = '__julia_py_repr({})'.format(item)
            response = self.sos_kernel.get_response(py_repr, ('execute_result',))[0][1]
            expr = response['data']['text/plain']
            from sos.utils import log_to_file
            log_to_file('Response {}'.format(response))
            log_to_file('Obained expression {}'.format(expr))

            try:
                if 'read_dataframe' in expr:
                    # imported to be used by eval
                    from feather import read_dataframe
                    # suppress flakes warning
                    read_dataframe
                # evaluate as raw string to correctly handle \\ etc
                res[item] = eval(eval(expr))
            except Exception as e:
                self.sos_kernel.warn('Failed to evaluate {!r}: {}'.format(expr, e))
                return None
        return res

    def sessioninfo(self):
        ret = self.sos_kernel.get_response(r'versioninfo(true)',
                ('stream',), name=('stdout',))
        return '\n'.join(x[1]['text'] for x in ret)

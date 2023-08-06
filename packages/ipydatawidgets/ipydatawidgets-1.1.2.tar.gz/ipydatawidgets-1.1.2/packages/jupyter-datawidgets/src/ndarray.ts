// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  WidgetModel, ManagerBase
} from '@jupyter-widgets/base';


export {
  JUPYTER_DATAWIDGETS_VERSION
} from './version';

import * as _ from 'underscore';

import ndarray = require('ndarray');


export
const version = (require('../package.json') as any).version;


export
type TypedArray = Int8Array | Uint8Array | Int16Array | Uint16Array | Int32Array | Uint32Array | Uint8ClampedArray | Float32Array | Float64Array;
export
type TypedArrayConstructor = Int8ArrayConstructor | Uint8ArrayConstructor | Int16ArrayConstructor | Uint16ArrayConstructor | Int32ArrayConstructor | Uint32ArrayConstructor | Uint8ClampedArrayConstructor | Float32ArrayConstructor | Float64ArrayConstructor;

export
interface IArrayLookup {
    int8: Int8Array,
    int16: Int16Array,
    int32: Int32Array,
    uint8: Uint8Array,
    uint16: Uint16Array,
    uint32: Uint32Array,
    float32: Float32Array,
    float64: Float64Array
};

/**
 * The serialized representation of a received array
 */
export
interface IReceivedSerializedArray {
  shape: number[];
  dtype: keyof IArrayLookup;
  buffer: DataView;
}

/**
 * The serialized representation of an array for sending
 */
export
interface ISendSerializedArray {
  shape: number[];
  dtype: keyof IArrayLookup;
  buffer: ArrayBuffer;
}


export
function JSONToArray(obj: IReceivedSerializedArray | null, manager?: ManagerBase<any>): ndarray.NDArray | null {
  if (obj === null) {
    return null;
  }
  // obj is {shape: list, dtype: string, array: DataView}
  // return an ndarray object
  return ndarray(new typesToArray[obj.dtype](obj.buffer.buffer), obj.shape);
}

export
function arrayToJSON(obj: ndarray.NDArray | null, widget?: WidgetModel): ISendSerializedArray | null {
  if (obj === null) {
    return null;
  }
  // serialize to {shape: list, dtype: string, array: buffer}
  return { shape: obj.shape, dtype: obj.dtype, buffer: obj.data as TypedArray };
}

export
const array_serialization = { deserialize: JSONToArray, serialize: arrayToJSON };

const typesToArray = {
    int8: Int8Array,
    int16: Int16Array,
    int32: Int32Array,
    uint8: Uint8Array,
    uint16: Uint16Array,
    uint32: Uint32Array,
    float32: Float32Array,
    float64: Float64Array
}

export
class NDArrayModel extends WidgetModel {
  defaults() {
    return _.extend(super.defaults(), {
      array: ndarray([]),
      _model_name: NDArrayModel.model_name,
      _model_module: NDArrayModel.model_module,
      _model_module_version: NDArrayModel.model_module_version,
      _view_name: NDArrayModel.view_name,
      _view_module: NDArrayModel.view_module,
      _view_module_version: NDArrayModel.view_module_version,
    });
  }

  static serializers = {
      ...WidgetModel.serializers,
      array: array_serialization,
    }

  static model_name = 'NDArrayModel';
  static model_module = 'jupyter-datawidgets';
  static model_module_version = version;
  static view_name = null;
  static view_module = null;
  static view_module_version = '';
}

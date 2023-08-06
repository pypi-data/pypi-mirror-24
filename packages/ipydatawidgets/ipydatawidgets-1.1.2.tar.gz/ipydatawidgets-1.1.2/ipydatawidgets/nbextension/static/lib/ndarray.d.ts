import { WidgetModel, ManagerBase } from '@jupyter-widgets/base';
export { JUPYTER_DATAWIDGETS_VERSION } from './version';
import ndarray = require('ndarray');
export declare const version: any;
export declare type TypedArray = Int8Array | Uint8Array | Int16Array | Uint16Array | Int32Array | Uint32Array | Uint8ClampedArray | Float32Array | Float64Array;
export declare type TypedArrayConstructor = Int8ArrayConstructor | Uint8ArrayConstructor | Int16ArrayConstructor | Uint16ArrayConstructor | Int32ArrayConstructor | Uint32ArrayConstructor | Uint8ClampedArrayConstructor | Float32ArrayConstructor | Float64ArrayConstructor;
export interface IArrayLookup {
    int8: Int8Array;
    int16: Int16Array;
    int32: Int32Array;
    uint8: Uint8Array;
    uint16: Uint16Array;
    uint32: Uint32Array;
    float32: Float32Array;
    float64: Float64Array;
}
/**
 * The serialized representation of a received array
 */
export interface IReceivedSerializedArray {
    shape: number[];
    dtype: keyof IArrayLookup;
    buffer: DataView;
}
/**
 * The serialized representation of an array for sending
 */
export interface ISendSerializedArray {
    shape: number[];
    dtype: keyof IArrayLookup;
    buffer: ArrayBuffer;
}
export declare function JSONToArray(obj: IReceivedSerializedArray | null, manager?: ManagerBase<any>): ndarray.NDArray | null;
export declare function arrayToJSON(obj: ndarray.NDArray | null, widget?: WidgetModel): ISendSerializedArray | null;
export declare const array_serialization: {
    deserialize: (obj: IReceivedSerializedArray | null, manager?: ManagerBase<any> | undefined) => ndarray.NDArray | null;
    serialize: (obj: ndarray.NDArray | null, widget?: WidgetModel | undefined) => ISendSerializedArray | null;
};
export declare class NDArrayModel extends WidgetModel {
    defaults(): any;
    static serializers: {
        array: {
            deserialize: (obj: IReceivedSerializedArray | null, manager?: ManagerBase<any> | undefined) => ndarray.NDArray | null;
            serialize: (obj: ndarray.NDArray | null, widget?: WidgetModel | undefined) => ISendSerializedArray | null;
        };
    };
    static model_name: string;
    static model_module: string;
    static model_module_version: any;
    static view_name: null;
    static view_module: null;
    static view_module_version: string;
}

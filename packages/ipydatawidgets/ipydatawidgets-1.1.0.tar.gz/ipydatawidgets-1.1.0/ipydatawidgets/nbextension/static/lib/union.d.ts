/// <reference types="backbone" />
import { WidgetModel, ManagerBase } from '@jupyter-widgets/base';
import { NDArrayModel, IReceivedSerializedArray, ISendSerializedArray } from './ndarray';
import ndarray = require('ndarray');
export declare type DataUnion = NDArrayModel | ndarray.NDArray;
/**
 * Deserializes union JSON to an ndarray or a NDArrayModel, as appropriate.
 */
export declare function JSONToUnion(obj: IReceivedSerializedArray | string | null, manager?: ManagerBase<any>): Promise<ndarray.NDArray | NDArrayModel | null>;
/**
 * Deserializes union JSON to an ndarray, regardless of whether it is a widget reference or direct data.
 */
export declare function JSONToUnionArray(obj: IReceivedSerializedArray | string | null, manager?: ManagerBase<any>): Promise<ndarray.NDArray | null>;
/**
 * Serializes a union to JSON.
 */
export declare function unionToJSON(obj: DataUnion | null, widget?: WidgetModel): ISendSerializedArray | string | null;
/**
 * Gets the array of a union.
 */
export declare function getArrayFromUnion(union: DataUnion): ndarray.NDArray;
/**
 * Sets up backbone events for listening to union changes.
 *
 * The callback will be called when:
 *  - The model is a widget, and its data changes
 *
 * Specify `allChanges` as truthy to also cover these cases:
 *  - The union changes from a widget to an array or vice-versa
 *  - The union is an array and its content changes
 *
 * To stop listening, call the return value.
 */
export declare function listenToUnion(model: Backbone.Model, unionName: string, callback: (model: Backbone.Model, options: any) => any, allChanges?: boolean): () => void;
export declare const data_union_array_serialization: {
    deserialize: (obj: string | IReceivedSerializedArray | null, manager?: ManagerBase<any> | undefined) => Promise<ndarray.NDArray | null>;
    serialize: (obj: ndarray.NDArray | NDArrayModel | null, widget?: WidgetModel | undefined) => string | ISendSerializedArray | null;
};
export declare const data_union_serialization: {
    deserialize: (obj: string | IReceivedSerializedArray | null, manager?: ManagerBase<any> | undefined) => Promise<ndarray.NDArray | NDArrayModel | null>;
    serialize: (obj: ndarray.NDArray | NDArrayModel | null, widget?: WidgetModel | undefined) => string | ISendSerializedArray | null;
};

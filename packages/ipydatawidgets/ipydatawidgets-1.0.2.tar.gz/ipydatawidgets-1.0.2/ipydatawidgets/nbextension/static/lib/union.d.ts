import { WidgetModel, ManagerBase } from '@jupyter-widgets/base';
import { IReceivedSerializedArray, ISendSerializedArray } from './ndarray';
import ndarray = require('ndarray');
export declare function JSONToUnion(obj: IReceivedSerializedArray | string | null, manager?: ManagerBase<any>): Promise<ndarray.NDArray | null>;
export declare function unionToJSON(obj: ndarray.NDArray | WidgetModel | null, widget?: WidgetModel): ISendSerializedArray | string | null;
export declare const data_union_serialization: {
    deserialize: (obj: string | IReceivedSerializedArray | null, manager?: ManagerBase<any> | undefined) => Promise<ndarray.NDArray | null>;
    serialize: (obj: ndarray.NDArray | WidgetModel | null, widget?: WidgetModel | undefined) => string | ISendSerializedArray | null;
};

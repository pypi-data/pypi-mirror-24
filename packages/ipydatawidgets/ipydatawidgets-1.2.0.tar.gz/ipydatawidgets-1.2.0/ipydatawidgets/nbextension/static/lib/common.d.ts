import { DataUnion } from './union';
import { ScaledArrayModel } from './scaled';
import ndarray = require('ndarray');
/**
 * Gets the array of any array source.
 */
export declare function getArray(data: DataUnion | ScaledArrayModel | null): ndarray.NDArray | null;

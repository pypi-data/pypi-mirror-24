/// <reference types="backbone" />
import { WidgetModel } from '@jupyter-widgets/base';
import { ObjectHash } from 'backbone';
import { ISerializers } from './base';
import { NDArrayModel, IArrayLookup } from './ndarray';
import ndarray = require('ndarray');
/**
 * Utility to create a copy of an ndarray
 *
 * @param {ndarray.NDArray} array
 * @returns {ndarray.NDArray}
 */
export declare function copyArray(array: ndarray.NDArray, dtype?: keyof IArrayLookup): ndarray.NDArray;
/**
 * Scaled array model.
 *
 * This model provides a scaled version of an array, that is
 * automatically recomputed when either the array or the scale
 * changes.
 *
 * It triggers an event 'change:scaledData' when the array is
 * recomputed. Note: 'scaledData' is a direct propetry, not a
 * model attribute. The event triggers with an argument
 * { resized: boolean}, which indicates whether the array changed
 * size. Note: When the 'resized' flag is false, the old array will
 * have been reused, otherwise a new array is allocated.
 *
 * @export
 * @class ScaledArrayModel
 * @extends {DataModel}
 */
export declare class ScaledArrayModel extends NDArrayModel {
    defaults(): any;
    /**
     * (Re-)compute the scaledData data.
     *
     * @returns {void}
     * @memberof ScaledArrayModel
     */
    computeScaledData(): void;
    /**
     * Initialize the model
     *
     * @param {Backbone.ObjectHash} attributes
     * @param {{model_id: string; comm?: any; widget_manager: any; }} options
     * @memberof ScaledArrayModel
     */
    initialize(attributes: ObjectHash, options: {
        model_id: string;
        comm?: any;
        widget_manager: any;
    }): void;
    /**
     * Sets up any relevant event listeners after the object has been initialized,
     * but before the initPromise is resolved.
     *
     * @memberof ScaledArrayModel
     */
    setupListeners(): void;
    /**
     * Callback for when the source data changes.
     *
     * @param {WidgetModel} model
     * @memberof ScaledArrayModel
     */
    protected onChange(model: WidgetModel): void;
    /**
     * Whether the array and scaledData have a mismatch in shape or type.
     *
     * @protected
     * @returns {boolean}
     * @memberof ScaledArrayModel
     */
    protected arrayMismatch(): boolean;
    protected scaledDtype(): keyof IArrayLookup | undefined;
    /**
     * The scaled data array.
     *
     * @type {(ndarray.NDArray | null)}
     * @memberof ScaledArrayModel
     */
    scaledData: ndarray.NDArray | null;
    /**
     * A promise that resolves once the model has finished its initialization.
     *
     * @type {Promise<void>}
     * @memberof ScaledArrayModel
     */
    initPromise: Promise<void>;
    static serializers: ISerializers;
    static model_name: string;
}

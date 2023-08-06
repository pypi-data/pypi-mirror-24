import { WidgetModel, ManagerBase } from '@jupyter-widgets/base';
export declare const version: any;
export interface ISerializers {
    [key: string]: {
        deserialize?: (value?: any, manager?: ManagerBase<any>) => any;
        serialize?: (value?: any, widget?: WidgetModel) => any;
    };
}
export declare class DataModel extends WidgetModel {
    defaults(): {
        _model_module: string;
        _model_module_version: any;
        _view_name: null;
        _view_module: never;
        _view_module_version: string;
        _model_name: string;
        _view_count: any;
    };
    static serializers: {
        [key: string]: {
            deserialize?: ((value?: any, manager?: ManagerBase<any> | undefined) => any) | undefined;
            serialize?: ((value?: any, widget?: WidgetModel | undefined) => any) | undefined;
        };
    };
    static model_module: string;
    static model_module_version: any;
    static view_name: null;
    static view_module: null;
    static view_module_version: string;
}

/// <reference types="backbone" />
import { WidgetModel, ManagerBase } from '@jupyter-widgets/base';
import { ScaleModel } from './scale';
/**
 * A widget model of a linear scale
 */
export declare class LinearScaleModel extends ScaleModel {
    defaults(): {
        _model_name: string;
        domain: number[];
        range: number[];
        interpolator: string;
        clamp: boolean;
        _model_module: string;
        _model_module_version: string;
        _view_name: any;
        _view_module: any;
        _view_module_version: string;
        _view_count: any;
    };
    /**
     * Create the wrapped d3-scale scaleLinear object
     */
    constructObject(): any;
    /**
     * Sync the model properties to the d3 object.
     */
    syncToObject(): void;
    /**
     * Synt the d3 object properties to the model.
     */
    syncToModel(toSet: Backbone.ObjectHash): void;
    static serializers: {
        [key: string]: {
            deserialize?: ((value?: any, manager?: ManagerBase<any> | undefined) => any) | undefined;
            serialize?: ((value?: any, widget?: WidgetModel | undefined) => any) | undefined;
        };
    };
    static model_name: string;
}

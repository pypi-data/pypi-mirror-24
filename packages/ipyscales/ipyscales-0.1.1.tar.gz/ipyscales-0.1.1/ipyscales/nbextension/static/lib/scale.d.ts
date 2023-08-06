/// <reference types="backbone" />
import { WidgetModel, ManagerBase } from '@jupyter-widgets/base';
export interface ISerializerMap {
    [key: string]: {
        deserialize?: (value?: any, manager?: ManagerBase<any>) => any;
        serialize?: (value?: any, widget?: WidgetModel) => any;
    };
}
export interface IInitializeOptions {
    model_id: string;
    comm?: any;
    widget_manager: ManagerBase<any>;
}
/**
 * Base model for scales
 */
export declare abstract class ScaleModel extends WidgetModel {
    /**
     * Returns default values for the model attributes.
     */
    defaults(): {
        _model_name: string;
        _model_module: string;
        _model_module_version: string;
        _view_name: any;
        _view_module: any;
        _view_module_version: string;
        _view_count: any;
    };
    /**
     * Backbone initialize function.
     */
    initialize(attributes: Backbone.ObjectHash, options: IInitializeOptions): void;
    /**
     * Update the model attributes from the objects properties.
     *
     * The base method calls `this.set(toSet, 'pushFromObject');`
     * if `toSet` is given. Overriding methods should add its
     * properties to the hash before calling the super method.
     */
    syncToModel(toSet: Backbone.ObjectHash): void;
    /**
     * Update the model attributes from the objects properties.
     */
    abstract syncToObject(): void;
    /**
     * Create or return the underlying object this model represents.
     */
    protected createObject(): Promise<any>;
    /**
     * Construct and return the underlying object this model represents.
     *
     * Override this in inherting classes.
     */
    protected abstract constructObject(): any | Promise<any>;
    /**
     * Process a new underlying object to represent this model.
     *
     * The base implementation sets up mapping between the model,
     * the cache, and the widget manager.
     */
    protected processNewObj(obj: any): any | Promise<any>;
    /**
     * Set up any event listeners.
     *
     * Called after object initialization is complete.
     */
    setupListeners(): void;
    onChange(model: Backbone.Model, options: any): void;
    onCustomMessage(content: any, buffers: any): void;
    static serializers: ISerializerMap;
    static model_name: string;
    static model_module: string;
    static model_module_version: string;
    static view_name: null;
    static view_module: null;
    static view_module_version: string;
    /**
     * The underlying object this model represents.
     */
    obj: any;
    /**
     * Promise that resolves when initialization is complete.
     */
    initPromise: Promise<void>;
}

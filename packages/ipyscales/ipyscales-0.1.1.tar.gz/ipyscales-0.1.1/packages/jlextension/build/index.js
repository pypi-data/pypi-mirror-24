"use strict";
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
var yourCode = require("jupyter-scales");
var jupyterlab_manager_1 = require("@jupyter-widgets/jupyterlab-manager");
var EXTENSION_ID = 'jupyter.extensions.jupyter-scales';
/**
 * The token identifying the JupyterLab plugin.
 */
exports.IExampleExtension = new coreutils_1.Token(EXTENSION_ID);
;
/**
 * The notebook diff provider.
 */
var exampleProvider = {
    id: EXTENSION_ID,
    requires: [jupyterlab_manager_1.INBWidgetExtension],
    activate: activateWidgetExtension,
    autoStart: true
};
exports.default = exampleProvider;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, widgetsManager) {
    widgetsManager.registerWidget({
        name: 'jupyter-scales',
        version: yourCode.JUPYTER_EXTENSION_VERSION,
        exports: yourCode
    });
    return {};
}
//# sourceMappingURL=index.js.map
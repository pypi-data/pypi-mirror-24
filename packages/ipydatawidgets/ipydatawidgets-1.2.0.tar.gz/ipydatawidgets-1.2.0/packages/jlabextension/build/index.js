"use strict";
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
var coreutils_1 = require("@phosphor/coreutils");
var dataWidgets = require("jupyter-datawidgets");
var jupyterlab_manager_1 = require("@jupyter-widgets/jupyterlab-manager");
var EXTENSION_ID = 'jupyter.extensions.datawidgets';
/**
 * The token identifying the JupyterLab plugin.
 */
exports.IDataWidgetsExtension = new coreutils_1.Token(EXTENSION_ID);
;
/**
 * The notebook diff provider.
 */
var dataWidgetsProvider = {
    id: EXTENSION_ID,
    requires: [jupyterlab_manager_1.INBWidgetExtension],
    activate: activateWidgetExtension,
    autoStart: true
};
exports.default = dataWidgetsProvider;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, widgetsManager) {
    widgetsManager.registerWidget({
        name: 'jupyter-datawidgets',
        version: dataWidgets.JUPYTER_DATAWIDGETS_VERSION,
        exports: dataWidgets
    });
    return {};
}
//# sourceMappingURL=index.js.map
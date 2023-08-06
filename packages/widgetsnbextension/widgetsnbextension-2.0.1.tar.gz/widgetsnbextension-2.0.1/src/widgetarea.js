// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
"use strict";

require('../css/outputarea.css');

var messaging = require('phosphor/lib/core/messaging');
var pwidgets = require('phosphor/lib/ui/widget');

/**
 * WidgetArea
 */
var WidgetArea = function(cell) {
    this.widget_views = [];

    this._cell = cell;
    this._widgets_live = true;

    this._create_elements();
    requirejs(['base/js/events'], (function(events) {
        events.trigger('create.WidgetArea', {widgetarea: this, cell: cell});
    }).bind(this));
};

/**
*  Display a widget view in the cell.
*/
WidgetArea.prototype.display_widget_view = function(view_promise) {

    // Display a dummy element
    var dummy = document.createElement('div');
    this.widget_subarea.appendChild(dummy);

    // Display the view.
    var that = this;
    return view_promise.then(function(view) {
        that.widget_area.style.display = '';

        // Do basically the same as Phosphor's Widget.attach, except we replace
        // a child rather than appending the view's Phosphor widget
        dummy.parentNode.replaceChild(view.pWidget.node, dummy);
        messaging.sendMessage(view.pWidget, pwidgets.WidgetMessage.AfterAttach)

        that.widget_views.push(view);

        // Check the live state of the view's model.
        if (view.model.comm_live) {
            that._widget_live(view);
        } else {
            that.disconnect(view);
        }

        // If the view is removed, check to see if the widget area is empty.
        // If the widget area is empty, close it.
        view.on('remove', function() {
            var index = that.widget_views.indexOf(view);
            if (index !== -1) that.widget_views.splice(index, 1);

            if (that.widget_views.length === 0) {
                that.clear();
            }
        });

        return view;
    });
};

/**
 * Creates the elements of the widget area and appends them
 * to the associated cell.
 */
WidgetArea.prototype._create_elements = function() {
    var widget_area = document.createElement('div');
    widget_area.classList.add('widget-area');
    widget_area.style.display = 'none';

    this.widget_area = widget_area;

    var widget_prompt = document.createElement('div');
    widget_prompt.classList.add('prompt');
    widget_area.appendChild(widget_prompt);

    var widget_subarea = document.createElement('div');
    widget_subarea.classList.add('widget-subarea');
    widget_subarea.classList.add('jp-Output-result');
    widget_area.appendChild(widget_subarea);

    this.widget_subarea = widget_subarea;
    var that = this;

    var widget_clear_button = document.createElement('button');
    widget_clear_button.classList.add('close');
    widget_clear_button.innerHTML = '&times;';
    widget_clear_button.onclick = function() {
      for (var i = 0; i < that.widget_views.length; i++) {
        var view = that.widget_views[i];
        view.remove();
      }
      that.widget_views = [];
      widget_subarea.innerHTML = '';
    }

    widget_prompt.appendChild(widget_clear_button);

    if (this._cell.input) {
        this._cell.input.after(widget_area);
    } else {
        throw new Error('Cell does not have an `input` element.  Is it not a CodeCell?');
    }
};

/**
 * Handles when a widget loses it's comm connection.
 * @param {WidgetView} view
 */
WidgetArea.prototype.disconnect = function() {
    if (this._widgets_live) {
        this._widgets_live = false;
        this.widget_area.classList.add('connection-problems');
    }
};

/**
 * Sends resize message to all child views
 */
WidgetArea.prototype.resize = function() {
    this.widget_views.forEach(function(view) {
        messaging.sendMessage(view.pWidget, pwidgets.ResizeMessage.UnknownSize);
    });
}

/**
 * Handles when a widget is connected to a live comm.
 */
WidgetArea.prototype._widget_live = function() {
    if (!this._widgets_live) {
        // Check that the other widgets are live too.  O(N) operation.
        // Abort the function at the first dead widget found.
        for (var i = 0; i < this.widget_views.length; i++) {
            if (!this.widget_views[i].model.comm_live) {
                return;
            }
        }
        this._widgets_live = true;
        this.widget_area.classList.remove('connection-problems');
    }
};

/**
 * Clears the widgets in the widget area.
 */
WidgetArea.prototype.clear = function() {
    // Clear widget area
    for (var i = 0; i < this.widget_views.length; i++) {
        var view = this.widget_views[i];
        view.remove();
    }
    this.widget_views = [];
    this.widget_subarea.innerHTML = '';
    this.widget_subarea.style.height = '';
    this.widget_area.style.height = '';
    this.widget_area.style.display = 'none';
};

module.exports = {
    WidgetArea: WidgetArea
};

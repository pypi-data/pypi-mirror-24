/// <reference path="signals.ts" />)
/// <reference path="globals.ts" />
/// <reference path="base.ts" />
/// <reference path="urls.ts" />
/// <reference path="dialog.ts" />
/// <reference path="widgets.ts" />
/// <reference path="session.ts" />
/// <reference path="state.ts" />
/// <reference path="DefinitelyTyped/jquery.d.ts" />
/// <reference path="DefinitelyTyped/jqueryui.d.ts" />
/*
spud - keep track of photos
Copyright (C) 2008-2013 Brian May

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
"use strict";
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
///////////////////////////////////////
// object_loader
///////////////////////////////////////
var ObjectLoader = (function () {
    function ObjectLoader(obj_type, obj_id) {
        this.obj_type = obj_type;
        this.loaded_item = new Signal();
        this.on_error = new Signal();
        if (typeof obj_id == "number") {
            this.obj_id = obj_id;
            this.obj = null;
            this.loading = false;
            this.finished = false;
        }
        else {
            this.obj = obj_id;
            this.obj_id = obj_id.id;
            this.loading = false;
            this.finished = true;
            this.loaded_item.disable(this.obj);
            this.on_error.disable(null);
        }
    }
    ObjectLoader.prototype.load = function () {
        var _this = this;
        var type = this.obj_type.get_type();
        if (this.loading) {
            return;
        }
        if (this.finished) {
            return;
        }
        //var criteria = this.criteria
        var page = this.page;
        //var params = $.extend({}, criteria, { 'page': page })
        var params = { 'page': page };
        console.log("loading object", type, this.obj_id);
        this.loading = true;
        this.obj = null;
        this.xhr = ajax({
            url: window.__api_prefix + "api/" + type + "/" + this.obj_id + "/",
            data: params
        }, function (data) {
            console.log("got object", type, _this.obj_id);
            _this.loading = false;
            _this.finished = true;
            _this.obj = _this.obj_type.object_from_streamable(data);
            _this.got_item(_this.obj);
            _this.on_error.disable(null);
        }, function (message, data) {
            console.log("error loading", type, _this.obj_id, message);
            _this.loading = false;
            _this.finished = true;
            _this.obj = null;
            _this.loaded_item.disable(null);
            _this.on_error.trigger(message);
            _this.on_error.disable(message);
        });
    };
    ObjectLoader.prototype.abort = function () {
        if (this.loading) {
            this.xhr.abort();
            this.loading = false;
            this.finished = true;
            this.obj = null;
            this.loaded_item.disable(null);
            this.on_error.disable("aborted");
        }
    };
    ObjectLoader.prototype.got_item = function (obj) {
        this.loaded_item.trigger(obj);
        this.loaded_item.disable(obj);
    };
    ObjectLoader.prototype.check_for_listeners = function () {
        if (this.loaded_item.is_any_listeners()) {
            return;
        }
        this.abort();
    };
    ObjectLoader.prototype.get_obj = function () {
        if (this.finished) {
            return this.obj;
        }
        else {
            return null;
        }
    };
    ObjectLoader.prototype.get_obj_id = function () {
        if (this.obj != null) {
            return this.obj.id;
        }
        else {
            return null;
        }
    };
    ObjectLoader.prototype.get_obj_type = function () {
        return this.obj_type.get_type();
    };
    return ObjectLoader;
}());
var IdMap = (function () {
    function IdMap() {
    }
    return IdMap;
}());
var ObjectListLoader = (function () {
    function ObjectListLoader(obj_type, criteria) {
        var _this = this;
        this.obj_type = obj_type;
        this.obj_array = [];
        this.criteria = criteria;
        this.page = 1;
        this.n = 0;
        this.loading = false;
        this.finished = false;
        // this.loaded_item = new Signal<ObjectNotification<U>>()
        // this.loaded_item.on_no_listeners = () => { this.check_for_listeners() }
        this.loaded_list = new Signal();
        this.loaded_list.on_no_listeners = function () { _this.check_for_listeners(); };
        this.on_error = new Signal();
        this.last_id = null;
        this.idmap = {};
    }
    ObjectListLoader.prototype.load_next_page = function () {
        var _this = this;
        var type = this.obj_type.get_type();
        if (this.loading) {
            return true;
        }
        if (this.finished) {
            return false;
        }
        var criteria = this.criteria;
        var page = this.page;
        var params = $.extend({}, criteria.get_streamable(), { 'page': page });
        console.log("loading list", type, criteria, page);
        this.loading = true;
        this.obj_array = [];
        this.xhr = ajax({
            url: window.__api_prefix + "api/" + type + "/",
            data: params
        }, function (data) {
            console.log("got list", type, criteria, page);
            _this.loading = false;
            _this.page = page + 1;
            if (!data['next']) {
                console.log("finished list", type, criteria, page);
                _this.finished = true;
            }
            var page_list = [];
            var list = get_streamable_array(data, 'results');
            for (var i = 0; i < list.length; i++) {
                var streamable = streamable_to_object(list[i]);
                var obj = _this.obj_type.object_from_streamable(streamable);
                page_list.push(obj);
                _this.obj_array.push(obj);
            }
            var count = get_streamable_number(data, 'count');
            _this.got_list(page_list, count, _this.finished);
        }, function (message, data) {
            _this.loading = false;
            _this.finished = true;
            console.log("error loading", _this.obj_type.get_type(), criteria, message);
            _this.loaded_list.disable(null);
            _this.on_error.trigger(message);
            _this.on_error.disable(message);
        });
        return true;
    };
    ObjectListLoader.prototype.abort = function () {
        if (this.loading) {
            this.xhr.abort();
        }
    };
    ObjectListLoader.prototype.got_list = function (object_list, count, last_page) {
        for (var i = 0; i < object_list.length; i++) {
            var obj = object_list[i];
            this.got_item(obj, count, this.n);
            this.n = this.n + 1;
        }
        // we trigger the object_list *after* all objects have been processed.
        var page_notification = {
            list: object_list,
            count: count
        };
        this.loaded_list.trigger(page_notification);
        // immediate dispatch for all objects
        var all_notification = {
            list: this.obj_array,
            count: count
        };
        if (last_page) {
            this.loaded_list.disable(all_notification);
            this.on_error.disable(null);
        }
        else {
            this.loaded_list.set_immediate_dispatch(all_notification);
        }
    };
    ObjectListLoader.prototype.got_item = function (obj, count, n) {
        var id = obj.id;
        if (id != null) {
            this.idmap[id] = Object();
            if (this.last_id) {
                this.idmap[this.last_id].next = id;
                this.idmap[id].prev = this.last_id;
            }
            this.last_id = id;
        }
    };
    ObjectListLoader.prototype.get_meta = function (obj_id) {
        var meta = this.idmap[obj_id];
        if (!meta) {
            return null;
        }
        if (!meta.next) {
            this.load_next_page();
        }
        return meta;
    };
    ObjectListLoader.prototype.check_for_listeners = function () {
        if (this.loaded_list.is_any_listeners()) {
            return;
        }
        // if (this.loaded_item.is_any_listeners()) {
        //     return
        // }
        this.abort();
    };
    return ObjectListLoader;
}());
var ObjectType = (function () {
    function ObjectType(type, type_name) {
        this.type = type;
        this.type_name = type_name;
    }
    ObjectType.prototype.get_type = function () { return this.type; };
    ObjectType.prototype.get_type_name = function () { return this.type_name; };
    ObjectType.prototype.get_loader_for_object = function (obj) {
        var loader = new ObjectLoader(this, obj);
        return loader;
    };
    ObjectType.prototype.load = function (id) {
        var loader = new ObjectLoader(this, id);
        loader.load();
        return loader;
    };
    ObjectType.prototype.load_list = function (criteria) {
        var loader = new ObjectListLoader(this, criteria);
        loader.load_next_page();
        return loader;
    };
    return ObjectType;
}());
var ObjectSearchDialogOptions = (function (_super) {
    __extends(ObjectSearchDialogOptions, _super);
    function ObjectSearchDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return ObjectSearchDialogOptions;
}(FormDialogOptions));
var ObjectSearchDialog = (function (_super) {
    __extends(ObjectSearchDialog, _super);
    function ObjectSearchDialog(options) {
        return _super.call(this, options) || this;
    }
    ObjectSearchDialog.prototype.submit_values = function (values) {
        var criteria = this.new_criteria();
        for (var key in values) {
            var value = values[key];
            if (value != null && value !== false) {
                criteria[key] = value;
            }
        }
        if (this.options.on_success(criteria)) {
            this.remove();
        }
    };
    return ObjectSearchDialog;
}(FormDialog));
var ObjectChangeDialogOptions = (function (_super) {
    __extends(ObjectChangeDialogOptions, _super);
    function ObjectChangeDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return ObjectChangeDialogOptions;
}(FormDialogOptions));
var ObjectChangeDialog = (function (_super) {
    __extends(ObjectChangeDialog, _super);
    function ObjectChangeDialog(options) {
        return _super.call(this, options) || this;
    }
    ObjectChangeDialog.prototype.set = function (obj) {
        this.obj = obj;
        if (obj.id != null) {
            this.set_title("Change " + this.type_name);
            this.set_description("Please change " + this.type_name + " " + obj.title + ".");
        }
        else {
            this.set_title("Add new album");
            this.set_description("Please add new album.");
        }
        _super.prototype.set.call(this, obj);
    };
    ObjectChangeDialog.prototype.submit_values = function (values) {
        for (var key in values) {
            this.obj[key] = values[key];
        }
        var updates = this.obj.get_streamable();
        if (this.obj.id != null) {
            this.save('PATCH', this.obj.id, updates);
        }
        else {
            this.save('POST', null, updates);
        }
    };
    return ObjectChangeDialog;
}(FormDialog));
var ObjectDeleteDialogOptions = (function (_super) {
    __extends(ObjectDeleteDialogOptions, _super);
    function ObjectDeleteDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return ObjectDeleteDialogOptions;
}(FormDialogOptions));
var ObjectDeleteDialog = (function (_super) {
    __extends(ObjectDeleteDialog, _super);
    function ObjectDeleteDialog(options) {
        return _super.call(this, options) || this;
    }
    ObjectDeleteDialog.prototype.show = function (element) {
        this.options.title = "Delete " + this.type_name;
        this.options.button = "Delete";
        _super.prototype.show.call(this, element);
    };
    ObjectDeleteDialog.prototype.set = function (obj) {
        this.obj_id = obj.id;
        this.set_description("Are you absolutely positively sure you really want to delete " +
            obj.title + "? Go ahead join the dark side. There are cookies.");
    };
    ObjectDeleteDialog.prototype.submit_values = function (values) {
        this.save('DELETE', this.obj_id, {});
    };
    return ObjectDeleteDialog;
}(FormDialog));
var ObjectCriteriaWidgetOptions = (function (_super) {
    __extends(ObjectCriteriaWidgetOptions, _super);
    function ObjectCriteriaWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return ObjectCriteriaWidgetOptions;
}(WidgetOptions));
var CriteriaItem = (function () {
    function CriteriaItem(key, title) {
        this.key = key;
        this.title = title;
    }
    return CriteriaItem;
}());
var CriteriaItemString = (function (_super) {
    __extends(CriteriaItemString, _super);
    function CriteriaItemString(key, title, value) {
        var _this = _super.call(this, key, title) || this;
        _this.key = key;
        _this.title = title;
        _this.value = value;
        return _this;
    }
    CriteriaItemString.prototype.render = function () {
        if (this.value == null) {
            return null;
        }
        return $('<li>').text(this.title + " == " + this.value);
    };
    CriteriaItemString.prototype.get_idinputfield = function () {
        return [this.key, new TextInputField(this.title, false)];
    };
    return CriteriaItemString;
}(CriteriaItem));
var CriteriaItemBoolean = (function (_super) {
    __extends(CriteriaItemBoolean, _super);
    function CriteriaItemBoolean(key, title, value) {
        var _this = _super.call(this, key, title) || this;
        _this.key = key;
        _this.title = title;
        _this.value = value;
        return _this;
    }
    CriteriaItemBoolean.prototype.render = function () {
        if (this.value == null) {
            return null;
        }
        return $('<li>').text(this.title + " == " + this.value);
    };
    CriteriaItemBoolean.prototype.get_idinputfield = function () {
        return [this.key, new booleanInputField(this.title, false)];
    };
    return CriteriaItemBoolean;
}(CriteriaItem));
var CriteriaItemNumber = (function (_super) {
    __extends(CriteriaItemNumber, _super);
    function CriteriaItemNumber(key, title, value) {
        var _this = _super.call(this, key, title) || this;
        _this.key = key;
        _this.title = title;
        _this.value = value;
        return _this;
    }
    CriteriaItemNumber.prototype.render = function () {
        if (this.value == null) {
            return null;
        }
        return $('<li>').text(this.title + " == " + this.value);
    };
    CriteriaItemNumber.prototype.get_idinputfield = function () {
        return [this.key, new IntegerInputField(this.title, false)];
    };
    return CriteriaItemNumber;
}(CriteriaItem));
var CriteriaItemDateTimeZone = (function (_super) {
    __extends(CriteriaItemDateTimeZone, _super);
    function CriteriaItemDateTimeZone(key, title, value) {
        var _this = _super.call(this, key, title) || this;
        _this.key = key;
        _this.title = title;
        _this.value = value;
        return _this;
    }
    CriteriaItemDateTimeZone.prototype.render = function () {
        if (this.value == null) {
            return null;
        }
        var datetime = moment(this.value[0]);
        var utc_offset = this.value[1];
        datetime.local();
        var datetime_str;
        datetime_str = datetime.format("dddd, MMMM Do YYYY, h:mm:ss a");
        return $('<li>').text(this.title + " == " + datetime_str);
    };
    CriteriaItemDateTimeZone.prototype.get_idinputfield = function () {
        return [this.key, new IntegerInputField(this.title, false)];
    };
    return CriteriaItemDateTimeZone;
}(CriteriaItem));
var CriteriaItemObject = (function (_super) {
    __extends(CriteriaItemObject, _super);
    function CriteriaItemObject(key, title, value, obj_type) {
        var _this = _super.call(this, key, title) || this;
        _this.key = key;
        _this.title = title;
        _this.value = value;
        _this.obj_type = obj_type;
        return _this;
    }
    CriteriaItemObject.prototype.render = function () {
        if (this.value == null) {
            return null;
        }
        return $('<li>').text(this.title + " == " + this.value.title);
    };
    CriteriaItemObject.prototype.get_idinputfield = function () {
        return [this.key, new AjaxSelectField(this.title, this.obj_type, false)];
    };
    return CriteriaItemObject;
}(CriteriaItem));
var CriteriaItemSelect = (function (_super) {
    __extends(CriteriaItemSelect, _super);
    function CriteriaItemSelect(key, title, value, options) {
        var _this = _super.call(this, key, title) || this;
        _this.key = key;
        _this.title = title;
        _this.value = value;
        _this.options = options;
        return _this;
    }
    CriteriaItemSelect.prototype.render = function () {
        if (this.value == null) {
            return null;
        }
        return $('<li>').text(this.title + " == " + this.value);
    };
    CriteriaItemSelect.prototype.get_idinputfield = function () {
        return [this.key, new SelectInputField(this.title, this.options, false)];
    };
    return CriteriaItemSelect;
}(CriteriaItem));
var ObjectCriteriaWidget = (function (_super) {
    __extends(ObjectCriteriaWidget, _super);
    function ObjectCriteriaWidget(options) {
        return _super.call(this, options) || this;
        // this.obj_type = obj_type
    }
    ObjectCriteriaWidget.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.element.data('object_criteria', this);
        this.loaders = [];
        this.criteria = $("<ul/>")
            .addClass("criteria")
            .appendTo(this.element);
        if (this.options.obj) {
            this.set(this.options.obj);
        }
    };
    ObjectCriteriaWidget.prototype.set = function (criteria) {
        this.options.obj = criteria;
        this.element.removeClass("error");
        var ul = this.criteria;
        ul.empty();
        var items = criteria.get_items();
        for (var i = 0; i < items.length; i++) {
            var item = items[i].render();
            if (item != null) {
                item.appendTo(ul);
            }
        }
    };
    ObjectCriteriaWidget.prototype.set_error = function () {
        this.element.addClass("error");
    };
    ObjectCriteriaWidget.prototype.cancel_loaders = function () {
        remove_all_listeners(this);
    };
    return ObjectCriteriaWidget;
}(Widget));
var ObjectListWidgetOptions = (function (_super) {
    __extends(ObjectListWidgetOptions, _super);
    function ObjectListWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return ObjectListWidgetOptions;
}(ImageListWidgetOptions));
var ObjectListWidget = (function (_super) {
    __extends(ObjectListWidget, _super);
    function ObjectListWidget(options, obj_type) {
        var _this = _super.call(this, options) || this;
        _this.obj_type = obj_type;
        return _this;
    }
    ObjectListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        this.element.data('object_list', this);
        this.page = 1;
        if (this.options.disabled) {
            this.element.addClass("disabled");
        }
        if (this.options.criteria != null) {
            this.filter(this.options.criteria);
        }
        this.element.scroll(function () {
            _this.load_if_required();
        });
        window._reload_all.add_listener(this, function () {
            _this.empty();
            _this.filter(_this.options.criteria);
        });
    };
    ObjectListWidget.prototype.get_item = function (obj_id) {
        return this.ul.find("[data-id=" + obj_id + "]");
    };
    ObjectListWidget.prototype.add_item = function (obj) {
        var li = this.create_li_for_obj(obj);
        li.appendTo(this.ul);
    };
    ObjectListWidget.prototype.add_list = function (notification) {
        for (var i = 0; i < notification.list.length; i++) {
            var obj = notification.list[i];
            this.add_item(obj);
        }
        this.element.toggleClass("hidden", notification.count === 0);
        this.load_if_required();
    };
    ObjectListWidget.prototype.load_if_required = function () {
        // if element is not displayed, we can't tell the scroll position,
        // so we must wait for element to be displayed before we can continue
        // loading
        if (!this.options.disabled && this.loader) {
            if (this.element.prop('scrollHeight') <
                this.element.scrollTop() + this.element.height() + 200) {
                this.loader.load_next_page();
            }
        }
    };
    ObjectListWidget.prototype.filter = function (criteria) {
        var _this = this;
        this.options.criteria = criteria;
        if (this.element == null) {
            return;
        }
        this.empty();
        var old_loader = this.loader;
        if (old_loader != null) {
            old_loader.loaded_list.remove_listener(this);
            old_loader.on_error.remove_listener(this);
        }
        this.loader = new ObjectListLoader(this.obj_type, criteria);
        this.loader.loaded_list.add_listener(this, this.add_list);
        this.loader.on_error.add_listener(this, function (message) {
            console.log(message);
            _this.element.addClass("error");
        });
        this.loader.load_next_page();
    };
    ObjectListWidget.prototype.empty = function () {
        this.page = 1;
        _super.prototype.empty.call(this);
        this.element.removeClass("error");
        if (this.loader) {
            this.loader.loaded_list.remove_listener(this);
            this.loader.on_error.remove_listener(this);
            this.loader = null;
        }
    };
    ObjectListWidget.prototype.enable = function () {
        this.element.removeClass("disabled");
        this.load_if_required();
        _super.prototype.enable.call(this);
    };
    ObjectListWidget.prototype.disable = function () {
        this.element.addClass("disabled");
        _super.prototype.disable.call(this);
    };
    ObjectListWidget.prototype.get_child_viewport = function () {
        var child_id = this.options.child_id;
        if (child_id != null) {
            var child = $(document.getElementById(child_id));
            if (child.length > 0) {
                var viewport = child.data('widget');
                return viewport;
            }
        }
        return null;
    };
    ObjectListWidget.prototype.get_or_create_child_viewport = function () {
        var viewport = this.get_child_viewport();
        if (viewport != null) {
            return viewport;
        }
        viewport = this.create_child_viewport();
        return viewport;
    };
    ObjectListWidget.prototype.obj_a = function (obj) {
        var _this = this;
        var mythis = this;
        var album_list_loader = this.loader;
        var title = obj.title;
        var a = $('<a/>')
            .attr('href', root_url() + this.obj_type.get_type() + "/" + obj.id + "/")
            .on('click', function () {
            if (mythis.options.disabled) {
                return false;
            }
            var viewport = _this.get_or_create_child_viewport();
            viewport.set_list_loader(album_list_loader);
            // We cannot use set(obj) here as required attributes may be
            // missing from list view for detail view
            viewport.load(obj.id);
            return false;
        })
            .data('photo', obj.cover_photo)
            .text(title);
        return a;
    };
    ObjectListWidget.prototype.get_photo = function (obj) {
        return obj.cover_photo;
    };
    ObjectListWidget.prototype.get_details = function (obj) {
        var details = [];
        return details;
    };
    ObjectListWidget.prototype.get_description = function (obj) {
        return null;
    };
    ObjectListWidget.prototype.create_li_for_obj = function (obj) {
        var photo = this.get_photo(obj);
        var details = this.get_details(obj);
        var description = this.get_description(obj);
        var a = this.obj_a(obj);
        var li = this.create_li(photo, obj.title, details, description, a);
        li.attr('data-id', obj.id);
        return li;
    };
    return ObjectListWidget;
}(ImageListWidget));
///////////////////////////////////////
// generic viewports
///////////////////////////////////////
var ObjectListViewportOptions = (function (_super) {
    __extends(ObjectListViewportOptions, _super);
    function ObjectListViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return ObjectListViewportOptions;
}(ViewportOptions));
var ObjectListViewport = (function (_super) {
    __extends(ObjectListViewport, _super);
    function ObjectListViewport(options, obj_type) {
        var _this = _super.call(this, options) || this;
        _this.obj_type = obj_type;
        return _this;
    }
    ObjectListViewport.prototype.setup_menu = function (menu) {
        var _this = this;
        menu.append($("<li/>")
            .text("Filter")
            .on("click", function (ev) {
            var on_success = function (criteria) {
                _this.filter(criteria);
                push_state();
                return true;
            };
            var dialog = _this.obj_type.search_dialog(_this.options.criteria, on_success);
            var div = $("<div/>");
            dialog.show(div);
        }));
        this.create_item = $("<li/>")
            .text("Create")
            .on("click", function (ev) {
            void ev;
            var dialog = _this.obj_type.create_dialog(null);
            var div = $("<div/>");
            dialog.show(div);
        })
            .appendTo(menu);
    };
    ObjectListViewport.prototype.show = function (element) {
        var _this = this;
        this.options.title = this.obj_type.get_type_name() + " list";
        _super.prototype.show.call(this, element);
        // create menu
        var menu = $("<ul/>")
            .addClass("menubar");
        this.setup_menu(menu);
        menu.menu()
            .appendTo(this.div);
        // create ObjectCriteriaWidget
        this.oc = this.obj_type.criteria_widget(this.options.criteria);
        this.set_title(this.obj_type.get_type_name() + " list: " + this.options.criteria.get_title());
        this.criteria = $("<div/>").appendTo(this.div);
        this.oc.show(this.criteria);
        // create ObjectListWidget
        this.ol = this.obj_type.list_widget(this.options.id + ".child", this.options.criteria, this.options.disabled);
        $("<div/>")
            .set_widget(this.ol)
            .appendTo(this.div);
        // setup permissions
        this.setup_perms(window._perms);
        window._perms_changed.add_listener(this, function (perms) {
            _this.setup_perms(perms);
            _this.filter(_this.options.criteria);
        });
    };
    ObjectListViewport.prototype.setup_perms = function (perms) {
        var can_create = false;
        var type = this.obj_type.get_type();
        if (perms[type] != null) {
            var perms_for_type = perms[type];
            can_create = perms_for_type.can_create;
        }
        this.create_item.toggle(can_create);
    };
    ObjectListViewport.prototype.filter = function (value) {
        this.options.criteria = value;
        if (this.element == null) {
            return;
        }
        this.oc.set(value);
        this.set_title(this.obj_type.get_type_name() + " list: " + this.options.criteria.get_title());
        this.ol.filter(value);
    };
    ObjectListViewport.prototype._enable = function () {
        _super.prototype._enable.call(this);
        if (this.ol != null) {
            this.ol.enable();
        }
    };
    ObjectListViewport.prototype._disable = function () {
        _super.prototype._disable.call(this);
        if (this.ol != null) {
            this.ol.disable();
        }
    };
    ObjectListViewport.prototype.get_url = function () {
        var params = $.param(this.get_streamable_state());
        var type = this.obj_type.get_type();
        if (params != "") {
            return root_url() + type + "/?" + params;
        }
        else {
            return root_url() + type + "/";
        }
    };
    ObjectListViewport.prototype.get_streamable_state = function () {
        var streamable = _super.prototype.get_streamable_state.call(this);
        if (this.options.criteria != null) {
            $.extend(streamable, this.options.criteria.get_streamable());
        }
        return streamable;
    };
    ObjectListViewport.prototype.set_streamable_state = function (streamable) {
        var _this = this;
        // load streamable state, must be called before show() is called.
        _super.prototype.set_streamable_state.call(this, streamable);
        this.obj_type.criteria_from_streamable(streamable, function (criteria) {
            _this.filter(criteria);
        });
    };
    return ObjectListViewport;
}(Viewport));
var ObjectDetailViewportOptions = (function (_super) {
    __extends(ObjectDetailViewportOptions, _super);
    function ObjectDetailViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return ObjectDetailViewportOptions;
}(ViewportOptions));
var ObjectDetailViewport = (function (_super) {
    __extends(ObjectDetailViewport, _super);
    function ObjectDetailViewport(options, obj_type) {
        var _this = _super.call(this, options) || this;
        _this.obj_type = obj_type;
        _this.display_photo_list_link = true;
        return _this;
    }
    ObjectDetailViewport.prototype.get_obj = function () {
        if (this.options.object_loader != null) {
            return this.options.object_loader.get_obj();
        }
        else {
            return null;
        }
    };
    ObjectDetailViewport.prototype.get_obj_id = function () {
        if (this.options.object_loader != null) {
            return this.options.object_loader.get_obj_id();
        }
        else {
            return null;
        }
    };
    ObjectDetailViewport.prototype.setup_menu = function (menu) {
        var _this = this;
        menu.append($("<li/>")
            .text("Children")
            .on("click", function (ev) {
            var children_criteria = _this.get_children_criteria();
            var viewport = _this.obj_type.list_viewport(children_criteria, null);
            add_viewport(viewport);
        }));
        if (this.display_photo_list_link) {
            menu.append($("<li/>")
                .text("Photos")
                .on("click", function (ev) {
                var children_criteria = _this.get_photo_criteria();
                var options = {
                    criteria: children_criteria
                };
                var viewport = new PhotoListViewport(options);
                add_viewport(viewport);
            }));
        }
        this.create_item = $("<li/>")
            .text("Create")
            .on("click", function (ev) {
            void ev;
            var obj = _this.get_obj();
            if (obj != null) {
                var dialog = _this.obj_type.create_dialog(obj);
                var div = $("<div/>");
                dialog.show(div);
            }
        })
            .appendTo(menu);
        this.change_item = $("<li/>")
            .text("Change")
            .on("click", function (ev) {
            var obj = _this.get_obj();
            if (obj != null) {
                var dialog = _this.obj_type.change_dialog(obj);
                var div = $("<div/>");
                dialog.show(div);
            }
        })
            .appendTo(menu);
        this.delete_item = $("<li/>")
            .text("Delete")
            .on("click", function (ev) {
            var obj = _this.get_obj();
            if (obj != null) {
                var dialog = _this.obj_type.delete_dialog(obj);
                var div = $("<div/>");
                dialog.show(div);
            }
        })
            .appendTo(menu);
    };
    ObjectDetailViewport.prototype.show = function (element) {
        var _this = this;
        var type_name = this.obj_type.get_type_name();
        this.options.title = type_name + " Detail";
        _super.prototype.show.call(this, element);
        var menu = $("<ul/>")
            .addClass("menubar");
        this.setup_menu(menu);
        menu
            .menu()
            .appendTo(this.div);
        var button_div = $("<div/>").appendTo(this.div);
        this.prev_button = $("<input/>")
            .attr('type', 'submit')
            .attr('value', '<<')
            .click(function () {
            var oll = _this.options.object_list_loader;
            var meta = oll.get_meta(_this.get_obj_id());
            var obj_id = meta.prev;
            if (obj_id) {
                _this.load(obj_id);
            }
            push_state();
        })
            .button()
            .appendTo(button_div);
        this.next_button = $("<input/>")
            .attr('type', 'submit')
            .attr('value', '>>')
            .click(function () {
            var oll = _this.options.object_list_loader;
            var meta = oll.get_meta(_this.get_obj_id());
            var obj_id = meta.next;
            if (obj_id) {
                _this.load(obj_id);
            }
            push_state();
        })
            .button()
            .appendTo(button_div);
        this.setup_buttons();
        this.od = this.obj_type.detail_infobox();
        $("<div/>")
            .set_widget(this.od)
            .appendTo(this.div);
        this.ol = this.obj_type.list_widget(this.options.id + ".child", null, this.options.disabled);
        $("<div/>")
            .set_widget(this.ol)
            .appendTo(this.div);
        if (this.options.object_loader != null) {
            this.set(this.options.object_loader);
        }
        this.setup_perms(window._perms);
        window._perms_changed.add_listener(this, function (perms) {
            _this.setup_perms(perms);
            _this.load(_this.get_obj_id());
        });
        window._reload_all.add_listener(this, function () {
            _this.load(_this.get_obj_id());
        });
        if (this.options.object_loader != null) {
            this.set(this.options.object_loader);
        }
    };
    ObjectDetailViewport.prototype.setup_perms = function (perms) {
        var can_create = false;
        var can_change = false;
        var can_delete = false;
        var type = this.obj_type.get_type();
        if (perms[type] != null) {
            var perms_for_type = perms[type];
            can_create = perms_for_type.can_create;
            can_change = perms_for_type.can_change;
            can_delete = perms_for_type.can_delete;
        }
        this.create_item.toggle(can_create);
        this.change_item.toggle(can_change);
        this.delete_item.toggle(can_delete);
    };
    ObjectDetailViewport.prototype.setup_buttons = function () {
        if (this.options.object_list_loader) {
            var oll = this.options.object_list_loader;
            var meta = null;
            var obj_id = this.get_obj_id();
            if (obj_id) {
                meta = oll.get_meta(obj_id);
            }
            this.prev_button.show();
            this.next_button.show();
            if (meta != null && meta.prev) {
                this.prev_button.button("enable");
            }
            else {
                this.prev_button.button("disable");
            }
            if (meta && meta.next) {
                this.next_button.button("enable");
            }
            else {
                this.next_button.button("disable");
            }
        }
        else {
            this.prev_button.hide();
            this.next_button.hide();
        }
    };
    ObjectDetailViewport.prototype.set = function (loader) {
        var _this = this;
        var old_loader = this.options.object_loader;
        if (old_loader != null) {
            old_loader.loaded_item.remove_listener(this);
            old_loader.on_error.remove_listener(this);
        }
        this.loaded(null);
        this.options.object_loader = loader;
        if (loader != null) {
            loader.loaded_item.add_listener(this, function (obj) {
                _this.loaded(obj);
            });
            loader.on_error.add_listener(this, function (message) {
                _this.loaded_error(message);
            });
        }
    };
    ObjectDetailViewport.prototype.set_list_loader = function (object_list_loader) {
        var _this = this;
        if (this.options.object_list_loader != null) {
            this.options.object_list_loader.loaded_list.remove_listener(this);
        }
        if (object_list_loader != null) {
            object_list_loader.loaded_list.add_listener(this, function (notification) {
                _this.setup_buttons();
            });
        }
    };
    ObjectDetailViewport.prototype.load = function (obj_id) {
        this.set(this.obj_type.load(obj_id));
    };
    ObjectDetailViewport.prototype.reload = function () {
        this.load(this.get_obj_id());
    };
    ObjectDetailViewport.prototype.loaded = function (obj) {
        var type = this.obj_type.get_type();
        if (this.element == null) {
            return;
        }
        if (obj == null) {
            this.set_title(type + ": loading");
            this.od.set(null);
        }
        else {
            this.set_title(type + ": " + obj.title);
            this.od.set(obj);
        }
        this.ol.filter(this.get_children_criteria());
        this.element.removeClass("error");
        this.setup_buttons();
    };
    ObjectDetailViewport.prototype.loaded_error = function (message) {
        console.log(message);
        this.element.addClass("error");
    };
    ObjectDetailViewport.prototype._enable = function () {
        _super.prototype._enable.call(this);
        if (this.ol) {
            this.ol.enable();
        }
    };
    ObjectDetailViewport.prototype._disable = function () {
        _super.prototype._disable.call(this);
        if (this.ol) {
            this.ol.disable();
        }
    };
    ObjectDetailViewport.prototype.get_url = function () {
        var state = this.get_streamable_state();
        delete state['obj_id'];
        var params = $.param(state);
        var type = this.obj_type.get_type();
        if (params != "") {
            return root_url() + type + "/" + this.get_obj_id() + "/?" + params;
        }
        else {
            return root_url() + type + "/" + this.get_obj_id() + "/";
        }
    };
    ObjectDetailViewport.prototype.get_streamable_state = function () {
        var streamable = _super.prototype.get_streamable_state.call(this);
        streamable['obj_id'] = this.get_obj_id();
        return streamable;
    };
    ObjectDetailViewport.prototype.set_streamable_state = function (streamable) {
        // load streamable state, must be called before show() is called.
        _super.prototype.set_streamable_state.call(this, streamable);
        if (streamable['obj_id'] != null) {
            var obj_id = get_streamable_number(streamable, 'obj_id');
            this.load(obj_id);
        }
    };
    return ObjectDetailViewport;
}(Viewport));

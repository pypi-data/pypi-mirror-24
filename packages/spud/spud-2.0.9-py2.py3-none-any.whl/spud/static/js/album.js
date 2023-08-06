/// <reference path="signals.ts" />
/// <reference path="globals.ts" />
/// <reference path="base.ts" />
/// <reference path="dialog.ts" />
/// <reference path="infobox.ts" />
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
window._album_created = new Signal();
window._album_changed = new Signal();
window._album_deleted = new Signal();
window._album_created.add_listener(null, function () {
    window._reload_all.trigger(null);
});
var Album = (function (_super) {
    __extends(Album, _super);
    function Album(streamable) {
        return _super.call(this, Album.type, streamable) || this;
    }
    Album.prototype.set_streamable = function (streamable) {
        _super.prototype.set_streamable.call(this, streamable);
        this.description = get_streamable_string(streamable, 'description');
        this.sort_order = get_streamable_string(streamable, 'sort_order');
        this.sort_name = get_streamable_string(streamable, 'sort_name');
        var utc_offset = get_streamable_number(streamable, 'revised_utc_offset');
        this.revised = get_streamable_datetimezone(streamable, 'revised', utc_offset);
        var ascendants = get_streamable_array(streamable, 'ascendants');
        this.ascendants = [];
        for (var i = 0; i < ascendants.length; i++) {
            var item = streamable_to_object(ascendants[i]);
            this.ascendants.push(new Album(item));
        }
        if (ascendants.length > 0) {
            var item = streamable_to_object(ascendants[0]);
            this.parent = new Album(item);
        }
        else {
            this.parent = null;
        }
    };
    Album.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        streamable['description'] = this.description;
        streamable['sort_order'] = this.sort_order;
        streamable['sort_name'] = this.sort_name;
        streamable['revised_utc_offset'] = streamable_datetimezone_offset(this.revised);
        streamable['revised'] = streamable_datetimezone_datetime(this.revised);
        if (this.parent != null) {
            streamable['parent'] = this.parent.id;
        }
        else {
            streamable['parent'] = null;
        }
        return streamable;
    };
    return Album;
}(SpudObject));
Album.type = 'albums';
var AlbumCriteria = (function (_super) {
    __extends(AlbumCriteria, _super);
    function AlbumCriteria() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlbumCriteria.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        var criteria = this;
        set_streamable_value(streamable, 'mode', criteria.mode);
        set_streamable_value(streamable, 'root_only', criteria.root_only);
        if (criteria.instance != null) {
            set_streamable_value(streamable, 'instance', criteria.instance.id);
        }
        set_streamable_value(streamable, 'q', criteria.q);
        set_streamable_value(streamable, 'needs_revision', criteria.needs_revision);
        return streamable;
    };
    AlbumCriteria.prototype.get_title = function () {
        var criteria = this;
        var title = null;
        var mode = criteria.mode || 'children';
        if (criteria.instance != null) {
            title = criteria.instance.title + " / " + mode;
        }
        else if (criteria.q != null) {
            title = "search " + criteria.q;
        }
        else if (criteria.root_only) {
            title = "root only";
        }
        else if (criteria.needs_revision) {
            title = "needs revision";
        }
        else {
            title = "All";
        }
        return title;
    };
    AlbumCriteria.prototype.get_items = function () {
        var criteria = this;
        var result = [];
        result.push(new CriteriaItemObject("instance", "Album", criteria.instance, new AlbumType()));
        result.push(new CriteriaItemSelect("mode", "Mode", criteria.mode, [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]]));
        result.push(new CriteriaItemBoolean("root_only", "Root Only", criteria.root_only));
        result.push(new CriteriaItemString("q", "Search for", criteria.q));
        result.push(new CriteriaItemBoolean("needs_revision", "Needs revision", criteria.needs_revision));
        return result;
    };
    return AlbumCriteria;
}(Criteria));
var AlbumType = (function (_super) {
    __extends(AlbumType, _super);
    function AlbumType() {
        return _super.call(this, Album.type, "album") || this;
    }
    AlbumType.prototype.object_from_streamable = function (streamable) {
        var obj = new Album();
        obj.set_streamable(streamable);
        return obj;
    };
    AlbumType.prototype.criteria_from_streamable = function (streamable, on_load) {
        var criteria = new AlbumCriteria();
        criteria.mode = get_streamable_string(streamable, 'mode');
        criteria.root_only = get_streamable_boolean(streamable, 'root_only');
        criteria.q = get_streamable_string(streamable, 'q');
        criteria.needs_revision = get_streamable_boolean(streamable, 'needs_revision');
        var id = get_streamable_number(streamable, 'instance');
        if (id != null) {
            var obj_type = new AlbumType();
            var loader = obj_type.load(id);
            loader.loaded_item.add_listener(this, function (object) {
                criteria.instance = object;
                on_load(criteria);
            });
            loader.on_error.add_listener(this, function (message) {
                console.log(message);
                criteria.instance = new Album();
                on_load(criteria);
            });
        }
        else {
            criteria.instance = null;
            on_load(criteria);
        }
    };
    // DIALOGS
    AlbumType.prototype.create_dialog = function (parent) {
        var obj = new Album();
        obj.parent = parent;
        var params = {
            obj: obj
        };
        var dialog = new AlbumChangeDialog(params);
        return dialog;
    };
    AlbumType.prototype.change_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new AlbumChangeDialog(params);
        return dialog;
    };
    AlbumType.prototype.delete_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new AlbumDeleteDialog(params);
        return dialog;
    };
    AlbumType.prototype.search_dialog = function (criteria, on_success) {
        var params = {
            obj: criteria,
            on_success: on_success
        };
        var dialog = new AlbumSearchDialog(params);
        return dialog;
    };
    // WIDGETS
    AlbumType.prototype.criteria_widget = function (criteria) {
        var params = {
            obj: criteria
        };
        var widget = new AlbumCriteriaWidget(params);
        return widget;
    };
    AlbumType.prototype.list_widget = function (child_id, criteria, disabled) {
        var params = {
            child_id: child_id,
            criteria: criteria,
            disabled: disabled
        };
        var widget = new AlbumListWidget(params);
        return widget;
    };
    AlbumType.prototype.detail_infobox = function () {
        var params = {};
        var widget = new AlbumDetailInfobox(params);
        return widget;
    };
    // VIEWPORTS
    AlbumType.prototype.detail_viewport = function (object_loader, state) {
        var params = {
            object_loader: object_loader,
            object_list_loader: null
        };
        var viewport = new AlbumDetailViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    AlbumType.prototype.list_viewport = function (criteria, state) {
        var params = {
            criteria: criteria
        };
        var viewport = new AlbumListViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    return AlbumType;
}(ObjectType));
///////////////////////////////////////
// album dialogs
///////////////////////////////////////
var AlbumSearchDialogOptions = (function (_super) {
    __extends(AlbumSearchDialogOptions, _super);
    function AlbumSearchDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumSearchDialogOptions;
}(ObjectSearchDialogOptions));
var AlbumSearchDialog = (function (_super) {
    __extends(AlbumSearchDialog, _super);
    function AlbumSearchDialog(options) {
        return _super.call(this, options) || this;
    }
    AlbumSearchDialog.prototype.new_criteria = function () {
        return new AlbumCriteria();
    };
    AlbumSearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Album", new AlbumType(), false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
            ["needs_revision", new booleanInputField("Needs revision", false)],
        ];
        this.options.title = "Search albums";
        this.options.description = "Please search for an album.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return AlbumSearchDialog;
}(ObjectSearchDialog));
var AlbumChangeDialogOptions = (function (_super) {
    __extends(AlbumChangeDialogOptions, _super);
    function AlbumChangeDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumChangeDialogOptions;
}(ObjectChangeDialogOptions));
var AlbumChangeDialog = (function (_super) {
    __extends(AlbumChangeDialog, _super);
    function AlbumChangeDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "albums";
        _this.type_name = "album";
        return _this;
    }
    AlbumChangeDialog.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextInputField("Title", true)],
            ["description", new PInputField("Description", false)],
            ["cover_photo", new PhotoSelectField("Photo", false)],
            ["sort_name", new TextInputField("Sort Name", false)],
            ["sort_order", new TextInputField("Sort Order", false)],
            ["parent", new AjaxSelectField("Parent", new AlbumType(), false)],
            ["revised", new DateTimeInputField("Revised", false)],
        ];
        this.options.title = "Change album";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    AlbumChangeDialog.prototype.save_success = function (data) {
        var album = new Album();
        album.set_streamable(data);
        if (this.obj.id != null) {
            window._album_changed.trigger(album);
        }
        else {
            window._album_created.trigger(album);
        }
        _super.prototype.save_success.call(this, data);
    };
    return AlbumChangeDialog;
}(ObjectChangeDialog));
var AlbumDeleteDialogOptions = (function (_super) {
    __extends(AlbumDeleteDialogOptions, _super);
    function AlbumDeleteDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumDeleteDialogOptions;
}(ObjectDeleteDialogOptions));
var AlbumDeleteDialog = (function (_super) {
    __extends(AlbumDeleteDialog, _super);
    function AlbumDeleteDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "albums";
        _this.type_name = "album";
        return _this;
    }
    AlbumDeleteDialog.prototype.save_success = function (data) {
        window._album_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return AlbumDeleteDialog;
}(ObjectDeleteDialog));
///////////////////////////////////////
// album widgets
///////////////////////////////////////
var AlbumCriteriaWidgetOptions = (function (_super) {
    __extends(AlbumCriteriaWidgetOptions, _super);
    function AlbumCriteriaWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumCriteriaWidgetOptions;
}(ObjectCriteriaWidgetOptions));
var AlbumCriteriaWidget = (function (_super) {
    __extends(AlbumCriteriaWidget, _super);
    function AlbumCriteriaWidget(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "albums";
        return _this;
    }
    return AlbumCriteriaWidget;
}(ObjectCriteriaWidget));
var AlbumListWidgetOptions = (function (_super) {
    __extends(AlbumListWidgetOptions, _super);
    function AlbumListWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumListWidgetOptions;
}(ObjectListWidgetOptions));
var AlbumListWidget = (function (_super) {
    __extends(AlbumListWidget, _super);
    function AlbumListWidget(options) {
        return _super.call(this, options, new AlbumType()) || this;
    }
    AlbumListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._album_changed.add_listener(this, function (album) {
            var li = _this.create_li_for_obj(album);
            _this.get_item(album.id).replaceWith(li);
        });
        window._album_deleted.add_listener(this, function (album_id) {
            _this.get_item(album_id).remove();
            _this.load_if_required();
        });
    };
    AlbumListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            object_loader: null,
            object_list_loader: null
        };
        var viewport;
        viewport = new AlbumDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    AlbumListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        if (obj.sort_order || obj.sort_name) {
            details.push($("<div/>").text(obj.sort_name + " " + obj.sort_order));
        }
        return details;
    };
    AlbumListWidget.prototype.get_description = function (obj) {
        return obj.description;
    };
    return AlbumListWidget;
}(ObjectListWidget));
var AlbumDetailInfoboxOptions = (function (_super) {
    __extends(AlbumDetailInfoboxOptions, _super);
    function AlbumDetailInfoboxOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumDetailInfoboxOptions;
}(InfoboxOptions));
var AlbumDetailInfobox = (function (_super) {
    __extends(AlbumDetailInfobox, _super);
    function AlbumDetailInfobox(options) {
        return _super.call(this, options) || this;
    }
    AlbumDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextOutputField("Title")],
            ["sort_name", new TextOutputField("Sort Name")],
            ["sort_order", new TextOutputField("Sort Order")],
            ["revised", new DateTimeOutputField("Revised")],
            ["description", new POutputField("Description")],
            ["ascendants", new LinkListOutputField("Ascendants", new AlbumType())],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    AlbumDetailInfobox.prototype.set = function (album) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, album);
        this.options.obj = album;
        if (album != null) {
            this.img.set(album.cover_photo);
        }
        else {
            this.img.set(null);
        }
    };
    return AlbumDetailInfobox;
}(Infobox));
///////////////////////////////////////
// album viewports
///////////////////////////////////////
var AlbumListViewportOptions = (function (_super) {
    __extends(AlbumListViewportOptions, _super);
    function AlbumListViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumListViewportOptions;
}(ObjectListViewportOptions));
var AlbumListViewport = (function (_super) {
    __extends(AlbumListViewport, _super);
    function AlbumListViewport(options) {
        return _super.call(this, options, new AlbumType()) || this;
    }
    AlbumListViewport.prototype.get_streamable_state = function () {
        var streamable = _super.prototype.get_streamable_state.call(this);
        return streamable;
    };
    AlbumListViewport.prototype.set_streamable_state = function (streamable) {
        // load streamable state, must be called before show() is called.
        _super.prototype.set_streamable_state.call(this, streamable);
    };
    return AlbumListViewport;
}(ObjectListViewport));
var AlbumDetailViewportOptions = (function (_super) {
    __extends(AlbumDetailViewportOptions, _super);
    function AlbumDetailViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return AlbumDetailViewportOptions;
}(ObjectDetailViewportOptions));
var AlbumDetailViewport = (function (_super) {
    __extends(AlbumDetailViewport, _super);
    function AlbumDetailViewport(options) {
        return _super.call(this, options, new AlbumType()) || this;
    }
    AlbumDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._album_changed.add_listener(this, function (obj) {
            var this_obj_id = _this.get_obj_id();
            if (obj.id === this_obj_id) {
                _this.set(_this.obj_type.load(obj.id));
            }
        });
        window._album_deleted.add_listener(this, function (obj_id) {
            var this_obj_id = _this.get_obj_id();
            if (obj_id === this_obj_id) {
                _this.remove();
            }
        });
    };
    AlbumDetailViewport.prototype.get_photo_criteria = function () {
        var criteria = new PhotoCriteria();
        criteria.album = this.get_obj_id();
        criteria.album_descendants = true;
        return criteria;
    };
    AlbumDetailViewport.prototype.get_children_criteria = function () {
        var criteria = new AlbumCriteria();
        criteria.instance = this.get_obj();
        criteria.mode = 'children';
        return criteria;
    };
    return AlbumDetailViewport;
}(ObjectDetailViewport));

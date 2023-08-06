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
window._place_created = new Signal();
window._place_changed = new Signal();
window._place_deleted = new Signal();
window._place_created.add_listener(null, function () {
    window._reload_all.trigger(null);
});
var Place = (function (_super) {
    __extends(Place, _super);
    function Place(streamable) {
        return _super.call(this, Place.type, streamable) || this;
    }
    Place.prototype.set_streamable = function (streamable) {
        _super.prototype.set_streamable.call(this, streamable);
        this.address = get_streamable_string(streamable, 'address');
        this.address2 = get_streamable_string(streamable, 'address2');
        this.city = get_streamable_string(streamable, 'city');
        this.state = get_streamable_string(streamable, 'state');
        this.country = get_streamable_string(streamable, 'country');
        this.postcode = get_streamable_string(streamable, 'postcode');
        this.url = get_streamable_string(streamable, 'url');
        this.urldesc = get_streamable_string(streamable, 'urldesc');
        this.notes = get_streamable_string(streamable, 'notes');
        var ascendants = get_streamable_array(streamable, 'ascendants');
        this.ascendants = [];
        for (var i = 0; i < ascendants.length; i++) {
            var item = streamable_to_object(ascendants[i]);
            this.ascendants.push(new Place(item));
        }
        if (ascendants.length > 0) {
            var item = streamable_to_object(ascendants[0]);
            this.parent = new Place(item);
        }
        else {
            this.parent = null;
        }
    };
    Place.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        streamable['address'] = this.address;
        streamable['address2'] = this.address2;
        streamable['city'] = this.city;
        streamable['state'] = this.state;
        streamable['country'] = this.country;
        streamable['postcode'] = this.postcode;
        streamable['url'] = this.url;
        streamable['urldesc'] = this.urldesc;
        streamable['notes'] = this.notes;
        if (this.parent != null) {
            streamable['parent'] = this.parent.id;
        }
        else {
            streamable['parent'] = null;
        }
        return streamable;
    };
    return Place;
}(SpudObject));
Place.type = 'place';
var PlaceCriteria = (function (_super) {
    __extends(PlaceCriteria, _super);
    function PlaceCriteria() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PlaceCriteria.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        var criteria = this;
        set_streamable_value(streamable, 'mode', criteria.mode);
        set_streamable_value(streamable, 'root_only', criteria.root_only);
        if (criteria.instance != null) {
            set_streamable_value(streamable, 'instance', criteria.instance.id);
        }
        set_streamable_value(streamable, 'q', criteria.q);
        return streamable;
    };
    PlaceCriteria.prototype.get_title = function () {
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
        else {
            title = "All";
        }
        return title;
    };
    PlaceCriteria.prototype.get_items = function () {
        var criteria = this;
        var result = [];
        result.push(new CriteriaItemObject("instance", "Place", criteria.instance, new PlaceType()));
        result.push(new CriteriaItemSelect("mode", "Mode", criteria.mode, [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]]));
        result.push(new CriteriaItemBoolean("root_only", "Root Only", criteria.root_only));
        result.push(new CriteriaItemString("q", "Search for", criteria.q));
        return result;
    };
    return PlaceCriteria;
}(Criteria));
var PlaceType = (function (_super) {
    __extends(PlaceType, _super);
    function PlaceType() {
        return _super.call(this, Place.type, "place") || this;
    }
    PlaceType.prototype.object_from_streamable = function (streamable) {
        var obj = new Place();
        obj.set_streamable(streamable);
        return obj;
    };
    PlaceType.prototype.criteria_from_streamable = function (streamable, on_load) {
        var criteria = new PlaceCriteria();
        criteria.mode = get_streamable_string(streamable, 'mode');
        criteria.root_only = get_streamable_boolean(streamable, 'root_only');
        criteria.q = get_streamable_string(streamable, 'q');
        var id = get_streamable_number(streamable, 'instance');
        if (id != null) {
            var obj_type = new PlaceType();
            var loader = obj_type.load(id);
            loader.loaded_item.add_listener(this, function (object) {
                criteria.instance = object;
                on_load(criteria);
            });
            loader.on_error.add_listener(this, function (message) {
                console.log(message);
                criteria.instance = new Place();
                on_load(criteria);
            });
        }
        else {
            criteria.instance = null;
            on_load(criteria);
        }
    };
    // DIALOGS
    PlaceType.prototype.create_dialog = function (parent) {
        var obj = new Place();
        obj.parent = parent;
        var params = {
            obj: obj
        };
        var dialog = new PlaceChangeDialog(params);
        return dialog;
    };
    PlaceType.prototype.change_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new PlaceChangeDialog(params);
        return dialog;
    };
    PlaceType.prototype.delete_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new PlaceDeleteDialog(params);
        return dialog;
    };
    PlaceType.prototype.search_dialog = function (criteria, on_success) {
        var params = {
            obj: criteria,
            on_success: on_success
        };
        var dialog = new PlaceSearchDialog(params);
        return dialog;
    };
    // WIDGETS
    PlaceType.prototype.criteria_widget = function (criteria) {
        var params = {
            obj: criteria
        };
        var widget = new PlaceCriteriaWidget(params);
        return widget;
    };
    PlaceType.prototype.list_widget = function (child_id, criteria, disabled) {
        var params = {
            child_id: child_id,
            criteria: criteria,
            disabled: disabled
        };
        var widget = new PlaceListWidget(params);
        return widget;
    };
    PlaceType.prototype.detail_infobox = function () {
        var params = {};
        var widget = new PlaceDetailInfobox(params);
        return widget;
    };
    // VIEWPORTS
    PlaceType.prototype.detail_viewport = function (object_loader, state) {
        var params = {
            object_loader: object_loader,
            object_list_loader: null
        };
        var viewport = new PlaceDetailViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    PlaceType.prototype.list_viewport = function (criteria, state) {
        var params = {
            criteria: criteria
        };
        var viewport = new PlaceListViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    return PlaceType;
}(ObjectType));
///////////////////////////////////////
// place dialogs
///////////////////////////////////////
var PlaceSearchDialogOptions = (function (_super) {
    __extends(PlaceSearchDialogOptions, _super);
    function PlaceSearchDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceSearchDialogOptions;
}(ObjectSearchDialogOptions));
var PlaceSearchDialog = (function (_super) {
    __extends(PlaceSearchDialog, _super);
    function PlaceSearchDialog(options) {
        return _super.call(this, options) || this;
    }
    PlaceSearchDialog.prototype.new_criteria = function () {
        return new PlaceCriteria();
    };
    PlaceSearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Place", new PlaceType(), false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
        ];
        this.options.title = "Search places";
        this.options.description = "Please search for an place.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return PlaceSearchDialog;
}(ObjectSearchDialog));
var PlaceChangeDialogOptions = (function (_super) {
    __extends(PlaceChangeDialogOptions, _super);
    function PlaceChangeDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceChangeDialogOptions;
}(ObjectChangeDialogOptions));
var PlaceChangeDialog = (function (_super) {
    __extends(PlaceChangeDialog, _super);
    function PlaceChangeDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "places";
        _this.type_name = "place";
        return _this;
    }
    PlaceChangeDialog.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextInputField("Title", true)],
            ["cover_photo", new PhotoSelectField("Photo", false)],
            ["address", new TextInputField("Address", false)],
            ["address2", new TextInputField("Address(ctd)", false)],
            ["city", new TextInputField("City", false)],
            ["state", new TextInputField("State", false)],
            ["country", new TextInputField("Country", false)],
            ["postcode", new TextInputField("Postcode", false)],
            ["url", new TextInputField("URL", false)],
            ["urldesc", new TextInputField("URL desc", false)],
            ["notes", new PInputField("Notes", false)],
            ["parent", new AjaxSelectField("Parent", new PlaceType(), false)],
        ];
        this.options.title = "Change place";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PlaceChangeDialog.prototype.save_success = function (data) {
        var place = new Place();
        place.set_streamable(data);
        if (this.obj.id != null) {
            window._place_changed.trigger(place);
        }
        else {
            window._place_created.trigger(place);
        }
        _super.prototype.save_success.call(this, data);
    };
    return PlaceChangeDialog;
}(ObjectChangeDialog));
var PlaceDeleteDialogOptions = (function (_super) {
    __extends(PlaceDeleteDialogOptions, _super);
    function PlaceDeleteDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceDeleteDialogOptions;
}(ObjectDeleteDialogOptions));
var PlaceDeleteDialog = (function (_super) {
    __extends(PlaceDeleteDialog, _super);
    function PlaceDeleteDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "places";
        _this.type_name = "place";
        return _this;
    }
    PlaceDeleteDialog.prototype.save_success = function (data) {
        window._place_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return PlaceDeleteDialog;
}(ObjectDeleteDialog));
///////////////////////////////////////
// place widgets
///////////////////////////////////////
var PlaceCriteriaWidgetOptions = (function (_super) {
    __extends(PlaceCriteriaWidgetOptions, _super);
    function PlaceCriteriaWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceCriteriaWidgetOptions;
}(ObjectCriteriaWidgetOptions));
var PlaceCriteriaWidget = (function (_super) {
    __extends(PlaceCriteriaWidget, _super);
    function PlaceCriteriaWidget(options) {
        return _super.call(this, options) || this;
    }
    return PlaceCriteriaWidget;
}(ObjectCriteriaWidget));
var PlaceListWidgetOptions = (function (_super) {
    __extends(PlaceListWidgetOptions, _super);
    function PlaceListWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceListWidgetOptions;
}(ObjectListWidgetOptions));
var PlaceListWidget = (function (_super) {
    __extends(PlaceListWidget, _super);
    function PlaceListWidget(options) {
        return _super.call(this, options, new PlaceType()) || this;
    }
    PlaceListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._place_changed.add_listener(this, function (place) {
            var li = _this.create_li_for_obj(place);
            _this.get_item(place.id).replaceWith(li);
        });
        window._place_deleted.add_listener(this, function (place_id) {
            _this.get_item(place_id).remove();
            _this.load_if_required();
        });
    };
    PlaceListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            object_loader: null,
            object_list_loader: null
        };
        var viewport;
        viewport = new PlaceDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    PlaceListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        return details;
    };
    PlaceListWidget.prototype.get_description = function (obj) {
        return obj.city;
    };
    return PlaceListWidget;
}(ObjectListWidget));
var PlaceDetailInfoboxOptions = (function (_super) {
    __extends(PlaceDetailInfoboxOptions, _super);
    function PlaceDetailInfoboxOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceDetailInfoboxOptions;
}(InfoboxOptions));
var PlaceDetailInfobox = (function (_super) {
    __extends(PlaceDetailInfobox, _super);
    function PlaceDetailInfobox(options) {
        return _super.call(this, options) || this;
    }
    PlaceDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["address", new TextOutputField("Address")],
            ["address2", new TextOutputField("Address(ctd)")],
            ["city", new TextOutputField("City")],
            ["state", new TextOutputField("State")],
            ["postcode", new TextOutputField("Postcode")],
            ["country", new TextOutputField("Country")],
            // FIXME
            // ["url", new HtmlOutputField("URL")],
            ["home_of", new LinkListOutputField("Home of", new PlaceType())],
            ["work_of", new LinkListOutputField("Work of", new PlaceType())],
            ["notes", new POutputField("notes")],
            ["ascendants", new LinkListOutputField("Ascendants", new PlaceType())],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    PlaceDetailInfobox.prototype.set = function (place) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, place);
        this.options.obj = place;
        if (place != null) {
            this.img.set(place.cover_photo);
        }
        else {
            this.img.set(null);
        }
    };
    return PlaceDetailInfobox;
}(Infobox));
///////////////////////////////////////
// place viewports
///////////////////////////////////////
var PlaceListViewportOptions = (function (_super) {
    __extends(PlaceListViewportOptions, _super);
    function PlaceListViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceListViewportOptions;
}(ObjectListViewportOptions));
var PlaceListViewport = (function (_super) {
    __extends(PlaceListViewport, _super);
    function PlaceListViewport(options) {
        return _super.call(this, options, new PlaceType()) || this;
    }
    PlaceListViewport.prototype.get_streamable_state = function () {
        var streamable = _super.prototype.get_streamable_state.call(this);
        return streamable;
    };
    PlaceListViewport.prototype.set_streamable_state = function (streamable) {
        // load streamable state, must be called before show() is called.
        _super.prototype.set_streamable_state.call(this, streamable);
    };
    return PlaceListViewport;
}(ObjectListViewport));
var PlaceDetailViewportOptions = (function (_super) {
    __extends(PlaceDetailViewportOptions, _super);
    function PlaceDetailViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PlaceDetailViewportOptions;
}(ObjectDetailViewportOptions));
var PlaceDetailViewport = (function (_super) {
    __extends(PlaceDetailViewport, _super);
    function PlaceDetailViewport(options) {
        return _super.call(this, options, new PlaceType()) || this;
    }
    PlaceDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._place_changed.add_listener(this, function (obj) {
            var this_obj_id = _this.get_obj_id();
            if (obj.id === this_obj_id) {
                _this.set(_this.obj_type.load(obj.id));
            }
        });
        window._place_deleted.add_listener(this, function (obj_id) {
            var this_obj_id = _this.get_obj_id();
            if (obj_id === this_obj_id) {
                _this.remove();
            }
        });
    };
    PlaceDetailViewport.prototype.get_photo_criteria = function () {
        var criteria = new PhotoCriteria();
        criteria.place = this.get_obj_id();
        criteria.place_descendants = true;
        return criteria;
    };
    PlaceDetailViewport.prototype.get_children_criteria = function () {
        var criteria = new PlaceCriteria();
        criteria.instance = this.get_obj();
        criteria.mode = 'children';
        return criteria;
    };
    return PlaceDetailViewport;
}(ObjectDetailViewport));

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
window._category_created = new Signal();
window._category_changed = new Signal();
window._category_deleted = new Signal();
window._category_created.add_listener(null, function () {
    window._reload_all.trigger(null);
});
var Category = (function (_super) {
    __extends(Category, _super);
    function Category(streamable) {
        return _super.call(this, Category.type, streamable) || this;
    }
    Category.prototype.set_streamable = function (streamable) {
        _super.prototype.set_streamable.call(this, streamable);
        this.description = get_streamable_string(streamable, 'description');
        this.sort_order = get_streamable_string(streamable, 'sort_order');
        this.sort_name = get_streamable_string(streamable, 'sort_name');
        var ascendants = get_streamable_array(streamable, 'ascendants');
        this.ascendants = [];
        for (var i = 0; i < ascendants.length; i++) {
            var item = streamable_to_object(ascendants[i]);
            this.ascendants.push(new Category(item));
        }
        if (ascendants.length > 0) {
            var item = streamable_to_object(ascendants[0]);
            this.parent = new Category(item);
        }
        else {
            this.parent = null;
        }
    };
    Category.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        streamable['description'] = this.description;
        streamable['sort_order'] = this.sort_order;
        streamable['sort_name'] = this.sort_name;
        if (this.parent != null) {
            streamable['parent'] = this.parent.id;
        }
        else {
            streamable['parent'] = null;
        }
        return streamable;
    };
    return Category;
}(SpudObject));
Category.type = 'categorys';
var CategoryCriteria = (function (_super) {
    __extends(CategoryCriteria, _super);
    function CategoryCriteria() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CategoryCriteria.prototype.get_streamable = function () {
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
    CategoryCriteria.prototype.get_title = function () {
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
    CategoryCriteria.prototype.get_items = function () {
        var criteria = this;
        var result = [];
        result.push(new CriteriaItemObject("instance", "Category", criteria.instance, new CategoryType()));
        result.push(new CriteriaItemSelect("mode", "Mode", criteria.mode, [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]]));
        result.push(new CriteriaItemBoolean("root_only", "Root Only", criteria.root_only));
        result.push(new CriteriaItemString("q", "Search for", criteria.q));
        return result;
    };
    return CategoryCriteria;
}(Criteria));
var CategoryType = (function (_super) {
    __extends(CategoryType, _super);
    function CategoryType() {
        return _super.call(this, Category.type, "category") || this;
    }
    CategoryType.prototype.object_from_streamable = function (streamable) {
        var obj = new Category();
        obj.set_streamable(streamable);
        return obj;
    };
    CategoryType.prototype.criteria_from_streamable = function (streamable, on_load) {
        var criteria = new CategoryCriteria();
        criteria.mode = get_streamable_string(streamable, 'mode');
        criteria.root_only = get_streamable_boolean(streamable, 'root_only');
        criteria.q = get_streamable_string(streamable, 'q');
        var id = get_streamable_number(streamable, 'instance');
        if (id != null) {
            var obj_type = new CategoryType();
            var loader = obj_type.load(id);
            loader.loaded_item.add_listener(this, function (object) {
                criteria.instance = object;
                on_load(criteria);
            });
            loader.on_error.add_listener(this, function (message) {
                console.log(message);
                criteria.instance = new Category();
                on_load(criteria);
            });
        }
        else {
            criteria.instance = null;
            on_load(criteria);
        }
    };
    // DIALOGS
    CategoryType.prototype.create_dialog = function (parent) {
        var obj = new Category();
        obj.parent = parent;
        var params = {
            obj: obj
        };
        var dialog = new CategoryChangeDialog(params);
        return dialog;
    };
    CategoryType.prototype.change_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new CategoryChangeDialog(params);
        return dialog;
    };
    CategoryType.prototype.delete_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new CategoryDeleteDialog(params);
        return dialog;
    };
    CategoryType.prototype.search_dialog = function (criteria, on_success) {
        var params = {
            obj: criteria,
            on_success: on_success
        };
        var dialog = new CategorySearchDialog(params);
        return dialog;
    };
    // WIDGETS
    CategoryType.prototype.criteria_widget = function (criteria) {
        var params = {
            obj: criteria
        };
        var widget = new CategoryCriteriaWidget(params);
        return widget;
    };
    CategoryType.prototype.list_widget = function (child_id, criteria, disabled) {
        var params = {
            child_id: child_id,
            criteria: criteria,
            disabled: disabled
        };
        var widget = new CategoryListWidget(params);
        return widget;
    };
    CategoryType.prototype.detail_infobox = function () {
        var params = {};
        var widget = new CategoryDetailInfobox(params);
        return widget;
    };
    // VIEWPORTS
    CategoryType.prototype.detail_viewport = function (object_loader, state) {
        var params = {
            object_loader: object_loader,
            object_list_loader: null
        };
        var viewport = new CategoryDetailViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    CategoryType.prototype.list_viewport = function (criteria, state) {
        var params = {
            criteria: criteria
        };
        var viewport = new CategoryListViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    return CategoryType;
}(ObjectType));
///////////////////////////////////////
// category dialogs
///////////////////////////////////////
var CategorySearchDialogOptions = (function (_super) {
    __extends(CategorySearchDialogOptions, _super);
    function CategorySearchDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategorySearchDialogOptions;
}(ObjectSearchDialogOptions));
var CategorySearchDialog = (function (_super) {
    __extends(CategorySearchDialog, _super);
    function CategorySearchDialog(options) {
        return _super.call(this, options) || this;
    }
    CategorySearchDialog.prototype.new_criteria = function () {
        return new CategoryCriteria();
    };
    CategorySearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Category", new CategoryType(), false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
        ];
        this.options.title = "Search categories";
        this.options.description = "Please search for an category.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return CategorySearchDialog;
}(ObjectSearchDialog));
var CategoryChangeDialogOptions = (function (_super) {
    __extends(CategoryChangeDialogOptions, _super);
    function CategoryChangeDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategoryChangeDialogOptions;
}(ObjectChangeDialogOptions));
var CategoryChangeDialog = (function (_super) {
    __extends(CategoryChangeDialog, _super);
    function CategoryChangeDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "categorys";
        _this.type_name = "category";
        return _this;
    }
    CategoryChangeDialog.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextInputField("Title", true)],
            ["description", new PInputField("Description", false)],
            ["cover_photo", new PhotoSelectField("Photo", false)],
            ["sort_name", new TextInputField("Sort Name", false)],
            ["sort_order", new TextInputField("Sort Order", false)],
            ["parent", new AjaxSelectField("Parent", new CategoryType(), false)],
        ];
        this.options.title = "Change category";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    CategoryChangeDialog.prototype.save_success = function (data) {
        var category = new Category();
        category.set_streamable(data);
        if (this.obj.id != null) {
            window._category_changed.trigger(category);
        }
        else {
            window._category_created.trigger(category);
        }
        _super.prototype.save_success.call(this, data);
    };
    return CategoryChangeDialog;
}(ObjectChangeDialog));
var CategoryDeleteDialogOptions = (function (_super) {
    __extends(CategoryDeleteDialogOptions, _super);
    function CategoryDeleteDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategoryDeleteDialogOptions;
}(ObjectDeleteDialogOptions));
var CategoryDeleteDialog = (function (_super) {
    __extends(CategoryDeleteDialog, _super);
    function CategoryDeleteDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "categorys";
        _this.type_name = "category";
        return _this;
    }
    CategoryDeleteDialog.prototype.save_success = function (data) {
        window._category_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return CategoryDeleteDialog;
}(ObjectDeleteDialog));
///////////////////////////////////////
// category widgets
///////////////////////////////////////
var CategoryCriteriaWidgetOptions = (function (_super) {
    __extends(CategoryCriteriaWidgetOptions, _super);
    function CategoryCriteriaWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategoryCriteriaWidgetOptions;
}(ObjectCriteriaWidgetOptions));
var CategoryCriteriaWidget = (function (_super) {
    __extends(CategoryCriteriaWidget, _super);
    function CategoryCriteriaWidget(options) {
        return _super.call(this, options) || this;
    }
    return CategoryCriteriaWidget;
}(ObjectCriteriaWidget));
var CategoryListWidgetOptions = (function (_super) {
    __extends(CategoryListWidgetOptions, _super);
    function CategoryListWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategoryListWidgetOptions;
}(ObjectListWidgetOptions));
var CategoryListWidget = (function (_super) {
    __extends(CategoryListWidget, _super);
    function CategoryListWidget(options) {
        return _super.call(this, options, new CategoryType()) || this;
    }
    CategoryListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._category_changed.add_listener(this, function (category) {
            var li = _this.create_li_for_obj(category);
            _this.get_item(category.id).replaceWith(li);
        });
        window._category_deleted.add_listener(this, function (category_id) {
            _this.get_item(category_id).remove();
            _this.load_if_required();
        });
    };
    CategoryListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            object_loader: null,
            object_list_loader: null
        };
        var viewport;
        viewport = new CategoryDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    CategoryListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        if (obj.sort_order || obj.sort_name) {
            details.push($("<div/>").text(obj.sort_name + " " + obj.sort_order));
        }
        return details;
    };
    CategoryListWidget.prototype.get_description = function (obj) {
        return obj.description;
    };
    return CategoryListWidget;
}(ObjectListWidget));
var CategoryDetailInfoboxOptions = (function (_super) {
    __extends(CategoryDetailInfoboxOptions, _super);
    function CategoryDetailInfoboxOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategoryDetailInfoboxOptions;
}(InfoboxOptions));
var CategoryDetailInfobox = (function (_super) {
    __extends(CategoryDetailInfobox, _super);
    function CategoryDetailInfobox(options) {
        return _super.call(this, options) || this;
    }
    CategoryDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["title", new TextOutputField("Title")],
            ["sort_name", new TextOutputField("Sort Name")],
            ["sort_order", new TextOutputField("Sort Order")],
            ["description", new POutputField("Description")],
            ["ascendants", new LinkListOutputField("Ascendants", new CategoryType())],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    CategoryDetailInfobox.prototype.set = function (category) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, category);
        this.options.obj = category;
        if (category != null) {
            this.img.set(category.cover_photo);
        }
        else {
            this.img.set(null);
        }
    };
    return CategoryDetailInfobox;
}(Infobox));
///////////////////////////////////////
// category viewports
///////////////////////////////////////
var CategoryListViewportOptions = (function (_super) {
    __extends(CategoryListViewportOptions, _super);
    function CategoryListViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategoryListViewportOptions;
}(ObjectListViewportOptions));
var CategoryListViewport = (function (_super) {
    __extends(CategoryListViewport, _super);
    function CategoryListViewport(options) {
        return _super.call(this, options, new CategoryType()) || this;
    }
    CategoryListViewport.prototype.get_streamable_state = function () {
        var streamable = _super.prototype.get_streamable_state.call(this);
        return streamable;
    };
    CategoryListViewport.prototype.set_streamable_state = function (streamable) {
        // load streamable state, must be called before show() is called.
        _super.prototype.set_streamable_state.call(this, streamable);
    };
    return CategoryListViewport;
}(ObjectListViewport));
var CategoryDetailViewportOptions = (function (_super) {
    __extends(CategoryDetailViewportOptions, _super);
    function CategoryDetailViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return CategoryDetailViewportOptions;
}(ObjectDetailViewportOptions));
var CategoryDetailViewport = (function (_super) {
    __extends(CategoryDetailViewport, _super);
    function CategoryDetailViewport(options) {
        return _super.call(this, options, new CategoryType()) || this;
    }
    CategoryDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._category_changed.add_listener(this, function (obj) {
            var this_obj_id = _this.get_obj_id();
            if (obj.id === this_obj_id) {
                _this.set(_this.obj_type.load(obj.id));
            }
        });
        window._category_deleted.add_listener(this, function (obj_id) {
            var this_obj_id = _this.get_obj_id();
            if (obj_id === this_obj_id) {
                _this.remove();
            }
        });
    };
    CategoryDetailViewport.prototype.get_photo_criteria = function () {
        var criteria = new PhotoCriteria();
        criteria.category = this.get_obj_id();
        criteria.category_descendants = true;
        return criteria;
    };
    CategoryDetailViewport.prototype.get_children_criteria = function () {
        var criteria = new CategoryCriteria();
        criteria.instance = this.get_obj();
        criteria.mode = 'children';
        return criteria;
    };
    return CategoryDetailViewport;
}(ObjectDetailViewport));

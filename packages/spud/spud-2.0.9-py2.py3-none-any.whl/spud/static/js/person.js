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
window._person_created = new Signal();
window._person_changed = new Signal();
window._person_deleted = new Signal();
window._person_created.add_listener(null, function () {
    window._reload_all.trigger(null);
});
var Person = (function (_super) {
    __extends(Person, _super);
    function Person(streamable) {
        return _super.call(this, Person.type, streamable) || this;
    }
    Person.prototype.set_streamable = function (streamable) {
        _super.prototype.set_streamable.call(this, streamable);
        this.first_name = get_streamable_string(streamable, 'first_name');
        this.middle_name = get_streamable_string(streamable, 'middle_name');
        this.last_name = get_streamable_string(streamable, 'last_name');
        this.called = get_streamable_string(streamable, 'called');
        this.sex = get_streamable_string(streamable, 'sex');
        this.email = get_streamable_string(streamable, 'email');
        this.dob = get_streamable_string(streamable, 'dob');
        this.dod = get_streamable_string(streamable, 'dod');
        this.notes = get_streamable_string(streamable, 'notes');
        var streamable_work = get_streamable_object(streamable, 'work');
        if (streamable_work != null) {
            this.work = new Place(streamable_work);
        }
        else {
            this.work = null;
        }
        var streamable_home = get_streamable_object(streamable, 'home');
        if (streamable_home != null) {
            this.home = new Place(streamable_home);
        }
        else {
            this.home = null;
        }
        var streamable_mother = get_streamable_object(streamable, 'mother');
        if (streamable_mother != null) {
            this.mother = new Person(streamable_mother);
        }
        else {
            this.mother = null;
        }
        var streamable_father = get_streamable_object(streamable, 'father');
        if (streamable_father != null) {
            this.father = new Person(streamable_father);
        }
        else {
            this.father = null;
        }
        var streamable_spouse = get_streamable_object(streamable, 'spouse');
        if (streamable_spouse != null) {
            this.spouse = new Person(streamable_spouse);
        }
        else {
            this.spouse = null;
        }
        var streamable_grandparents = get_streamable_array(streamable, 'grandparents');
        this.grandparents = [];
        for (var i = 0; i < streamable_grandparents.length; i++) {
            var item = streamable_to_object(streamable_grandparents[i]);
            this.grandparents.push(new Person(item));
        }
        var streamable_uncles_aunts = get_streamable_array(streamable, 'uncles_aunts');
        this.uncles_aunts = [];
        for (var i = 0; i < streamable_uncles_aunts.length; i++) {
            var item = streamable_to_object(streamable_uncles_aunts[i]);
            this.uncles_aunts.push(new Person(item));
        }
        var streamable_parents = get_streamable_array(streamable, 'parents');
        this.parents = [];
        for (var i = 0; i < streamable_parents.length; i++) {
            var item = streamable_to_object(streamable_parents[i]);
            this.parents.push(new Person(item));
        }
        var streamable_siblings = get_streamable_array(streamable, 'siblings');
        this.siblings = [];
        for (var i = 0; i < streamable_siblings.length; i++) {
            var item = streamable_to_object(streamable_siblings[i]);
            this.siblings.push(new Person(item));
        }
        var streamable_cousins = get_streamable_array(streamable, 'cousins');
        this.cousins = [];
        for (var i = 0; i < streamable_cousins.length; i++) {
            var item = streamable_to_object(streamable_cousins[i]);
            this.cousins.push(new Person(item));
        }
        var streamable_children = get_streamable_array(streamable, 'children');
        this.children = [];
        for (var i = 0; i < streamable_children.length; i++) {
            var item = streamable_to_object(streamable_children[i]);
            this.children.push(new Person(item));
        }
        var streamable_nephews_nieces = get_streamable_array(streamable, 'nephews_nieces');
        this.nephews_nieces = [];
        for (var i = 0; i < streamable_nephews_nieces.length; i++) {
            var item = streamable_to_object(streamable_nephews_nieces[i]);
            this.nephews_nieces.push(new Person(item));
        }
        var streamable_grandchildren = get_streamable_array(streamable, 'grandchildren');
        this.grandchildren = [];
        for (var i = 0; i < streamable_grandchildren.length; i++) {
            var item = streamable_to_object(streamable_grandchildren[i]);
            this.grandchildren.push(new Person(item));
        }
    };
    Person.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        streamable['first_name'] = this.first_name;
        streamable['middle_name'] = this.middle_name;
        streamable['last_name'] = this.last_name;
        streamable['called'] = this.called;
        streamable['sex'] = this.sex;
        streamable['email'] = this.email;
        streamable['dob'] = this.dob;
        streamable['dod'] = this.dod;
        streamable['notes'] = this.notes;
        if (this.work != null) {
            streamable['work_pk'] = this.work.id;
        }
        else {
            streamable['work_pk'] = null;
        }
        if (this.home != null) {
            streamable['home_pk'] = this.home.id;
        }
        else {
            streamable['home_pk'] = null;
        }
        if (this.mother != null) {
            streamable['mother_pk'] = this.mother.id;
        }
        else {
            streamable['mother_pk'] = null;
        }
        if (this.father != null) {
            streamable['father_pk'] = this.father.id;
        }
        else {
            streamable['father_pk'] = null;
        }
        if (this.spouse != null) {
            streamable['spouse_pk'] = this.spouse.id;
        }
        else {
            streamable['spouse_pk'] = null;
        }
        return streamable;
    };
    return Person;
}(SpudObject));
Person.type = 'persons';
var PersonCriteria = (function (_super) {
    __extends(PersonCriteria, _super);
    function PersonCriteria() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PersonCriteria.prototype.get_streamable = function () {
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
    PersonCriteria.prototype.get_title = function () {
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
    PersonCriteria.prototype.get_items = function () {
        var criteria = this;
        var result = [];
        result.push(new CriteriaItemObject("instance", "Person", criteria.instance, new PersonType()));
        result.push(new CriteriaItemSelect("mode", "Mode", criteria.mode, [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]]));
        result.push(new CriteriaItemBoolean("root_only", "Root Only", criteria.root_only));
        result.push(new CriteriaItemString("q", "Search for", criteria.q));
        return result;
    };
    return PersonCriteria;
}(Criteria));
var PersonType = (function (_super) {
    __extends(PersonType, _super);
    function PersonType() {
        return _super.call(this, Person.type, "person") || this;
    }
    PersonType.prototype.object_from_streamable = function (streamable) {
        var obj = new Person();
        obj.set_streamable(streamable);
        return obj;
    };
    PersonType.prototype.criteria_from_streamable = function (streamable, on_load) {
        var criteria = new PersonCriteria();
        criteria.mode = get_streamable_string(streamable, 'mode');
        criteria.root_only = get_streamable_boolean(streamable, 'root_only');
        criteria.q = get_streamable_string(streamable, 'q');
        var id = get_streamable_number(streamable, 'instance');
        if (id != null) {
            var obj_type = new PersonType();
            var loader = obj_type.load(id);
            loader.loaded_item.add_listener(this, function (object) {
                criteria.instance = object;
                on_load(criteria);
            });
            loader.on_error.add_listener(this, function (message) {
                console.log(message);
                criteria.instance = new Person();
                on_load(criteria);
            });
        }
        else {
            criteria.instance = null;
            on_load(criteria);
        }
    };
    // DIALOGS
    PersonType.prototype.create_dialog = function (parent) {
        var obj = new Person();
        if (parent != null) {
            if (parent.sex === "1") {
                obj.father = parent;
            }
            else if (parent.sex === "2") {
                obj.mother = parent;
            }
        }
        var params = {
            obj: obj
        };
        var dialog = new PersonChangeDialog(params);
        return dialog;
    };
    PersonType.prototype.change_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new PersonChangeDialog(params);
        return dialog;
    };
    PersonType.prototype.delete_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new PersonDeleteDialog(params);
        return dialog;
    };
    PersonType.prototype.search_dialog = function (criteria, on_success) {
        var params = {
            obj: criteria,
            on_success: on_success
        };
        var dialog = new PersonSearchDialog(params);
        return dialog;
    };
    // WIDGETS
    PersonType.prototype.criteria_widget = function (criteria) {
        var params = {
            obj: criteria
        };
        var widget = new PersonCriteriaWidget(params);
        return widget;
    };
    PersonType.prototype.list_widget = function (child_id, criteria, disabled) {
        var params = {
            child_id: child_id,
            criteria: criteria,
            disabled: disabled
        };
        var widget = new PersonListWidget(params);
        return widget;
    };
    PersonType.prototype.detail_infobox = function () {
        var params = {};
        var widget = new PersonDetailInfobox(params);
        return widget;
    };
    // VIEWPORTS
    PersonType.prototype.detail_viewport = function (object_loader, state) {
        var params = {
            object_loader: object_loader,
            object_list_loader: null
        };
        var viewport = new PersonDetailViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    PersonType.prototype.list_viewport = function (criteria, state) {
        var params = {
            criteria: criteria
        };
        var viewport = new PersonListViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    return PersonType;
}(ObjectType));
///////////////////////////////////////
// person dialogs
///////////////////////////////////////
var PersonSearchDialogOptions = (function (_super) {
    __extends(PersonSearchDialogOptions, _super);
    function PersonSearchDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonSearchDialogOptions;
}(ObjectSearchDialogOptions));
var PersonSearchDialog = (function (_super) {
    __extends(PersonSearchDialog, _super);
    function PersonSearchDialog(options) {
        return _super.call(this, options) || this;
    }
    PersonSearchDialog.prototype.new_criteria = function () {
        return new PersonCriteria();
    };
    PersonSearchDialog.prototype.show = function (element) {
        this.options.fields = [
            ["q", new TextInputField("Search for", false)],
            ["instance", new AjaxSelectField("Person", new PersonType(), false)],
            ["mode", new SelectInputField("Mode", [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]], false)],
            ["root_only", new booleanInputField("Root only", false)],
        ];
        this.options.title = "Search persons";
        this.options.description = "Please search for an person.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return PersonSearchDialog;
}(ObjectSearchDialog));
var PersonChangeDialogOptions = (function (_super) {
    __extends(PersonChangeDialogOptions, _super);
    function PersonChangeDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonChangeDialogOptions;
}(ObjectChangeDialogOptions));
var PersonChangeDialog = (function (_super) {
    __extends(PersonChangeDialog, _super);
    function PersonChangeDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "persons";
        _this.type_name = "person";
        return _this;
    }
    PersonChangeDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["cover_photo", new PhotoSelectField("Photo", false)],
                    ["first_name", new TextInputField("First name", true)],
                    ["middle_name", new TextInputField("Middle name", false)],
                    ["last_name", new TextInputField("Last name", false)],
                    ["called", new TextInputField("Called", false)],
                    ["sex", new SelectInputField("Sex", [["1", "Male"], ["2", "Female"]], true)],
                ] },
            { name: 'connections', title: 'Connections', fields: [
                    ["work", new AjaxSelectField("Work", new PlaceType(), false)],
                    ["home", new AjaxSelectField("Home", new PlaceType(), false)],
                    ["mother", new AjaxSelectField("Mother", new PersonType(), false)],
                    ["father", new AjaxSelectField("Father", new PersonType(), false)],
                    ["spouse", new AjaxSelectField("Spouse", new PersonType(), false)],
                ] },
            { name: 'other', title: 'Other', fields: [
                    ["email", new TextInputField("E-Mail", false)],
                    ["dob", new DateInputField("Date of birth", false)],
                    ["dod", new DateInputField("Date of death", false)],
                    ["notes", new PInputField("Notes", false)],
                ] },
        ];
        this.options.title = "Change person";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PersonChangeDialog.prototype.save_success = function (data) {
        var person = new Person();
        person.set_streamable(data);
        if (this.obj.id != null) {
            window._person_changed.trigger(person);
        }
        else {
            window._person_created.trigger(person);
        }
        _super.prototype.save_success.call(this, data);
    };
    return PersonChangeDialog;
}(ObjectChangeDialog));
var PersonDeleteDialogOptions = (function (_super) {
    __extends(PersonDeleteDialogOptions, _super);
    function PersonDeleteDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonDeleteDialogOptions;
}(ObjectDeleteDialogOptions));
var PersonDeleteDialog = (function (_super) {
    __extends(PersonDeleteDialog, _super);
    function PersonDeleteDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "persons";
        _this.type_name = "person";
        return _this;
    }
    PersonDeleteDialog.prototype.save_success = function (data) {
        window._person_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return PersonDeleteDialog;
}(ObjectDeleteDialog));
///////////////////////////////////////
// person widgets
///////////////////////////////////////
var PersonCriteriaWidgetOptions = (function (_super) {
    __extends(PersonCriteriaWidgetOptions, _super);
    function PersonCriteriaWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonCriteriaWidgetOptions;
}(ObjectCriteriaWidgetOptions));
var PersonCriteriaWidget = (function (_super) {
    __extends(PersonCriteriaWidget, _super);
    function PersonCriteriaWidget(options) {
        return _super.call(this, options) || this;
    }
    return PersonCriteriaWidget;
}(ObjectCriteriaWidget));
var PersonListWidgetOptions = (function (_super) {
    __extends(PersonListWidgetOptions, _super);
    function PersonListWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonListWidgetOptions;
}(ObjectListWidgetOptions));
var PersonListWidget = (function (_super) {
    __extends(PersonListWidget, _super);
    function PersonListWidget(options) {
        return _super.call(this, options, new PersonType()) || this;
    }
    PersonListWidget.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._person_changed.add_listener(this, function (person) {
            var li = _this.create_li_for_obj(person);
            _this.get_item(person.id).replaceWith(li);
        });
        window._person_deleted.add_listener(this, function (person_id) {
            _this.get_item(person_id).remove();
            _this.load_if_required();
        });
    };
    PersonListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            object_loader: null,
            object_list_loader: null
        };
        var viewport;
        viewport = new PersonDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    PersonListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        return details;
    };
    PersonListWidget.prototype.get_description = function (obj) {
        return _super.prototype.get_description.call(this, obj);
    };
    return PersonListWidget;
}(ObjectListWidget));
var PersonDetailInfoboxOptions = (function (_super) {
    __extends(PersonDetailInfoboxOptions, _super);
    function PersonDetailInfoboxOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonDetailInfoboxOptions;
}(InfoboxOptions));
var PersonDetailInfobox = (function (_super) {
    __extends(PersonDetailInfobox, _super);
    function PersonDetailInfobox(options) {
        return _super.call(this, options) || this;
    }
    PersonDetailInfobox.prototype.show = function (element) {
        this.options.fields = [
            ["middle_name", new TextOutputField("Middle name")],
            ["last_name", new TextOutputField("Last name")],
            ["called", new TextOutputField("Called")],
            ["sex", new SelectOutputField("Sex", [["1", "Male"], ["2", "Female"]])],
            ["email", new TextOutputField("E-Mail")],
            ["dob", new TextOutputField("Date of birth")],
            ["dod", new TextOutputField("Date of death")],
            ["work", new LinkOutputField("Work", new PlaceType())],
            ["home", new LinkOutputField("Home", new PlaceType())],
            ["spouses", new LinkListOutputField("Spouses", new PersonType())],
            ["notes", new POutputField("Notes")],
            ["grandparents", new LinkListOutputField("Grand Parents", new PersonType())],
            ["uncles_aunts", new LinkListOutputField("Uncles and Aunts", new PersonType())],
            ["parents", new LinkListOutputField("Parents", new PersonType())],
            ["siblings", new LinkListOutputField("Siblings", new PersonType())],
            ["cousins", new LinkListOutputField("Cousins", new PersonType())],
            ["children", new LinkListOutputField("Children", new PersonType())],
            ["nephews_nieces", new LinkListOutputField("Nephews and Nieces", new PersonType())],
            ["grandchildren", new LinkListOutputField("Grand children", new PersonType())],
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: true });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    PersonDetailInfobox.prototype.set = function (person) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, person);
        this.options.obj = person;
        if (person != null) {
            this.img.set(person.cover_photo);
        }
        else {
            this.img.set(null);
        }
    };
    return PersonDetailInfobox;
}(Infobox));
///////////////////////////////////////
// person viewports
///////////////////////////////////////
var PersonListViewportOptions = (function (_super) {
    __extends(PersonListViewportOptions, _super);
    function PersonListViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonListViewportOptions;
}(ObjectListViewportOptions));
var PersonListViewport = (function (_super) {
    __extends(PersonListViewport, _super);
    function PersonListViewport(options) {
        return _super.call(this, options, new PersonType()) || this;
    }
    PersonListViewport.prototype.get_streamable_state = function () {
        var streamable = _super.prototype.get_streamable_state.call(this);
        return streamable;
    };
    PersonListViewport.prototype.set_streamable_state = function (streamable) {
        // load streamable state, must be called before show() is called.
        _super.prototype.set_streamable_state.call(this, streamable);
    };
    return PersonListViewport;
}(ObjectListViewport));
var PersonDetailViewportOptions = (function (_super) {
    __extends(PersonDetailViewportOptions, _super);
    function PersonDetailViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PersonDetailViewportOptions;
}(ObjectDetailViewportOptions));
var PersonDetailViewport = (function (_super) {
    __extends(PersonDetailViewport, _super);
    function PersonDetailViewport(options) {
        return _super.call(this, options, new PersonType()) || this;
    }
    PersonDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._person_changed.add_listener(this, function (obj) {
            var this_obj_id = _this.get_obj_id();
            if (obj.id === this_obj_id) {
                _this.set(_this.obj_type.load(obj.id));
            }
        });
        window._person_deleted.add_listener(this, function (obj_id) {
            var this_obj_id = _this.get_obj_id();
            if (obj_id === this_obj_id) {
                _this.remove();
            }
        });
    };
    PersonDetailViewport.prototype.get_photo_criteria = function () {
        var criteria = new PhotoCriteria();
        criteria.person = this.get_obj_id();
        return criteria;
    };
    PersonDetailViewport.prototype.get_children_criteria = function () {
        var criteria = new PersonCriteria();
        criteria.instance = this.get_obj();
        criteria.mode = 'children';
        return criteria;
    };
    return PersonDetailViewport;
}(ObjectDetailViewport));

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
window._photo_created = new Signal();
window._photo_changed = new Signal();
window._photo_deleted = new Signal();
window._photo_created.add_listener(null, function () {
    window._reload_all.trigger(null);
});
var PhotoThumb = (function () {
    function PhotoThumb() {
    }
    return PhotoThumb;
}());
var PhotoVideo = (function () {
    function PhotoVideo() {
    }
    return PhotoVideo;
}());
var PriorityPhotoVideo = (function () {
    function PriorityPhotoVideo() {
    }
    return PriorityPhotoVideo;
}());
var Photo = (function (_super) {
    __extends(Photo, _super);
    function Photo(streamable) {
        return _super.call(this, Photo.type, streamable) || this;
    }
    Photo.prototype.set_streamable = function (streamable) {
        _super.prototype.set_streamable.call(this, streamable);
        this.action = get_streamable_string(streamable, 'action');
        var utc_offset = get_streamable_number(streamable, 'datetime_utc_offset');
        this.datetime = get_streamable_datetimezone(streamable, 'datetime', utc_offset);
        this.description = get_streamable_string(streamable, 'description');
        this.camera_make = get_streamable_string(streamable, 'camera_make');
        this.camera_model = get_streamable_string(streamable, 'camera_model');
        this.flash_used = get_streamable_string(streamable, 'flash_used');
        this.focal_length = get_streamable_string(streamable, 'focal_length');
        this.exposure = get_streamable_string(streamable, 'exposure');
        this.aperture = get_streamable_string(streamable, 'aperture');
        this.iso_equiv = get_streamable_string(streamable, 'iso_equiv');
        this.metering_mode = get_streamable_string(streamable, 'metering_mode');
        this.orig_url = get_streamable_string(streamable, 'orig_url');
        var streamable_albums = get_streamable_array(streamable, 'albums');
        this.albums = [];
        for (var i = 0; i < streamable_albums.length; i++) {
            var item = streamable_to_object(streamable_albums[i]);
            this.albums.push(new Album(item));
        }
        var streamable_categorys = get_streamable_array(streamable, 'categorys');
        this.categorys = [];
        for (var i = 0; i < streamable_categorys.length; i++) {
            var item = streamable_to_object(streamable_categorys[i]);
            this.categorys.push(new Category(item));
        }
        var streamable_persons = get_streamable_array(streamable, 'persons');
        this.persons = [];
        for (var i = 0; i < streamable_persons.length; i++) {
            var item = streamable_to_object(streamable_persons[i]);
            this.persons.push(new Person(item));
        }
        var streamable_photographer = get_streamable_object(streamable, 'photographer');
        if (streamable_photographer != null) {
            this.photographer = new Person(streamable_photographer);
        }
        var streamable_place = get_streamable_object(streamable, 'place');
        if (streamable_place != null) {
            this.place = new Place(streamable_place);
        }
        var streamable_thumbs = get_streamable_string_array(streamable, 'thumbs');
        this.thumbs = {};
        for (var size in streamable_thumbs) {
            var item = streamable_to_object(streamable_thumbs[size]);
            var thumb = new PhotoThumb();
            thumb.width = get_streamable_number(item, 'width');
            thumb.height = get_streamable_number(item, 'height');
            thumb.url = get_streamable_string(item, 'url');
            this.thumbs[size] = thumb;
        }
        var streamable_videos = get_streamable_string_array(streamable, 'videos');
        this.videos = {};
        for (var size in streamable_videos) {
            var item = streamable_to_object(streamable_videos[size]);
            this.videos[size] = [];
            var streamable_array = streamable_to_array(item);
            for (var i = 0; i < streamable_array.length; i++) {
                var array_item = streamable_to_array(streamable_array[i]);
                if (array_item.length != 2) {
                    continue;
                }
                var priority = streamable_to_number(array_item[0]);
                var svideo = streamable_to_object(array_item[1]);
                var video = new PhotoVideo();
                video.width = get_streamable_number(svideo, 'width');
                video.height = get_streamable_number(svideo, 'height');
                video.url = get_streamable_string(svideo, 'url');
                video.format = get_streamable_string(svideo, 'format');
                this.videos[size].push([priority, video]);
            }
        }
    };
    Photo.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        streamable['action'] = this.action;
        streamable['datetime_utc_offset'] = streamable_datetimezone_offset(this.datetime);
        streamable['datetime'] = streamable_datetimezone_datetime(this.datetime);
        streamable['description'] = this.description;
        streamable['camera_make'] = this.camera_make;
        streamable['camera_model'] = this.camera_model;
        streamable['flash_used'] = this.flash_used;
        streamable['focal_length'] = this.focal_length;
        streamable['exposure'] = this.exposure;
        streamable['aperture'] = this.aperture;
        streamable['iso_equiv'] = this.iso_equiv;
        streamable['metering_mode'] = this.metering_mode;
        var streamable_albums = [];
        for (var i = 0; i < this.albums.length; i++) {
            streamable_albums.push(this.albums[i].id);
        }
        streamable['albums_pk'] = streamable_albums;
        var streamable_categorys = [];
        for (var i = 0; i < this.categorys.length; i++) {
            streamable_categorys.push(this.categorys[i].id);
        }
        streamable['categorys_pk'] = streamable_categorys;
        var streamable_persons = [];
        for (var i = 0; i < this.persons.length; i++) {
            streamable_persons.push(this.persons[i].id);
        }
        streamable['persons_pk'] = streamable_persons;
        streamable['photographer_pk'] = null;
        if (this.photographer != null) {
            streamable['photographer_pk'] = this.photographer.id;
        }
        streamable['place_pk'] = null;
        if (this.place != null) {
            streamable['place_pk'] = this.place.id;
        }
        return streamable;
    };
    return Photo;
}(SpudObject));
Photo.type = 'photos';
var PhotoCriteria = (function (_super) {
    __extends(PhotoCriteria, _super);
    function PhotoCriteria() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PhotoCriteria.prototype.get_streamable = function () {
        var streamable = _super.prototype.get_streamable.call(this);
        var criteria = this;
        set_streamable_array_as_string(streamable, 'photos', criteria.photos);
        set_streamable_datetimezone_datetime(streamable, 'first_datetime', criteria.first_datetime);
        //set_streamable_datetimezone_offset(streamable, 'first_datetime_utc_offset', criteria.first_datetime)
        set_streamable_datetimezone_datetime(streamable, 'last_datetime', criteria.last_datetime);
        //set_streamable_datetimezone_offset(streamable, 'last_datetime_utc_offset', criteria.last_datetime)
        set_streamable_value(streamable, 'action', criteria.action);
        set_streamable_value(streamable, 'mode', criteria.mode);
        if (criteria.instance != null) {
            set_streamable_value(streamable, 'instance', criteria.instance.id);
        }
        set_streamable_value(streamable, 'q', criteria.q);
        set_streamable_value(streamable, 'album', criteria.album);
        set_streamable_value(streamable, 'category', criteria.category);
        set_streamable_value(streamable, 'place', criteria.place);
        set_streamable_value(streamable, 'person', criteria.person);
        set_streamable_value(streamable, 'album_descendants', criteria.album_descendants);
        set_streamable_value(streamable, 'category_descendants', criteria.category_descendants);
        set_streamable_value(streamable, 'place_descendants', criteria.place_descendants);
        set_streamable_value(streamable, 'person_descendants', criteria.person_descendants);
        return streamable;
    };
    PhotoCriteria.prototype.get_title = function () {
        var criteria = this;
        var title = null;
        var mode = criteria.mode || 'children';
        if (criteria.instance != null) {
            title = criteria.instance.title + " / " + mode;
        }
        else if (criteria.q != null) {
            title = "search " + criteria.q;
        }
        else if (criteria.album != null) {
            title = "album " + criteria.album;
        }
        else if (criteria.category != null) {
            title = "category " + criteria.category;
        }
        else if (criteria.place != null) {
            title = "place " + criteria.place;
        }
        else if (criteria.person != null) {
            title = "person " + criteria.person;
        }
        else {
            title = "All";
        }
        return title;
    };
    PhotoCriteria.prototype.get_items = function () {
        var criteria = this;
        var result = [];
        var mode = criteria.mode || 'children';
        result.push(new CriteriaItemObject("instance", "Photo", criteria.instance, new PhotoType()));
        result.push(new CriteriaItemSelect("mode", "Mode", criteria.mode, [["children", "Children"], ["descendants", "Descendants"], ["ascendants", "Ascendants"]]));
        //result.push("photos = " + criteria.photos)
        result.push(new CriteriaItemDateTimeZone("first_datetime", "First Date Time", criteria.first_datetime));
        result.push(new CriteriaItemDateTimeZone("last_datetime", "Last Date Time", criteria.last_datetime));
        result.push(new CriteriaItemSelect("action", "Action", criteria.action, [
            ["", "no action"],
            ["D", "delete"],
            ["R", "regenerate thumbnails & video"],
            ["M", "move photo"],
            ["auto", "rotate automatic"],
            ["90", "rotate 90 degrees clockwise"],
            ["180", "rotate 180 degrees clockwise"],
            ["270", "rotate 270 degrees clockwise"],
        ]));
        result.push(new CriteriaItemString("q", "Search for", criteria.q));
        result.push(new CriteriaItemNumber("album", "Album", criteria.album));
        result.push(new CriteriaItemNumber("category", "Category", criteria.category));
        result.push(new CriteriaItemNumber("place", "Place", criteria.place));
        result.push(new CriteriaItemNumber("person", "Person", criteria.person));
        result.push(new CriteriaItemBoolean("album_descendants", "Album Descendants", criteria.album_descendants));
        result.push(new CriteriaItemBoolean("category_descendants", "Category Descendants", criteria.category_descendants));
        result.push(new CriteriaItemBoolean("place_descendants", "Place Descendants", criteria.place_descendants));
        result.push(new CriteriaItemBoolean("person_descendants", "Person Descendants", criteria.person_descendants));
        return result;
    };
    return PhotoCriteria;
}(Criteria));
var PhotoType = (function (_super) {
    __extends(PhotoType, _super);
    function PhotoType() {
        return _super.call(this, Photo.type, "photo") || this;
    }
    PhotoType.prototype.object_from_streamable = function (streamable) {
        var obj = new Photo();
        obj.set_streamable(streamable);
        return obj;
    };
    PhotoType.prototype.criteria_from_streamable = function (streamable, on_load) {
        var criteria = new PhotoCriteria();
        criteria.photos = get_streamable_number_array(streamable, 'photos');
        var first_datetime_offset = get_streamable_number(streamable, 'first_datetime_utc_offset');
        criteria.first_datetime = get_streamable_datetimezone(streamable, 'first_datetime', first_datetime_offset);
        var last_datetime_offset = get_streamable_number(streamable, 'last_datetime_utc_offset');
        criteria.last_datetime = get_streamable_datetimezone(streamable, 'last_datetime', last_datetime_offset);
        criteria.action = get_streamable_string(streamable, 'action');
        criteria.q = get_streamable_string(streamable, 'q');
        criteria.album = get_streamable_number(streamable, 'album');
        criteria.category = get_streamable_number(streamable, 'category');
        criteria.place = get_streamable_number(streamable, 'place');
        criteria.person = get_streamable_number(streamable, 'person');
        criteria.album_descendants = get_streamable_boolean(streamable, 'album_descendants');
        criteria.category_descendants = get_streamable_boolean(streamable, 'category_descendants');
        criteria.place_descendants = get_streamable_boolean(streamable, 'place_descendants');
        criteria.person_descendants = get_streamable_boolean(streamable, 'person_descendants');
        var id = get_streamable_number(streamable, 'instance');
        if (id != null) {
            var obj_type = new PhotoType();
            var loader = obj_type.load(id);
            loader.loaded_item.add_listener(this, function (object) {
                criteria.instance = object;
                on_load(criteria);
            });
            loader.on_error.add_listener(this, function (message) {
                console.log(message);
                criteria.instance = new Photo();
                on_load(criteria);
            });
        }
        else {
            criteria.instance = null;
            on_load(criteria);
        }
    };
    // DIALOGS
    PhotoType.prototype.create_dialog = function (parent) {
        var obj = new Photo();
        var params = {
            obj: obj
        };
        var dialog = new PhotoChangeDialog(params);
        return dialog;
    };
    PhotoType.prototype.change_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new PhotoChangeDialog(params);
        return dialog;
    };
    PhotoType.prototype.delete_dialog = function (obj) {
        var params = {
            obj: obj
        };
        var dialog = new PhotoDeleteDialog(params);
        return dialog;
    };
    PhotoType.prototype.search_dialog = function (criteria, on_success) {
        var params = {
            obj: criteria,
            on_success: on_success
        };
        var dialog = new PhotoSearchDialog(params);
        return dialog;
    };
    // WIDGETS
    PhotoType.prototype.criteria_widget = function (criteria) {
        var params = {
            obj: criteria
        };
        var widget = new PhotoCriteriaWidget(params);
        return widget;
    };
    PhotoType.prototype.list_widget = function (child_id, criteria, disabled) {
        var params = {
            child_id: child_id,
            criteria: criteria,
            disabled: disabled
        };
        var widget = new PhotoListWidget(params);
        return widget;
    };
    PhotoType.prototype.detail_infobox = function () {
        var params = {};
        var widget = new PhotoDetailInfobox(params);
        return widget;
    };
    // VIEWPORTS
    PhotoType.prototype.detail_viewport = function (object_loader, state) {
        var params = {
            object_loader: object_loader,
            object_list_loader: null
        };
        var viewport = new PhotoDetailViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    PhotoType.prototype.list_viewport = function (criteria, state) {
        var params = {
            criteria: criteria
        };
        var viewport = new PhotoListViewport(params);
        if (state != null) {
            viewport.set_streamable_state(state);
        }
        return viewport;
    };
    return PhotoType;
}(ObjectType));
///////////////////////////////////////
// photo dialogs
///////////////////////////////////////
var PhotoSearchDialogOptions = (function (_super) {
    __extends(PhotoSearchDialogOptions, _super);
    function PhotoSearchDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoSearchDialogOptions;
}(ObjectSearchDialogOptions));
var PhotoSearchDialog = (function (_super) {
    __extends(PhotoSearchDialog, _super);
    function PhotoSearchDialog(options) {
        return _super.call(this, options) || this;
    }
    PhotoSearchDialog.prototype.new_criteria = function () {
        return new PhotoCriteria();
    };
    PhotoSearchDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["q", new TextInputField("Search for", false)],
                    ["first_datetime", new DateTimeInputField("First date", false)],
                    ["last_datetime", new DateTimeInputField("Last date", false)],
                    ["lower_rating", new IntegerInputField("Upper rating", false)],
                    ["upper_rating", new IntegerInputField("Lower rating", false)],
                    ["title", new TextInputField("Title", false)],
                    ["photographer", new AjaxSelectField("Photographer", new PersonType(), false)],
                    ["path", new TextInputField("Path", false)],
                    ["name", new TextInputField("Name", false)],
                    ["first_id", new IntegerInputField("First id", false)],
                    ["last_id", new IntegerInputField("Last id", false)],
                ] },
            { name: 'connections', title: 'Connections', fields: [
                    // ["album", new AjaxSelectField("Album", new AlbumType(), false)],
                    ["album", new IntegerInputField("Album ID", false)],
                    ["album_descendants", new booleanInputField("Descend albums", false)],
                    ["album_none", new booleanInputField("No albums", false)],
                    // ["category", new AjaxSelectField("Category", new CategoryType(), false)],
                    ["category", new IntegerInputField("Category ID", false)],
                    ["category_descendants", new booleanInputField("Descend categories", false)],
                    ["category_none", new booleanInputField("No categories", false)],
                    // ["place", new AjaxSelectField("Place", new PlaceType(), false)],
                    ["place", new IntegerInputField("Place ID", false)],
                    ["place_descendants", new booleanInputField("Descend places", false)],
                    ["place_none", new booleanInputField("No places", false)],
                    // ["person", new AjaxSelectField("Person", new PersonType(), false)],
                    ["person", new IntegerInputField("Person ID", false)],
                    ["person_none", new booleanInputField("No people", false)],
                    ["person_descendants", new booleanInputField("Descend people", false)],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextInputField("Camera Make", false)],
                    ["camera_model", new TextInputField("Camera Model", false)],
                ] },
        ];
        this.options.title = "Search photos";
        this.options.description = "Please search for an photo.";
        this.options.button = "Search";
        _super.prototype.show.call(this, element);
    };
    return PhotoSearchDialog;
}(ObjectSearchDialog));
var PhotoChangeDialogOptions = (function (_super) {
    __extends(PhotoChangeDialogOptions, _super);
    function PhotoChangeDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoChangeDialogOptions;
}(ObjectChangeDialogOptions));
var PhotoChangeDialog = (function (_super) {
    __extends(PhotoChangeDialog, _super);
    function PhotoChangeDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "photos";
        _this.type_name = "photo";
        return _this;
    }
    PhotoChangeDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["datetime", new DateTimeInputField("Date", true)],
                    ["title", new TextInputField("Title", true)],
                    ["photographer", new AjaxSelectField("Photographer", new PersonType(), false)],
                    ["action", new SelectInputField("Action", [
                            ["", "no action"],
                            ["D", "delete"],
                            ["R", "regenerate thumbnails & video"],
                            ["M", "move photo"],
                            ["auto", "rotate automatic"],
                            ["90", "rotate 90 degrees clockwise"],
                            ["180", "rotate 180 degrees clockwise"],
                            ["270", "rotate 270 degrees clockwise"],
                        ], false)],
                ] },
            { name: 'connections', title: 'Connections', fields: [
                    ["albums", new AjaxSelectMultipleField("Album", new AlbumType(), false)],
                    ["categorys", new AjaxSelectMultipleField("Category", new CategoryType(), false)],
                    ["place", new AjaxSelectField("Place", new PlaceType(), false)],
                    ["persons", new AjaxSelectSortedField("Person", new PersonType(), false)],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextInputField("Camera Make", false)],
                    ["camera_model", new TextInputField("Camera Model", false)],
                ] },
        ];
        this.options.title = "Change photo";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PhotoChangeDialog.prototype.save_success = function (data) {
        var photo = new Photo();
        photo.set_streamable(data);
        if (this.obj.id != null) {
            window._photo_changed.trigger(photo);
        }
        else {
            window._photo_created.trigger(photo);
        }
        _super.prototype.save_success.call(this, data);
    };
    return PhotoChangeDialog;
}(ObjectChangeDialog));
var PhotoBulkUpdateDialogOptions = (function (_super) {
    __extends(PhotoBulkUpdateDialogOptions, _super);
    function PhotoBulkUpdateDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoBulkUpdateDialogOptions;
}(FormDialogOptions));
var PhotoBulkUpdateDialog = (function (_super) {
    __extends(PhotoBulkUpdateDialog, _super);
    function PhotoBulkUpdateDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "photos";
        return _this;
    }
    PhotoBulkUpdateDialog.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["datetime", new DateTimeInputField("Date", false)],
                    ["title", new TextInputField("Title", false)],
                    ["photographer", new AjaxSelectField("Photographer", new PersonType(), false)],
                    ["place", new AjaxSelectField("Place", new PlaceType(), false)],
                    ["action", new SelectInputField("Action", [
                            ["none", "no action"],
                            ["D", "delete"],
                            ["R", "regenerate thumbnails & video"],
                            ["M", "move photo"],
                            ["auto", "rotate automatic"],
                            ["90", "rotate 90 degrees clockwise"],
                            ["180", "rotate 180 degrees clockwise"],
                            ["270", "rotate 270 degrees clockwise"],
                        ], false)],
                ] },
            { name: 'add', title: 'Add', fields: [
                    ["add_albums", new AjaxSelectMultipleField("Album", new AlbumType(), false)],
                    ["add_categorys", new AjaxSelectMultipleField("Category", new CategoryType(), false)],
                    ["add_persons", new AjaxSelectSortedField("Person", new PersonType(), false)],
                ] },
            { name: 'rem', title: 'Remove', fields: [
                    ["rem_albums", new AjaxSelectMultipleField("Album", new AlbumType(), false)],
                    ["rem_categorys", new AjaxSelectMultipleField("Category", new CategoryType(), false)],
                    ["rem_persons", new AjaxSelectSortedField("Person", new PersonType(), false)],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextInputField("Camera Make", false)],
                    ["camera_model", new TextInputField("Camera Model", false)],
                ] },
        ];
        this.options.title = "Bulk photo update";
        this.options.button = "Save";
        _super.prototype.show.call(this, element);
    };
    PhotoBulkUpdateDialog.prototype.set = function (photo) {
        _super.prototype.set.call(this, photo);
    };
    PhotoBulkUpdateDialog.prototype.submit_values = function (values) {
        var data = {};
        if (values["datetime"] != null) {
            data.datetime = values["datetime"];
        }
        if (values["title"] != null) {
            data.title = values["title"];
        }
        if (values["photographer"] != null) {
            data.photographer_pk = values["photographer"].id;
        }
        if (values["place"] != null) {
            data.place_pk = values["place"].id;
        }
        if (values["action"] != null) {
            data.action = null;
            if (values["action"] != "none") {
                data.action = values["action"];
            }
        }
        data.add_albums_pk = [];
        for (var i = 0; i < values["add_albums"].length; i++) {
            data.add_albums_pk.push(values["add_albums"][i].id);
        }
        data.rem_albums_pk = [];
        for (var i = 0; i < values["rem_albums"].length; i++) {
            data.rem_albums_pk.push(values["rem_albums"][i].id);
        }
        data.add_categorys_pk = [];
        for (var i = 0; i < values["add_categorys"].length; i++) {
            data.add_categorys_pk.push(values["add_categorys"][i].id);
        }
        data.rem_categorys_pk = [];
        for (var i = 0; i < values["rem_categorys"].length; i++) {
            data.rem_categorys_pk.push(values["rem_categorys"][i].id);
        }
        data.add_persons_pk = [];
        for (var i = 0; i < values["add_persons"].length; i++) {
            data.add_persons_pk.push(values["add_persons"][i].id);
        }
        data.rem_persons_pk = [];
        for (var i = 0; i < values["rem_persons"].length; i++) {
            data.rem_persons_pk.push(values["rem_persons"][i].id);
        }
        if (values["camera_make"] != null) {
            data.camera_make = values["camera_make"];
        }
        if (values["camera_model"] != null) {
            data.camera_model = values["camera_model"];
        }
        this.data = data;
        this.element.hide();
        var params = {
            criteria: this.options.criteria,
            obj: data,
            on_proceed: $.proxy(this.proceed, this),
            on_cancel: $.proxy(this.cancel, this)
        };
        var div = $("<div/>");
        var dialog = new PhotoBulkConfirmDialog(params);
        dialog.show(div);
    };
    PhotoBulkUpdateDialog.prototype.proceed = function () {
        this.remove();
        var params = {
            criteria: this.options.criteria,
            obj: this.data
        };
        var div = $("<div/>");
        var dialog = new PhotoBulkProceedDialog(params);
        dialog.show(div);
    };
    PhotoBulkUpdateDialog.prototype.cancel = function () {
        this.element.show();
        this.enable();
    };
    return PhotoBulkUpdateDialog;
}(FormDialog));
var PhotoBulkConfirmDialogOptions = (function (_super) {
    __extends(PhotoBulkConfirmDialogOptions, _super);
    function PhotoBulkConfirmDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoBulkConfirmDialogOptions;
}(BaseDialogOptions));
var PhotoBulkConfirmDialog = (function (_super) {
    __extends(PhotoBulkConfirmDialog, _super);
    function PhotoBulkConfirmDialog(options) {
        var _this = this;
        options.title = "Confirm bulk update";
        options.button = "Confirm";
        _this = _super.call(this, options) || this;
        _this.proceed = false;
        _this.type = "photos";
        return _this;
    }
    PhotoBulkConfirmDialog.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.ul = $("<ul/>").appendTo(this.element);
        this.ol = $("<div/>").appendTo(this.element);
        var options = {};
        this.photo_list = new PhotoListWidget(options);
        this.photo_list.show(this.ol);
        this.set(this.options.criteria);
    };
    PhotoBulkConfirmDialog.prototype.set = function (values) {
        var _this = this;
        this.ul.empty();
        $.each(values, function (key, value) {
            $("<li/>").text(key + " = " + value)
                .appendTo(_this.ul);
        });
        this.photo_list.filter(this.options.criteria);
    };
    PhotoBulkConfirmDialog.prototype.disable = function () {
        this.photo_list.disable();
        _super.prototype.disable.call(this);
    };
    PhotoBulkConfirmDialog.prototype.enable = function () {
        this.photo_list.enable();
        _super.prototype.enable.call(this);
    };
    PhotoBulkConfirmDialog.prototype.submit = function () {
        this.proceed = true;
        this.remove();
    };
    PhotoBulkConfirmDialog.prototype.destroy = function () {
        _super.prototype.destroy.call(this);
        if (this.proceed) {
            this.options.on_proceed();
        }
        else {
            this.options.on_cancel();
        }
    };
    return PhotoBulkConfirmDialog;
}(BaseDialog));
var PhotoBulkProceedDialogOptions = (function (_super) {
    __extends(PhotoBulkProceedDialogOptions, _super);
    function PhotoBulkProceedDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoBulkProceedDialogOptions;
}(BaseDialogOptions));
var PhotoBulkProceedDialog = (function (_super) {
    __extends(PhotoBulkProceedDialog, _super);
    function PhotoBulkProceedDialog(options) {
        var _this = this;
        options.title = "Bulk update";
        options.button = "Retry";
        _this = _super.call(this, options) || this;
        _this.type = "photos";
        return _this;
    }
    PhotoBulkProceedDialog.prototype.show = function (element) {
        _super.prototype.show.call(this, element);
        this.pb = $("<div/>").appendTo(this.element);
        this.pb.progressbar({ value: false });
        this.status = $("<div/>")
            .text("Please wait")
            .appendTo(this.element);
        this.set(this.options.obj);
    };
    PhotoBulkProceedDialog.prototype.set = function (values) {
        this.values = values;
        this.check_submit();
    };
    PhotoBulkProceedDialog.prototype.submit = function () {
        var data = {
            'criteria': this.options.criteria,
            'values': this.values
        };
        this._save("PATCH", null, data);
    };
    PhotoBulkProceedDialog.prototype.save_success = function (data) {
        //        $.each(data.results, function(photo) {
        //            window._photo_changed.trigger(photo)
        //        })
        window._reload_all.trigger(null);
        _super.prototype.save_success.call(this, data);
    };
    PhotoBulkProceedDialog.prototype.destroy = function () {
        _super.prototype.destroy.call(this);
    };
    return PhotoBulkProceedDialog;
}(BaseDialog));
var PhotoDeleteDialogOptions = (function (_super) {
    __extends(PhotoDeleteDialogOptions, _super);
    function PhotoDeleteDialogOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoDeleteDialogOptions;
}(ObjectDeleteDialogOptions));
var PhotoDeleteDialog = (function (_super) {
    __extends(PhotoDeleteDialog, _super);
    function PhotoDeleteDialog(options) {
        var _this = _super.call(this, options) || this;
        _this.type = "photos";
        _this.type_name = "photo";
        return _this;
    }
    PhotoDeleteDialog.prototype.save_success = function (data) {
        window._photo_deleted.trigger(this.obj_id);
        _super.prototype.save_success.call(this, data);
    };
    return PhotoDeleteDialog;
}(ObjectDeleteDialog));
///////////////////////////////////////
// photo widgets
///////////////////////////////////////
var PhotoCriteriaWidgetOptions = (function (_super) {
    __extends(PhotoCriteriaWidgetOptions, _super);
    function PhotoCriteriaWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoCriteriaWidgetOptions;
}(ObjectCriteriaWidgetOptions));
var PhotoCriteriaWidget = (function (_super) {
    __extends(PhotoCriteriaWidget, _super);
    function PhotoCriteriaWidget(options) {
        return _super.call(this, options) || this;
    }
    return PhotoCriteriaWidget;
}(ObjectCriteriaWidget));
var PhotoListWidgetOptions = (function (_super) {
    __extends(PhotoListWidgetOptions, _super);
    function PhotoListWidgetOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoListWidgetOptions;
}(ObjectListWidgetOptions));
var PhotoListWidget = (function (_super) {
    __extends(PhotoListWidget, _super);
    function PhotoListWidget(options) {
        return _super.call(this, options, new PhotoType()) || this;
    }
    PhotoListWidget.prototype.add_selection = function (photo) {
        var selection = this.options.selection;
        if (selection.indexOf(photo.id) === -1) {
            selection.push(photo.id);
            push_state(true);
        }
    };
    PhotoListWidget.prototype.del_selection = function (photo) {
        var selection = this.options.selection;
        var index = selection.indexOf(photo.id);
        if (index !== -1) {
            selection.splice(index, 1);
            push_state(true);
        }
    };
    PhotoListWidget.prototype.set_selection = function (selection) {
        this.options.selection = selection;
    };
    PhotoListWidget.prototype.get_selection = function () {
        return this.options.selection;
    };
    PhotoListWidget.prototype.is_photo_selected = function (photo) {
        var selection = this.options.selection;
        var index = selection.indexOf(photo.id);
        return index !== -1;
    };
    PhotoListWidget.prototype.show = function (element) {
        var _this = this;
        if (this.options.selection == null) {
            this.options.selection = [];
        }
        _super.prototype.show.call(this, element);
        var options = {
            filter: "li",
            selected: function (event, ui) {
                _this.add_selection($(ui.selected).data('item'));
            },
            unselected: function (event, ui) {
                _this.del_selection($(ui.unselected).data('item'));
            }
        };
        $.spud.myselectable(options, this.ul);
        window._photo_changed.add_listener(this, function (photo) {
            var li = _this.create_li_for_obj(photo);
            _this.get_item(photo.id).replaceWith(li);
        });
        window._photo_deleted.add_listener(this, function (photo_id) {
            _this.get_item(photo_id).remove();
            _this.load_if_required();
        });
    };
    PhotoListWidget.prototype.create_child_viewport = function () {
        var child_id = this.options.child_id;
        var params = {
            id: child_id,
            object_loader: null,
            object_list_loader: null
        };
        var viewport;
        viewport = new PhotoDetailViewport(params);
        add_viewport(viewport);
        return viewport;
    };
    PhotoListWidget.prototype.get_photo = function (obj) {
        return obj;
    };
    PhotoListWidget.prototype.get_details = function (obj) {
        var details = _super.prototype.get_details.call(this, obj);
        var datetime = moment(obj.datetime[0]);
        datetime.zone(-obj.datetime[1]);
        var datetime_str = datetime.format("YYYY-MM-DD hh:mm");
        details.push($("<div/>").text(datetime_str));
        if (obj.place != null) {
            details.push($("<div/>").text(obj.place.title));
        }
        return details;
    };
    PhotoListWidget.prototype.get_description = function (obj) {
        return obj.description;
    };
    PhotoListWidget.prototype.create_li = function (photo, title, details, description, a) {
        var li = _super.prototype.create_li.call(this, photo, title, details, description, a);
        li.data("item", photo);
        li.toggleClass("removed", photo.action === "D");
        li.toggleClass("regenerate", photo.action != null && photo.action !== "D");
        li.toggleClass("ui-selected", this.is_photo_selected(photo));
        return li;
    };
    PhotoListWidget.prototype.bulk_update = function () {
        var criteria = this.options.criteria;
        if (this.options.selection.length > 0) {
            criteria = $.extend({}, criteria);
            criteria.photos = this.options.selection;
        }
        var params = {
            criteria: criteria
        };
        var div = $("<div/>");
        var dialog = new PhotoBulkUpdateDialog(params);
        dialog.show(div);
    };
    return PhotoListWidget;
}(ObjectListWidget));
var PhotoDetailInfoboxOptions = (function (_super) {
    __extends(PhotoDetailInfoboxOptions, _super);
    function PhotoDetailInfoboxOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoDetailInfoboxOptions;
}(InfoboxOptions));
var PhotoDetailInfobox = (function (_super) {
    __extends(PhotoDetailInfobox, _super);
    function PhotoDetailInfobox(options) {
        return _super.call(this, options) || this;
    }
    PhotoDetailInfobox.prototype.show = function (element) {
        this.options.pages = [
            { name: 'basic', title: 'Basics', fields: [
                    ["title", new TextOutputField("Title")],
                    ["description", new POutputField("Description")],
                    ["view", new POutputField("View")],
                    ["comment", new POutputField("Comment")],
                    ["name", new TextOutputField("File")],
                    ["albums", new LinkListOutputField("Albums", new AlbumType())],
                    ["categorys", new LinkListOutputField("Categories", new CategoryType())],
                    ["place", new LinkOutputField("Place", new PlaceType())],
                    ["persons", new LinkListOutputField("People", new PersonType())],
                    ["datetime", new DateTimeOutputField("Date & time")],
                    ["photographer", new LinkOutputField("Photographer", new PersonType())],
                    ["rating", new TextOutputField("Rating")],
                    //                ["videos", new HtmlOutputField("Videos")],
                    //                ["related", new HtmlListOutputField("Related")],
                    ["action", new TextOutputField("Action")],
                ] },
            { name: 'camera', title: 'Camera', fields: [
                    ["camera_make", new TextOutputField("Camera make")],
                    ["camera_model", new TextOutputField("Camera model")],
                    ["flash_used", new TextOutputField("Flash")],
                    ["focal_length", new TextOutputField("Focal Length")],
                    ["exposure", new TextOutputField("Exposure")],
                    ["aperture", new TextOutputField("Aperture")],
                    ["iso_equiv", new TextOutputField("ISO")],
                    ["metering_mode", new TextOutputField("Metering mode")],
                ] },
        ];
        _super.prototype.show.call(this, element);
        this.img = new ImageWidget({ size: "mid", include_link: false });
        var e = $("<div></div>")
            .set_widget(this.img)
            .appendTo(this.element);
    };
    PhotoDetailInfobox.prototype.set = function (photo) {
        this.element.removeClass("error");
        _super.prototype.set.call(this, photo);
        this.options.obj = photo;
        this.img.set(photo);
    };
    return PhotoDetailInfobox;
}(Infobox));
///////////////////////////////////////
// photo viewports
///////////////////////////////////////
var PhotoListViewportOptions = (function (_super) {
    __extends(PhotoListViewportOptions, _super);
    function PhotoListViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoListViewportOptions;
}(ObjectListViewportOptions));
var PhotoListViewport = (function (_super) {
    __extends(PhotoListViewport, _super);
    function PhotoListViewport(options) {
        return _super.call(this, options, new PhotoType()) || this;
    }
    PhotoListViewport.prototype.setup_menu = function (menu) {
        _super.prototype.setup_menu.call(this, menu);
        menu.append($("<li/>")
            .text("Update")
            .on("click", function (ev) {
            void ev;
            var instance = this.ol;
            instance.bulk_update();
        }));
    };
    PhotoListViewport.prototype.get_streamable_state = function () {
        var streamable = _super.prototype.get_streamable_state.call(this);
        if (this.ol != null) {
            var instance = this.ol;
            var selection = instance.get_selection();
            if (selection.length > 0) {
                set_streamable_array_as_string(streamable, 'selection', selection);
            }
        }
        return streamable;
    };
    PhotoListViewport.prototype.set_streamable_state = function (streamable) {
        // load streamable state, must be called before show() is called.
        _super.prototype.set_streamable_state.call(this, streamable);
        var object_list_options = {};
        var selection = get_streamable_number_array(streamable, 'selection');
        // FIXME
        if (this.element != null) {
            this.ol.set_selection(selection);
        }
        else {
            this.selection = selection;
        }
    };
    PhotoListViewport.prototype.filter = function (value) {
        _super.prototype.filter.call(this, value);
        if (this.element != null) {
            this.ol.set_selection(null);
            this.selection = null;
        }
    };
    return PhotoListViewport;
}(ObjectListViewport));
var PhotoDetailViewportOptions = (function (_super) {
    __extends(PhotoDetailViewportOptions, _super);
    function PhotoDetailViewportOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PhotoDetailViewportOptions;
}(ObjectDetailViewportOptions));
var PhotoDetailViewport = (function (_super) {
    __extends(PhotoDetailViewport, _super);
    function PhotoDetailViewport(options) {
        return _super.call(this, options, new PhotoType()) || this;
    }
    PhotoDetailViewport.prototype.setup_menu = function (menu) {
        var _this = this;
        _super.prototype.setup_menu.call(this, menu);
        this.orig = $("<li/>")
            .text("Original")
            .on("click", function (ev) {
            void ev;
            var obj = _this.get_obj();
            if (obj.orig_url != null) {
                window.open(obj.orig_url);
            }
        })
            .hide()
            .appendTo(menu);
    };
    PhotoDetailViewport.prototype.loaded = function (obj) {
        this.orig.toggle(obj.orig_url != null);
        this.div
            .toggleClass("removed", obj.action === "D")
            .toggleClass("regenerate", obj.action != null && obj.action !== "D");
        _super.prototype.loaded.call(this, obj);
    };
    PhotoDetailViewport.prototype.show = function (element) {
        var _this = this;
        _super.prototype.show.call(this, element);
        window._photo_changed.add_listener(this, function (obj) {
            var this_obj_id = _this.get_obj_id();
            if (obj.id === this_obj_id) {
                _this.set(_this.obj_type.load(obj.id));
            }
        });
        window._photo_deleted.add_listener(this, function (obj_id) {
            var this_obj_id = _this.get_obj_id();
            if (obj_id === this_obj_id) {
                _this.remove();
            }
        });
    };
    PhotoDetailViewport.prototype.get_photo_criteria = function () {
        return null;
    };
    PhotoDetailViewport.prototype.get_children_criteria = function () {
        var criteria = new PhotoCriteria();
        criteria.instance = this.get_obj();
        criteria.mode = 'children';
        return criteria;
    };
    return PhotoDetailViewport;
}(ObjectDetailViewport));

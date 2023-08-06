/// <reference path="photo.ts" />
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var Streamable = (function () {
    function Streamable() {
    }
    return Streamable;
}());
var GetStreamable = (function (_super) {
    __extends(GetStreamable, _super);
    function GetStreamable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return GetStreamable;
}(Streamable));
var PostStreamable = (function (_super) {
    __extends(PostStreamable, _super);
    function PostStreamable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return PostStreamable;
}(Streamable));
//class ListStreamable<T extends ObjectStreamable> extends PostStreamable {
//    // results : Array<T>
//    // count : string
//}
//class ObjectStreamable extends PostStreamable {
//}
var SpudObject = (function () {
    function SpudObject(obj_type, streamable) {
        this.obj_type = obj_type;
        if (streamable != null) {
            this.set_streamable(streamable);
        }
    }
    SpudObject.prototype.set_streamable = function (streamable) {
        this.id = get_streamable_number(streamable, "id");
        this.title = get_streamable_string(streamable, "title");
        var streamable_cover_photo = get_streamable_object(streamable, 'cover_photo');
        if (streamable_cover_photo != null) {
            this.cover_photo = new Photo(streamable_cover_photo);
        }
    };
    SpudObject.prototype.get_streamable = function () {
        var streamable = new PostStreamable;
        streamable['id'] = this.id;
        streamable['title'] = this.title;
        if (this.cover_photo != null) {
            streamable['cover_photo_pk'] = this.cover_photo.id;
        }
        return streamable;
    };
    return SpudObject;
}());
SpudObject.type = null;
var Criteria = (function () {
    function Criteria() {
    }
    Criteria.prototype.get_streamable = function () {
        var streamable = {};
        return streamable;
    };
    Criteria.prototype.get_idinputfields = function () {
        var items = this.get_items();
        var result = [];
        for (var i = 0; i < items.length; i++) {
            result.push(items[i].get_idinputfield());
        }
        return result;
    };
    return Criteria;
}());

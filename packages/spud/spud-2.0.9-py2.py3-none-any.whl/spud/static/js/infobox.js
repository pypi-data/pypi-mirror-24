/// <reference path="globals.ts" />
/// <reference path="generic.ts" />
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
// define output_field
var OutputField = (function () {
    function OutputField(title) {
        this.title = title;
    }
    OutputField.prototype.to_html = function (id) {
        var html = this.create(id);
        this.dt = $("<div class='term'/>")
            .text(this.title);
        this.dd = $("<div class='definition'/>")
            .append(html);
        this.item = $("<div class='item'/>")
            .append(this.dt)
            .append(this.dd);
        this.visible = true;
        return this.item;
    };
    OutputField.prototype.create = function (id) {
        this.output = $('<span />');
        return this.output;
    };
    OutputField.prototype.destroy = function () {
        this.item.remove();
    };
    OutputField.prototype.set = function (value) {
    };
    OutputField.prototype.set_edit_value = function (html) {
        html.addClass("edit");
        var edit = this.dd.find(".edit");
        if (edit.length > 0) {
            edit.replaceWith(html);
        }
        else {
            this.dd.append(" ");
            this.dd.append(html);
        }
    };
    OutputField.prototype.toggle = function (show) {
        this.item.toggleClass("hidden", !show);
        this.visible = show;
    };
    OutputField.prototype.hide = function () {
        this.item.addClass("hidden");
        this.visible = false;
    };
    OutputField.prototype.show = function () {
        this.item.removeClass("hidden");
        this.visible = true;
    };
    return OutputField;
}());
// define text_output_field
var TextOutputField = (function (_super) {
    __extends(TextOutputField, _super);
    function TextOutputField(title) {
        return _super.call(this, title) || this;
    }
    TextOutputField.prototype.set = function (value) {
        if (value != null) {
            this.output.text(value);
        }
        else {
            this.output.text("None");
        }
        this.toggle(Boolean(value));
    };
    return TextOutputField;
}(OutputField));
// define select_input_field
var SelectOutputField = (function (_super) {
    __extends(SelectOutputField, _super);
    function SelectOutputField(title, options) {
        var _this = _super.call(this, title) || this;
        _this.options = {};
        for (var _i = 0, options_1 = options; _i < options_1.length; _i++) {
            var option = options_1[_i];
            var id = option[0];
            var value = option[1];
            _this.options[id] = value;
        }
        return _this;
    }
    SelectOutputField.prototype.set = function (value) {
        value = this.options[value];
        this.output.text(value);
        this.toggle(value != null);
    };
    return SelectOutputField;
}(OutputField));
// define boolean_outbooleanut_field
var booleanOutputField = (function (_super) {
    __extends(booleanOutputField, _super);
    function booleanOutputField(title) {
        return _super.call(this, title) || this;
    }
    booleanOutputField.prototype.set = function (value) {
        this.output.text(value ? "True" : " False");
        this.toggle(value != null);
    };
    return booleanOutputField;
}(OutputField));
// define integer_outintegerut_field
var IntegerOutputField = (function (_super) {
    __extends(IntegerOutputField, _super);
    function IntegerOutputField(title) {
        return _super.call(this, title) || this;
    }
    IntegerOutputField.prototype.set = function (value) {
        this.output.text(value);
        this.toggle(value != null);
    };
    return IntegerOutputField;
}(OutputField));
// define p_output_field
var POutputField = (function (_super) {
    __extends(POutputField, _super);
    function POutputField(title) {
        return _super.call(this, title) || this;
    }
    POutputField.prototype.set = function (value) {
        this.output.p(value);
        this.toggle(Boolean(value));
    };
    return POutputField;
}(OutputField));
// define datetime_output_field
var DateTimeOutputField = (function (_super) {
    __extends(DateTimeOutputField, _super);
    function DateTimeOutputField(title) {
        var _this = _super.call(this, title) || this;
        _this.timezone = "local";
        return _this;
    }
    DateTimeOutputField.prototype.create = function (id) {
        var _this = this;
        void id;
        this.datetime = null;
        var div = $('<div/>');
        this.output = $('<div />').appendTo(div);
        $('<select />')
            .append($('<option />')
            .attr('value', "UTC")
            .text("utc"))
            .append($('<option />')
            .attr('value', "source")
            .text("source"))
            .append($('<option />')
            .attr('value', "local")
            .text("local"))
            .val(this.timezone)
            .on("change", function (ev) {
            void ev;
            _this.timezone = $(_this).val();
            _this.set(_this.value);
        })
            .appendTo(div);
        return div;
    };
    DateTimeOutputField.prototype.set = function (value) {
        this.value = value;
        this.output.empty();
        if (value != null) {
            var datetime = moment(value[0]);
            var utc_offset = value[1];
            if (this.timezone === "local") {
                datetime.local();
            }
            else if (this.timezone === "source") {
                datetime.zone(-utc_offset);
            }
            else {
                datetime = datetime.tz(this.timezone);
            }
            var datetime_str = void 0;
            if (datetime != null) {
                datetime_str = datetime.format("dddd, MMMM Do YYYY, h:mm:ss a");
            }
            else {
                datetime_str = "N/A";
            }
            this.output
                .append($("<p/>").text(datetime_str + " " + this.timezone));
            this.show();
        }
        else {
            this.hide();
        }
    };
    return DateTimeOutputField;
}(OutputField));
// define link_output_field
var LinkOutputField = (function (_super) {
    __extends(LinkOutputField, _super);
    function LinkOutputField(title, type) {
        var _this = _super.call(this, title) || this;
        _this.type = type;
        return _this;
    }
    LinkOutputField.prototype.set = function (value) {
        this.toggle(value != null);
        if (value == null) {
            this.output.text("");
            return;
        }
        var a = object_a(this.type, value);
        this.output.empty();
        this.output.append(a);
    };
    return LinkOutputField;
}(OutputField));
// define link_list_output_field
var LinkListOutputField = (function (_super) {
    __extends(LinkListOutputField, _super);
    function LinkListOutputField(title, type) {
        var _this = _super.call(this, title) || this;
        _this.type = type;
        return _this;
    }
    LinkListOutputField.prototype.set = function (value) {
        this.output.empty();
        if (value == null || value.length === 0) {
            this.hide();
            return;
        }
        var sep = "";
        for (var _i = 0, value_1 = value; _i < value_1.length; _i++) {
            var item = value_1[_i];
            this.output.append(sep);
            if (item != null) {
                this.output.append(object_a(this.type, item));
            }
            else {
                this.output.append("Unknown");
            }
            sep = ", ";
        }
        this.output.append(".");
        this.toggle(value.length > 0);
    };
    return LinkListOutputField;
}(OutputField));
// define photo_output_field
var PhotoOutputField = (function (_super) {
    __extends(PhotoOutputField, _super);
    function PhotoOutputField(title, size, do_link) {
        var _this = _super.call(this, title) || this;
        _this.size = size;
        _this.do_link = do_link;
        return _this;
    }
    PhotoOutputField.prototype.create = function (id) {
        this.output = $('<div />');
        this.img = new ImageWidget({ size: this.size, include_link: this.do_link });
        this.img.show(this.output);
        return this.output;
    };
    PhotoOutputField.prototype.set = function (value) {
        this.img.set(value);
        this.toggle(value != null);
    };
    PhotoOutputField.prototype.destroy = function () {
        this.img.remove();
        _super.prototype.destroy.call(this);
    };
    return PhotoOutputField;
}(OutputField));
// define infobox widget
var InfoboxOptions = (function (_super) {
    __extends(InfoboxOptions, _super);
    function InfoboxOptions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    return InfoboxOptions;
}(WidgetOptions));
var Infobox = (function (_super) {
    __extends(Infobox, _super);
    function Infobox(options) {
        return _super.call(this, options) || this;
    }
    Infobox.prototype.show = function (element) {
        var mythis = this;
        var options = this.options;
        _super.prototype.show.call(this, element);
        this.element.addClass("infobox");
        if (options.title != null) {
            $("<h2></h2")
                .text(this.options.title)
                .appendTo(this.element);
        }
        this.fields = {};
        if (this.options.pages != null) {
            this.page = {};
            this.tabs = $("<div/>")
                .addClass("fields")
                .appendTo(this.element);
            var ul = $("<ul></ul>").appendTo(this.tabs);
            for (var i = 0; i < this.options.pages.length; i++) {
                var page = this.options.pages[i];
                var name = page.name;
                var title = page.title;
                $("<li/>")
                    .append($("<a/>")
                    .attr("href", '#' + name)
                    .text(title))
                    .appendTo(ul);
                this.page[name] = $("<div/>")
                    .addClass("def_list")
                    .attr('id', name)
                    .appendTo(mythis.tabs);
                this.create_fields(name, page.fields);
            }
            this.tabs.tabs();
        }
        else {
            this.dl = $("<div/>")
                .addClass("fields")
                .addClass("def_list")
                .appendTo(this.element);
            this.create_fields(null, this.options.fields);
        }
        if (this.options.obj != null) {
            this.set(this.options.obj);
        }
    };
    Infobox.prototype.destroy = function () {
        this.element.removeClass("infobox");
        for (var id in this.fields) {
            var field = this.fields[id];
            field.destroy();
        }
        _super.prototype.destroy.call(this);
    };
    Infobox.prototype.create_fields = function (page, fields) {
        if (fields != null) {
            this.add_fields(page, fields);
        }
    };
    Infobox.prototype.set = function (values) {
        var visible = false;
        for (var id in this.fields) {
            var field = this.fields[id];
            if (values != null) {
                this.set_value(id, values[id]);
            }
            else {
                this.set_value(id, null);
            }
            if (field.visible) {
                visible = true;
            }
        }
        if (this.tabs != null) {
            this.tabs.toggleClass("hidden", !visible);
        }
        if (this.dl != null) {
            this.dl.toggleClass("hidden", !visible);
        }
    };
    Infobox.prototype.add_field = function (page, id, field) {
        this.remove_field(id);
        var html = field.to_html(id);
        if (page == null) {
            this.dl.append(html);
        }
        else {
            this.page[page].append(html);
        }
        this.fields[id] = field;
    };
    Infobox.prototype.add_fields = function (page, fields) {
        for (var _i = 0, fields_1 = fields; _i < fields_1.length; _i++) {
            var item = fields_1[_i];
            var id = item[0];
            var field = item[1];
            this.add_field(page, id, field);
        }
    };
    Infobox.prototype.remove_field = function (id) {
        var field = this.fields[id];
        if (field != null) {
            field.destroy();
            delete this.fields[id];
        }
    };
    Infobox.prototype.remove_all_fields = function () {
        for (var id in this.fields) {
            var field = this.fields[id];
            this.remove_field(id);
        }
    };
    Infobox.prototype.set_value = function (id, value) {
        this.fields[id].set(value);
    };
    Infobox.prototype.set_edit_value = function (id, value, can_change, a) {
        this.fields[id].set(value);
        if (can_change) {
            this.fields[id].show();
            this.fields[id].set_edit_value(a);
        }
    };
    return Infobox;
}(Widget));

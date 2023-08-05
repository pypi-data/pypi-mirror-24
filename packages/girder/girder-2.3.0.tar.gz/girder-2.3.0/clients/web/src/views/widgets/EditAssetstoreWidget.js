import $ from 'jquery';
import _ from 'underscore';

import View from 'girder/views/View';
import { AssetstoreType } from 'girder/constants';
import { handleClose, handleOpen } from 'girder/dialog';

import EditAssetstoreWidgetTemplate from 'girder/templates/widgets/editAssetstoreWidget.pug';

import 'girder/utilities/jquery/girderEnable';
import 'girder/utilities/jquery/girderModal';

/**
 * This widget is used to edit an existing assetstore.
 */
var EditAssetstoreWidget = View.extend({
    events: {
        'submit #g-assetstore-edit-form': function (e) {
            e.preventDefault();

            var fields = this.fieldsMap[this.model.get('type')].get.call(this);
            fields.name = this.$('#g-edit-name').val();

            this.updateAssetstore(fields);

            this.$('button.g-save-assetstore').girderEnable(false);
            this.$('.g-validation-failed-message').text('');
        }
    },

    initialize: function (settings) {
        this.model = settings.model || null;
    },

    /**
     * This maps each type of assetstore to a function to getter and setter
     * functions. The set functions are reponsible for populating the dialog
     * fields with the appropriate current model values, and the get functions
     * are responsible for reading the user input values from the dialog and
     * returning a set of fields (excluding the name field) to set on the model.
     *
     * This is meant to make it easy for plugins that add new assetstore types
     * to extend this dialog to allow the setting of custom fields using whatever
     * widgets make the most sense. By adding a new field to this object, this
     * edit dialog can support any type of assetstore dynamically.
     *
     * Since the keys of this array are values defined by variables,
     * we set them after this class rather than inline with object creation syntax.
     */
    fieldsMap: {},

    render: function () {
        var view = this;
        var modal = this.$el.html(EditAssetstoreWidgetTemplate({
            assetstore: view.model,
            types: AssetstoreType
        })).girderModal(this).on('shown.bs.modal', function () {
            view.$('#g-edit-name').focus();
            handleOpen('assetstoreedit', undefined, view.model.get('id'));
            view.$('#g-edit-name').val(view.model.get('name'));
            view.fieldsMap[view.model.get('type')].set.call(view);
        }).on('hidden.bs.modal', function () {
            handleClose('assetstoreedit', undefined, view.model.get('id'));
        });
        modal.trigger($.Event('ready.girder.modal', {relatedTarget: modal}));
        return this;
    },

    updateAssetstore: function (fields) {
        var oldfields = {};
        var model = this.model;
        _.each(fields, function (value, key) {
            oldfields[key] = model.get(key);
        });
        this.model.set(fields);
        this.model.on('g:saved', function () {
            this.$el.modal('hide');
            this.trigger('g:saved', this.model);
        }, this).on('g:error', function (err) {
            this.$('.g-validation-failed-message').text(err.responseJSON.message);
            this.$('button.g-save-assetstore').girderEnable(true);
            this.$('#g-' + err.responseJSON.field).focus();
            this.model.set(oldfields);
        }, this).save();
    }
});

var fieldsMap = EditAssetstoreWidget.prototype.fieldsMap;

fieldsMap[AssetstoreType.FILESYSTEM] = {
    get: function () {
        return {
            root: this.$('#g-edit-fs-root').val(),
            perms: this.$('#g-edit-fs-perms').val()
        };
    },
    set: function () {
        var permStr = this.model.get('perms') ? this.model.get('perms').toString(8) : '600';
        this.$('#g-edit-fs-perms').val(permStr);
        this.$('#g-edit-fs-root').val(this.model.get('root'));
    }
};

fieldsMap[AssetstoreType.GRIDFS] = {
    get: function () {
        return {
            db: this.$('#g-edit-gridfs-db').val(),
            mongohost: this.$('#g-edit-gridfs-mongohost').val(),
            replicaset: this.$('#g-edit-gridfs-replicaset').val(),
            shard: this.$('#g-edit-gridfs-shard-auto').is(':checked') ? 'auto' : false
        };
    },
    set: function () {
        this.$('#g-edit-gridfs-db').val(this.model.get('db'));
        this.$('#g-edit-gridfs-mongohost').val(this.model.get('mongohost'));
        this.$('#g-edit-gridfs-replicaset').val(this.model.get('replicaset'));
        this.$('#g-edit-gridfs-shard-auto').attr('checked', this.model.get('shard') === 'auto');
    }
};

fieldsMap[AssetstoreType.S3] = {
    get: function () {
        return {
            bucket: this.$('#g-edit-s3-bucket').val(),
            prefix: this.$('#g-edit-s3-prefix').val(),
            accessKeyId: this.$('#g-edit-s3-access-key-id').val(),
            secret: this.$('#g-edit-s3-secret').val(),
            service: this.$('#g-edit-s3-service').val(),
            readOnly: this.$('#g-edit-s3-readonly').is(':checked')
        };
    },
    set: function () {
        this.$('#g-edit-s3-bucket').val(this.model.get('bucket'));
        this.$('#g-edit-s3-prefix').val(this.model.get('prefix'));
        this.$('#g-edit-s3-access-key-id').val(this.model.get('accessKeyId'));
        this.$('#g-edit-s3-secret').val(this.model.get('secret'));
        this.$('#g-edit-s3-service').val(this.model.get('service'));
        this.$('#g-edit-s3-readonly').attr('checked', this.model.get('readOnly') ? 'checked' : undefined);
    }
};

export default EditAssetstoreWidget;

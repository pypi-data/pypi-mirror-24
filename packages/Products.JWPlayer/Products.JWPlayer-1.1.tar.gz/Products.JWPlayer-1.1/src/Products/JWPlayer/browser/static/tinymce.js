(function ($) {
    tinymce.create('tinymce.plugins.JWplayerPlugin', {

        init: function (ed, url) {

            ed.addButton('jwplayer', {
                title: 'Insert/Edit JWPlayer Element',
                cmd: 'jwplayer',
                image: url + '/jw.jpg',
                onclick: function () {
                    try {
                        openSettingsPanel(url + '/@@jwp-tinymce-settings');
                    } catch (e) {
                        alert('Whoops. Something went wrong!');
                    }
                }
            });

            ed.onNodeChange.add(function (ed, cm, node) {
                var $node = $(ed.selection.getNode());
                if ($node.hasClass('jwp-tinymce-plone')) {
                    cm.setActive('jwplayer', true);
                    setTimeout(function(){
                        cm.setActive('image', false);
                    }, 300);
                } else {
                    cm.setActive('jwplayer', false);
                }
            });

        }

    });

    function openSettingsPanel(url) {
        tinyMCE.activeEditor.jwptinymce = null;
        var ed = tinyMCE.activeEditor;
        if (ed == null) {
            return;
        }

        var $node = $(ed.selection.getNode());
        if ($node.hasClass('jwp-tinymce-plone')) {
            tinyMCE.activeEditor.jwptinymce = $node.data();
        }

        ed.windowManager.open({
            title: "Insert Uploaded Video",
            url: url,
            width: 890,
            height: 760,
            inline: true,
            close_previous: "yes"
        });
    }

    tinymce.PluginManager.add('jwplayer', tinymce.plugins.JWplayerPlugin);
})(jQuery);


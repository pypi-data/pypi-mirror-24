(function ($, mcePopup) {
    var editor = mcePopup.editor;
 
    mcePopup.onInit.add(function() {
        var player_type = 'could-hosted';
        jq('#jwp-insert').bind('click', insertVideo);
        jq('#jwp-preview').bind('click', previewVideo);
        jq('#jwp-close').bind('click', closeVideo);
        jq('.toggle-trigger').bind('click', togglelize);
        if (editor.jwptinymce) {
            jq('#jwp-player-url').val(editor.jwptinymce.player_url);
            jq('#jwp-video-url').val(editor.jwptinymce.video_url);
            jq('#jwp-player-self-url').val(editor.jwptinymce.player_self_url);
            jq('#jwp-player-self-key').val(editor.jwptinymce.player_self_key);
            var str = '';
            for (var m in editor.jwptinymce) {
                if (m.indexOf('meta') === 0) {
                    str += m.replace('meta_', '') + ' = ' + editor.jwptinymce[m] + "\n";
                }
            }
            jq('#jwp-video-opts').val(str);
            player_type = editor.jwptinymce.player_type || player_type;
            jq('#is-'+player_type).trigger('click');
        }
    });
    
    function jq(args) {
        return $(args, document);
    }
    
    
    function togglelize() {
        var $opt = jq(this);
        var target = $opt.data('target');
        jq('.toggle-content').removeClass('active');
        jq(target).addClass('active');
        
    }

    function parseForm() {
        var player_url = $.trim(jq('#jwp-player-url').val());
        var video_url = $.trim(jq('#jwp-video-url').val());
        var player_self_url = $.trim(jq('#jwp-player-self-url').val());
        var player_self_key = $.trim(jq('#jwp-player-self-key').val());
        var opts = parseOptions($.trim(jq('#jwp-video-opts').val()));
        var player_type = jq('#is-self-hosted').is(':checked') ? 'self-hosted' : 'could-hosted';

        if (!player_url || !video_url || typeof JSON == 'undefined') {
            //alert ('video url and player url are required');
            //return;
        }

        var dom_opts = {
            'player_url': player_url,
            'video_url': video_url,
            'player_self_url': player_self_url,
            'player_self_key': player_self_key,
            'player_type': player_type,
            'meta': opts
        };
        return dom_opts;
    }

    function insertVideo() {
        var ed = editor;
        if (ed == null) {
            return;
        }

        var dom_opts = parseForm();
        var item = ed.selection.getNode();
        var jqitem = $(item);
        if (!jqitem.length) {
            ed.insertContent(_getHtml(dom_opts));
        } else {
            jqitem.replaceWith(_getHtml(dom_opts));
        }
        mcePopup.close();
    }

    function previewVideo() {
        var dom_opts = parseForm();
        var player_opts = {
            'width': 450,
            'height': 300,
            'autostart': true
        };

        jq('.jwp-tinymce-plone-container').remove();
        jq('#jwp-preview-tv').html(_getHtml(dom_opts));

        var pjwp = new ProductsJWPlayer($, player_opts);
        pjwp.initialize(jq('.jwp-tinymce-plone'));
    }

    function closeVideo() {
        mcePopup.close();
    }

    function parseSources(sources_string) {
        var sources = [];
        var lines = sources_string.split(";");
        for (var i = 0; i < lines.length; i++) {
            var file = $.trim(lines[i]);
            if (file) {
                sources.push({'file': file});
            }
        }
        return sources;
    }

    function parseOptions(opts_string) {
        var opts = {};
        var lines = opts_string.split("\n");
        if (lines.length) {
            for (var i = 0; i < lines.length; i++) {
                var line_parts = lines[i].split('=');
                if (line_parts.length === 2) {
                    var key = $.trim(line_parts[0]);
                    var val = $.trim(line_parts[1]);
                    opts[key] = val;
                }
            }
        }
        return opts;
    }

    function _getHtml(opts) {
        //var img_src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1BMVEX/TQBcNTh/AAAAAXRSTlPM0jRW/QAAAApJREFUeJxjYgAAAAYAAzY3fKgAAAAASUVORK5CYII=';
        //var img_src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKBAMAAAB/HNKOAAAAG1BMVEXMzMyWlpbFxcWxsbG3t7e+vr6jo6OcnJyqqqoOiJIsAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAHUlEQVQImWNgIBqoFTOkGjF4sDIYuDCktjIYaAAAHT0DNAs9MVkAAAAASUVORK5CYII=';
        //var img_src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAV4AAABLBAMAAADKafK1AAAAG1BMVEXMzMyWlpa3t7e+vr6jo6PFxcWcnJyqqqqxsbHfQEMwAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABZElEQVRoge3XzW6CQBQF4CM/g0sQEJbjG8gblEX3uOlaTatdQpp0DW/eOwjdGBpdDTTnizHjrI43l3sVICIiIiIiIiIiIiL6h1RoO8FzlpbX0bYTPMO5u1lbSPG4nfRDEENtEKQqbD6lP2rbmf7gJpLXybHKoY4qu55qyKf5Kl4kr5+gSHCo1bbyYqBrbaea5F8qMx8u2JUotMrhZkCwsR1r0ttHP8+a6rurukpJcRO5bbTtXBNMeU3ebn8tdAOVQkoNmKaYpT6Y5C3afNW+95vjZO5Ly7mmjHlXX7H3mvf13cKU3XawCWM/eOcw2MgQjuGb/jVdPU/D87bOjk4WQubDOh++xTwN88yNaj+SSRzpIp3x44ZhXwCRRtRCJZG8o9zbTjWt38d9RHmptDzLuphxeW+/d8bz7eRpa2Ee4Nzlde2FecjhOJ4W8U/DkcEwWEbe7e84WERezHY5EBERERERLdsP/mwjuikPM7cAAAAASUVORK5CYII=';
        var img_src = '../++resource++Products.JWPlayer/dummy.gif';
        var width = opts.meta.width || 320;
        var height = opts.meta.height || 240;
        var $ele = $('<div />');
        var $embed = $('<img />');
        for (var opt in opts) {
            if (opt === 'meta') {
                for (var meta_opt in opts['meta']) {
                    $embed.attr('data-meta_'+meta_opt, opts['meta'][meta_opt]);
                }
            } else {
                $embed.attr('data-'+opt, opts[opt]);
            }
        }
        $embed.attr({'src': img_src, width: width, height: height});
        $embed.addClass('jwp-tinymce-player jwp-tinymce-plone jwp-tinymce-item');
        $ele.append($embed);
        return $ele.html();
    }


})(top.jQuery, tinyMCEPopup);


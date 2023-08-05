/**
 * class ProductsJWPlayer
 *
 * @author Cyril Tata
 */

function ProductsJWPlayer(jq, opts) {
    this.jq = jq;
    this.opts = opts;
    this.players = {};
}

ProductsJWPlayer.prototype.initialize = function ($objs) {
    var $ = this.jq;
    var self = this;
    if (typeof $objs === 'undefined') {
        $objs = $('.jwp-tinymce-plone');
    }

    $objs.each(function (i, e) {
        var $obj = $(e);
        var id = 'jwp-tinymce-plone-' + i + '-' + Math.random().toString(36).substring(7);
        var data = $obj.data();
        data['meta'] = {};
        for (var key in data) {
            if (key.indexOf('meta_') === 0) {
                var v = data[key];
                var k = key.replace('meta_', '');
                data['meta'][k] = v;
                delete data[key];
            }

        }
        if (self.opts) {
            data['meta'] = $.extend(data['meta'], self.opts);
        }

        var $player = $('<div />').attr('id', id).html(' &nbsp; ');
        $player.data(data).addClass('jwp-tinymce-plone-container');
        $obj.after($player);
        self.players[i] = {
            'id': id,
            'data': data
        };
        $obj.remove();
        var player_url = null, player_key = null;
        if (data.player_type === 'self-hosted') {
            player_url = data.player_self_url;
            player_key = data.player_self_key;
        } else {
            player_url = data.player_url;
        }
        self.loadPlayerJS(player_url, player_key);
    });
};

ProductsJWPlayer.prototype.loadPlayerJS = function (player_url, player_key) {
    if (!player_url) {
        return;
    }

    var self = this;
    var jsLoaded = function() {
        if (player_key && !jwplayer.key) {
            jwplayer.key = player_key;
        }
        self.setupPlayers();
    };
    if (typeof jwplayer !== 'undefined') {
        jsLoaded();
        return;
    }

    var script = document.createElement('script');
    script.onload = jsLoaded;
    script.src = player_url;
    script.type = "text/javascript";
    document.head.appendChild(script);
};

ProductsJWPlayer.prototype.setupPlayers = function () {
    var $ = this.jq;
    for (var i in this.players) {
        var player = this.players[i];
        var playerInstance = jwplayer(this.players[i].id);
        var setup = {sources: this.parseSources(player.data.video_url)};
        if (setup.sources.length <= 0) {
            return;
        }

        setup = $.extend({}, setup, player.data.meta);
        playerInstance.setup(setup);
        this.players[i]['instance'] = playerInstance;
    }
};

ProductsJWPlayer.prototype.parseSources = function (sources_string) {
    var $ = this.jq;
    var sources = [];
    var lines = sources_string.split("||");
    for (var i = 0; i < lines.length; i++) {
        var file = $.trim(lines[i]);
        if (file) {
            sources.push({'file': file});
        }
    }
    return sources;
};
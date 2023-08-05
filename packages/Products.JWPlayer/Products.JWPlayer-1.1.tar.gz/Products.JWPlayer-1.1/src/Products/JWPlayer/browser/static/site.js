jQuery(document).ready(function() {

    // Intialize player instances on page
    if (typeof ProductsJWPlayer === 'undefined') {
        return;
    }
    (new ProductsJWPlayer(jQuery)).initialize();

});



    SETTINGS = {
        'offer_id': 2999,
        'adv_sub': "[0].ecommerce.purchase.actionField.id",
        'adv_sub2': "[0].ecommerce.purchase.actionField.coupon",
        'adv_sub3': null,
        'adv_sub4': null,
        'adv_sub5': null,
        'amount': "[0].ecommerce.purchase.products[0].price",
        'quantity': "[0].ecommerce.purchase.products[0].quantity"
    }
    Object.byString = function (o, s) {
        s = s.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
        s = s.replace(/^\./, ''); // strip a leading dot
        var a = s.split('.');
        for (var i = 0, n = a.length; i < n; ++i) {
            var k = a[i];
            if (k in o) {
                o = o[k];
            } else {
                return;
            }
        }
        return o;
    }
    SETTINGS_KEYS = ['adv_sub2','adv_sub3','adv_sub4','adv_sub5','amount']
    CONTROLS = {
        'itemsListPath': ''
    }
    function setItemsPath() {
        var re = /.+(?=\[([0-9]*)\])/g
        CONTROLS.itemsListPath = SETTINGS.amount.match(re)[0]
        re = /.+\[([0-9]*)\]\.?/g
        for(var i = 0; i < SETTINGS_KEYS.length; i++) {
            if(SETTINGS[SETTINGS_KEYS[i]])
                SETTINGS[SETTINGS_KEYS[i]] = SETTINGS[SETTINGS_KEYS[i]].replace(SETTINGS[SETTINGS_KEYS[i]].match(re),'')
        }
        if(typeof SETTINGS['quantity'] == 'string')
            SETTINGS['quantity'] = SETTINGS['quantity'].replace(SETTINGS['quantity'].match(re),'')
    }
    function parseDataLayer() {
        var orderID = Object.byString(dataLayer, SETTINGS.adv_sub)
        var qs = {
            "items": [],
            "orderID": orderID
        }
        items = Object.byString(dataLayer, CONTROLS.itemsListPath)
        for(var i = 0; i < items.length; i++) {
            item = {
                "adv_sub": orderID,
                "offer_id": SETTINGS.offer_id
            }
            for(var j = 0; j < SETTINGS_KEYS.length; j++) {
                if(SETTINGS[SETTINGS_KEYS[j]]) {
                    if(SETTINGS_KEYS[j] == "amount") {
                        if (typeof SETTINGS['quantity'] == "number") {
                            item[SETTINGS_KEYS[j]] = Object.byString(items[i], SETTINGS[SETTINGS_KEYS[j]]) * SETTINGS['quantity'];
                        } else {
                            item[SETTINGS_KEYS[j]] = Object.byString(items[i], SETTINGS[SETTINGS_KEYS[j]]) * Object.byString(items[i], SETTINGS['quantity']) ;
                        }
                    } else {
                        item[SETTINGS_KEYS[j]] = Object.byString(items[i], SETTINGS[SETTINGS_KEYS[j]]);
                    }
                }
            }
            qs.items.push(item)
        }
        return qs
    }
    function createPix(debug_mode=false) {
        if (true) {
            setItemsPath()
            var orderDetails = parseDataLayer()
            var items = orderDetails["items"];
            console.log(items)
            for (var i = 0; i < items.length; i++) {
                var params = [];
                var src = "https://shopback.go2cloud.org/aff_l?"
                var keys = Object.keys(items[i])
                for(var param_idx = 0; param_idx < keys.length; param_idx++)
                    if(SETTINGS[keys[param_idx]])
                        params.push(keys[param_idx] + '=' + items[i][keys[param_idx]])
                src += params.join('&');
                if (debug_mode) {
                    console.log(src)
                    continue;
                }
                var pix = document.createElement("img");
                pix.setAttribute("width", "1");
                pix.setAttribute("height", "1");
                pix.setAttribute("src", decodeURIComponent(src));
                document.body.appendChild(pix);
            }
        }
        else {
            console.log("no cookie has been stored.")
        }
    }
    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(";");
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i].trim();
            if (c.indexOf(name) == 0)
                return c.substring(name.length);
        }
        return "";
    }
    createPix(debug_mode=false)
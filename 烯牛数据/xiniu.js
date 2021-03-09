
hex_md5 = require('js-md5');
var _p = 'W5D80NFZHAYB8EUI2T649RT2MNRMVE2O'
var _keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
function d1(e) {

    var t, n, r, o, i, a, u = "", c = 0;
    for (e = e.replace(/[^A-Za-z0-9\+\/\=]/g, ""); c < e.length;)
        t = _keyStr.indexOf(e.charAt(c++)) << 2 | (o = _keyStr.indexOf(e.charAt(c++))) >> 4,
            n = (15 & o) << 4 | (i = _keyStr.indexOf(e.charAt(c++))) >> 2,
            r = (3 & i) << 6 | (a = _keyStr.indexOf(e.charAt(c++))),
            u += String.fromCharCode(t),
        64 != i && (u += String.fromCharCode(n)),
        64 != a && (u += String.fromCharCode(r));
    return u
}


function _u_d(e) {
    for (var t = "", n = 0, r = 0, o = 0, i = 0; n < e.length; )
        (r = e.charCodeAt(n)) < 128 ? (t += String.fromCharCode(r),
            n++) : r > 191 && r < 224 ? (o = e.charCodeAt(n + 1),
            t += String.fromCharCode((31 & r) << 6 | 63 & o),
            n += 2) : (o = e.charCodeAt(n + 1),
            i = e.charCodeAt(n + 2),
            t += String.fromCharCode((15 & r) << 12 | (63 & o) << 6 | 63 & i),
            n += 3);
    return t
}


function d2(e) {

    for (var t = "", n = 0; n < e.length; n++) {
        var r = _p.charCodeAt(n % _p.length);
        t += String.fromCharCode(e.charCodeAt(n) ^ r)
    }
    return t = _u_d(t)
}



function e1(e) {
    if (null == e)
        return null;
    for (var t, n, r, o, i, a, u, c = "", s = 0; s < e.length; )
        o = (t = e.charCodeAt(s++)) >> 2,
            i = (3 & t) << 4 | (n = e.charCodeAt(s++)) >> 4,
            a = (15 & n) << 2 | (r = e.charCodeAt(s++)) >> 6,
            u = 63 & r,
            isNaN(n) ? a = u = 64 : isNaN(r) && (u = 64),
            c = c + _keyStr.charAt(o) + _keyStr.charAt(i) + _keyStr.charAt(a) + _keyStr.charAt(u);
    return c
}

function _u_e(e) {
    if (null == e)
        return null;
    e = e.replace(/\r\n/g, "\n");
    for (var t = "", n = 0; n < e.length; n++) {
        var r = e.charCodeAt(n);
        r < 128 ? t += String.fromCharCode(r) : r > 127 && r < 2048 ? (t += String.fromCharCode(r >> 6 | 192),
            t += String.fromCharCode(63 & r | 128)) : (t += String.fromCharCode(r >> 12 | 224),
            t += String.fromCharCode(r >> 6 & 63 | 128),
            t += String.fromCharCode(63 & r | 128))
    }
    return t
}

function e2(e) {
    if (null == (e = _u_e(e)))
        return null;
    for (var t = "", n = 0; n < e.length; n++) {
        var r = _p.charCodeAt(n % _p.length);
        t += String.fromCharCode(e.charCodeAt(n) ^ r)
    }
    return t
}


function get_request_payload(n){
    s = JSON.stringify(n)
    l= JSON.parse(s)
    payload = e1(e2(JSON.stringify(l.payload)))
    sig= hex_md5(payload + _p).toUpperCase()
    // console.log(payload)
    // console.log(sign)
    return JSON.stringify({"payload":payload,"sig":sig,"v":1})
}


function get_data(l){
    var s = d1(l)
    var res = d2(s)
    return res

}
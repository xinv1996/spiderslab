const askHDw8mF41d = "aJaGd9AxaaOJO3DG";
const asi20yNEfu4y = "bAgWzf8AWlcaWS3t";
const acknj6RCuLB8 = "dw9o4pWsWXTmMjWR";
const aciyPZ4GpjAT = "fpMoeT9tApkTf4lT";
const dskaBsDilVyZ = "hiSXkIRtNR4eGTA8";
const dsijCfADZ8ye = "xGWEpt9Vb27luOpy";
const dck5HQVoSFpK = "o0AMV4QDYQJ8DeMM";
const dciT38OZnJvK = "pPxAQCAndL5CKqU1";
const aes_local_key = 'emhlbnFpcGFsbWtleQ==';
const aes_local_iv = 'emhlbnFpcGFsbWl2';
var BASE64 = {
    encrypt: function (text) {
        var b = new Base64();
        return b.encode(text)
    }, decrypt: function (text) {
        var b = new Base64();
        return b.decode(text)
    }
};
var DES = {
    encrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.DES.encrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString()
    }, decrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.DES.decrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString(CryptoJS.enc.Utf8)
    }
};
var AES = {
    encrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.AES.encrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString()
    }, decrypt: function (text, key, iv) {
        var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
        var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
        secretkey = CryptoJS.enc.Utf8.parse(secretkey);
        secretiv = CryptoJS.enc.Utf8.parse(secretiv);
        var result = CryptoJS.AES.decrypt(text, secretkey, {
            iv: secretiv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
        return result.toString(CryptoJS.enc.Utf8)
    }
};
var localStorageUtil = {
    save: function (name, value) {
        var text = JSON.stringify(value);
        text = BASE64.encrypt(text);
        text = AES.encrypt(text, aes_local_key, aes_local_iv);
        try {
            localStorage.setItem(name, text)
        } catch (oException) {
            if (oException.name === 'QuotaExceededError') {
                console.log('Local limit exceeded');
                localStorage.clear();
                localStorage.setItem(name, text)
            }
        }
    }, check: function (name) {
        return localStorage.getItem(name)
    }, getValue: function (name) {
        var text = localStorage.getItem(name);
        var result = null;
        if (text) {
            text = AES.decrypt(text, aes_local_key, aes_local_iv);
            text = BASE64.decrypt(text);
            result = JSON.parse(text)
        }
        return result
    }, remove: function (name) {
        localStorage.removeItem(name)
    }
};

function dHDaJ2hgyGU(pSilpKc) {
    pSilpKc = DES.decrypt(pSilpKc, dskaBsDilVyZ, dsijCfADZ8ye);
    return pSilpKc
}

function d0kFOTD0Os(pSilpKc) {
    pSilpKc = BASE64.decrypt(pSilpKc);
    return pSilpKc
}

function g1D2UMKzcFrrFfIr(key, period) {
    if (typeof period === 'undefined') {
        period = 0
    }
    var d = DES.encrypt(key);
    d = BASE64.encrypt(key);
    var data = localStorageUtil.getValue(key);
    if (data) {
        const time = data.time;
        const current = new Date().getTime();
        if (new Date().getHours() >= 0 && new Date().getHours() < 5 && period > 1) {
            period = 1
        }
        if (current - (period * 60 * 60 * 1000) > time) {
            data = null
        }
        if (new Date().getHours() >= 5 && new Date(time).getDate() !== new Date().getDate() && period === 24) {
            data = null
        }
    }
    return data
}

function osVxudaUdL(obj) {
    var newObject = {};
    Object.keys(obj).sort().map(function (key) {
        newObject[key] = obj[key]
    });
    return newObject
}

function da5OTZI4JcF(data) {
    data = BASE64.decrypt(data);
    data = DES.decrypt(data, dskaBsDilVyZ, dsijCfADZ8ye);
    data = AES.decrypt(data, askHDw8mF41d, asi20yNEfu4y);
    data = BASE64.decrypt(data);
    return data
}

var pGKLynWgZ = (function () {
    function osVxudaUdL(obj) {
        var newObject = {};
        Object.keys(obj).sort().map(function (key) {
            newObject[key] = obj[key]
        });
        return newObject
    }

    return function (mJfvsEJUH, oWa6Lc) {
        var aQrT = '9d1da400c676a69d5619868a961b3f03';
        var cynGN = 'WEB';
        var tWymzKh = new Date().getTime();
        var pSilpKc = {
            appId: aQrT,
            method: mJfvsEJUH,
            timestamp: tWymzKh,
            clienttype: cynGN,
            object: oWa6Lc,
            secret: hex_md5(aQrT + mJfvsEJUH + tWymzKh + cynGN + JSON.stringify(osVxudaUdL(oWa6Lc)))
        };
        pSilpKc = BASE64.encrypt(JSON.stringify(pSilpKc));
        return pSilpKc
    }
})();

function s3Z3vKhoUnjJodHGwK(mJfvsEJUH, oHne8wNStZ, cOwu0CGVc, p8kkWL3) {
    const kYMZ = hex_md5(mJfvsEJUH + JSON.stringify(oHne8wNStZ));
    const dK4fR = g1D2UMKzcFrrFfIr(kYMZ, p8kkWL3);
    if (!dK4fR) {
        var pSilpKc = pGKLynWgZ(mJfvsEJUH, oHne8wNStZ);
        $.ajax({
            url: 'api/historyapi.php', data: {hXcshIDLp: pSilpKc}, type: "post", success: function (dK4fR) {
                dK4fR = da5OTZI4JcF(dK4fR);
                oWa6Lc = JSON.parse(dK4fR);
                if (oWa6Lc.success) {
                    if (p8kkWL3 > 0) {
                        oWa6Lc.result.time = new Date().getTime();
                        localStorageUtil.save(kYMZ, oWa6Lc.result)
                    }
                    cOwu0CGVc(oWa6Lc.result)
                } else {
                    console.log(oWa6Lc.errcode, oWa6Lc.errmsg)
                }
            }
        })
    } else {
        cOwu0CGVc(dK4fR)
    }
}
const  askH3G2f8hoq = "aJoQtX23yozrU3lC";//AESkey，可自定义
const  asiI0QI5rULO = "bCHVjx8NioaVDasQ";//密钥偏移量IV，可自定义
const  ackgvCsBCbUz = "dVBr2f9OdFEWJuvr";//AESkey，可自定义
const  aciivmnCJjop = "ffxSh6rArNJMRu9c";//密钥偏移量IV，可自定义
const  dskW8VQd4hi2 = "hfROFWOYOfqNDpLe";//DESkey，可自定义
const  dsiQIHQX3fBz = "xmWA34EVWHFgaoZk";//密钥偏移量IV，可自定义
const  dckeCHDjiP3k = "oWSh3LPWpfM4S9up";//DESkey，可自定义
const  dcicbgjuN9xM = "p6ks8Spt5G8mtRFX";//密钥偏移量IV，可自定义
const aes_local_key = 'emhlbnFpcGFsbWtleQ==';
const aes_local_iv = 'emhlbnFpcGFsbWl2';
var BASE64 = {
    encrypt: function(text) {
        var b = new Base64();
        return b.encode(text);
    },
    decrypt: function(text) {
        var b = new Base64();
        return b.decode(text);
    }
};

var DES = {
 encrypt: function(text, key, iv){
    var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.DES.encrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString();
 },
 decrypt: function(text, key, iv){
    var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.DES.decrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString(CryptoJS.enc.Utf8);
  }
};

var AES = {
  encrypt: function(text, key, iv) {
    var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
    // console.log('real key:', secretkey);
    // console.log('real iv:', secretiv);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.AES.encrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString();
  },
  decrypt: function(text, key, iv) {
    var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.AES.decrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString(CryptoJS.enc.Utf8);
  }
};

var localStorageUtil = {
  save: function(name, value) {
    var text = JSON.stringify(value);
    text = BASE64.encrypt(text);
    text = AES.encrypt(text, aes_local_key, aes_local_iv);
    try {
      localStorage.setItem(name, text);
    } catch (oException) {
      if (oException.name === 'QuotaExceededError') {
        console.log('Local limit exceeded');
        localStorage.clear();
        localStorage.setItem(name, text);
      }
    }
  },
  check: function(name) {
    return localStorage.getItem(name);
  },
  getValue: function(name) {
    var text = localStorage.getItem(name);
    var result = null;
    if (text) {
      text = AES.decrypt(text, aes_local_key, aes_local_iv);
      text = BASE64.decrypt(text);
      result = JSON.parse(text);
    }
    return result;
  },
  remove: function(name) {
    localStorage.removeItem(name);
  }
};

// console.log('base64', BASE64.encrypt('key'));

function dOz9ddS2f9j(p3p1lY7) {
  p3p1lY7 = DES.decrypt(p3p1lY7, dskW8VQd4hi2, dsiQIHQX3fBz);
  return p3p1lY7;
}

function dlj93SrB6V(p3p1lY7) {
  p3p1lY7 = AES.decrypt(p3p1lY7, askH3G2f8hoq, asiI0QI5rULO);
  return p3p1lY7;
}

function gSdoB01Y9Tg2Fike(key, period) {
    if (typeof period === 'undefined') {
        period = 0;
    }
    var d = DES.encrypt(key);
    d = BASE64.encrypt(key);
    var data = localStorageUtil.getValue(key);
    if (data) { // 判断是否过期
        const time = data.time;
        const current = new Date().getTime();
        if (new Date().getHours() >= 0 && new Date().getHours() < 5 && period > 1) {
            period = 1;
        }
        if (current - (period * 60 * 60 * 1000) > time) { // 更新
           data = null;
        }
        // 防止1-5点用户不打开页面，跨天的情况
        if (new Date().getHours() >= 5 && new Date(time).getDate() !== new Date().getDate() && period === 24) {
           data = null;
        }
    }
    return data;
}

function osKNak2xR5(obj) {
    var newObject = {};
    Object.keys(obj).sort().map(function(key){
      newObject[key] = obj[key];
    });
    return newObject;
}
function dWeakEZ9h6J6(data) {
    data = BASE64.decrypt(data);
    data = DES.decrypt(data, dskW8VQd4hi2, dsiQIHQX3fBz);
    data = AES.decrypt(data, askH3G2f8hoq, asiI0QI5rULO);
    data = BASE64.decrypt(data);
    return data;
}
var pCvG1DPhnVpa = (function(){

function osKNak2xR5(obj){
    var newObject = {};
    Object.keys(obj).sort().map(function(key){
        newObject[key] = obj[key];
    });
    return newObject;
}
return function(mgp9V1Jf1, oabuwM){
    var aQ5W = '5c4c8f09422523121332ea6c36f5c5dd';
    var cJZC0 = 'WEB';
    var tT0iESD = new Date().getTime();

    var p3p1lY7 = {
      appId: aQ5W,
      method: mgp9V1Jf1,
      timestamp: tT0iESD,
      clienttype: cJZC0,
      object: oabuwM,
      secret: hex_md5(aQ5W + mgp9V1Jf1 + tT0iESD + cJZC0 + JSON.stringify(osKNak2xR5(oabuwM)))
    };
    p3p1lY7 = BASE64.encrypt(JSON.stringify(p3p1lY7));
    p3p1lY7 = DES.encrypt(p3p1lY7, dckeCHDjiP3k, dcicbgjuN9xM);
    return p3p1lY7;
};
})();

function s0y5uzoESwq4Y9u3xBXh(mgp9V1Jf1, o08eB72bkL, ccysruM6B, pQvrWht) {
    const kwzz = hex_md5(mgp9V1Jf1 + JSON.stringify(o08eB72bkL));

    const d50fq = gSdoB01Y9Tg2Fike(kwzz, pQvrWht);
    if (!d50fq) {
        var p3p1lY7 = pCvG1DPhnVpa(mgp9V1Jf1, o08eB72bkL);
        $.ajax({
            url: 'api/historyapi.php',
            data: { hEGCupyyO: p3p1lY7 },
            type: "post",
            success: function (d50fq) {
                d50fq = dWeakEZ9h6J6(d50fq);
                oabuwM = JSON.parse(d50fq);
                if (oabuwM.success) {
                    if (pQvrWht > 0) {
                      oabuwM.result.time = new Date().getTime();
                      localStorageUtil.save(kwzz, oabuwM.result);
                    }
                    ccysruM6B(oabuwM.result);
                } else {
                    console.log(oabuwM.errcode, oabuwM.errmsg);
                }
            }
        });
    } else {
        ccysruM6B(d50fq);
    }
}

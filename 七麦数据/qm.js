function o() {
    return unescape("861831832863830866861836861862839831831839862863839830865834861863837837830830837839836861835833".replace(/8/g, "%u00"))
}
function i() {
    var e = "";
    return ["66", "72", "6f", "6d", "43", "68", "61", "72", "43", "6f", "64", "65"].forEach(function(t) {
        e += unescape("%u00" + t)
    }),
        e
}
function r(e) {
    var t = i();
    return String[t](e)
}

function f(e, t) {
    t || (t = o()),
    e = e.split("");
    var array=new Array(e.length)

    for (var n = e.length, a = t.length, i = "charCodeAt", s = 0; s < n; s++)
        array[s]=  r(e[s][i](0) ^ t[(s + 10) % a][i](0))
    return array.join("");

}

function get_data(s1){
    s2 = '00000008d78d46a'
    return f(s1,s2)
}



var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

const eA = function(sel) {
    return document.querySelectorAll(sel)
}

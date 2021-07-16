let buttonToggle = function(node) {

    addOrRemove = 'add'
    if (node.classList.contains('saved')) {
        addOrRemove = 'remov'
    }

    let semaClass = `to-be-${addOrRemove}ed`
    let buttonSelector = `.${addOrRemove}-button`
    let selectedSemas = eA(`.${semaClass}`)
    let button = e(buttonSelector)
    if (node.classList.contains(semaClass)) {
        node.classList.remove(semaClass)
    } else {
        node.classList.add(semaClass)
    }
    selectedSemas = eA(`.${semaClass}`)
    if (selectedSemas.length > 0) {
        button.hidden = false
    } else {
        button.hidden = true
    }
}

// let semaSelectToggle = function(addOrRemove) {
//     let semaClass = `.to-be-${addOrRemove}ed`
//     let selectedSemas = eA(semaClass)
//     if (selectedSemas.length > 0) {
//         button.hidden = false
//     } else {
//         button.hidden = true
//     }
// }

let bindSemaEntries = function() {
    let semasList = eA('.sema')
    for (let sema of semasList) {
        sema.addEventListener('click', function(){
            buttonToggle(sema)
        })
    }
}


let bindFloatButton = function(addOrRemove) {
    let semaClass = `to-be-${addOrRemove}ed`
    let buttonSelector = `.${addOrRemove}-button`
    let button = e(buttonSelector)
    button.addEventListener('click', function(){
        let selected = eA(`.${semaClass}`)
        let selectedList = []
        for (i of selected) {
            selectedList.push(i.dataset.semaId)
        }
        form = selectedList
        ajax('POST', `/api/memo/${addOrRemove}`, form, function() {
            loadAndMarkSavedMemos()
        })
        for (i of selected) {
            i.classList.remove(semaClass)
            button.hidden = true
        }
    })
}


let loadAndMarkSavedMemos = function() {
    let semas = eA('.sema')
    ajax('GET', '/api/memo/load', '', function(r){
        let memos = JSON.parse(r)
        for (let sema of semas) {
            semaId = sema.dataset.semaId
            if (memos.includes(semaId)) {
                sema.classList.add('saved')
            } else {
                sema.classList.remove('saved')
            }
        }
    })
}


let _main = function() {
    loadAndMarkSavedMemos()
    bindSemaEntries()
    bindFloatButton('add')
    bindFloatButton('remov')
}

_main()
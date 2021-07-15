let semas = eA('.definitions')
let button = e('.float-button')

let sema_template = function(word) {
    title = e('.word-name')
    ajax('GET', '/api/dict/{title}', form, function(){})

}

for (let sema of semas) {
    sema.addEventListener('click', function(event){
        let self = event.target
        if (self.classList.contains('sema')) {
            if (self.classList.contains('selected')) {
                self.classList.remove('selected')
            } else {
                self.classList.add('selected')
            }
        }
        allSelected = eA('.selected')
        if (allSelected.length > 0) {
            button.hidden = false
        } else {
            button.hidden = true
        }
    })
}

button.addEventListener('click', function(event){
    let selected = eA('.selected')
    let selectedList = []
    for (i of selected) {
        selectedList.push(i.dataset.semaId)
    }
    form = selectedList
    ajax('POST', '/api/memo/add', form, function(){})
    for (i of selected) {
        i.classList.remove('selected')
        button.hidden = true
    }
})
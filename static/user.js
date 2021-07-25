// 用来撤销对笔记的修改
let noteContent = {}

// 用于定位折叠栏
const locateCollapseTableRow = function (tr, semaId) {
    let collapseTableRow = tr.nextElementSibling
    if (tr.nextElementSibling === null || tr.nextElementSibling.className != 'card-collapse') {
        const collapseHTML = collapseTemplate(semaId)
        tr.insertAdjacentHTML('afterEnd', collapseHTML)
        collapseTableRow = tr.nextElementSibling
    }
    return collapseTableRow
}

// FIXME 删除折叠栏按钮 ❌ 的事件，删除折叠栏和折叠按钮 
const removeCollapse = function (semaId) {
    const collapseElement = e(`#collapse-${semaId}`)
    const collapseButton = e(`#collapse-button-${semaId}`)
    collapseElement.remove()
    collapseButton.remove()
}

// 详情按钮 🔎 的事件
const cardDetailButtonOnClick = function (semaId) {
    const path = '/api/memo/detail?id=' + semaId
    ajax('GET', path, '', function (r) {
        const detail = JSON.parse(r)
        const td = cardDetailTemplate(detail)
        const tr = e(`#sema-${semaId}`)
        locateCollapseTableRow(tr, semaId).innerHTML = td
    })
}

// 笔记按钮 📝 的事件
const cardNoteButtonOnClick = function (semaId) {
    const path = '/api/memo/note?id=' + semaId
    ajax('GET', path, '', function (r) {
        noteContent[semaId] = r // 保存在全局变量中，用于撤销
        const td = cardNoteTemplate(semaId, r)
        const tr = e(`#sema-${semaId}`)
        locateCollapseTableRow(tr).innerHTML = td
    })
}

// 添加到单词本 🗂️ 按钮的事件
const cardAdd2MemopadButtonOnClick = function (semaId) {
    const tr = e(`#sema-${semaId}`)
    // 找到所有单词本
    const path = '/api/memo/note/get_memopads'
    ajax('GET', path, '', function (r) {
        const data = JSON.parse(r)
        // 找到卡片所属的单词本
        const path2 = '/api/memo/note/get_memopads_of_the_card?id=' + semaId
        ajax('GET', path2, '', function (r) {
            const data2 = JSON.parse(r)
            for (i of data) {
                if (data2.includes(i.id)) {
                    log('ever here')
                    i.isChecked = true
                } else {
                    i.isChecked = false
                }
            }
            const td = add2memopadTemplate(semaId, data)
            locateCollapseTableRow(tr).innerHTML = td
        })
    })
}

// 修改所属单词本的确认按钮的事件
const add2memopadYes = function (semaId) {
    const tr = e(`#sema-${semaId}`)
    const collapseTableRow = tr.nextElementSibling
    const inputBoxes = collapseTableRow.querySelectorAll('input')
    let memoIdDict = {}
    for (i of inputBoxes) {
        if (i.type == 'checkbox') {
            const memoId = i.id.slice(9)
            if (i.checked === true) {
                memoIdDict[memoId] = 1
            } else {
                memoIdDict[memoId] = 0
            }
        }
    }
    const path = '/api/memo/note/add_to_memopad?id=' + semaId
    const form = memoIdDict
    ajax('POST', path, form, function (r) {
        log(r)
    })
    // 刷新单词本栏
    const memopadsTd = tr.querySelector('.memopads')
    const path2 = '/api/memo/note/get_memopad_objects_of_the_card?id=' + semaId
    ajax('GET', path2, '', function (r) {
        const memopads = JSON.parse(r)
        memopadsTd.innerHTML = ''
        generateMemopads(tr, memopads)
    })
}

// 新建单词本按钮的事件
const newMemopadButtonOnclick = function (semaId) {
    const newMemopadInputBox = e(`#newMemopad-${semaId}`)
    const memopadName = newMemopadInputBox.value
    path = '/api/memo/note/new_memopad'
    form = {
        'name': memopadName
    }
    ajax('POST', path, form, function (r) {
        log(r)
        cardAdd2MemopadButtonOnClick(semaId)
    })
}

// 刷新单词本栏
const generateMemopads = function (tr, memopads) {
    for (m of memopads) {
        memopad = memopadTemplate(m)
        tr.getElementsByClassName('memopads')[0].insertAdjacentHTML('afterbegin', memopad)
    }
}

// 卡片的模板
const semaTemplate = function (semaData) {
    let template = document.createElement('template')
    let t = `
            <tr class="sema" id="sema-${semaData.id}">
                <td>${semaData.lemma}</td>
                <td>${semaData.lang}</td>
                <td>${semaData.pos}</td>
                <td>${semaData.content}</td>
                <td class="memopads"></td>
                <td class="clpsed">
                    <button class="btn" onclick="cardDetailButtonOnClick(${semaData.id})">🔎</button>
                    <button class="btn" onclick="cardNoteButtonOnClick(${semaData.id})">📝</button>
                    <button class="btn" onclick="cardAdd2MemopadButtonOnClick(${semaData.id})">🗂️</button>
                </td>
            </tr>
            `
    template.innerHTML = t.trim()
    generateMemopads(template.content.firstElementChild, semaData.memopads)
    return template.content.firstElementChild.outerHTML
}

// 单词本链接按钮的模板
const memopadTemplate = function (data) {
    let t = `<a style="margin-right: 3px; font-size: 0.5em" class="btn btn-link btn-sm" href="/memopad/${data.id}">${data.name}</a>`
    return t
}

// 卡片详情的模板
const cardDetailTemplate = function (semaData) {
    t = `<td class="card-detail" colspan="6">
            <div>
                词形：${semaData.text}
                <br>
                词源：${semaData.etym}
                <br>
                发音：${semaData.prnn}
                <br>
            </div>
        </td>`
    return t
}

// 编辑笔记的模板
const cardNoteTemplate = function (semaId, note) {
    t = `<td class="card-note" colspan="6">
            <div class="form-floating">
                <textarea id="note-${semaId}" class="form-control">${note}</textarea>
                <button onClick="cancelButtonOnClick(${semaId})" class="note-cancel">↩️</button>
                <button onClick="saveButtonOnClick(${semaId})" class="note-save">💾</button>
                <label for="floatingTextarea">添加或修改笔记</label>
            </div>
        </td>`
    return t
}

// 保存笔记按钮 💾 的事件
const saveButtonOnClick = function (semaId) {
    let noteTextarea = e(`#note-${semaId}`)
    form = { 'sema_id': semaId, 'note': noteTextarea.value }
    tr = e('.form-floating')
    ajax('POST', '/api/memo/note/save', form, function (r) {
        log(r)
        noteContent[semaId] = noteTextarea.value
    })
    
}

// 撤销笔记编辑按钮 ↩️ 的事件
const cancelButtonOnClick = function (semaId) {
    let noteTextarea = e(`#note-${semaId}`)
    noteTextarea.value = noteContent[semaId]
}

// 添加到单词本界面中的单词本按钮模板
const memopadButtonTemplate = function (data) {
    let t = `<label class="btn btn-default">
                <input id="checkbox-${data.id}" type="checkbox">${data.name}
            </label>`
    if (data.isChecked === true) {
        t = `<label class="btn btn-default">
                <input id="checkbox-${data.id}" type="checkbox" checked>${data.name}
            </label>`
    }
    return t
}

// 添加到单词本的模板
const add2memopadTemplate = function (semaId, data) {
    let template = document.createElement('template')
    let t = `
    <td class="card-note" colspan="6">
        <div class="btn-group" data-toggle="buttons">
        </div>
        <button class="btn btn-sm" onClick="add2memopadYes(${semaId})">💾</button>
        <div class="input-group">
            <input id="newMemopad-${semaId}" type="text" class="form-control" placeholder="新建单词本" aria-label="新建单词本" aria-describedby="button-addon2">
            <button onclick="newMemopadButtonOnclick(${semaId})" class="btn btn-outline-secondary" type="button" id="button-addon2">确定</button>
        </div>
    </td>
    `
    template.innerHTML = t
    for (d of data) {
        btn = memopadButtonTemplate(d)
        template.content.firstElementChild.firstElementChild.insertAdjacentHTML('afterBegin', btn)
    }
    return template.content.firstElementChild.outerHTML
}

// 折叠栏的模板
const collapseTemplate = function (semaId) {
    t = `<tr id="collapse-${semaId}" class="card-collapse">
        </tr>`
    return t
}

// 加载单词数据
const loadSemas = function () {
    tbody = e('tbody')
    form = { 'quantity': 10 }
    ajax('POST', '/api/memo/load_some', form, function (r) {
        let semas = JSON.parse(r)
        for (sema of semas) {
            semaCell = semaTemplate(sema)
            tbody.insertAdjacentHTML('beforeend', semaCell)
        }
    })
}

let _main = function () {
    loadSemas()
}

_main()
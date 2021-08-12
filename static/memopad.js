easinessCode = {
    'easy': 5,
    'good': 4,
    'hard': 3,
    'again': 0,
}

const bindShowAnswerButton = function () {
    const showAnswerButton = e('.btn-show-answer')
    showAnswerButton.addEventListener('click', function () {
        const showAnswerForm = e('.show-answer-form')
        showAnswerForm.hidden = true
        const cardBackSide = e('.card-back-side')
        cardBackSide.hidden = false
        const choiceForm = e('.choice-form')
        choiceForm.hidden = false
    })
}

const bindChoiceButton = function () {
    const choiceForm = e('.choice-form')
    choiceForm.addEventListener('click', function (event) {
        const clicked = event.target
        if (clicked.classList.contains('btn-easiness')) {
            const cardNode = e('.card-main')
            const card_id = cardNode.id
            const easiness = clicked.id.slice(4)
            form = {
                'card_id': card_id.slice(5),
                'easiness': easinessCode[easiness],
            }
            path = '/api/memo/review'
            ajax('POST', path, form, function (r) {
                log(r)
                loadCard()
            })
            const showAnswerForm = e('.show-answer-form')
            showAnswerForm.hidden = false
            const cardBackSide = e('.card-back-side')
            cardBackSide.hidden = true
            const choiceForm = e('.choice-form')
            choiceForm.hidden = true
        }
    })
}

const templateReviewDone = function () {
    t = `<div class="alert alert-success" role="alert">
        <h4 class="alert-heading">Well done!</h4>
        <hr>
        <p class="mb-0">您已完成了这个单词本的复习！</p>
        </div>`
    return t
}

const loadCard = function () {
    const memo_id = e('.memopad-main').id.slice(8)
    const path = '/api/memo/cards_to_review?id=' + memo_id
    ajax('GET', path, '', function (r) {
        const cardNode = e('.card-main')
        if (r == 'review done!') {
            cardNode.innerHTML = templateReviewDone()
        } else {
            const card = JSON.parse(r)
            const lemmaNode = e('.card-lemma')
            const detailNode = e('.card-detail')
            const cardBackNode = e('.card-back')
            cardNode.id = 'card-' + card.id
            lemmaNode.innerText = card.lemma
            detailNode.innerText = card.lang + ' | ' + card.pos
            cardBackNode.innerHTML = `<p>${card.content}</p><p>${card.note}</p>`
        }
    })
}

const _main = function () {
    bindShowAnswerButton()
    loadCard()
    bindChoiceButton()
}

_main()
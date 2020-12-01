const $msgArea = $('#msg-area');
const $scoredWords = $('#scored-words');

const scoredWordsSet = new Set();

$('body').on('submit', '#word-form', async function(evt){
    evt.preventDefault();

    const word = $('#word').val();
    
    const response = await axios.get('/guess', {params: {word: word}});

    $('#word-form').trigger('reset');
    
    wordResponse(response.data);
    checkScoredWords(response.data);
});

function wordResponse(response){
    $msgArea.empty();
    const markup = `<p>Your entry, <em>${response.word}</em>, is <strong>${response.message}</strong></p>`;
    $msgArea.append(markup);
    $msgArea.show();
}

function checkScoredWords(response){
    if (response.message === 'a valid response'){
        if (scoredWordsSet.has(response.word)){
            alert(`You already guessed ${response.word}. Make another guess.`);
        }
        else {
            scoredWordsSet.add(response.word);
            scoredWords(response);
        }
    }
}

function scoredWords(response){
    const markup = `<li><em>${response.word}</em> - ${response.word.length} points</li>`;
    $scoredWords.children('ul').append(markup)
    $scoredWords.show()
}


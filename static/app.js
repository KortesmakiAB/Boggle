const $msgArea = $('#msg-area');
const $scoredWords = $('#scored-words');

const scoredWordsSet = new Set();
let score = 0;

// 2.75 hours spent trying to get setTimeout to remove <form> event listener. 1 second spent removing <form> from DOM. sigh.
$(document).ready(async function(){    
    if (window.location.href.includes("/game-board")){
        setTimeout(async function (){
            alert("Time's up!");                  
            // $('body').off('submit', '#word-form', wordForm);
            handleGameEnd(score);
        }, 60*1000);
    }
});

async function handleGameEnd(score){
    $('#word-form').remove();
    $msgArea.remove();
    const resp = await axios.post('/play-again', {score: score});
    addPlayAgainButton();
}

function addPlayAgainButton(){
    const markup = `
        <form action="/game-board">
            <button>Play Again</button>
        </form>`;
    $('#play-again-div').append(markup);
    $('#play-again-div').show();
}


$('body').on('submit', '#word-form', wordForm);

async function wordForm(evt){
    evt.preventDefault();

    const word = $('#word').val();
    
    const response = await axios.get('/guess', {params: {word: word}});

    $('#word-form').trigger('reset');
    
    wordResponse(response.data);
    checkScoredWords(response.data);
};

function wordResponse(response){
    $msgArea.empty();
    const markup = `<p>Your entry: <em>${response.word}</em>, is <strong>${response.message}</strong></p>`;
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
            displayScoredWords(response);
        }
    }
}

function displayScoredWords(response){
    const markup = `<li><em>${response.word}</em> - ${response.word.length} points</li>`;
    $scoredWords.children('ul').append(markup);
    updateScore(response);
    // $scoredWords.show();
}

function updateScore(response){
    score += response.word.length;
    const text = `Current Score: ${score}`;
    $scoredWords.children('h4').text(text);
}
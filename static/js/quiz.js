console.log('hello world quiz')
const url = window.location.href

const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')


let timer; // Variable to hold the interval ID of the timer
let timerState = false; // Variable to track the state of the timer
let requiredTime // Time to be taken to complete the quiz
let minutes 
let seconds
let completionTime // Time user took to complete the quiz

// Quiz timer and also sends data to backend when timer reaches zero
const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else { 
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    minutes = time - 1
    seconds = 60
    let displaySeconds
    let displayMinutes

    timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time over')
                sendData()
            }, 500)
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)

    timerState = true;
}

// get quizzes and answers
$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        const data = response.data
        data.forEach(el => {
            for (const [question, answers] of Object.entries(el)){
                quizBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
                answers.forEach(answer=>{
                    quizBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                            <label for="${question}">${answer}</label>
                        </div>
                    `
                })
            }
        });
        requiredTime = response.time
        activateTimer(requiredTime)
        
    },
    error: function(error){
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// sends a POST request returns scores and completion time
// Display questions with their right answers and wrong answers chosen by user
const sendData = () => {
    const minutesTaken = requiredTime - minutes - 1; // Subtract 1 to account for the final minute
    const secondsTaken = 60 - seconds;
    console.log(`${minutesTaken}:${secondsTaken}`)
    completionTime = (minutesTaken + secondsTaken/60).toFixed(2)
    console.log(completionTime)

    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    data['completionTime'] = completionTime
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })
    

    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){

            const results = response.results
            console.log(results)
            quizForm.classList.add('d-none')

            scoreBox.innerHTML = `${response.passed ? 'Congratulations! ' : 'Ups..:( '}Your result is ${response.score.toFixed(2)}%`

            results.forEach(res=>{
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)){

                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'text-light', 'h6']
                    resDiv.classList.add(...cls)

                    if (resp=='not answered') {
                        resDiv.innerHTML += '- not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']

                        if (answer == correct) {
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += ` answered: ${answer}`
                        } else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += ` | correct answer: ${correct}`
                            resDiv.innerHTML += ` | answered: ${answer}`
                        }
                    }
                }
                resultBox.append(resDiv)
            })
            
        },

        error: function(error){
            console.log(error)
        }
    })
}

// call the sendData() function when the form is being submitted
quizForm.addEventListener('submit', e=>{
    e.preventDefault()
    if (timerState) {
        clearInterval(timer); // Stop the timer
        timerState = false; // Set the timer state to inactive
    }
    sendData();
    
})



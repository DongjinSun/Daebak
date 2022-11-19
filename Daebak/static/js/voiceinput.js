
window.SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

// 인스턴스 생성
const recognition = new SpeechRecognition();

// 음절을 연속적으로 인식
recognition.interimResults = true;

recognition.lang = "ko-KR";

// true means continuous, and false means not continuous (single result each time.)
// true면 음성 인식이 안 끝나고 계속 됩니다.
recognition.continuous = false;
// 숫자가 작을수록 발음대로 적고, 크면 문장의 적합도에 따라 알맞은 단어로 대체합니다.
// maxAlternatives가 크면 이상한 단어도 문장에 적합하게 알아서 수정합니다.
recognition.maxAlternatives = 10000;

let p = document.createElement("p");
p.classList.add("para");

let words = document.querySelector(".words");
words.appendChild(p);

let speechToText = "";
recognition.addEventListener("result", (e) => {
  let interimTranscript = "";
  for (let i = e.resultIndex, len = e.results.length; i < len; i++) {
    let transcript = e.results[i][0].transcript;
    console.log(transcript);
    if (e.results[i].isFinal) {
      speechToText += transcript;
    } else {
      interimTranscript += transcript;
    }
  }
  document.querySelector(".para").innerHTML = speechToText + interimTranscript;
});

/*
var form = document.getElementById("voiceform")
var hiddenField = document.createElement("input");
hiddenField.setAttribute("type", "hidden");
hiddenField.setAttribute("name", "voicesubmit");
var inputtext = document.getElementsByClassName('para')[0].innerText;
hiddenField.setAttribute("value", inputtext);
form.appendChild(hiddenField);
*/

// 음성인식이 끝나면 자동으로 재시작합니다.
// recognition.addEventListener("end", recognition.start);

// 음성 인식 시작
function voiceinput(){
  recognition.start();
  
}

// 음성 인식 중지
function voicestop(){
  recognition.stop();
  var form = document.getElementById("voiceform")
  var hiddenField = document.createElement("input");
  hiddenField.setAttribute("type", "hidden");
  hiddenField.setAttribute("name", "voicesubmit");
  var inputtext = document.getElementsByClassName('para')[0].innerText;
  hiddenField.setAttribute("value", inputtext);
  form.appendChild(hiddenField);
}

function submitvoice(){
  var voice = document.getElementsByName('voicesubmit')[0];
  var voicesubmit =voice.value;
  $('input[name=voicesubmit]').attr('value',voicesubmit);
}

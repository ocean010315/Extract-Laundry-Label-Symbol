var submitButton = document.getElementById('submitButton');
submitButton.onclick = showImage;     //Submit 버튼 클릭시 이미지 보여주기

function showImage() {
  
    
    document.getElementById('loading-container').style.visibility = 'visible';

    document.getElementById('fileName').textContent = null;     //기존 파일 이름 지우기
}


function loadFile(input) {
    var file = input.files[0];

    var name = document.getElementById('fileName');
    name.textContent = "C:/CV2/img/" + file.name;

    var newImage = document.createElement("img");
    newImage.setAttribute("class", 'img');

    newImage.src = URL.createObjectURL(file);   

    newImage.style.width = "70%";
    newImage.style.height = "70%";
    newImage.style.visibility = "hidden";   //버튼을 누르기 전까지는 이미지 숨기기
    newImage.style.objectFit = "contain";
  
};
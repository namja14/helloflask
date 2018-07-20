function check() {
    if(document.frml.name.value == ""){
        alert("이름을 꼭 입력해주세요!");
        document.frml.name.focus();
    } else if(document.frml.subject.value == "") {
        alert("제목을 꼭 입력해주세요!");
        document.frml.subject.focus();
    } else if(document.frml.content.value == "") {
        alert("내용을 꼭 입력해주세요!");
        document.frml.content.focus();
    }
    else{
        document.frml.submit() //저농해줌
    }
}


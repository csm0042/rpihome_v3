function myAjax() {
    $.ajax({
        type: "POST",
        url: 'php/get_status.php',
        data: {name:'call_this', }
    }
}
function myAjax() {
    $.ajax({
        type: "POST",
        url: 'php/get_status.php',
        data: {name:'call_this', }
    })
}


<script>
    function get_device_status(name) {
        $.post("php/get_status.php",
        {
            device: name,
        },
        function(device,status) {
            alert("Device: " + device + "\nStatus: " + status);
        });
    }
</script>
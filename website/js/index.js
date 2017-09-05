// Plays a sound file 
function playSound(sound) {
    var snd = new Audio(sound);
    snd.play()
    return true;
}


// Toggles visibility state of device command buttons
function toggleDeviceState(id, sound) {
    playSound(sound)
    // Check if device is already "on"
    if (document.getElementById(id).style.background != "rgb(33, 193, 23)") {
        // Set device to on if not
        document.getElementById(id).style.background = "rgb(33, 193, 23)"
        setState(id, 'on');
    } else {
        // If device was on, toggle state to off
        document.getElementById(id).style.background = "rgb(192, 192, 192)"
        setState(id, 'off');
    }
}


// Ajax call to a PHP script on server which sets device state commands in a database
function setState(id, state) {
    var id_sep = id.split("-")
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById(id).style.innerHTML = this.responseText;
        }
    };
    var url = "php/set_state.php?";
    var data = "devname=" + id_sep[0] + "&devcmd=" + state;
    xhttp.open("POST", url + data, true);
    xhttp.send();
}


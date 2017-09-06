// Plays a sound file 
function playSound(sound) {
    var snd = new Audio(sound);
    snd.play()
    return true;
}


// Toggles visibility state of device command buttons
function toggleDeviceState(id, sound) {
    // Check if device is already "on"
    if (document.getElementById(id).style.background != "rgb(33, 193, 23)") {
        // Set device to on if not
        setState(id, 'on');
        playSound(sound);
    } else {
        // If device was on, toggle state to off
        setState(id, 'off');
        playSound(sound);
    }
}


// Home screen refresh
function homeScreenRefresh(sound) {
    getState('fylt1-toggle');
    getState('fylt2-toggle');
    getState('cclt1-toggle');
    getState('ewlt1-toggle');
    getState('lrlt1-toggle');
    getState('lrlt2-toggle');
    getState('drlt1-toggle');
    getState('bylt1-toggle');
    getState('br1lt1-toggle');
    getState('br1lt2-toggle');
    getState('br2lt1-toggle');
    getState('br2lt2-toggle');
    getState('br3lt1-toggle');
    getState('br3lt2-toggle');
    playSound(sound);
}


// Ajax call to a PHP script on server which sets device state commands in a database
function setState(id, state) {
    var id_sep = id.split("-");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Search result for keywords

            if (this.responseText.search(/on/i) != -1 || this.responseText == '1') {
                document.getElementById(id).style.background = "rgb(33, 193, 23)";
            };

            if ((this.responseText.search(/off/i) != -1 && this.responseText.search(/offline/i) == -1) || this.responseText.search(/0/i) != -1) {
                document.getElementById(id).style.background = "rgb(192, 192, 192)";
            };

            if (this.responseText.search(/offline/i) != -1 || this.responseText.search(/error/i) != -1) {
                document.getElementById(id).style.background = "rgb(255, 0, 0)";
            };
        }
    };
    var url = "php/set_state.php?";
    xhttp.open("POST", url, true); 
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("devname=" + id_sep[0] + "&devcmd=" + state);
}


// Ajax call to a PHP script on server to get current device state from database
function getState(id) {
    var id_sep = id.split("-");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Search result for keywords

            if (this.responseText.search(/on/i) != -1 || this.responseText == '1') {
                document.getElementById(id).style.background = "rgb(33, 193, 23)";
            };

            if ((this.responseText.search(/off/i) != -1 && this.responseText.search(/offline/i) == -1) || this.responseText.search(/0/i) != -1) {
                document.getElementById(id).style.background = "rgb(192, 192, 192)";
            };

            if (this.responseText.search(/offline/i) != -1 || this.responseText.search(/error/i) != -1) {
                document.getElementById(id).style.background = "rgb(255, 0, 0)";
            };
        }
    };
    var url = "php/get_state.php?";   
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("devname=" + id_sep[0]);    
}

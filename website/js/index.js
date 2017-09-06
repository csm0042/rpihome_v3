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
    systemClock('datetime');
    playSound(sound);
}


// System Date and Time
function systemClock(id) {
    setInterval(function() {
    var d = new Date();
    // get named day
    var day;
    switch (d.getDay()) {
        case 0:
            day = "Sunday";
            break;
        case 1:
            day = "Monday";
            break;
        case 2:
            day = "Tuesday";
            break;
        case 3:
            day = "Wednesday";
            break;
        case 4:
            day = "Thursday";
            break;
        case 5:
            day = "Friday";
            break;
        case 6:
            day = "Saturday";
    };
    // get named month
    var month;
    switch (d.getMonth()) {
        case 0:
            month = "January";
            break;
        case 1:
            month = "February";
            break;
        case 2:
            month = "March";
            break;
        case 3:
            month = "April";
            break;
        case 4:
            month = "May";
            break;
        case 5:
            month = "June";
            break;
        case 6:
            month = "July";
            break;
        case 7:
            month = "August";
            break;
        case 8:
            month = "September";
            break;
        case 9:
            month = "October";
            break;
        case 10:
            month = "November";
            break;
        case 11:
            month = "December";
            break;           
    };

    var date = d.getDate();
    var year = d.getFullYear();
    var hour = d.getHours();
    var ampm = "AM"
    if (hour > 12) {
        hour = hour - 12
        ampm = "PM"
    }
    var minute = d.getMinutes();
    minute = minute.toString();
    if (minute.length == 1) {
        minute = '0' + minute
    }

    var second = d.getSeconds();
    second = second.toString();
    if (second.length == 1) {
        second = '0' + second
    }

    document.getElementById(id).innerHTML = hour + ':' + minute + ':' + second + ' ' + ampm + ' - ' + day + '  ' + month + ' ' + date + ', ' + year;

}, 1000);
}


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

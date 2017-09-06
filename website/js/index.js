// MENU TOGGLE
function toggleMenu(id) {
    if (document.getElementById(id).className == "fa fa-bars") {
        document.getElementById(id).className = "fa fa-remove"
    } else {
        document.getElementById(id).className = "fa fa-bars"
    }
}


// Plays a sound file 
function playSound(sound) {
    var snd = new Audio(sound);
    snd.play()
    return true;
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
    systemClock('datetime');
    playSound(sound);
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

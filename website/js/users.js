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
function screenRefresh(sound) {
    playSound(sound);
}
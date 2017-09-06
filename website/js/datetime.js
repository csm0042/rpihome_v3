//

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

        // Get date and year
        var date = d.getDate();
        var year = d.getFullYear();
        
        // Get hour and adjust for AM/PM
        var hour = d.getHours(); 
        var ampm = "AM"
        if (hour > 12) {
            hour = hour - 12
            ampm = "PM"
        }

        // Get minute and front pad with zero if necessary
        var minute = d.getMinutes();
        minute = minute.toString();
        if (minute.length == 1) {
            minute = '0' + minute
        }

        // Get second and front-pad with zero if necessary
        var second = d.getSeconds();
        second = second.toString();
        if (second.length == 1) {
            second = '0' + second
        }

        // Update page with current date and time
        document.getElementById(id).innerHTML = hour + ':' + minute + ':' + second + ' ' + ampm + ' - ' + day + '  ' + month + ' ' + date + ', ' + year;

    }, 1000);
}
<html>
    <body>
        <?php
        $servername = "localhost";
        $dbname = "rpihome";        
        $username = "python";
        $password = "python";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $devname = $_POST['devname'];
        $devcmd = $_POST['devcmd'];
        
         // Execute query
         $sql = "INSERT INTO device_cmd (device, cmd) VALUES ('$devname', '$devcmd')";

         // Exxecute query and return results
         if ($conn->query($sql) === TRUE) {
             echo $devcmd;
         } else {
             echo "??";
         }

         // Close connection to database
         $conn->close();
        ?>

    </body>
</html>

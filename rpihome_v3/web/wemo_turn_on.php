<html>
    <body>
        <?php
        $servername = "localhost";
        $username = "python";
        $password = "python";
        $dbname = "rpihome";

        try {
            $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
            // set the PDR error mode to exception
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $sql = "INSERT INTO device_cmd (device, cmd)
            VALUES ('$_POST[devName]', '$_POST[devCmd]')";
            // use exec() because no results are returned
            $conn->exec($sql);
            echo "New record created successfully";
            }
        catch(PDOException $e)
            {
            echo $sql . "<br>" . $e->getMessage();
            }
        $conn = null;
        ?>

    </body>
</html>

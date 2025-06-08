<?php
$servername = "localhost";
$username = "103_133_178_203";
$password = "KDHpmPSt2KEs8r7m";
$dbname = "103_133_178_203";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// $conn = mysqli_connect($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 获取传递的班级 ID
// $classID = isset($_GET['classID']) ? intval($_GET['classID']) : "Others";
$classID = $_GET['classID'];

// echo $classID;
// 查询对应班级的数据
// $sql = "SELECT * FROM AIFdata WHERE Species = ' .$classID.'";
$sql = "SELECT * FROM AIFdata WHERE Poultry_Species LIKE '%$classID%'";
// -- $sql = "SELECT * FROM AIFdata where species = \'$classID\'";
// $sql = "SELECT * FROM AIFdata";

$result = mysqli_query($conn,$sql);

// echo "result";
// echo  $result;
// echo "result";

// 检查查询是否成功
if ($result === false) {
    // 查询失败，输出错误信息
    echo json_encode(['error' => 'SQL query failed: ' . mysqli_error($conn)]);
    exit;
}

// 输出结果
if (mysqli_num_rows($result) > 0) {

    $data = array();
    while ($row = $result->fetch_assoc()){
        $data[] = $row;
    }

    echo json_encode($data);
    
    // echo "<table>";
    // echo "<tr><th>Species</th><th>poultry_Species</th><th>Parts</th></tr>";

    // // 输出数据到表格
    // while($row = $result->fetch_assoc()) {
    //     echo "<tr><td>" . $row["Species"]. "</td><td>" . $row["poultry_Species"]. "</td><td>" . $row["Parts"]. "</td></tr>";
    // }

    // echo "</table>";
} else {
    echo json_encode(array());
    // echo "No data available for Class $classID.";
}

$conn->close();
?>


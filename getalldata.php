<?php

$servername = "localhost";
$username = "103_133_178_203";
$password = "KDHpmPSt2KEs8r7m";
$dbname = "103_133_178_203";

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);

// 检查连接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$Poultry_Species = $_GET['Poultry_Species'];
// echo $Poultry_Species;

$table_name = "AIFdata";

$sql_columns = "SHOW COLUMNS FROM $table_name";
// 去除Species_Properties
// $sql_columns = "SHOW COLUMNS FROM $table_name WHERE Field NOT IN ('Species_Properties')";

$result_columns = mysqli_query($conn, $sql_columns);
$columns = array();
while ($row = mysqli_fetch_assoc($result_columns)) {
    $columns[] = $row['Field'];
}
// 查询数据
// $sql_data = "SELECT * FROM $table_name";
$sql_data = "SELECT * FROM AIFdata WHERE Poultry_Species LIKE '%$Poultry_Species%'";

// $sql_data = "SELECT current.*
//         FROM AIFdata current
//         JOIN AIFdata next ON next.Poultry_Species > current.Poultry_Species
//         WHERE current.Poultry_Species = '$Poultry_Species'
//         ORDER BY current.Poultry_Species";

$result_data = mysqli_query($conn, $sql_data);
// 检查查询是否成功
if ($result_data === false) {
    echo json_encode(['error' => 'SQL query failed: ' . mysqli_error($conn)]);
    exit;
}
// 输出结果
$data = array();
while ($row = $result_data->fetch_assoc()) {
    $data[] = $row;
}
// 返回列名和数据
echo json_encode(['columns' => $columns, 'data' => $data]);


$conn->close();

?>


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

$searchQuery = $_GET['searchQuery'];
$category = $_GET['category'];  // 获取前端传递的 category 参数

// echo 'Category: ' . $category . ' | Search Query: ' . $searchQuery;

// 根据 category 值查询不同的表
$table_name = '';
switch ($category) {
    // case 'browse':
    //     $table_name = 'AIFdata';
    //     break;
    case 'flj':
        $table_name = 'AIFdata_VOC_FLJ';
        break;
    case 'wc':
        $table_name = 'AIFdata_VOC_WC';
        break;
    case 'gxy':
        $table_name = 'AIFdata_VOC_GXY';
        break;
    case 'ch':
        $table_name = 'AIFdata_VOC_CH';
        break; 
    case 'sh':
        $table_name = 'AIFdata_VOC_SH';
        break;
    default:
        echo json_encode(['error' => 'Invalid category']);
        exit;
}

if(!$searchQuery){
    // 获取列名
    $sql_columns = "SHOW COLUMNS FROM $table_name";
    $result_columns = mysqli_query($conn, $sql_columns);
    $columns = array();
    while ($row = mysqli_fetch_assoc($result_columns)) {
        $columns[] = $row['Field'];
    }
    // 查询数据
    $sql_data = "SELECT * FROM $table_name";
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
}else{
    $sql_data = "SELECT $searchQuery FROM $table_name";
    $result_data = mysqli_query($conn, $sql_data);
    $columns = array_map('trim', explode(',', $searchQuery));
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
}


$conn->close();

?>


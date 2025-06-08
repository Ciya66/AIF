<?php
// 连接数据库
$conn = new mysqli('localhost', 'username', 'password', 'database');
$class = $_GET['class'];
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = 10;  // 每页显示10条记录
$offset = ($page - 1) * $limit;

// 查询指定班级的成绩数据
$sql = "SELECT id, student_name, subject, score FROM scores WHERE class_name = ? LIMIT ?, ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param('sii', $class, $offset, $limit);
$stmt->execute();
$result = $stmt->get_result();

// 获取数据并返回JSON
$scores = [];
while ($row = $result->fetch_assoc()) {
    $scores[] = $row;
}

// 获取总页数
$total_sql = "SELECT COUNT(*) FROM scores WHERE class_name = ?";
$stmt_total = $conn->prepare($total_sql);
$stmt_total->bind_param('s', $class);
$stmt_total->execute();
$total_result = $stmt_total->get_result();
$total_rows = $total_result->fetch_row()[0];
$total_pages = ceil($total_rows / $limit);

echo json_encode(['scores' => $scores, 'total_pages' => $total_pages]);
?>

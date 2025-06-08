<?php
$id = $_GET['id'];
// 从数据库获取单个学生的成绩
$conn = new mysqli('localhost', 'username', 'password', 'database');
$sql = "SELECT student_name, subject, score FROM scores WHERE id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param('i', $id);
$stmt->execute();
$result = $stmt->get_result();
$student_scores = $result->fetch_all(MYSQLI_ASSOC);
?>

<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>学生详细成绩</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1><?php echo $student_scores[0]['student_name']; ?>的成绩</h1>

    <canvas id="studentChart"></canvas>

    <script>
        const data = {
            labels: [<?php foreach ($student_scores as $score) { echo "'".$score['subject']."',"; } ?>],
            datasets: [{
                data: [<?php foreach ($student_scores as $score) { echo $score['score'].","; } ?>],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
            }]
        };

        const ctx = document.getElementById('studentChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: data
        });
    </script>
</body>
</html>

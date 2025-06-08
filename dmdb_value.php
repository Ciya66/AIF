
<!--负责展示跳转HMDB的内容-->


<?php
ini_set('memory_limit', '512M'); // 设置内存限制

if (isset($_GET['file'])) {
    $file = $_GET['file'];
    $page = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $pageSize = 50; // 每页显示50行

    if (file_exists($file)) {
        $handle = fopen($file, 'r');
        if ($handle) {
            $header = fgetcsv($handle); // 读取表头

            // 统计总行数（不含表头）
            $totalLines = 0;
            while (fgetcsv($handle) !== false) {
                $totalLines++;
            }
            fclose($handle);

            $totalPages = ceil($totalLines / $pageSize); // 总页数

            // 重新打开文件，读取当前页的数据
            $handle = fopen($file, 'r');
            fgetcsv($handle); // 跳过表头

            $start = ($page - 1) * $pageSize;
            $currentLine = 0;
            $data = [];

            while (($line = fgetcsv($handle)) !== false) {
                if ($currentLine >= $start && $currentLine < $start + $pageSize) {
                    $data[] = $line;
                }
                $currentLine++;
                if ($currentLine >= $start + $pageSize) {
                    break;
                }
            }
            fclose($handle);

            // 生成表格HTML
            $table = '<table class="custom-table">';
            $table .= '<thead><tr>';
            foreach ($header as $h) {
                $table .= '<th>' . htmlspecialchars($h) . '</th>';
            }
            $table .= '<th></th>';
            $table .= '</tr></thead><tbody>';

            foreach ($data as $row) {
                $table .= '<tr>';
                foreach ($row as $cell) {
                    $table .= '<td>' . htmlspecialchars($cell) . '</td>';
                }
                $hmdbId = htmlspecialchars($row[0]);
                // 添加图片列
                $table .= '<td style="border: none;"><a href="https://hmdb.ca/metabolites/'.$hmdbId.'"><img src="./Fig/userguide/HMDB.png"></a></td>';
                $table .= '</tr>';
            }
            $table .= '</tbody></table>';

            // 生成分页按钮
            $pagination = '<div class="pagination">';

            // 首页按钮
            if ($page > 1) {
                $pagination .= '<a href="?file=' . urlencode($file) . '&page=1">&laquo; 首页</a>';
            }

            // 上一页按钮
            if ($page > 1) {
                $pagination .= '<a href="?file=' . urlencode($file) . '&page=' . ($page - 1) . '">&lt; 上一页</a>';
            }

            // 中间页码按钮（最多显示10个）
            $startPage = max(1, $page - 5);
            $endPage = min($totalPages, $page + 4);

            if ($endPage - $startPage < 9) {
                $startPage = max(1, $endPage - 9);
            }

            if ($startPage > 1) {
                $pagination .= '<a href="?file=' . urlencode($file) . '&page=1">1</a>';
                if ($startPage > 2) {
                    $pagination .= '<span>...</span>';
                }
            }

            for ($i = $startPage; $i <= $endPage; $i++) {
                if ($i == $page) {
                    $pagination .= '<a class="active" href="?file=' . urlencode($file) . '&page=' . $i . '">' . $i . '</a>';
                } else {
                    $pagination .= '<a href="?file=' . urlencode($file) . '&page=' . $i . '">' . $i . '</a>';
                }
            }

            if ($endPage < $totalPages) {
                if ($endPage < $totalPages - 1) {
                    $pagination .= '<span>...</span>';
                }
                $pagination .= '<a href="?file=' . urlencode($file) . '&page=' . $totalPages . '">' . $totalPages . '</a>';
            }

            // 下一页按钮
            if ($page < $totalPages) {
                $pagination .= '<a href="?file=' . urlencode($file) . '&page=' . ($page + 1) . '">下一页 &gt;</a>';
            }

            // 末页按钮
            if ($page < $totalPages) {
                $pagination .= '<a href="?file=' . urlencode($file) . '&page=' . $totalPages . '">末页 &raquo;</a>';
            }

            $pagination .= '</div>';

            // 读取HTML模板
            $template = file_get_contents('./list_value.html');

            // 将CSV表格和分页导航一起填充进模板
            $output = str_replace('{{csv_data}}', $table . $pagination, $template);



            $style = '
            <style>
            /* 去除最后一列上下左右边框 */
            .custom-table td:last-child,
            .custom-table th:last-child {
                border: none !important;
            }
            
            /* 去除表头最后一列的背景色 */
            .custom-table th:last-child {
                background: none !important;
            }
            
            /* 去除整个表格的上、下、右边框 */
            .custom-table {
                border-collapse: collapse;
                border-top: none !important;
                border-bottom: none !important;
                border-right: none !important;
            }
            </style>
            ';

            $output = $style . $output;
            // 输出最终页面
            echo $output;
        } else {
            echo '文件无法打开';
        }
    } else {
        echo '文件不存在';
    }
}
?>

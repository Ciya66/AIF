function loadClassData(classId) {
    fetch(`get_info.php?classID=${classId}`)
        .then(response => response.json()) // 解析 JSON 数据
        .then(data => {
            if (data.length > 0) {
                let table = '<table class="custom-table"><tr><th>Poultry Species</th><th>Species Properties</th><th>Poultry Source</th><th>DATA</th></tr>';
                data.forEach(row => {
                    table += `<tr><td>${row.Poultry_Species}</td><td>${row.Species_Properties}</td><td>${row.Poultry_Source}</td><td>
                                <a href="link-to-food-quality.html?Poultry_Species=${row.Poultry_Species}" target="_blank">Food Quality Indicators</a>、
                                <a href="link-to-voc.html" target="_blank" onclick="handleVOCClick('${row.Poultry_Species}')">VOC</a>、
                                <a href="link-to-metabolites" target="_blank">metabolites</a>
                            </td></tr>`;
                });
                table += '</table>';
                document.getElementById('class-data').innerHTML = table;
            } else {
                document.getElementById('class-data').innerHTML = 'No data found for this class.';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('class-data').innerHTML = 'Error loading data.';
        });
}

//点击VOC获取当前行的Poultry_Species
function handleVOCClick(poultrySpecies) {
    // 使用 encodeURIComponent 对名字进行编码以确保 URL 安全
    const encodedSpecies = encodeURIComponent(poultrySpecies);
    // 跳转到新的页面，并将 poultrySpecies 作为 URL 参数传递
    window.location.href = `link-to-voc.html?poultrySpecies=${encodedSpecies}`;
}

//高级检索————搜索
function loadClassData_VOC(category,searchQuery) {
    fetch(`get_voc.php?category=${category}&searchQuery=${searchQuery}`)
        // .then(response => response.text()) 
        // .then(data => {
        //     console.log(data);  // 在控制台查看输出
        // })
        // .catch(error => {
        //     console.error('Error fetching data:', error);
        // });
        .then(response => response.json())
        .then(data => {
            if (data.data.length > 0) {
                // 动态生成表头
                let table = '<table class="custom-table"><tr>';
                data.columns.forEach(col => {
                    table += `<th>${col}</th>`;
                });
                table += '</tr>';

                // 动态生成表格内容
                data.data.forEach(row => {
                    table += '<tr>';
                    data.columns.forEach(col => {
                        table += `<td>${row[col]}</td>`;
                    });
                    table += '</tr>';
                });
                table += '</table>';
                document.getElementById('class-data').innerHTML = table;
            } else {
                document.getElementById('class-data').innerHTML = 'No data found for this category.';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('class-data').innerHTML = 'Error loading data.';
        });
}

//advanceed_search
function searchInputData() {    
    // 获取输入框的值
    var category = document.getElementById("searchCategory").value;
    // console.log(category)
    const searchQuery = document.getElementById('searchData').value;
    if(category=="browse"){
        if (searchQuery) {
            loadClassData(searchQuery);
        } else {
            alert("please input search content!");
        }
    }else if(category=="flj"||category=="wc"||category=="gxy"){
        if (searchQuery)
            loadClassData_VOC(category,searchQuery);
        else 
            loadClassData_VOC(category,'');
    }
    
}

//高级检索————清除表格
function clearForm(){
    document.getElementById('class-data').innerHTML = '';
}

//高级检索————例子
function example(){
    var popup = document.getElementById('example-popup');
    popup.style.display = 'block'; // 显示提示框
    // alert("FLJ,WC,GXY查询时输入表头(表头之间用,)隔开,不输出默认查询全部");
}

//高级检索————例子————关闭
function closePopup() {
    var popup = document.getElementById('example-popup');
    popup.style.display = 'none';  // 隐藏提示框
}
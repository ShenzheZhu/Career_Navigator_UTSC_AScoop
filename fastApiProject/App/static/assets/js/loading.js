function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function hideUpload() {
    document.getElementById('main').style.display = 'none';
}

document.getElementById('file-upload').onchange = function() {
    showLoading();  // 显示加载界面
    var formData = new FormData();
    formData.append('file', this.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();  // 隐藏加载界面
        console.log(data); // 处理服务器返回的数据
        if (data.results) {
            displayResults(data.results); // 显示结果
        }
        document.getElementById('file-upload').value = ''
    })
    .catch(error => {
        hideLoading();  // 出错也要确保隐藏加载界面
        console.error('Error:', error);
        document.getElementById('file-upload').value = ''
    });
};

function displayResults(results) {
    // 将结果保存到localStorage
    localStorage.setItem('results', JSON.stringify(results));
    // 跳转到 result.html
    window.location.href = '/result';
}
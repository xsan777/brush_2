// 当鼠标移动到喝酒数据状态图标时提示该图标代表什么含义
$('[data-toggle="popover"]').popover();
$('#online_stats_unexist').hover(function () {
        $(this).popover('show')
    },
    function () {
        $(this).popover('hide')
    }
);
$('#order_special_unexist').hover(function () {
        $(this).popover('show')
    },
    function () {
        $(this).popover('hide')
    }
);
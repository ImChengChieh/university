/**
 * Created by jiy on 2016/8/19.
 */

window.onload = function () {
    Article_list.init();
}


var Article_list = (function () {

    var page = 1
        , type_id = 0
        , keywords = null

    // 加载列表
    function get_list(table_id, pagination_id) {
        $.ajax({
            url: "/api/article/list",
            type: "post",
            data: {
                page: page,
                type_id: type_id,
                keywords: keywords
            },
            success: function (data) {
                render_list(table_id, data)
                render_pagination(pagination_id, data, table_id, pagination_id)
                bind_del_btn(table_id, pagination_id)
                bind_top_or_cancel_btn(table_id, pagination_id)
            }
        })
    }

    // 渲染文章列表
    function render_list(table_id, data) {
        var rows = ''
        for (var item in data.items) {
            item = data.items[item]

            rows += ' <tr>'
                + '     <td>' + item.id + '</td>'
                + '     <td><a href="article/update/' + item.id + '">' + item.title + '</a></td>'
                + '     <td>' + item.type + '</td>'
                + '     <td class="am-hide-sm-only">' + item.create_at + '</td>'
                + '     <td>'
                + '         <div class="am-btn-toolbar">'
                + '             <div class="am-btn-group am-btn-group-xs">'
                + '                 <a class="top_or_cancel" data-id="' + item.id + '" href="javascript:;">'
                + '                     <span ' + (item.top_to_index == 'True' ? 'class="am-icon-share"' : 'class="am-icon-copy"') + '></span> ' + (item.top_to_index == 'True' ? '取消置顶' : '首页置顶')
                + '                 </a>'
                + '                 <a href="article/update/' + item.id + '" class="edit-article">'
                + '                     <span class="am-icon-pencil-square-o"></span> 编辑'
                + '                 </a>'
                + '                 <a href="javascript:;" data-art-id="' + item.id + '"  class="delete-article">'
                + '                     <span class="am-icon-trash-o"></span> 删除'
                + '                 </a>'
                + '             </div>'
                + '         </div>'
                + '     </td>'
                + ' </tr>'
        }

        $(table_id).find("tbody").html(rows)


    }

    // 渲染分页条
    function render_pagination(pagination_id, data, table_id, pagination_id) {
        // 页面总数
        var page_count = data.total % data.per_page == 0 ? parseInt(data.total / data.per_page) : parseInt(data.total / data.per_page) + 1

        var pagination = '共' + data.total + '条记录 ' + data.page + '/' + page_count + '页'
            + '<div class="am-fr">'
            + '    <ul class="am-pagination">'
            + '        <li id="pre_page" ' + (data.page == 1 ? 'class="am-disabled"' : '') + '><a href="#">«</a></li>'

        for (var i = (data.page > 2 ? data.page - 2 : (data.page > 1 ? data.page - 1 : data.page)); i <= (page_count - data.page > 2 ? data.page + 2 : (page_count - data.page > 2 ? data.page + 2 : page_count)); i++) {
            pagination += '<li class="page_btn ' + (i == data.page ? 'am-active' : '') + '" >'
                + ' <a href="#">' + i + '</a>'
                + '</li>'
        }
        pagination += '        <li id="next_page" ' + (data.page == page_count ? 'class="am-disabled"' : '') + '><a href="#">»</a></li>'
            + '    </ul>'
            + '</div>'


        $(pagination_id).html(pagination);
        bind_page_btn(page_count, table_id, pagination_id)
    }

    // 绑定分页按钮的事件
    function bind_page_btn(page_count, table_id, pagination_id) {

        // 数字按钮事件
        $(".page_btn").on('click', 'a', function () {
            page = parseInt($(this).html())
            get_list(table_id, pagination_id)
        })

        // 上一页事件
        $("#pre_page").on('click', 'a', function () {
            page = (page == 1 ? page : page - 1)
            get_list(table_id, pagination_id)
        })

        // 下一页事件
        $("#next_page").on('click', 'a', function () {
            page = (page == page_count ? page : page + 1)
            get_list(table_id, pagination_id)
        })

    }

    // 绑定搜索按钮的点击事件
    function bind_find_btn(type_input_id, keywords_input_id, btn_id, table_id, pagination_id) {
        $(btn_id).on("click", function () {
            type_id = $(type_input_id).val()
            keywords = $(keywords_input_id).val()
            page = 1
            get_list(table_id, pagination_id)
        })
    }

    // 绑定类型下拉框的改变事件
    function bind_type_select_change(select_id, table_id, pagination_id) {
        $("#type").on("change", function () {
            type_id = $(select_id).val()
            page = 1
            get_list(table_id, pagination_id)
        })
    }

    // 绑定删除按钮点击事件
    function bind_del_btn(table_id, pagination_id) {
        $('.delete-article').add('#doc-confirm-toggle').on('click', function () {
            $('#delete-confirm').modal({
                relatedTarget: this,
                onConfirm: function (options) {
                    var $link = $(this.relatedTarget)
                    $.ajax({
                        url: "/api/article/delete",
                        type: "post",
                        data: {
                            article_id: $link.data('art-id')
                        },
                        success: function (data) {
                            if (data.success) {
                                get_list(table_id, pagination_id)
                                alert(data.msg)
                            }
                        }
                    })
                },
                // closeOnConfirm: false,
                onCancel: function () {
                }
            });
        });
    }

    // 绑定置顶和取消按钮事件
    function bind_top_or_cancel_btn(table_id, pagination_id) {
        $('.top_or_cancel').add('#doc-confirm-toggle').on('click', function () {
            $('#set-top-confirm').modal({
                relatedTarget: this,
                onConfirm: function (options) {
                    var id = $(this.relatedTarget).data("id")
                    $.ajax({
                        url: "/api/article/top_or_cancel",
                        type: "post",
                        data: {
                            article_id: id
                        },
                        success: function (data) {
                            if (data.success) {
                                console.info(data)
                                get_list(table_id, pagination_id)
                            }
                        }
                    })
                },
                // closeOnConfirm: false,
                onCancel: function () {
                }
            });
        });
    }

    function init() {
        get_list("#article_list", "#pagination")
        bind_find_btn("#type", "#keywords", "#do_find", "#article_list", "#pagination")
        bind_type_select_change("#type", "#article_list", "#pagination")
    }

    return {
        init: init
    }
})()
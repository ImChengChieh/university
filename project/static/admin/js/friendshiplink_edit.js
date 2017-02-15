/**
 * Created by Administrator on 2016/8/24 0024.
 */
/**
 * Created by jiy on 2016/8/18.
 */

window.onload = function () {
    Friendshiplink_edit.init();
}

var Friendshiplink_edit = (function () {
    //初始化富文本
    function initEditor() {
        var $textArea = $('[name=detail]');
        var editor = UE.getEditor('detail', {
            toolbars: [
                ['paragraph', 'fontfamily', 'fontsize', 'forecolor', 'bold', 'italic', 'underline', 'insertorderedlist', 'insertunorderedlist', 'justifyleft', 'justifyright', 'justifycenter']
            ],
            autoHeightEnabled: true,
            autoFloatEnabled: true,
            elementPathEnabled: false,
            wordCount: false,
            initialFrameHeight: 300,
            enableAutoSave: false
        });
    }

    //验证表单
    function validateForm(id) {
        var $form = $(id);
        $form.validator({
            onValid: function (validity) {
                $(validity.field).closest('.am-form-group').find('.am-alert').hide();
            },

            onInValid: function (validity) {
                var $field = $(validity.field);
                var $group = $field.closest('.am-form-group');
                var $alert = $group.find('.am-alert');
                // 使用自定义的提示信息 或 插件内置的提示信息
                var msg = $field.data('validationMessage') || this.getValidationMessage(validity);

                if (!$alert.length) {
                    $alert = $('<div class="am-alert am-alert-error"></div>').hide().appendTo($group);
                }

                $alert.html(msg).show();
            },

            submit: function () {
                var formValidity = this.isFormValid();
                var $id = $form.selector;

                if (formValidity) {
                    //验证成功的逻辑

                    return false;
                } else {
                    return false;
                }
            },

            validClass: ''

        })

    }

    // 提交数据
    function postForm(id) {
        var $submit = $(id).find('button[type="submit"]');
        var $selectType = $('.s-type'),
            $recommend = $('input[type="checkbox"]'),
            $title = $('.title'),
            $img_src = $('#file_cover'),
            $edui = $('#detail'),
            $id = $('#id')

        $submit.on('click', function () {

            var not_null = true

            $("*[required]").each(function () {
                not_null = not_null && ($(this).val() != "")
            })
            if (not_null) {
                $.ajax({
                    url: "/api/friendshiplink/update",
                    type: "post",
                    data: {
                        "id": $id.val(),
                        "title": $title.val(),
                        "img": $img_src.data("img-src"),
                        "link": $edui.val()
                    },
                    success: function (data) {
                        console.info(data)
                        if (data.success) {
                            alert("添加成功！")
                            $("input").val("")
                        }
                    }
                })
            } else {
                alert("请填写所有参数再提交！")
            }
        })
    }

    // 上传图像按钮的绑定
    function bind_upload_btn(btn_id, input_id) {

        $(btn_id).on("change", function () {
            var fileObj = $(input_id).get(0).files[0] // 获取文件对象
            var FileController = "/api/upload";                    // 接收上传文件的后台地址

            console.info(fileObj)

            // FormData 对象
            var form = new FormData();
            form.append("file_cover", fileObj);                           // 文件对象

            // XMLHttpRequest 对象
            var xhr = new XMLHttpRequest();
            xhr.open("post", FileController, true);
            xhr.onreadystatechange = function () {
                //如果请求成功
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = (new Function("return " + xhr.responseText))();
                    if (data.success) {
                        var file_path = data.file_path
                        var img = $("<img width='200' />").attr("src", file_path)
                        $(btn_id).parent().append(img)
                        $(input_id).data("img-src", file_path)
                        console.info($(input_id))
                    }
                }
            }

            xhr.send(form);
        })

    }

    function init() {
        initEditor();
        validateForm('#article');
        postForm('#article');
        bind_upload_btn("#file_cover", "#file_cover")
    }

    return {
        init: init
    }
})();
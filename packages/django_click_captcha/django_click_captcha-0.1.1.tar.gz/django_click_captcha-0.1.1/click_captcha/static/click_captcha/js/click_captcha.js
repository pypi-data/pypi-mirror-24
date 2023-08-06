(function ($, window, document, undefined) {

    'use strict';

    var Captcha = {

        init: function () {
            this.dom = {
                captcha_wrapper: $('.captcha-image-wrapper'),
                captcha_img: $('#captcha-image'),
                refresh_button: $('#captcha-refresh'),
                captcha_input: $('.captcha-field')

            };

            this.click_points = [];

            this.origin_url = this.dom.captcha_img.attr('src');

            this.timeout = this.dom.captcha_wrapper.attr('data-time-refresh');

            this.refresh_captcha_listen();

            this.captcha_click_listen();

            this.captcha_span_delegate();

        },

        refresh_captcha_listen: function () {
            // 刷新验证码
            var that = this;
            this.dom.refresh_button.click(function () {
                that.dom.captcha_img.attr('src', that.origin_url + '?r=' + Math.random());
                that.clear_span_and_point();
            });
        },
        clear_span_and_point: function () {
            this.click_points = [];
            this.dom.captcha_input.attr('value', []);
            this.dom.captcha_wrapper.find('span').remove();
        },

        points_to_string: function (points) {
            // var ret = '';
            // for (var key in points) {
            //     ret = ret + points[key][0] + ',' + points[key][1] + ',';
            // }
            // return ret.substring(0, ret.length - 1);
            return points.join(',');
        },

        add_click_point: function (point) {
            // 添加点击的倒字
            var timestamp = '' + new Date().getTime();
            this.click_points[timestamp] = point;
            this.fill_captcha_value();
            return timestamp;
        },

        remove_click_point: function (timestamp) {
            // 删除点击的倒字
            delete(this.click_points[timestamp]);
            this.fill_captcha_value();
        },

        _compare: function (point1, point2) {
            // 根据横坐标点的前后位置进行排序
            var temp1 = parseInt(point1[0]);
            var temp2 = parseInt(point2[0]);
            if (temp1 < temp2) {
                return -1;
            } else if (temp1 === temp2) {
                return 0;
            } else {
                return 1;
            }
        },

        fill_captcha_value: function () {
            var ret = [];
            // 获取时间戳字典对应的值
            for (var key in this.click_points) {
                ret.push(this.click_points[key]);
            }
            if (ret.length > 0) {
                ret.sort(this._compare);
            }

            // console.log(this.points_to_string(ret) + 'asdfkjasljdfljaskf');
            // 更新 form 表单提交的数据
            this.dom.captcha_input.attr('value', this.points_to_string(ret));
        },

        captcha_span_delegate: function () {
            // 倒字对应的点后期增加，使用 delegate 处理未来的增加的元素的事件
            var that = this;

            this.dom.captcha_wrapper.delegate(
                '.captcha-span', 'mouseover', function () {
                    $(this).addClass('glyphicon glyphicon-remove');
                }
            );

            this.dom.captcha_wrapper.delegate(
                '.captcha-span', 'mouseleave', function () {
                    $(this).removeClass('glyphicon glyphicon-remove');
                }
            );

            this.dom.captcha_wrapper.delegate(
                '.captcha-span', 'click', function () {
                    var timestamp = $(this).attr('data-index');
                    $(this).remove();
                    that.remove_click_point(timestamp);
                }
            );
        },

        captcha_click_listen: function () {
            var that = this;
            this.dom.captcha_img.click(function (e) {
                // 获得点击的位置, 这里不能用 position() 因为它会受父元素位置的影响， 而 offset() 不会
                var x = $(this).offset().left, y = $(this).offset().top;
                x = e.pageX - x;
                y = e.pageY - y;
                console.log(x, y);
                var span_index = that.add_click_point([x, y]);
                // 由于绘制的点向上和向右进行了偏离， 因此为了确保绘制的点处于鼠标点击的位置，进行了位置的微调
                // 去掉 label 向下偏移的 6 px， 去掉 border 1 px, 点本身的宽度 8 px, 这样鼠标就处在点的中间了
                x = x - 8 - 1;
                y = y + 8 + 1 + 6;
                // data-index 属性保留当前点击点以便后面删除处理
                var new_span = $('<span class="captcha-span" style="left:' + x + 'px; top:' + y + 'px" data-index="' + span_index + '"></span>');
                that.dom.captcha_img.after(new_span);

            });
        }

    };

    $(function () {
        Captcha.init();
    });

})(jQuery, window, document);

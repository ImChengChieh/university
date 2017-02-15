util = (function () {
    var nav = function (index) {
        var uls = document.getElementsByClassName("main_nav");
        var as = uls[0].getElementsByTagName('a');
        as[index - 1].setAttribute('class', 'on_')
    }
    return {
        nav: nav
    }
})()

var headr_text = document.getElementById('headr_text');
var banner_innerhtml = document.getElementById('banner_innerhtml');
var imgs = document.getElementById('banner_img');
var b_ul = document.getElementById('banner_paging');
var b_li = b_ul.getElementsByTagName('li');
var banner = document.getElementById('banner');
var banner_img = banner.getElementsByTagName('img');
var banner_sm = document.getElementById('banner_sm');
var banner_sm_div = banner_sm.getElementsByTagName('div');
var num = 0;
function lunbo() {
    num++;
    if (num >= b_li.length) {
        num = 0;
    }
    for (var t = 0; t < banner_sm_div.length; t++) {
        banner_sm_div[t].style.display = 'none';
        banner_img[t].style.display = 'none';
    }
    banner_img[num].style.display = 'block';
    banner_sm_div[num].style.display = 'block';
    for (var i = 0; i < b_li.length; i++) {
        b_li[i].style.backgroundColor = "";
    }
    b_li[num].style.backgroundColor = "#fff";
}

var timer = setInterval(lunbo, 2000);
banner.onmouseover = function () {
    clearInterval(timer);
}
banner.onmouseout = function () {
    clearInterval(timer);
    timer = setInterval(lunbo, 2000);
}
for (var j = 0; j < b_li.length; j++) {
    b_li[j].index = j;
}
for (var j = 0; j < b_li.length; j++) {
    b_li[j].onmouseover = function () {
        clearInterval(timer);
        for (var s = 0; s < b_li.length; s++) {
            b_li[s].style.backgroundColor = '';
        }
        this.style.backgroundColor = '#fff';
        num = this.index;
        for (var t = 0; t < banner_sm_div.length; t++) {
            banner_sm_div[t].style.display = 'none';
            banner_img[t].style.display = 'none';
        }
        banner_sm_div[num].style.display = 'block';
        banner_img[num].style.display = 'block';
    }
}


var r_fl = document.getElementById('referral_fl');
var r_fr = document.getElementById('referral_fr');
var add = document.getElementById('add_');
var donates = document.getElementById('donates');
r_fl.onclick = function () {
    add.style.display = 'block';
    donates.style.display = 'none';
    this.style.backgroundColor = "#fff";
    r_fr.style.backgroundColor = '#e2e2e2';
}
r_fr.onclick = function () {
    add.style.display = 'none';
    donates.style.display = 'block';
    this.style.backgroundColor = "#fff";
    r_fl.style.backgroundColor = '#e2e2e2';
}


var demo = document.getElementById("demo");//通过id获取div的文本域
var demo1 = document.getElementById("demo1");//通过id获取ul的文本域
demo2.innerHTML += demo1.innerHTML;//复制一个一模一样的demo1作备用
function scrollUp() {//声明函数名为scrollUp的函数
    if (demo.scrollTop >= demo2.offsetHeight) {//判断当向上的位移大于或等于任意一个ul的高度时
        demo.scrollTop = 0 + 'px';//让第一个ul回到初始位置，以保证不间断滚动
    }
    else {
        demo.scrollTop++;//否则，向上移动1px
    }
}
var myScroll = setInterval(scrollUp, 30);//每30毫秒调用一次scrollUp函数
demo.onmouseout = function () {//鼠标移入div的方法
    myScroll = setInterval(scrollUp, 30);//每30毫秒调用一次scrollUp函数
}

demo.onmouseover = function () {//鼠标移出div的方法
    clearInterval(myScroll);//清除定时器myScroll
}

var demo_ = document.getElementById("demo_");//通过id获取div的文本域
var demo_1 = document.getElementById("demo_1");//通过id获取ul的文本域
demo_2.innerHTML += demo_1.innerHTML;//复制一个一模一样的demo1作备用
function scrollUp_() {//声明函数名为scrollUp的函数
    if (demo_.scrollTop >= demo_2.offsetHeight) {//判断当向上的位移大于或等于任意一个ul的高度时
        demo_.scrollTop = 0 + 'px';//让第一个ul回到初始位置，以保证不间断滚动
    }
    else {
        demo_.scrollTop++;//否则，向上移动1px
    }
}
var myScroll_ = setInterval(scrollUp_, 30);//每30毫秒调用一次scrollUp函数
demo_.onmouseout = function () {//鼠标移入div的方法
    myScroll_ = setInterval(scrollUp_, 30);//每30毫秒调用一次scrollUp函数
}

demo_.onmouseover = function () {//鼠标移出div的方法
    clearInterval(myScroll_);//清除定时器myScroll
}

var v_img = document.getElementById('v_img');
var a_video = document.getElementById('a_video');
var a_videos = ['忆往昔，我们的青春', '忆往昔，我们的师长', '忆往昔，我们的校园'];
var v_imgs = ['static/images/img_5.jpg', 'static/images/video_1.jpg', 'static/images/video_3.jpg'];
var divs = document.getElementById('video_header');
var prev = document.getElementById('prev');
var next = document.getElementById('next');
var s = 0;
function mover() {
    if (s > v_imgs.length - 1) {
        s = 0;
    }
    v_img.src = v_imgs[s];
    a_video.innerHTML = a_videos[s];
    s++;
}
var time = setInterval(mover, 2000);

divs.onmouseover = function () {
    clearInterval(time);
}
divs.onmouseout = function () {
    clearInterval(time);
    time = setInterval(mover, 2000);
}
prev.onclick = function () {
    clearInterval(time);
    s -= 2;
    if (s < 0) {
        s = v_imgs.length - 1;
    }
    mover();
}
next.onclick = function () {
    clearInterval(time);
    mover();
}

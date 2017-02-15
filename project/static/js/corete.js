var boxs=document.getElementById('box');
		var samp=boxs.getElementsByTagName('samp');
		//获取焦点
		function name_focus(){
          samp[0].innerHTML='请输入正确的姓名';
          samp[0].style.color='#000';
       }
		//名称
		function class_blur(){
			var classed=document.getElementById('class_').value;
			if(classed == ''||classed==null){
                samp[0].innerHTML='* 企业名称必填';
                samp[0].style.color='red';
                return false;
            }
			else{
				samp[0].innerHTML=' ';
				return true;
			}
		}
		//法人
		function name_blur(){
			var names=document.getElementById('names').value;
			if(names == ''||names==null){
                samp[1].innerHTML='* 法人代表必填';
                samp[1].style.color='red';
                return false;
            }
			else{
				samp[1].innerHTML=' ';
				return true;
			}
		}
		function name_focus(){
		  samp[1].innerHTML='请输入法人代表';
          samp[1].style.color='#000';
		}
       //企业简介
		function ms_blur(){
			var message=document.getElementById('message').value;
			if(message == ''||message==null){
                samp[3].innerHTML='* 请填写简介';
                samp[3].style.color='red';
                return false;
            }
			else{
				samp[3].innerHTML=' ';
				return true;
			}
		}
		function ms_focus(){
		  samp[3].innerHTML='请填写企业简介';
          samp[3].style.color='#000';
		}

		//联络人
		function tels_blur(){
			var tel=document.getElementById('tel').value;
			if(tel == ''||tel==null){
                samp[4].innerHTML='* 联络人不能为空';
                samp[4].style.color='red';
                return false;
           }
			else{
				samp[4].innerHTML=' ';
				return true;
			}
		}
		function tels_focus(){
		  samp[4].innerHTML='请填写联络人';
          samp[4].style.color='#000';
		}
		//联系电话
		function phones_blur(){
			var phones=document.getElementById('phones').value;
			if(phones == ''||phones==null){
                samp[5].innerHTML='* 电话号码不能为空';
                samp[5].style.color='red';
                return false;
            }
            if(!/^((\d{11})|(\d{7,8})|(\d{4}|\d{3})-(\d{7,8}))$/.test(phones)){
				 samp[5].innerHTML='* 电话号码错误';
				 samp[5].style.color='red';
				 return false;
			}
			else{
				samp[5].innerHTML=' ';
				return true;
			}
		}
		function phones_focus(){
		  samp[5].innerHTML='请输入正确的电话号码';
          samp[5].style.color='#000';
		}
	   //提交验证
	   function regin() {
		 var classed=document.getElementById('class_').value;
			if(classed == ''||classed==null){
                samp[0].innerHTML='* 企业名称必填';
                samp[0].style.color='red';
                return false;
            }

		   var names=document.getElementById('names').value;
			if(names == ''||names==null){
                samp[1].innerHTML='* 法人代表必填';
                samp[1].style.color='red';
                return false;
            }

            var message=document.getElementById('message').value;
			if(message == ''||message==null){
                samp[3].innerHTML='* 请填写简介';
                samp[3].style.color='red';
                return false;
            }
		   var tel=document.getElementById('tel').value;
			if(tel == ''||tel==null){
                samp[4].innerHTML='* 联络人不能为空';
                samp[4].style.color='red';
                return false;
           }
           var phones=document.getElementById('phones').value;
			if(phones == ''||phones==null){
                samp[5].innerHTML='* 电话号码不能为空';
                samp[5].style.color='red';
                return false;
            }

           var deals = document.getElementById('deal');
		   if (deals.checked != true) {
			  samp[6].innerHTML = '* 请同意《校友会章程》';
			   samp[6].style.color = 'red';
			   return false;
		   }
		    else {
			   return true;
		   }
	   }/**
 * Created by Administrator on 2016/11/21.
 */

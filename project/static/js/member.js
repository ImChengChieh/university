document.getElementById('date_img').onclick = function(){

            laydate({

                elem: '#date_input',

            });
        }
		
		var boxs=document.getElementById('box');
		var samp=boxs.getElementsByTagName('samp');	
		//获取焦点
		function name_focus(){
          samp[0].innerHTML='请输入正确的姓名';
          samp[0].style.color='#000';
       }
		//姓名
		function name_blur(){
		  var usesd=document.getElementById('name_').value;
			if(usesd == ''||usesd==null){
                samp[0].innerHTML='* 姓名不能为空';
                samp[0].style.color='red';
                return false;
			/*}if(usesd.indexOf(' ')!==-1){
                spans[0].innerHTML='*用户名不能包含空格特殊字符';
                spans[0].style.color='red';
                return false;*/
			}
			if(!/^([\u4e00-\u9fa5]+|([a-zA-Z]+\s?)+)$/.test(usesd)){
				 samp[0].innerHTML='* 姓名格式错误';
				 samp[0].style.color='red';
				 return false;
			}
			else{
				samp[0].innerHTML=' ';
				return true;
			}
        }
		//入学班级
		function class_blur(){
			var classed=document.getElementById('class_').value;
			if(classed == ''||classed==null){
                samp[1].innerHTML='* 入学班级不能为空';
                samp[1].style.color='red';
                return false;
            }
            if(!/^[\u4E00-\u9FA5]{2}\d{4}/.test(classed)){
				 samp[1].innerHTML='* 班级格式错误';
				 samp[1].style.color='red';
				 return false;
			}
			else{
				samp[1].innerHTML=' ';
				return true;
			}
		}	
		function class_focus(){
		  samp[1].innerHTML='请输入正确的入学班级(2个汉字+4个数字,如土建2012)';
          samp[1].style.color='#000';
		}
		
		
		//联络人
		function contact_blur(){
			var contact=document.getElementById('contact').value;
			if(contact == ''||contact==null){
                samp[2].innerHTML='* 联络人不能为空';
                samp[2].style.color='red';
                return false;
           }
			else{
				samp[2].innerHTML=' ';
				return true;
			}
		}
		function contact_focus(){
		  samp[2].innerHTML='请填写联络人';
          samp[2].style.color='#000';
		}
		//验证信息
		function message_blur(){
			var message=document.getElementById('message').value;
			if(message == ''||message==null){
                samp[5].innerHTML='* 验证信息不能为空';
                samp[5].style.color='red';
                return false;
            }
            if(!/^[\u4e00-\u9fa5]*$/.test(message)){
				 samp[5].innerHTML='* 请输入描述';
				 samp[5].style.color='red';
				 return false;
			}
			else{
				samp[5].innerHTML=' ';
				return true;
			}
		}	
		function message_focus(){
		  samp[5].innerHTML='请输入正确的验证信息';
          samp[5].style.color='#000';
		}
		//联系电话
		function tel_blur(){
			var tel=document.getElementById('tel').value;
			if(tel == ''||tel==null){
                samp[6].innerHTML='* 电话号码不能为空';
                samp[6].style.color='red';
                return false;
            }
            if(!/^((\d{11})|(\d{7,8})|(\d{4}|\d{3})-(\d{7,8}))$/.test(tel)){
				 samp[6].innerHTML='* 电话号码错误';
				 samp[6].style.color='red';
				 return false;
			}
			else{
				samp[6].innerHTML=' ';
				return true;
			}
		}	
		function tel_focus(){
		  samp[6].innerHTML='请输入正确的电话号码';
          samp[6].style.color='#000';
		}
		//联络邮箱
		function eamil_blur(){
			var eamil=document.getElementById('eamil').value;
			if(eamil == ''||eamil==null){
                samp[7].innerHTML='* 邮箱不能为空';
                samp[7].style.color='red';
                return false;
            }
            if(!/^[\w_-]+@[\w_-]+[\.a-zA-Z]+[^\.]$/.test(eamil)){
				 samp[7].innerHTML='* 邮箱格式错误';
				 samp[7].style.color='red';
				 return false;
			}
			else{
				samp[7].innerHTML=' ';
				return true;
			}
		}	
		function eamil_focus(){
		  samp[7].innerHTML='请输入正确的邮箱';
          samp[7].style.color='#000';
		}
		
	   //选择身份、当前所在地、出生日期
	   function checkeds() {
		   var usesd = document.getElementById('name_').value;
		   if (usesd == '' || usesd == null) {
			   samp[0].innerHTML = '* 姓名不能为空';
			   samp[0].style.color = 'red';
			   return false;
		   }

		   	var classed=document.getElementById('class_').value;
			if(classed == ''||classed==null){
                samp[1].innerHTML='* 入学班级不能为空';
                samp[1].style.color='red';
                return false;
            }
            var contact=document.getElementById('contact').value;
			if(contact == ''||contact==null){
                samp[2].innerHTML='* 联络人不能为空';
                samp[2].style.color='red';
                return false;
           }
		   var message=document.getElementById('message').value;
			if(message == ''||message==null){
                samp[5].innerHTML='* 验证信息不能为空';
                samp[5].style.color='red';
                return false;
            }
            var tel=document.getElementById('tel').value;
			if(tel == ''||tel==null){
                samp[6].innerHTML='* 电话号码不能为空';
                samp[6].style.color='red';
                return false;
            }
            var eamil=document.getElementById('eamil').value;
			if(eamil == ''||eamil==null){
                samp[7].innerHTML='* 邮箱不能为空';
                samp[7].style.color='red';
                return false;
            }
		    var deals = document.getElementById('deal');
		   if (deals.checked != true) {
			  samp[8].innerHTML = '* 请同意《校友会章程》';
			   samp[8].style.color = 'red';
			   return false;
		   }
		    else {
			   return true;
		   }
	   }
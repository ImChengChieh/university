//注册
//用户名
      var register_=document.getElementById('register_');
      var samp_=register_.getElementsByTagName('samp'); 
      function user_focus(){
      	samp_[0].innerHTML='用户名由3-11位的字母下划线或数字不能含有空格';
        samp_[0].style.color='#44aae4';
      }
      function user_blur(){
		 var users=document.getElementById('user').value;
			if(users == ''||users==null){
                samp_[0].innerHTML='* 用户名不能为空';
                samp_[0].style.color='red';
                return false;
           }

			if(users.indexOf(' ')!=-1){
                samp_[0].innerHTML='*用户名不能包含空格';
                samp_[0].style.color='red';
                return false;
			}

			if(users.length<3||users.length>11){
                samp_[0].innerHTML='用户名长度大于3小于11位';
                samp_[0].style.color='red';
                return false;
			}
			else{
				samp_[0].innerHTML=' ';
				return true;
			}
        }
//    密码
      function password_focus(){
      	samp_[1].innerHTML='密码由 6-22位的字母或数字或特殊字符组成不能含有空格';
        samp_[1].style.color='#44aae4';
      }
      function password_blur(){
		  var passwords=document.getElementById('password').value;
			if(passwords == ''||passwords==null){
                samp_[1].innerHTML='* 密码不能为空';
                samp_[1].style.color='red';
                return false;
           }      
			if(!/^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,22}$/.test(passwords)){
				 samp_[1].innerHTML='* 密码格式错误';
				 samp_[1].style.color='red';
				 return false;
			}
			else{
				samp_[1].innerHTML=' ';
				return true;
			}
        }
//重复密码
   function repassword_focus(){
      	samp_[2].innerHTML='请再次输入密码';
        samp_[2].style.color='#44aae4';
      }
     function repassword_blur(){
     var s=document.getElementById('password').value;
		  var repassword=document.getElementById('repassword').value;
			if(repassword == ''||repassword==null){
                samp_[2].innerHTML='* 密码不能为空';
                samp_[2].style.color='red';
                return false;
        }      
			if(repassword!=s){
				 samp_[2].innerHTML='* 密码不一致';
				 samp_[2].style.color='red';
				 return false;
			}
			else{
				samp_[2].innerHTML=' ';
				return true;
			}
     }
      
  //注册提交验证
  function checkes(){	
  	var checkde=document.getElementById('checkde');
  	if(checkde.checked==true){
  		return true;
  	}
  	else{
  	    samp_[3].innerHTML='* 请同意《校友会章程》';
  	    samp_[3].style.color='red';
  	    return false;
  	}
  	
  }
  
//登录界面验证
function checkes_enter(){
var users=document.getElementById('user').value;
var passwords=document.getElementById('password').value;
			if(users == ''||users==null){
                samp_[0].innerHTML='* 用户名不能为空';
                samp_[0].style.color='red';
                return false;
           }      
			if(users.indexOf(' ')!=-1){
                samp_[0].innerHTML='*用户名不能包含空格';
                samp_[0].style.color='red';
                return false;
			}
			if(users.length<3 || users.length>11){
                samp_[0].innerHTML='用户名长度大于3小于11位';
                samp_[0].style.color='red';
                return false;
			}
			else{
				samp_[0].innerHTML=' ';
			}

		if(passwords == ''||passwords==null){
                samp_[1].innerHTML='* 密码不能为空';
                samp_[1].style.color='red';
                return false;
           }      
			if(!/^[\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{6,22}$/.test(passwords)){
				 samp_[1].innerHTML='* 密码格式错误';
				 samp_[1].style.color='red';
				 return false;
			}
			else{
				samp_[1].innerHTML=' ';
				return true;
			}
}

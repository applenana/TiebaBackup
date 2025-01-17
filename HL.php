<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<link rel="stylesheet" type="text/css" href="css/public.css">
<style>
/* === Remove input autofocus webkit === */
body{font:13px/26px "微软雅黑";}
*:focus {outline: none;}
.contact{width:720px;background:#F1F1F1;margin:20px auto;padding:10px;}

/* === Form Typography === */
.contact_form h2{font-size:18px;font-weight:bold;}
.contact_form label{font-size:14px;}
.form_hint, .required_notification{font-size: 12px;}

/* === List Styles === */
.contact_form ul {width:720px;list-style-type:none;list-style-position:outside;padding:0px;}
.contact_form li{padding:12px; border-bottom:1px solid #DFDFDF;position:relative;} 
.contact_form li:first-child, .contact_form li:last-child {border-bottom:1px solid #777;}

/* === Form Header === */
.contact_form h2 {margin:0;display: inline;}
.required_notification {color:#d45252; margin:5px 0 0 0; display:inline;float:right;}

/* === Form Elements === */
.contact_form label {width:150px;margin-top: 3px;display:inline-block;float:left;padding:3px;}
.contact_form input {height:20px; width:220px; padding:5px 8px;}
.contact_form textarea {padding:8px; width:300px;}
.contact_form button {margin-left:156px;}

    /* form element visual styles */
.contact_form input, .contact_form textarea { 
    border:1px solid #aaa;
    box-shadow: 0px 0px 3px #ccc, 0 10px 15px #eee inset;
    border-radius:2px;
    padding-right:30px;
    -moz-transition: padding .25s; 
    -webkit-transition: padding .25s; 
    -o-transition: padding .25s;
    transition: padding .25s;
}
.contact_form input:focus, .contact_form textarea:focus {
    background: #fff url(images/red_asterisk.png) no-repeat; 
    border:1px solid #555; 
    box-shadow: 0 0 3px #aaa; 
    padding-right:70px;
}

/* === HTML5 validation styles === */    
.contact_form input:required, .contact_form textarea:required {background: #fff url(images/red_asterisk.png) no-repeat 98% center;}
.contact_form input:required:valid, .contact_form textarea:required:valid {background: #fff url(images/valid.png) no-repeat 98% center;box-shadow: 0 0 5px #5cd053;border-color: #28921f;}
.contact_form input:focus:invalid, .contact_form textarea:focus:invalid {background: #fff url(images/invalid.png) no-repeat 98% center;box-shadow: 0 0 5px #d45252;border-color: #b03535;}

/* === Form hints === */
.form_hint {
    background: #d45252;
    border-radius: 3px 3px 3px 3px;
    color: white;
    margin-left:8px;
    padding: 1px 6px;
    z-index: 999; 
    position: absolute; 
    display: none;
}
.form_hint::before {
    content: "\25C0";
    color:#d45252;
    position: absolute;
    top:1px;
    left:-6px;
}
.contact_form input:focus + .form_hint {display: inline;}
.contact_form input:required:valid + .form_hint {background: #28921f;}
.contact_form input:required:valid + .form_hint::before {color:#28921f;}
    
/* === Button Style === */
button.submit {
    background-color: #68b12f;
    background: -webkit-gradient(linear, left top, left bottom, from(#68b12f), to(#50911e));
    background: -webkit-linear-gradient(top, #68b12f, #50911e);
    background: -moz-linear-gradient(top, #68b12f, #50911e);
    background: -ms-linear-gradient(top, #68b12f, #50911e);
    background: -o-linear-gradient(top, #68b12f, #50911e);
    background: linear-gradient(top, #68b12f, #50911e);
    border: 1px solid #509111;
    border-bottom: 1px solid #5b992b;
    border-radius: 3px;
    -webkit-border-radius: 3px;
    -moz-border-radius: 3px;
    -ms-border-radius: 3px;
    -o-border-radius: 3px;
    box-shadow: inset 0 1px 0 0 #9fd574;
    -webkit-box-shadow: 0 1px 0 0 #9fd574 inset ;
    -moz-box-shadow: 0 1px 0 0 #9fd574 inset;
    -ms-box-shadow: 0 1px 0 0 #9fd574 inset;
    -o-box-shadow: 0 1px 0 0 #9fd574 inset;
    color: white;
    font-weight: bold;
    padding: 6px 20px;
    text-align: center;
    text-shadow: 0 -1px 0 #396715;
}
button.submit:hover {
    opacity:.85;
    cursor: pointer; 
}
button.submit:active {
    border: 1px solid #20911e;
    box-shadow: 0 0 10px 5px #356b0b inset; 
    -webkit-box-shadow:0 0 10px 5px #356b0b inset ;

    -moz-box-shadow: 0 0 10px 5px #356b0b inset;
    -ms-box-shadow: 0 0 10px 5px #356b0b inset;
    -o-box-shadow: 0 0 10px 5px #356b0b inset;
    
}
</style>
    <script src="http://www.jiawin.com/wp-content/themes/javin/js/jquery.js"></script>
    <script type="text/javascript">
    jQuery(document).ready(function($){                            
        $('#ads_close').click(function(e){
            $('#ads_box').fadeOut();
            e.preventDefault();
        });
    });
</script>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

<title>提交你的帖子！</title>

</head>

 

<body>

<h1 align="center" class="STYLE2"><span class="STYLE3"><span class="STYLE1"><img src="a111.png" width="117" height="117" /></span></span></h1>

<h1 align="center" class="STYLE3">欢迎来到帖子备份提交页</p>

<h1 align="center" class="STYLE3">url的填写例子:“https://tieba.baidu.com/p/7276062535”</h1>

<div class="contact">
<form class="contact_form" action="up.php" method="post" name="contact_form">
    <ul>
        <li>
             <h2>备份帖子申请</h2>
             <span class="required_notification">* 表示必填项</span>
        </li>

        <li>
            <label for="website">链接:<span style="color=red">*</span></label>
            <input type="url" name="url" placeholder="帖子的url" required pattern="(http|https)://.+"/ >
            <span class="form_hint">正确格式为：http://tieba.baidu.com/p/6807929303</span>
        </li>
        <li>
            <label for="message">留言:</label>
            <textarea name="message" cols="40" rows="6" placeholder="非必须，随便填" ></textarea>
        </li>
        <li>
            <button class="submit" type="submit">提交</button>
        </li>
    </ul>
</form>
</div>

<body background="bg.png">


</body>

</html>


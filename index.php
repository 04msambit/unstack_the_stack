<!DOCTYPE html>
<html>
<body>
<font size="20" color="black" style="position:absolute;left:50px;">Unstack the Stack !!!</font>
<img src ="stack-overflow.png"style="position:absolute;left:500px;top:10px;"/> 
<form name="input" action="search.php" method="get" >
<input type="text" name="title" size="100" style="position:absolute;left:50px;top:100px;">
<input type="submit" value="Search" style="position:absolute;left:700px;top:100px;">
</form>
<div style="position:absolute;left:50px;top:200px;">
<?php
exec("python php_helper.py",$output);
foreach($output as $value){
$idpos =strpos($value,"Id") + 7; 
$tpos = strpos($value,"Title") ;
$id = substr($value,$idpos,$tpos-4-$idpos);
$title = substr($value,$tpos+9);
#$bodypos = strpos($value,"Body") ;
#$body = substr($value,$bodypos+9);
?>
<a href="answers.php?id=<?php echo $id;?>"><?php echo $title; 
?></a><br/>
<br/>
<?php
}
?>
</div>
</body>
</html>

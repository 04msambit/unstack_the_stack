<!DOCTYPE html>
<html>
<body>
<?php
$id = $_GET["id"];

exec("python unanswered_cosine_new.py $id",$output);
foreach($output as $value) {
  if (strstr($value,"Id")!==FALSE){
  $idpos =strpos($value,"Id") + 7; 
  $tpos = strpos($value,"Title") ;
  $id = substr($value,$idpos,$tpos-4-$idpos);
  $title = substr($value,$tpos+9);
  
}else{
  $id = -1;
}
if($id!==-1){
?>
<a href="http://www.stackoverflow.com/questions/<?php echo $id;?>"><?php echo $title; ?></a><br/><br/>
<?php
}
else{
  print $value. "<br />";
}
}
?>
</body>
</html>

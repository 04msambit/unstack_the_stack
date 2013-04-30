<!DOCTYPE html>
<html>
<body>
<?php
$text = $_GET["title"];
exec("python search.py $text",$output);
foreach($output as $value){
$idpos =strpos($value,"Id") + 7; 
$tpos = strpos($value,"Title") ;
$id = substr($value,$idpos,$tpos-4-$idpos);
$title = substr($value,$tpos+9);
?>
<a href="answers.php?id=<?php echo $id;?>"><?php echo $title; ?></a><br/><br/>
<?php
}
?>
</body>
</html>

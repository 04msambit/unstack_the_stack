<!DOCTYPE html>
<html>
<body>
<?php
exec("python php_helper.py",$output);
$title =  $output[0];
#print $title

?>  
<a href="answers.php"><?php echo $title; ?></a>
</body>
</html>

<?php
$id = $_GET["id"];
print $id;
exec("python unanswered_cosine_new.py $id",$output);
foreach($output as $value) {
  print $value. "<br />";
}
?>


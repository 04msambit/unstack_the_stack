#call python function passing it the unanswered ID echo the results
<?php
exec("python unanswered_cosine_new.py 649980",$output);
foreach($output as $value) {
  print $value. "<br />";
}
?>


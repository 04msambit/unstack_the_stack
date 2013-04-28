#call python function passing it the unanswered ID echo the results
<?php
exec("python unanswered_cosine_new.py",$output);
foreach($output as $value) {
  print $value. "<br />";
}
?>


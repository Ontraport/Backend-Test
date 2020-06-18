package main

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"
)

func main() {
	str := `{
		"one":
		{
			"two": 3,
			"four": [ 5,6,7]
		},
		"eight":
		{
			"nine":
			{
				"ten":11
			}
		}
	}`

	v := make(map[string]interface{})
	json.Unmarshal([]byte(str), &v)

	c := Flatten(v)
	a, _ := json.Marshal(c)
	fmt.Println(string(a))

	u, _ := Unflatten(c)
	a, _ = json.Marshal(u)
	fmt.Print(string(a))
}

func Unflatten(flat map[string]interface{}) (nested map[string]interface{}, err error) {
	nested = make(map[string]interface{})

	for k, v := range flat {
		temp := uf(k, v).(map[string]interface{})
		merge(nested, temp)
	}

	return
}

func merge(left, right map[string]interface{}) map[string]interface{} {
	for key, rightVal := range right {
		if leftVal, present := left[key]; present {
			//then we don't want to replace it - recurse
			switch leftVal.(type) {
			case map[string]interface{}:
				left[key] = merge(leftVal.(map[string]interface{}), rightVal.(map[string]interface{}))
			default:
				m := new([]interface{})
				switch left[key].(type) {
				case []interface{}:
					for _, v := range left[key].([]interface{}) {
						*m = append(*m, v)
					}
					left[key] = append(*m, rightVal)
				default:
					left[key] = append(*m, left[key], rightVal)
				}

			}
		} else {
			// key not in left so we can just shove it in
			left[key] = rightVal
		}
	}
	return left
}

func uf(k string, v interface{}) (n interface{}) {
	n = v

	keys := strings.Split(k, ".")

	for i := len(keys) - 1; i >= 0; i-- {
		_, err := strconv.ParseInt(keys[i], 10, 0)
		if err != nil {
			temp := make(map[string]interface{})
			temp[keys[i]] = n
			n = temp
		}

	}

	return
}

func Flatten(m map[string]interface{}) map[string]interface{} {
	o := make(map[string]interface{})
	for k, v := range m {
		switch child := v.(type) {
		case []interface{}:
			for nk, nv := range child {
				o[k+"."+strconv.Itoa(nk)] = nv
			}
		case map[string]interface{}:
			nm := Flatten(child)
			for nk, nv := range nm {
				o[k+"."+nk] = nv
			}
		default:
			o[k] = v
		}
	}
	return o
}

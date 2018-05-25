(ns app.core-test
  (:require [clojure.test :refer :all]
            [app.core :refer :all]))

(deftest test-flatten-map
  (testing "README example"
    (is (= {"one/two" 3
            "one/four/0" 5
            "one/four/1" 6
            "one/four/2" 7
            "eight/nine/ten" 11}
           (flatten-map
             {"one" {"two" 3 "four" [5 6 7]}
              "eight" {"nine" {"ten" 11}}})))))

(deftest test-expand-map
  (testing "README example"
    (is (= {"one" {"two" 3 "four" [5 6 7]}
            "eight" {"nine" {"ten" 11}}}
           (expand-map
             (array-map
               "one/two" 3
               "one/four/0" 5
               "one/four/1" 6
               "one/four/2" 7
               "eight/nine/ten" 11))))))

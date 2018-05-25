(ns app.core
  (:require [clojure.string :as string]))

(defn- sequential-to-map [s]
  (zipmap (range) s))

(defn- convert-int [v]
  (try (Integer/parseInt v)
       (catch NumberFormatException _ v)))

; #1
(defn flatten-map
  ([input] (flatten-map input nil))
  ([input pre]
   (reduce-kv
     (fn [m k v]
         (let [prefix (str (when pre
                             (str pre "/"))
                           k)]
           (merge m
             (cond
               (map? v) (flatten-map v prefix)
               (sequential? v) (flatten-map (sequential-to-map v) prefix)
               :default {prefix v}))))
     (array-map) input)))

; #2
; Known limitations of this solution:
; - integer keys in input must be in order, e.g.
;     {"one/1" 3 "one/0" 11} may fail
; - arrays must be at leaf nodes, e.g.
;     {"one/0/two" 3 "one/0/three" 11 "one/1/four" 5} won't return
;     what you'd probably want it to
(defn expand-map [input]
  (reduce-kv
    (fn [m k v]
      (let [keys (map convert-int (string/split k #"/"))]
        (cond-> m
                (integer? (last keys)) (update-in (butlast keys) #(or % []))
                true (assoc-in keys v))))
    {} input))
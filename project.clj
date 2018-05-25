(defproject test "0.1.0-SNAPSHOT"
  :dependencies [[org.clojure/clojure "1.9.0"]]
  :main ^:skip-aot app.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})

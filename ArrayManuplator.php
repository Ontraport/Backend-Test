<?php
namespace BackendTest;

class BackendTestRecursiveKeysIterator extends \RecursiveIteratorIterator
{
    public function __construct(array $arg_multi_dimensional_array)
    {
        $objRecursiveArrayIterator = new \RecursiveArrayIterator(
          $arg_multi_dimensional_array
        );

        parent::__construct($objRecursiveArrayIterator);
    }

    /**
     * Get the traversed array keys
     *
     * @return array
     */
    public function getTraversedKeys()
    {
        $return = array();

        $array_depth = $this->getDepth();

        for ($i = 0; $i <= $array_depth; $i++){
          $return[] = $this->getSubIterator($i)->key();
        }

        return $return;
    }
}

/**
 * An array manipulator to serve Backend-Test needs
 */
class ArrayManipulator
{

  public function __construct()
  {
  }

  /**
   * Convert multidimensional array to associative array
   *
   * @param  array $arg_multi_dimensional_array
   *
   * @return array
   */
  public function doConvertToAssociativeArray($arg_multi_dimensional_array)
  {
      $return = array();

      $objBackendTestRecursiveKeysIterator = new BackendTestRecursiveKeysIterator(
        $arg_multi_dimensional_array
      );

      foreach($objBackendTestRecursiveKeysIterator as $key => $value){

          $traversed_keys = implode(
            '/',
            $objBackendTestRecursiveKeysIterator->getTraversedKeys()
          );

          $return[$traversed_keys] = $value;
      }
      return $return;
  }

  /**
   * Reverse output from doConvertToAssociativeArray to original state
   *
   * @param array $arg_associative_array
   *
   * @return array
   */
  public function doReverseToOriginalArray($arg_associative_array)
  {

      $return = array();

      foreach ($arg_associative_array as $traversed_path => $value) {

          $keys = explode('/', $traversed_path);

          $_return = &$return;

          foreach ($keys as $key) {
            if(is_array($_return)){
              if (!array_key_exists($key, $_return)) {
                  $_return[$key] = [];
              }
            }
            $_return = &$_return[$key];
          }

          $_return = $value;


          unset($_return);
      }

      return $return;
  }

}

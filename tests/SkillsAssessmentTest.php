<?php
declare(strict_types = 1);

require_once 'src/SkillsAssessment.php';

use PHPUnit\Framework\TestCase;

final class SkillsAssessmentTest extends TestCase
{
    protected $SK;
    
    /**
     * @test
     * @return void
     */
    public function testDeepenEmptyArray()
    {
        $this->SK = new SkillsAssessment();
        $obj=array();
        $deep = $this->SK->deepenArray($obj);
        $this->assertEquals(empty($deep),true);
    }    
    
    /**
    * @test
    * @return void
    */
    public function testFlattenEmptyArray()
    {
        $this->SK = new SkillsAssessment();
        $obj=array();
        $flat = $this->SK->flattenArray($obj);
        $this->assertEquals(empty($flat),true);
    }

    /**
     * @test
     * @return void
     */
    public function testFlattenBasicInput()
    {
        $this->SK = new SkillsAssessment();
        $json = file_get_contents("tests/json1.txt");
        $obj = json_decode($json, true);
        $flat = $this->SK->flattenArray($obj);
        $this->assertEquals($flat["one/two"], 3);
        $this->assertEquals($flat["one/four/2"], 7);
    }
    
    /**
     * @test
     * @return void
     */
    public function testDeepenBasicInput()
    {
        $this->SK = new SkillsAssessment();
        $json = file_get_contents("tests/json1a.txt");
        $obj = json_decode($json, true);
        $deep = $this->SK->deepenArray($obj);
        $this->assertEquals($deep["one"]["two"], 3);
        $this->assertEquals($deep["one"]["four"][1], 6);
        $this->assertEquals($deep["eight"]["nine"]["ten"], 11);
    }
    
}
?>
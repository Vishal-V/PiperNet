pragma solidity ^0.4.16;

contract testContract {
    
    uint value;
    function testContract(uint _p){
        value = _p;
    }
    
    function setP(uint _n) payable
    {
        value = _n;
    }
    
    function setNP(uint _n){
        value = _n;
    }
    
    function get() constant returns (uint){
        return value;
    }
}
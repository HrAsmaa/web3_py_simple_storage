// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract myFirstContract {
    uint104 public myFavoritNumber;
    struct Person {
        string name;
        uint104 age;
    }
    Person[] public persons;

    mapping(string => uint104) public nameAge;

    function getMyFavoritNumber() public view returns (uint104) {
        return myFavoritNumber;
    }

    function setMyFavoritNumber(uint104 _myFavoritNumber) public {
        myFavoritNumber = _myFavoritNumber;
    }

    function addPerson(string memory _name, uint104 _age) public {
        persons.push(Person(_name, _age));
        nameAge[_name] = _age;
    }
}

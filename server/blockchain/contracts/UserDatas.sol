pragma solidity >=0.4.21 <0.7.0;
pragma experimental ABIEncoderV2;

contract UserDatas {
    struct UserShopMapping {
        uint id;
        string shop_id;
        string customer_id;
        uint256 slot_begin;
        uint256 slot_end;
    }

    mapping(uint => UserShopMapping) public userDatas;
    uint public userDatasCount;

    constructor () public {
        userDatasCount = 0;
    }

    function addUser (string memory shop_id, string memory customer_id, uint256 slot_begin, uint256 slot_end) public {
        userDatas[userDatasCount] = UserShopMapping(userDatasCount, shop_id, customer_id, slot_begin, slot_end);
        userDatasCount++;
    }

    function getUserDataById(uint _id) public view returns(uint, string memory, string memory, uint256, uint256) {
        return (userDatas[_id].id, userDatas[_id].shop_id, userDatas[_id].customer_id,
        userDatas[_id].slot_begin, userDatas[_id].slot_end);
    }
    
    function getAllUserDatas(string memory user_id) public view returns (uint[] memory, string[] memory, uint256[] memory, uint256[] memory) {
    uint[] memory ids = new uint[](userDatasCount);
    string[] memory shop_ids = new string[](userDatasCount);
    uint[] memory slot_begins = new uint[](userDatasCount);
    uint[] memory slot_ends = new uint[](userDatasCount);

  
    for(uint i = 0; i<userDatasCount;i++){
      if(keccak256(abi.encodePacked(userDatas[i].customer_id)) == keccak256(abi.encodePacked(user_id))){
            ids[i] = userDatas[i].id;
            shop_ids[i] = userDatas[i].shop_id;
            slot_begins[i] = userDatas[i].slot_begin;
            slot_ends[i] = userDatas[i].slot_end;
            }
    }
    return (ids, shop_ids, slot_begins, slot_ends);
    }
}
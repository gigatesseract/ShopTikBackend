const UserDatas = artifacts.require("UserDatas");

module.exports = function(deployer) {
  deployer.deploy(UserDatas);
};

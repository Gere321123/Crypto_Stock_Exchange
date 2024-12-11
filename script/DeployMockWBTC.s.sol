// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "../src/MockWBTC.sol";

contract DeployMockWBTC is Script {
    function run() external {
        vm.startBroadcast(); // Start broadcasting transactions

        // Deploy the MockWBTC contract
        MockWBTC mockWBTC = new MockWBTC();

        console.log("MockWBTC deployed at:", address(mockWBTC));

        console.log("Deployer balance after minting:", mockWBTC.balanceOf(msg.sender));

        console.log("Deployer balance after to the contract:", mockWBTC.balanceOf(address(this)));

        vm.stopBroadcast(); // Stop broadcasting transactions
    }
}

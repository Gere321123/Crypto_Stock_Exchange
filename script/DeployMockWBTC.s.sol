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

        vm.stopBroadcast(); // Stop broadcasting transactions
    }
}

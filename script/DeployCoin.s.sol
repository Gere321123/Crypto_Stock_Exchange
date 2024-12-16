// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "../src/Coin.sol";

contract DeployCoin is Script {
    function run() external returns (Coin) {
        // Addresses provided
        address company = 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266;
        address secondOwner = 0x565FaF97aDcdb3E70e8d00691485E16A1cf4ba25;

        // Parameters for deployment
        uint256 numberOfTokens = 10000000; // Example token supply, adjust as needed
        uint8 companyWithdrawalPercentage = 20; // Company withdrawal percentage
        uint8 ownerWithdrawalPercentage = 5; // Owner withdrawal percentage
        uint8 secondOwnerWithdrawalPercentage = 3; // Second owner withdrawal percentage
        uint256 numberOfVirtualWei = 10000000000000000000; // Example virtual Wei balance, adjust as needed

        // Start broadcasting transactions
        vm.startBroadcast();

        // Deploy Coin contract with the specified parameters
        Coin coin = new Coin(
            numberOfTokens,
            company,
            companyWithdrawalPercentage,
            ownerWithdrawalPercentage,
            secondOwnerWithdrawalPercentage,
            secondOwner,
            numberOfVirtualWei
        );

        vm.stopBroadcast();
        return coin;
    }
}

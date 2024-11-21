// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "../src/Coin.sol";

contract DeployCoin is Script {
    function run() external returns (Coin) {
        // Addresses provided
        address company = 0x70997970C51812dc3A010C7d01b50e0d17dc79C8;
        address secondOwner = 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC;

        // Parameters for deployment
        uint256 numberOfTokens = 1000000; // Example token supply, adjust as needed
        uint8 companyWithdrawalPercentage = 20; // Company withdrawal percentage
        uint8 ownerWithdrawalPercentage = 5; // Owner withdrawal percentage
        uint8 secondOwnerWithdrawalPercentage = 3; // Second owner withdrawal percentage
        uint256 numberOfVirtualWei = 100000000000000000; // Example virtual Wei balance, adjust as needed

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

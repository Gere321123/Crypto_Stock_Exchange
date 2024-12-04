// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../../src/Coin.sol"; // Path to your Coin.sol contract
import {DeployCoin} from "../../script/DeployCoin.s.sol";
import {console} from "forge-std/console.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract CoinTest is Test {
    Coin private coin;
    DeployCoin private deployCoin;

    address private wBTCAddress = 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512;
    address public USER = makeAddr("user");

    uint256 public constant STARTING_WBTC_BALANCE = 100 * 10 ** 18; // 100 wBTC (assuming 18 decimals)
    uint256 public constant TOKENS_TO_BUY = 1 * 10 ** 18; // Amount of WBTC the user wants to spend

    function setUp() public {
        deployCoin = new DeployCoin();
        coin = deployCoin.run();

        // Mock the WBTC balance for the user
        vm.mockCall(
            wBTCAddress, abi.encodeWithSelector(IERC20.balanceOf.selector, USER), abi.encode(STARTING_WBTC_BALANCE)
        );

        // Mock the approval for transferFrom
        vm.mockCall(
            wBTCAddress, abi.encodeWithSelector(IERC20.approve.selector, address(coin), TOKENS_TO_BUY), abi.encode(true)
        );

        // Mock transferFrom to simulate a successful transfer
        vm.mockCall(wBTCAddress, abi.encodeWithSelector(IERC20.transferFrom.selector), abi.encode(true));
    }

    function testBuyTokensWithWBTC() public {
        // Ensure USER has the correct WBTC balance
        uint256 userWBTCBalance = IERC20(wBTCAddress).balanceOf(USER);
        assertEq(userWBTCBalance, STARTING_WBTC_BALANCE, "User should have 100 WBTC");

        // Call buyTokens to simulate the purchase
        vm.prank(USER); // Set the sender to USER
        coin.buyTokens(TOKENS_TO_BUY);

        // Verify that the user's balance has decreased and the contract's balance has increased
        uint256 userWBTCBalanceAfter = IERC20(wBTCAddress).balanceOf(USER);
        uint256 contractWBTCBalance = IERC20(wBTCAddress).balanceOf(address(coin));

        assertEq(userWBTCBalanceAfter, STARTING_WBTC_BALANCE - TOKENS_TO_BUY, "User's WBTC balance should decrease");
        assertEq(contractWBTCBalance, TOKENS_TO_BUY, "Contract should receive the WBTC");
    }

    // Additional tests for edge cases, events, etc.
}

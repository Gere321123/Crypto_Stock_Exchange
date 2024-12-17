// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockWBTC is ERC20 {
    constructor() ERC20("Wrapped Bitcoin", "WBTC") {
        _mint(msg.sender, 1000000 * 10 ** 18); // Mint 1,000,000 WBTC (18 decimals)
    }

    // Mint 0.01 WBTC (0.01 * 10^18 = 10^16)
    function mint() external {
        _mint(msg.sender, 10 ** 16); // Mint 0.01 WBTC to sender
    }
}
